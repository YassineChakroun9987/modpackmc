"""Which structures are at a position? Reads the saved region files directly (server must have saved).

Usage:  python -I tools/whatstructure.py <x> <z> [--world server/world] [--dim overworld|nether|end] [--radius 1]

Lists the structure starts and references stored in the chunk(s) around block x,z.
Useful for "what is floating here?" or "which structure logged an error at x,y,z?".
"""
import argparse
import gzip
import io
import struct
import sys
import zlib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DIMS = {"overworld": "region", "nether": "DIM-1/region", "end": "DIM1/region"}


def read_nbt(buf):
    def rd(fmt):
        return struct.unpack(">" + fmt, buf.read(struct.calcsize(">" + fmt)))[0]

    def string():
        return buf.read(rd("H")).decode("utf-8", "replace")

    def payload(t):
        if t == 1: return rd("b")
        if t == 2: return rd("h")
        if t == 3: return rd("i")
        if t == 4: return rd("q")
        if t == 5: return rd("f")
        if t == 6: return rd("d")
        if t == 7: return buf.read(rd("i"))
        if t == 8: return string()
        if t == 9:
            et, n = rd("b"), rd("i")
            return [payload(et) for _ in range(n)]
        if t == 10:
            out = {}
            while True:
                ct = rd("b")
                if ct == 0: return out
                out[string()] = payload(ct)
        if t == 11: return [rd("i") for _ in range(rd("i"))]
        if t == 12: return [rd("q") for _ in range(rd("i"))]
        raise ValueError(f"bad NBT tag {t}")

    t = rd("b")
    string()
    return payload(t)


def chunk_nbt(region_dir, cx, cz):
    f = region_dir / f"r.{cx >> 5}.{cz >> 5}.mca"
    if not f.exists():
        return None
    data = f.read_bytes()
    idx = 4 * ((cx & 31) + (cz & 31) * 32)
    loc = int.from_bytes(data[idx:idx + 3], "big")
    if loc == 0:
        return None
    off = loc * 4096
    length, comp = struct.unpack(">iB", data[off:off + 5])
    raw = data[off + 5: off + 4 + length]
    raw = zlib.decompress(raw) if comp == 2 else gzip.decompress(raw) if comp == 1 else raw
    return read_nbt(io.BytesIO(raw))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("x", type=int)
    ap.add_argument("z", type=int)
    ap.add_argument("--world", default=str(Path(__file__).resolve().parent.parent / "server" / "world"))
    ap.add_argument("--dim", default="overworld", choices=DIMS)
    ap.add_argument("--radius", type=int, default=1)
    a = ap.parse_args()
    region = Path(a.world) / DIMS[a.dim]
    ccx, ccz = a.x >> 4, a.z >> 4
    starts, refs, missing = {}, {}, 0
    for cx in range(ccx - a.radius, ccx + a.radius + 1):
        for cz in range(ccz - a.radius, ccz + a.radius + 1):
            nbt = chunk_nbt(region, cx, cz)
            if nbt is None:
                missing += 1
                continue
            s = nbt.get("structures", {})
            for sid, st in s.get("starts", {}).items():
                if st.get("id") != "INVALID":
                    starts[sid] = (cx, cz)
            for sid, longs in s.get("References", {}).items():
                for l in longs:
                    refs.setdefault(sid, set()).add(((l & 0xFFFFFFFF) - (1 << 32) if l & 0x80000000 else l & 0xFFFFFFFF,
                                                     l >> 32))
    print(f"Block {a.x},{a.z} -> chunk {ccx},{ccz} ({a.dim}, radius {a.radius}, {missing} chunk(s) not saved)")
    print("Structures STARTING here:", ", ".join(f"{k} @chunk{v}" for k, v in starts.items()) or "none")
    print("Structures REACHING into here (start chunk):")
    for sid, owners in sorted(refs.items()):
        print(f"   {sid}: {', '.join(f'{x},{z} (block ~{x * 16},{z * 16})' for x, z in sorted(owners))}")
    if not refs and not starts:
        print("   none")


if __name__ == "__main__":
    main()
