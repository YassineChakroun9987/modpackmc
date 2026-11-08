"""Ask the local server for its status, the same way the multiplayer screen does.

Usage:  python tools/ping.py            (defaults to 127.0.0.1:25565)
        python tools/ping.py 127.0.0.1 25565

Prints the MOTD, version, player count and whether the server reports itself as modded.
"""
import json
import socket
import struct
import sys


def varint(n):
    out = b""
    while True:
        b = n & 0x7F
        n >>= 7
        out += bytes([b | (0x80 if n else 0)])
        if not n:
            return out


def read_varint(sock):
    n = shift = 0
    while True:
        b = sock.recv(1)
        if not b:
            raise ConnectionError("closed")
        n |= (b[0] & 0x7F) << shift
        if not b[0] & 0x80:
            return n
        shift += 7


def ping(host="127.0.0.1", port=25565):
    with socket.create_connection((host, port), timeout=5) as s:
        hb = varint(0) + varint(767) + varint(len(host)) + host.encode() + struct.pack(">H", port) + varint(1)
        s.sendall(varint(len(hb)) + hb)
        s.sendall(varint(1) + varint(0))
        read_varint(s)  # packet length
        read_varint(s)  # packet id
        size = read_varint(s)
        data = b""
        while len(data) < size:
            data += s.recv(size - len(data))
        return json.loads(data)


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 25565
    st = ping(host, port)
    desc = st.get("description")
    print("MOTD:    ", desc.get("text", desc) if isinstance(desc, dict) else desc)
    print("Version: ", st["version"]["name"], f"(protocol {st['version']['protocol']})")
    print("Players: ", f"{st['players']['online']}/{st['players']['max']}")
    print("Modded:  ", st.get("isModded", False))
