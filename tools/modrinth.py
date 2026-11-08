"""Look up, download and identify mods on Modrinth for this pack (MC 1.21.1, NeoForge).

Usage:
  python -I tools/modrinth.py info <slug> [<slug> ...]      latest version, sides, dependencies
  python -I tools/modrinth.py get  <slug> <dest_dir> [--beta]  download the primary file + verify sha512
  python -I tools/modrinth.py identify <file.jar> [...]        which Modrinth version is this exact jar?

Release builds are preferred. A beta/alpha is only picked if no release exists (or with --beta),
and it is always flagged.
"""
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console defaults to cp1252

API = "https://api.modrinth.com/v2"
HEADERS = {"User-Agent": "greenlanterns-modpack-tools/1.0"}
MC, LOADER = "1.21.1", "neoforge"


def api(path, **params):
    query = "?" + urllib.parse.urlencode({k: json.dumps(v) for k, v in params.items()}) if params else ""
    req = urllib.request.Request(API + path + query, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pick_version(slug, allow_beta=False):
    versions = api(f"/project/{slug}/version", game_versions=[MC], loaders=[LOADER])
    if not versions:
        return None, None
    releases = [v for v in versions if v["version_type"] == "release"]
    chosen = versions[0] if (allow_beta or not releases) else releases[0]
    newest = versions[0] if versions[0] is not chosen else None
    return chosen, newest


def primary_file(version):
    return next((f for f in version["files"] if f["primary"]), version["files"][0])


def project_names(ids):
    if not ids:
        return {}
    return {p["id"]: f'{p["title"]} ({p["slug"]})' for p in api("/projects", ids=sorted(ids))}


def cmd_info(slugs):
    for slug in slugs:
        try:
            p = api(f"/project/{slug}")
        except urllib.error.HTTPError as e:
            print(f"== {slug}: not found on Modrinth ({e.code})\n")
            continue
        print(f'== {p["title"]} ({p["slug"]})  client:{p["client_side"]}  server:{p["server_side"]}  '
              f'license:{p["license"]["id"]}')
        v, newest = pick_version(slug)
        if not v:
            print("   NO 1.21.1 NeoForge version\n")
            continue
        f = primary_file(v)
        flag = "" if v["version_type"] == "release" else "   <-- NOT A RELEASE"
        print(f'   {v["version_number"]}  [{v["version_type"]}]  {v["date_published"][:10]}  {f["filename"]}{flag}')
        if newest:
            print(f'   (newer {newest["version_type"]}: {newest["version_number"]}, {newest["date_published"][:10]})')
        names = project_names({d["project_id"] for d in v["dependencies"] if d.get("project_id")})
        for kind in ("required", "optional", "incompatible", "embedded"):
            deps = [names.get(d.get("project_id"), d.get("file_name") or "?")
                    for d in v["dependencies"] if d["dependency_type"] == kind]
            if deps:
                print(f"   {kind}: {', '.join(deps)}")
        print()


def cmd_get(slug, dest, allow_beta):
    v, _ = pick_version(slug, allow_beta)
    if not v:
        sys.exit(f"{slug}: no 1.21.1 NeoForge version")
    f = primary_file(v)
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / f["filename"]
    req = urllib.request.Request(f["url"], headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    if hashlib.sha512(data).hexdigest() != f["hashes"]["sha512"]:
        sys.exit(f"{slug}: SHA512 MISMATCH, not saved")
    out.write_bytes(data)
    print(f'{out}  [{v["version_type"]}] sha512 OK')


def cmd_identify(files):
    for path in files:
        sha1 = hashlib.sha1(Path(path).read_bytes()).hexdigest()
        try:
            v = api(f"/version_file/{sha1}", algorithm="sha1")
        except urllib.error.HTTPError:
            print(f"{Path(path).name}: not a known Modrinth file (CurseForge-only or modified)")
            continue
        p = api(f'/project/{v["project_id"]}')
        print(f'{Path(path).name}: {p["title"]} ({p["slug"]}) {v["version_number"]} [{v["version_type"]}], genuine')


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "info":
        cmd_info(a[1:])
    elif len(a) >= 3 and a[0] == "get":
        cmd_get(a[1], a[2], "--beta" in a)
    elif len(a) >= 2 and a[0] == "identify":
        cmd_identify(a[1:])
    else:
        sys.exit(__doc__)
