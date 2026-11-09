"""Pre-generate the real world around spawn with Chunky, headless, then stop cleanly.

Usage:  python -I tools/pregen.py [--radius 1200] [--nether 0] [--timeout 5400]

Boots server/world (creating it if it doesn't exist), runs
    chunky spawn / chunky radius R / chunky start
in the Overworld (and optionally the Nether with --nether R), prints Chunky's progress,
and sends `stop` once every task has finished. Exploring pre-generated land doesn't lag.
The story doesn't start until the first player logs in, so this doesn't spoil anything.
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boottest import JAVA, SRV, log_lines, port_open  # noqa: E402
from boottime import LOG, report  # noqa: E402

DONE = re.compile(r"\[Chunky\] Task finished for ([\w:]+)")
PROGRESS = re.compile(r"\[Chunky\] Task running for ([\w:]+)\. Processed: (\d+) chunks \(([\d.]+)%\)")


def send(proc, cmd):
    proc.stdin.write(cmd + "\n")
    proc.stdin.flush()
    time.sleep(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius", type=int, default=1200)
    ap.add_argument("--nether", type=int, default=0)
    ap.add_argument("--timeout", type=int, default=5400)
    a = ap.parse_args()
    if port_open():
        sys.exit("Server already running on 25565. Stop it first.")
    nf = re.search(r'set "NEOFORGE=([\d.]+)"', (SRV / "start.bat").read_text()).group(1)
    args = [str(JAVA), "@user_jvm_args.txt", f"@libraries/net/neoforged/neoforge/{nf}/win_args.txt", "nogui"]
    t0 = time.time()
    proc = subprocess.Popen(args, cwd=SRV, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT, text=True)
    while time.time() - t0 < 600:
        if proc.poll() is not None:
            report()
            sys.exit("!! Server exited during startup.")
        if LOG.exists() and LOG.stat().st_mtime >= t0 and "]: Done (" in LOG.read_text(encoding="utf-8", errors="replace"):
            break
        time.sleep(1)
    else:
        proc.kill()
        sys.exit("!! Server did not start within 600s.")
    report()

    # On a new world, story/05_town.js moves spawn to the story town right after "Done".
    # Pre-generate around the town, not around the old spawn: wait for its log line.
    t1 = time.time()
    while time.time() - t1 < 180 and "[gl] story town" not in LOG.read_text(encoding="utf-8", errors="replace"):
        time.sleep(1)
    town = [l for l in log_lines() if "[gl] story town" in l]
    print(town[-1].split("]: ", 1)[-1] if town else "(no story-town line: this world already had its town picked)")

    worlds = ["minecraft:overworld"] + (["minecraft:the_nether"] if a.nether else [])
    start_line = len(log_lines())
    send(proc, "chunky world minecraft:overworld")
    send(proc, "chunky spawn")
    send(proc, f"chunky radius {a.radius}")
    send(proc, "chunky start")
    if a.nether:
        send(proc, "chunky world minecraft:the_nether")
        send(proc, "chunky center 0 0")
        send(proc, f"chunky radius {a.nether}")
        send(proc, "chunky start")
    print(f"Pre-generating {', '.join(worlds)} (overworld radius {a.radius} around spawn)...")
    finished, last = set(), 0
    while time.time() - t0 < a.timeout and len(finished) < len(worlds):
        if proc.poll() is not None:
            sys.exit("!! Server stopped unexpectedly during pre-generation.")
        lines = log_lines()[start_line:]
        for l in lines:
            m = DONE.search(l)
            if m:
                finished.add(m.group(1))
        if time.time() - last > 60:
            prog = [PROGRESS.search(l) for l in lines]
            prog = [p for p in prog if p]
            if prog:
                p = prog[-1]
                print(f"   {p.group(1)}: {p.group(2)} chunks ({p.group(3)}%)  [{int(time.time() - t0)}s]", flush=True)
            last = time.time()
        time.sleep(2)
    print("Finished:", ", ".join(sorted(finished)) or "nothing (timeout)")
    send(proc, "stop")
    try:
        proc.wait(180)
        print(f"Stopped cleanly (exit {proc.returncode}).")
    except subprocess.TimeoutExpired:
        proc.kill()
        print("!! Did not stop within 180s - killed.")
    sys.exit(0 if len(finished) == len(worlds) else 1)


if __name__ == "__main__":
    main()
