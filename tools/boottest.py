"""Boot the dev server headless, wait until it is up (or dies), report, then stop it cleanly.

Usage:  python -I tools/boottest.py [--fresh] [--timeout N] [--cmd "command"] [--cmd "..."]

  --fresh       boot into a brand-new throwaway world (server/.boottest/), deleted first.
                The real server/world is never touched. Use this for worldgen mods.
  --cmd "..."   console command to run once the server is up (repeatable), e.g.
                --cmd "locate biome terralith:moonlight_grove". Its reply is printed.
  --timeout N   seconds to wait for the server to finish starting (default 300).

Exit code 0 = reached "Done" with no ERROR lines; 1 = errors, crash or timeout.
For normal play use server/start.bat instead (it gives you a console window).
"""
import argparse
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boottime import LOG, report  # noqa: E402

SRV = Path(__file__).resolve().parent.parent / "server"
JAVA = Path(os.environ["APPDATA"]) / ".minecraft/runtime/java-runtime-delta/windows/java-runtime-delta/bin/java.exe"
FRESH_DIR = ".boottest"
# Replies to the commands we send (locate, give, summon, ...). Keep these specific: startup lines
# such as "Successfully initialized permission handler" can land right after Done.
REPLY = re.compile(r"^The nearest |^Could not find |^Can't locate |^Unknown |^Incorrect argument|^There is no |^Invalid |"
                   r"^Teleported |^Set the |^Gave |^Showing |^Changed |^No (entity|player) |^Summoned ", re.I)


def port_open(port=25565):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def log_lines():
    return LOG.read_text(encoding="utf-8", errors="replace").splitlines() if LOG.exists() else []


def tail(n=30):
    for l in log_lines()[-n:]:
        print("   |", l[:240])


def run_commands(proc, commands, per_cmd_timeout=120):
    print("--- commands:")
    for cmd in commands:
        before = len(log_lines())
        proc.stdin.write(cmd.lstrip("/") + "\n")
        proc.stdin.flush()
        t0, reply = time.time(), None
        while time.time() - t0 < per_cmd_timeout and reply is None:
            time.sleep(0.5)
            for l in log_lines()[before:]:
                if "Server thread/INFO" in l and REPLY.search(l.split("]: ", 1)[-1]):
                    reply = l.split("]: ", 1)[-1]
                    break
        print(f"   > {cmd}\n     {reply or f'(no reply within {per_cmd_timeout}s)'}")


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--cmd", action="append", default=[])
    ap.add_argument("legacy_timeout", nargs="?", type=int)  # old style: boottest.py 300
    a = ap.parse_args()
    timeout = a.legacy_timeout or a.timeout

    if port_open():
        sys.exit("Server already running on 25565. Stop it first: python -I tools/rcon.py stop")
    nf = re.search(r'set "NEOFORGE=([\d.]+)"', (SRV / "start.bat").read_text()).group(1)
    args = [str(JAVA), "@user_jvm_args.txt", f"@libraries/net/neoforged/neoforge/{nf}/win_args.txt", "nogui"]
    if a.fresh:
        shutil.rmtree(SRV / FRESH_DIR, ignore_errors=True)
        args += ["--universe", FRESH_DIR, "--world", "world"]
        print(f"(fresh throwaway world in server/{FRESH_DIR}/world)")

    t0 = time.time()
    proc = subprocess.Popen(args, cwd=SRV, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT, text=True)
    state = "timeout"
    while time.time() - t0 < timeout:
        if proc.poll() is not None:
            state = "exited"
            break
        if LOG.exists() and LOG.stat().st_mtime >= t0 and "]: Done (" in LOG.read_text(encoding="utf-8", errors="replace"):
            state = "done"
            break
        time.sleep(0.5)

    if state == "done":
        ok, n_err = report()
        if a.cmd:
            run_commands(proc, a.cmd)
        proc.stdin.write("stop\n")
        proc.stdin.flush()
        try:
            proc.wait(120)
            print(f"Stopped cleanly (exit {proc.returncode}).")
        except subprocess.TimeoutExpired:
            proc.kill()
            print("!! Did not stop within 120s - killed.")
        sys.exit(0 if n_err == 0 else 1)

    print(f"!! Server {'crashed / exited early' if state == 'exited' else f'did not finish within {timeout}s'}.")
    if state == "timeout":
        proc.kill()
    report()
    print("--- last log lines:")
    tail()
    crashes = sorted((SRV / "crash-reports").glob("*.txt"), key=lambda p: p.stat().st_mtime) if (SRV / "crash-reports").exists() else []
    if crashes and crashes[-1].stat().st_mtime >= t0:
        print(f"--- crash report: {crashes[-1]}")
        for l in crashes[-1].read_text(encoding="utf-8", errors="replace").splitlines()[:25]:
            print("   |", l[:240])
    sys.exit(1)


if __name__ == "__main__":
    main()
