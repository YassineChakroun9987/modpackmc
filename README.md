# Green Lanterns Modpack

Fantasy RPG modpack for a server with friends: dungeons, dragons, schools of magic,
seven class paths (one per light of the emotional spectrum), and a Green Lantern
storyline. Each class's road ends with a mid-game boss and a ring trial that gives
you your class ring, or the White or Black ring, depending on your choices.

**Start here:** `docs/FINAL-REPORT.md` (what's in the pack, every design decision, what to test).

> **Phase: DEVELOPMENT** (owner, 2026-11-09). The server world may be regenerated whenever a
> worldgen change needs it: back up `server/world` to `server/backups/`, then
> `python -I tools/pregen.py --radius 1200`. When the owner says play has started, change this line to
> **Phase: PLAYING**. From then on there are no regenerations, and worldgen changes only reach new chunks.

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
├── docs/              FINAL-REPORT.md (start here), CONTRACT.md (names/stages/commands every
│                      script and quest uses), STORY-design.md, broken-data.md, research notes
├── quests/src/        the quest book's source (one JSON per chapter) → tools/questgen.py
├── client-only/       mods that go ONLY in the client (minimaps, shaders, sound, HUD)
├── server/            the NeoForge dedicated server
│   ├── start.bat      ← double-click to run (uses Java 21)
│   ├── mods/          mods that run on both sides (the client needs these too)
│   ├── config/        per-mod server/common configs (generated on first run)
│   ├── kubejs/        KubeJS scripts and data (startup_scripts must match the client's)
│   │   ├── server_scripts/  story/ (the story engine), glue/ (parties, skill tags), loot/,
│   │   │                    tweaks/, fixes/, dev/ (selftest, registry export)
│   │   └── data/      datapacks (lowercase file names only!): greenlanterns/ (skill trees,
│   │                  loot tables) + fixes for other mods' broken data
│   ├── world/         the save (seed "greenlanterns"), pre-generated 1,200 blocks around spawn
│   ├── backups/       archived worlds (git-ignored)
│   └── server.properties
└── tools/
    ├── modrinth.py    info / get / identify mods on Modrinth (downloads are sha512-verified)
    ├── boottest.py    boot the server headless → report → clean stop (exit 1 on errors)
    ├── boottime.py    report on the last boot: time, mods, errors, new warnings
    ├── checkdeps.py   missing or mismatched dependencies in a mods set
    ├── structinfo.py  structures per jar: biome tags vs IDs, terrain adaptation, vanilla overrides, file conflicts
    ├── whatstructure.py  which structures are at block x,z (reads saved region files)
    ├── questgen.py    quests/src → FTB Quests files (--check validates every id first)
    ├── pregen.py      pre-generate the world with Chunky, headless
    ├── disable_broken.py  switch off recipes/loot tables that point at missing items
    ├── loot/          gen_loot.py (tiered loot tables) + check_loot.py
    ├── skills/        gen_skills.py (Pufferfish trees) + check_skills.py
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
| `view-distance` | `12` | The final boss is ~335 blocks long; entities are only sent to clients inside the view distance. |
| `max-tick-time` | `-1` | Heavy modded worldgen can stall a tick for more than 60s; stops the watchdog from killing the server. |
| `spawn-protection` | `0` | Spawn is the story village: players need to build and defend there. |
| `enable-command-block` | `true` | Handy for admins; the story itself runs on KubeJS, not command blocks. |
| `enable-rcon` | `true`, port 25575 | Lets `tools/rcon.py` (and Claude) run console commands. Bound to 127.0.0.1. |

`kayachin` is pre-opped at level 4 (the offline-mode UUID is in `ops.json`).

Memory: `server\user_jvm_args.txt` sets 4G–10G. If you play on the same PC, give TLauncher 8–10 GB
(it was set to 21 GB, and both together won't fit in 32 GB).

**Friends:** see `docs/FINAL-REPORT.md` §2 (VPN + whitelist; offline mode means names can be faked).

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
   - For structure mods, first run `python -I tools/structinfo.py server/mods <new jar>`. It shows whether the mod uses biome tags and whether it overrides files another mod also ships.
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
