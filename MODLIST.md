# Mod list

Every mod in the pack is in exactly one of five categories. NeoForge only loads jars that
sit directly in `mods/` (it ignores subfolders), so this file is where the categories live.

| # | Category | What belongs here |
|---|---|---|
| 1 | [Editing mods](#1-editing-mods) | Tools that let us change other mods easily: recipes, loot, tags, configs, inspecting items/IDs |
| 2 | [Main mods](#2-main-mods) | The mods the pack is built around: dungeons, dragons, magic, mobs, worldgen |
| 3 | [Dependencies](#3-dependencies) | Libraries/APIs that are only here because another mod needs them |
| 4 | [Our own mods](#4-our-own-mods) | Mods we write ourselves to stitch the pack together (story, Lantern attribute, ring, cross-mod glue) |
| 5 | [Quality of life](#5-quality-of-life) | Makes playing smoother without adding content: performance, HUD info, inventory, controls. Often client-only |

**Legend**
- **Side:**
  - `both`: server + client.
  - `server`: server only.
  - `client`: client only. These go in `client-only/` and the greenlanterns instance, never in `server/mods/`.
- **Status:** `testing` → `tuned` → `locked`, or `dropped` (with the reason in the notes).
- **Dependency status:**
  - `needed`: at least one mod still uses it.
  - `orphaned`: nothing needs it any more → remove.

**Where the jars go**
- Server = `server/mods/` (every `both` and `server` mod).
- Client = `%APPDATA%\.minecraft\versions\greenlanterns\mods`: every `both` mod plus everything in `client-only/`.
- Check both with `python -I tools/checkdeps.py --side server server/mods` and `--side client <client mods dir>`.

---

## 1. Editing mods

| Mod | Version | Side | What we use it for | Status |
|---|---|---|---|---|
| Just Enough Items (JEI) | 19.69.0.457 (**beta**; latest release is 19.64.0.455) | both | Looking up item IDs, tags and recipes while we edit other mods. Also the players' recipe browser | testing |
| KubeJS | 2101.7.2-build.381 | both | The main editing tool: recipes, tags, custom items (the ring), event scripts (the willpower counter). Lives in `kubejs/` | testing |
| LootJS | 1.21.1-3.7.0 | server | KubeJS addon for loot tables and mob/chest drops | testing |

## 2. Main mods

### Worldgen: terrain (decided 2026-11-08, not to be changed)
| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| Terralith | 2.6.2 | both | **Overworld:** terrain + ~99 biomes (85 surface incl. Skylands, Moonlight Grove, Amethyst Canyon; 14 cave), Mage Towers, fortified villages. Vanilla blocks only | Lithostitched | — | locked |
| Nullscape | 1.2.14 | both | **End:** surreal 384-tall islands, 3 new biomes (Crystal Peaks, Shadowlands, Void Barrens) | — | — | locked |
| Jaden's Nether Expansion | 2.4.1 | both | **Nether:** reworks the 5 vanilla biomes (+ Black Ice Glaciers), new blocks and mobs, Sanctum / Chapel / Mega Fossil | Lodestone, Elysium API | 6 broken data files disabled | locked |

### Worldgen: structures (YUNG's)
| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| YUNG's Better Dungeons | 5.1.4 | server | Redesigned spawner dungeons (zombie, skeleton, spider, Nether) | YUNG's API | — | testing |
| YUNG's Better Mineshafts | 5.1.1 | server | 13 mineshaft styles matched to biome | YUNG's API | **Terralith cave-biome tag patch** | tuned |
| YUNG's Better Strongholds | 5.1.3 | server | Huge redesigned strongholds (15+ room types) | YUNG's API | — | testing |
| YUNG's Better Nether Fortresses | 3.1.5 | server | Redesigned fortresses (Keep, Lava Halls) | YUNG's API | — | testing |
| YUNG's Better Ocean Monuments | 4.1.2 | server | Redesigned ocean monuments | YUNG's API | — | testing |
| YUNG's Better Desert Temples | 4.1.5 | server | Redesigned desert temples with puzzles | YUNG's API | — | testing |
| YUNG's Better Jungle Temples | 3.1.2 | server | Redesigned jungle temples with traps | YUNG's API | — | testing |
| YUNG's Better Witch Huts | 4.1.1 | server | Redesigned witch huts + witch circles | YUNG's API | — | testing |
| YUNG's Better End Island | 3.1.2 | server | Redesigned main End island; the dragon is summoned at a bell tower | YUNG's API | — | testing |
| YUNG's Extras | 5.1.1 | server | Small Overworld structures and decorations | YUNG's API | — | testing |
| YUNG's Bridges | 5.1.1 | server | Bridges over rivers | YUNG's API | — | testing |

## 3. Dependencies

When a mod is dropped, check this table for libraries that become `orphaned`.

| Library | Version | Side | Required by | Bundled? | Status |
|---|---|---|---|---|---|
| mezz_config | 0.6.6 | both | JEI | Yes, inside the JEI jar | needed |
| Rhino | 2101.2.7-build.85 | both | KubeJS (needs ≥ 2101.2.7-build.81) | No | needed |
| Better Advanced Tooltips | 2101.1.0-build.5 | client | KubeJS (optional, client side) | No | needed |
| Bookshelf | 21.1.81 | both | AttributeFix | No | needed |
| Prickle | 21.1.11 | both | AttributeFix | No | needed |
| Searchables | 1.0.2 | client | Controlling | No | needed |
| Lithostitched | 1.8.1 | both | Terralith (needed on the client too, despite Modrinth's "server-only" label) | No | needed |
| YUNG's API | 5.1.9 | both | All YUNG's mods, Traveler's Titles | No | needed |
| Lodestone | 1.8.2 | both | Jaden's Nether Expansion | No | needed |
| Elysium API | 2.0.1 | both | Jaden's Nether Expansion | No | needed |

## 4. Our own mods

| Mod | Mod ID | Version | Side | What it stitches together | Source | Status |
|---|---|---|---|---|---|---|
| *none yet* | | | | | | |

## 5. Quality of life

### Performance
| Mod | Version | Side | What it improves | Depends on | Status |
|---|---|---|---|---|---|
| ModernFix | 5.27.27+mc1.21.1 | both | Faster startup, lower RAM, bundled vanilla/NeoForge bug fixes | none | testing |
| FerriteCore | 7.0.3 | both | Big RAM saving: deduplicates block states, models and item data | none | testing |
| Packet Fixer | 3.3.1 | both | Raises network packet limits so big modded data doesn't kick players | none | testing |
| spark | 1.10.124 | both | Profiler for lag hunting (`spark profiler`, `spark health`; `sparkc` on the client) | none | testing |
| Chunky | 1.4.23 | server | Pre-generates the world so exploring doesn't lag | none | testing |
| Sodium | 0.8.13 | client | Replaces the renderer: much higher FPS | none | testing |
| ImmediatelyFast | 1.6.15 | client | Faster HUD, text and entity rendering | none | testing |
| Entity Culling | 1.11.3 | client | Skips drawing mobs and block entities you can't see | none | testing |

### Gameplay
| Mod | Version | Side | What it improves | Depends on | Status |
|---|---|---|---|---|---|
| Jade | 15.10.6 | both | Shows what you're looking at: block or mob, health, which mod it's from | (JEI, optional) | testing |
| AppleSkin | 3.0.9 | both | Shows food and saturation values | none | testing |
| AttributeFix | 21.1.3 | both | Removes vanilla stat caps (armor, damage, …) so RPG gear can go higher | Bookshelf, Prickle | testing |
| Controlling | 19.0.5 | client | Searchable keybind menu that shows conflicts. Needed once dozens of mods add keys | Searchables | testing |
| Mouse Tweaks | 2.26.1 | client | Drag and scroll-wheel item moving in inventories | none | testing |
| Traveler's Titles | 5.1.3 | client | RPG-style title on screen when you enter a new biome or dimension | YUNG's API | testing |

---

## On deck (planned, not installed)
| Mod | Category | Waiting for |
|---|---|---|
| AllTheLeaks | QoL · performance | CurseForge-only. We can't checksum-verify CurseForge files without an API key, so add it by hand once the pack is big |
| Configured + Catalogue | QoL | CurseForge-only (same) |
| ProbeJS | Editing (dev machine only) | When we start writing KubeJS scripts (autocompletion in VS Code) |
| Structurify (+ YACL) | Editing | When structure mods beyond YUNG's arrive (density, overlap, biome lists, floating-dungeon fix) |
| Structure Layout Optimizer | QoL · performance | With When Dungeons Arise or other big jigsaw structures |
| YUNG's Better Caves | Main · worldgen | **Held back on purpose.** It rewrites cave generation, which could limit cave mods we add later (e.g. Alex's Caves). Only via a test world |
| Polymorph | QoL | When two mods' recipes start conflicting |
| Lithium | QoL · performance | After the magic mods are chosen (needs the Iron's Spellbooks shield fix) |
| Default Options | QoL | When we package the pack for other players |
| Enchantment Descriptions | QoL | When enchantment mods arrive |
| More Culling · BadOptimizations · Dynamic FPS | QoL · performance | Nice-to-have client extras |

**Design choices waiting for you:** map (Xaero's?) · backpacks · gravestone · waystones · shaders (Iris) · EMI on top of JEI?

---

## Notes per mod

### Log warnings we've reviewed (all harmless)
`tools/boottime.py` hides these so that only new warnings show up.
- `Reference map '…refmap.json' … could not be read`: FerriteCore, Bookshelf, Prickle, AttributeFix. NeoForge 1.21.1 doesn't use refmaps.
- `Static binding violation: PRIVATE @Overwrite … from mod modernfix`: the mixin system widens the method's visibility itself.
- `KubeJS: Plugin …ClientPlugin does not load on server side` / `does not have required mod 'architectury'`: client-only parts and an optional integration are skipped.
- `ModernFix: Dedicated server took X seconds` / `Initial datapack load took X s`: timing info only.
- `[spark] async-profiler engine is not supported for your os/arch (windows11/amd64)`: on Windows spark uses its built-in Java engine. That's fine.
- `Redundant @Unique on injector method netherexp$…` and `Not all defined tags … present: netherexp:…`: Jaden's Nether Expansion dev notices and empty tag definitions.
- `yungsapi: block minecraft:iron_ore added to BlockStateRandomizer exceeds max probabiltiy of 1`: a quirk in YUNG's own Better Strongholds data.
- `Ignoring unknown attribute 'forge:entity_gravity'`: mobs saved inside structure files with old Forge attribute names; the game skips them.
- Not whitelisted: `Block-attached entity at invalid position` (ERROR). It appeared once, on a random test seed: a structure's item frame had no wall. It's harmless, but ERRORs are never hidden. If it shows up on our seed, find the structure.

### 1. Editing

#### JEI
- File: `jei-1.21.1-neoforge-19.69.0.457.jar` (copied from the chinatown instance).
- On the server it handles cheat-mode item giving and recipe transfer. The browser itself is client-side.
- Its metadata says it supports Minecraft `[1.21, 1.21.1)`, which technically leaves out 1.21.1 itself. It looks like a typo in this beta. NeoForge loads it fine, and `tools/checkdeps.py` lists it as accepted.
- Later: hide the Green Lantern ring and other story items so nobody spoils the questline (with JEI's hide config or the `c:hidden_from_recipe_viewers` item tag).

#### KubeJS
- **Folders:** `server/kubejs/` holds `startup_scripts/`, `server_scripts/`, `client_scripts/` (client only), plus `data/`, `assets/` and `config/`.
  - **Startup scripts must be identical on client and server.** They register items, like the ring.
  - Server scripts only need to be on the server.
- **Reload:** `kubejs reload server-scripts` reloads scripts; `/reload` reloads recipes, tags and loot. Startup scripts need a restart.
- It ships an example `server_scripts/main.js` (it logs "Hello, World!"). We'll replace it once we start scripting.
- Modrinth lists Better Advanced Tooltips as *required*, but the KubeJS jar itself marks it as optional and client-side, so it's only on the client.
- `kubejs/data/` can stand in for a datapack-loader mod (Global Packs / Paxi / Open Loader).

#### LootJS
- Server-only (Modrinth marks the client side as unsupported), so it isn't in the client folder.

### 2. Main

#### Terrain decision (2026-11-08)
- **What we chose:** Terralith (Overworld) · vanilla + Jaden's Nether Expansion (Nether) · Nullscape + YUNG's Better End Island (End).
  - These were the most *flexible* options: they keep vanilla biome IDs, fill the common biome tags, and are stable releases.
  - The full comparison is in `docs/RESEARCH-terrain.md`.
- **What we deliberately didn't choose:**
  - Tectonic: makes non-adapting dungeons float and sky structures clip.
  - Biomes O' Plenty / Oh The Biomes We've Gone: tiny biomes or freezes alongside Terralith.
  - Incendium: an old alpha on 1.21.1, and it blocks other Nether biome mods.
  - Enderscape: its NeoForge version is abandoned and it clashes with Nullscape. Stellarity: final version, clashes with Better End Island.
- **World:** seed `greenlanterns` (numeric -655238224) is set in `server.properties`. Every test world and the real world use it, so results are reproducible.
- **This is still a dev world.** Structures only generate in new chunks, so we'll make the final world (and pregenerate it with Chunky) once all structure mods are in.

#### Jaden's Nether Expansion: disabled broken data
- JNE 2.4.1 ships 5 recipes and 1 advancement that point at items that don't exist in that version (`iron_scrap`, `igneous_reeds`, `warphopper_fur`, `indented_soul_slate_tiles`). That's an ERROR per file on every start.
- `server/kubejs/data/netherexp/` overrides each one with `{"neoforge:conditions":[{"type":"neoforge:false"}]}`, so it's skipped silently. Nothing playable is lost.
- **Delete that folder when JNE fixes them.**
- (Every file in `kubejs/data` must have a lowercase name. A `README.md` there crashed KubeJS at startup.)

#### YUNG's Better Mineshafts × Terralith: cave-biome patch
- **The problem** (Terralith issue #225): mineshaft styles look for *surface* biomes, but underground Terralith's 11 cave biomes win. Measured on our seed: **0 of 9** surface-type styles found near spawn.
- **The fix:** `server/kubejs/data/bettermineshafts/tags/worldgen/biome/has_structure/*.json` adds the matching cave biomes to each style (merge, `required: false`):

  | Style | Terralith cave biomes |
  |---|---|
  | oak | andesite, diorite, granite, tuff |
  | spruce | deep, infested |
  | ice + spruce_snowy | frostfire |
  | mushroom | fungal |
  | jungle + overgrown | underground jungle |
  | mesa + desert | thermal |
  | red_desert | mantle |

- **After the fix: 5 of 10** styles were found near spawn, the nearest 224 blocks away. The rest follow their rarer cave biomes.

#### YUNG's structure mods
- All are **server-only**. They aren't in the client instance and players don't need them.
- Traveler's Titles is the only client-side YUNG's mod.

### 3. Dependencies
*Only note a library here if it needs a config change or has a version conflict.*
- Rhino: KubeJS works with the stable release (2101.2.7-build.85). The newer 2101.2.8 is only a beta.

### 5. Quality of life

#### ModernFix
- File: `modernfix-neoforge-5.27.27+mc1.21.1.jar`, from Modrinth (sha512 checked). Licence LGPL-3.0, so it can be redistributed.
- **Sides:** it adds no content or network traffic, so a player can join with or without it. We run it on both sides for the speed and memory savings.
- **Configs:** `config/modernfix-mixins.properties` holds the feature toggles; `modernfix-common.toml` is the general config. All defaults.
- **Keep `mixin.perf.dynamic_resources` off** (the default). It's known to cause crashes and missing textures.
- Its "FerriteCore is not installed" warning went away once FerriteCore was added.

#### FerriteCore / Packet Fixer
- Default configs (`config/ferritecore-mixin.toml`, `config/packetfixer.properties`). No tweaks needed.

#### spark
- **Output timing:** spark replies after the command has already returned, so its output doesn't come back through `tools/rcon.py`. Run spark commands in the server console or in-game.

#### Chunky
- Server-only.
- **Don't pregenerate until terrain and structures are locked.** Pregenerated chunks keep the old worldgen.
- Typical use: `chunky radius 3000`, then `chunky start`.

#### Sodium
- 0.8.13 is a backport. It's incompatible with *Sodium Options API* and every add-on that needs it.
- If we add Iris later, it must be the build made for Sodium 0.8.13 (Iris 1.8.14-beta.1).

#### Entity Culling
- If a huge boss model vanishes when you look at it partly hidden, add that mob to Entity Culling's whitelist in its config.

#### AttributeFix
- `config/attributefix/` raises vanilla's attribute caps. Defaults are fine. Revisit this when RPG gear arrives.

---

## Boot history (server)
| Date | Change | Server jars | Boot | Errors |
|---|---|---|---|---|
| 2026-11-08 | First boot, JEI only (NeoForge 21.1.264; this boot created the world) | 1 | 13.8s | 0 |
| 2026-11-08 | NeoForge → 21.1.265 | 1 | 10.7s | 0 |
| 2026-11-08 | + ModernFix | 2 | 9.7s | 0 |
| 2026-11-08 | + FerriteCore | 3 | 9.7s | 0 |
| 2026-11-08 | + Packet Fixer | 4 | 9.7s | 0 |
| 2026-11-08 | + spark | 5 | 10.0s | 0 |
| 2026-11-08 | + Chunky | 6 | 9.8s | 0 |
| 2026-11-08 | + KubeJS, Rhino | 8 | 10.5s | 0 |
| 2026-11-08 | + LootJS | 9 | 11.0s | 0 |
| 2026-11-08 | + Jade | 10 | 10.9s | 0 |
| 2026-11-08 | + AppleSkin | 11 | 11.1s | 0 |
| 2026-11-08 | + AttributeFix, Prickle, Bookshelf | 14 | 11.7s | 0 |
| | *From here on, worldgen boots run in a fresh throwaway world (`boottest.py --fresh`), so the time includes creating that world.* | | | |
| 2026-11-08 | + Terralith, Lithostitched | 16 | 16.8s | 0 |
| 2026-11-08 | + Nullscape | 17 | 18.4s | 0 |
| 2026-11-08 | + Jaden's Nether Expansion, Lodestone, Elysium API | 20 | 18.1s → 20.2s | 6 → 0 (broken data disabled) |
| 2026-11-08 | + YUNG's API, Better Dungeons | 22 | 19.4s | 0 |
| 2026-11-08 | + Better Mineshafts | 23 | 20.3s | 0 |
| 2026-11-08 | + Better Strongholds | 24 | 20.0s | 0 |
| 2026-11-08 | + Better Nether Fortresses | 25 | 21.0s | 0 |
| 2026-11-08 | + Better Ocean Monuments | 26 | 21.6s | 0 |
| 2026-11-08 | + Better Desert Temples | 27 | 19.6s | 0 |
| 2026-11-08 | + Better Jungle Temples | 28 | 20.2s | 0 |
| 2026-11-08 | + Better Witch Huts | 29 | 23.7s | 0 |
| 2026-11-08 | + Better End Island | 30 | 23.6s | 1 (random-seed item frame; gone on our seed) |
| 2026-11-08 | + Extras, Bridges (fixed seed from here) | 32 | 20.9s | 0 |
| 2026-11-08 | **New real world** (seed `greenlanterns`), all of the above | 32 | 19.9s | 0 |
