# Green Lanterns Modpack

Fantasy RPG modpack: dungeons, dragons, schools of magic, plus a Green Lantern
storyline where what you do on the server builds an attribute, and crossing a
threshold earns your ring.

## Stack

| Thing     | Version                                   |
|-----------|-------------------------------------------|
| Minecraft | 1.21.1                                    |
| NeoForge  | 21.1.265 (same build as the `greenlanterns` TLauncher client; the version is set in `server\start.bat`) |
| Java      | 21, from the launcher runtime `%APPDATA%\.minecraft\runtime\java-runtime-delta` (system Java is 25, which NeoForge 1.21.1 isn't built for) |

## Folder layout

```
GREENLANTERS MODPACK/
├── README.md          this file
├── MODLIST.md         every mod, grouped into 5 categories: Editing / Main / Dependencies / Our own / QoL
├── mods-manifest.txt  every jar + side + SHA-1, generated (git tracks this instead of the jars)
├── docs/              design + research: STORY-design.md (the story and classes),
│                      RESEARCH-terrain.md, RESEARCH-foundations.md
├── client-only/       mods that go ONLY in the client (minimaps, shaders, sound, HUD)
├── server/            the NeoForge dedicated server
│   ├── start.bat      ← double-click to run (uses Java 21)
│   ├── mods/          mods that run on both sides (the client needs these too)
│   ├── config/        per-mod server/common configs (generated on first run)
│   ├── kubejs/        KubeJS scripts and data (startup_scripts must match the client's)
│   │   └── data/      our datapack fixes (lowercase file names only!), e.g. the mineshaft tag patch
│   ├── world/         the save (seed "greenlanterns"; still a dev world, see MODLIST › Main notes)
│   ├── backups/       archived worlds (git-ignored)
│   └── server.properties
└── tools/
    ├── modrinth.py    info / get / identify mods on Modrinth (downloads are sha512-verified)
    ├── boottest.py    boot the server headless → report → clean stop (exit 1 on errors)
    ├── boottime.py    report on the last boot: time, mods, errors, new warnings
    ├── checkdeps.py   missing or mismatched dependencies in a mods set
    ├── ping.py        is the server up?
    └── rcon.py        send a console command, e.g. python -I tools/rcon.py "list"
```

## Running the server

- **Start:** double-click `server\start.bat`. A console window opens; you can type commands there without a `/`.
- **Stop:** type `stop` in that window. Don't just close it, or the world may not save.
- **Connect:** in Multiplayer, add the server `127.0.0.1` (or `localhost`).

### Why server.properties is set the way it is
Minecraft rewrites this file on start and strips comments, so the reasons are listed here:

| Setting | Value | Why |
|---|---|---|
| `server-ip` | `127.0.0.1` | Only this PC can connect, nothing on the LAN or internet. Clear it to allow LAN friends. |
| `online-mode` | `false` | TLauncher "free" accounts can't authenticate with Mojang. Safe only because of the line above. |
| `allow-flight` | `true` | Otherwise dragons and flying mounts get you kicked for "flying". |
| `max-tick-time` | `-1` | Heavy modded worldgen can stall a tick for more than 60s; stops the watchdog from killing the server. |
| `spawn-protection` | `0` | Dev server, so we build and test at spawn. |
| `enable-command-block` | `true` | For prototyping the storyline and quests. |
| `enable-rcon` | `true`, port 25575 | Lets `tools/rcon.py` (and Claude) run console commands. Bound to 127.0.0.1. |

`kayachin` is pre-opped at level 4 (the offline-mode UUID is in `ops.json`).

Memory: `server\user_jvm_args.txt` sets 2G–6G. Raise `-Xmx` when the big content mods go in.

## Workflow: adding a mod

1. Classify it:
   - **Category:** Editing / Main / Dependency / Our own / Quality of life (see `MODLIST.md`).
   - **Side:** **both** (most content mods), **client-only** (minimaps, shaders, sounds, HUD), or **server-only**.
   - Note every library it needs; each one gets a row under Dependencies with "Required by".
2. Look it up and download it:
   - Run `python -I tools/modrinth.py info <slug>` to see the version, sides and dependencies.
   - Then run `python -I tools/modrinth.py get <slug> <folder>`.
3. Put the jar in `server\mods\` (both / server) or `client-only\` (client).
   - Copy every *both* and *client* jar into the greenlanterns instance as well.
   - Mismatched *both* mods will get you refused when you join.
4. Test it:
   - Run `python -I tools/checkdeps.py` on both sets.
   - Run `python -I tools/boottest.py` (with the server stopped).
     - For worldgen mods use `--fresh`, so each test generates a brand-new throwaway world.
     - Add `--cmd "locate structure <id>"` to prove a structure actually generates.
   - Join with the client.
5. Tweak the configs in `server\config\` (and `server\world\serverconfig\` for per-world configs).
6. Add or update the row in `MODLIST.md`.

## Version control (git)

This whole folder is a local git repository (no remote), so every config change can be undone.

| Tracked | Not tracked (see `.gitignore`) |
|---|---|
| docs, tools, README, MODLIST | mod jars (size and licences); `mods-manifest.txt` lists them instead |
| `server/config/`, `server/defaultconfigs/`, `server/kubejs/` | `server/world/`, which needs its own backups |
| `server.properties`, `start.bat`, `user_jvm_args.txt`, ops/whitelist | `server/libraries/` (re-created by the NeoForge installer), logs, crash reports |

- **Before each commit:** run `python -I tools/manifest.py`. It refreshes the jar list and checks the client instance is in sync.
- **What changed:** `git log --oneline`, and `git diff` for uncommitted edits.
- **Undo a file you haven't committed yet:** `git restore <file>`.
- **Undo a commit:** `git revert <commit>`.
- ⚠ `server.properties` contains the RCON password. Change it before ever pushing this repo anywhere public.

## Client

The client is the TLauncher instance **`greenlanterns`**. Its mods folder is
`%APPDATA%\.minecraft\versions\greenlanterns\mods`.

- It has to carry the same *both*-side mods as `server\mods\`, plus anything in `client-only\`.
- Don't use `chinatown` for this pack. It has ~89 mods the server doesn't, so it will be refused.
- If you update NeoForge, update the client and server together. Change the version in `server\start.bat` to match.
