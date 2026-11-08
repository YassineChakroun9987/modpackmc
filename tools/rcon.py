"""Send a console command to the local dev server over RCON.

Usage:  python tools/rcon.py "list"
        python tools/rcon.py "neoforge tps"

Reads host/port/password from server/server.properties. Stdlib only.
"""
import socket
import struct
import sys
from pathlib import Path

PROPS = Path(__file__).resolve().parent.parent / "server" / "server.properties"


def load_props():
    props = {}
    for line in PROPS.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            props[k.strip()] = v.strip()
    return props


def packet(req_id, ptype, body):
    payload = struct.pack("<ii", req_id, ptype) + body.encode("utf-8") + b"\x00\x00"
    return struct.pack("<i", len(payload)) + payload


def read_packet(sock):
    def recv_exact(n):
        buf = b""
        while len(buf) < n:
            chunk = sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("RCON connection closed")
            buf += chunk
        return buf

    (length,) = struct.unpack("<i", recv_exact(4))
    data = recv_exact(length)
    req_id, ptype = struct.unpack("<ii", data[:8])
    return req_id, ptype, data[8:-2].decode("utf-8", errors="replace")


def run(command):
    p = load_props()
    host = p.get("server-ip") or "127.0.0.1"
    port = int(p.get("rcon.port", 25575))
    with socket.create_connection((host, port), timeout=10) as s:
        s.sendall(packet(1, 3, p["rcon.password"]))  # 3 = login
        req_id, _, _ = read_packet(s)
        if req_id == -1:
            raise PermissionError("RCON login rejected - check rcon.password")
        s.sendall(packet(2, 2, command))  # 2 = exec command
        _, _, body = read_packet(s)
        return body


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(run(" ".join(sys.argv[1:])))
