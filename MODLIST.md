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

| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| *none yet* | | | | | | |

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

---

## On deck (planned, not installed)
| Mod | Category | Waiting for |
|---|---|---|
| AllTheLeaks | QoL · performance | CurseForge-only. We can't checksum-verify CurseForge files without an API key, so add it by hand once the pack is big |
| Configured + Catalogue | QoL | CurseForge-only (same) |
| ProbeJS | Editing (dev machine only) | When we start writing KubeJS scripts (autocompletion in VS Code) |
| Structurify (+ YACL) | Editing | When structure and dungeon mods arrive |
| Polymorph | QoL | When two mods' recipes start conflicting |
| Lithium | QoL · performance | After the magic mods are chosen (needs the Iron's Spellbooks shield fix) |
| Default Options | QoL | When we package the pack for other players |
| Enchantment Descriptions | QoL | When enchantment mods arrive |
| More Culling · BadOptimizations · Dynamic FPS | QoL · performance | Nice-to-have client extras |

**Design choices waiting for you:** terrain/biomes · map (Xaero's?) · backpacks · gravestone · waystones · shaders (Iris) · EMI on top of JEI?

---

## Notes per mod

### Log warnings we've reviewed (all harmless)
`tools/boottime.py` hides these so that only new warnings show up.
- `Reference map '…refmap.json' … could not be read`: FerriteCore, Bookshelf, Prickle, AttributeFix. NeoForge 1.21.1 doesn't use refmaps.
- `Static binding violation: PRIVATE @Overwrite … from mod modernfix`: the mixin system widens the method's visibility itself.
- `KubeJS: Plugin …ClientPlugin does not load on server side` / `does not have required mod 'architectury'`: client-only parts and an optional integration are skipped.
- `ModernFix: Dedicated server took X seconds` / `Initial datapack load took X s`: timing info only.
- `[spark] async-profiler engine is not supported for your os/arch (windows11/amd64)`: on Windows spark uses its built-in Java engine. That's fine.

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
