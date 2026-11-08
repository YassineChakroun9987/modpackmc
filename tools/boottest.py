"""Boot the dev server headless, wait until it is up (or dies), report, then stop it cleanly.

Usage:  python -I tools/boottest.py [timeout_seconds]     (default 300)

Exit code 0 = reached "Done" with no ERROR lines; 1 = errors, crash or timeout.
For normal play use server/start.bat instead (it gives you a console window).
"""
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boottime import LOG, report  # noqa: E402

SRV = Path(__file__).resolve().parent.parent / "server"
JAVA = Path(os.environ["APPDATA"]) / ".minecraft/runtime/java-runtime-delta/windows/java-runtime-delta/bin/java.exe"


def port_open(port=25565):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def tail(n=30):
    if LOG.exists():
        for l in LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-n:]:
            print("   |", l[:240])


def main():
    timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    if port_open():
        sys.exit("Server already running on 25565. Stop it first: python -I tools/rcon.py stop")
    nf = re.search(r'set "NEOFORGE=([\d.]+)"', (SRV / "start.bat").read_text()).group(1)
    t0 = time.time()
    proc = subprocess.Popen(
        [str(JAVA), "@user_jvm_args.txt", f"@libraries/net/neoforged/neoforge/{nf}/win_args.txt", "nogui"],
        cwd=SRV, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, text=True)

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
        proc.stdin.write("stop\n")
        proc.stdin.flush()
        try:
            proc.wait(90)
            print(f"Stopped cleanly (exit {proc.returncode}).")
        except subprocess.TimeoutExpired:
            proc.kill()
            print("!! Did not stop within 90s - killed.")
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
