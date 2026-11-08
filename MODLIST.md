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
| Structurify | 2.0.43 | both | **The one tool that controls structure placement**: overlap prevention, global spacing ×1.5, per-structure flatness checks and biome lists. Config: `server/config/structurify.json` | tuned |

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

### Worldgen: dungeons, ruins and exploration (added 2026-11-09)
Every structure here picks biomes by **tag** (D&T: 90 of 97), so they all reach Terralith, Nullscape and JNE biomes. `tools/structinfo.py` found **0 file conflicts** between any two mods.

| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| Dungeons and Taverns | v4.4.4 | both | 97 structures: taverns, crypts, shrine towers (combat trials, tiers 1–5), illager manors, witch villas, Nether Keep, quest-trader maps | — | 2 orphaned advancements repaired | tuned |
| When Dungeons Arise | 2.1.68 | server | 40 huge dungeons: Heavenly Rider sky fortresses, Mechanical Nest, Foundry, Coliseum, Plague Asylum, Shiraz Palace, Thornborn Towers | — | 2 orphaned advancements repaired; flatness check on 5 surface builds | tuned |
| WDA: Seven Seas | 1.0.4 | server | Pirate and naval ships: Victory Frigate, Unicorn Galleon, Corsair Corvette, Pirate Junk, Small Yacht | — | — | testing |
| The Lost Castle | 2.1.0 | server | One huge, rare castle dungeon (≈9,500 blocks from spawn on our seed) | — | — | testing |
| Philips Ruins | 1.21.1-2.0 | both | 17 ruins with loot: ancient crypts, dungeons, towers | — | — (known harmless error, see notes) | testing |
| Grim Kingdoms: Lost Structures & Ruins (Vanilla Ed.) | 2.0.0 | both | 65 lost-kingdom ruins, watchtowers, camps | — | — | testing |
| Ember's Castles and Keeps | 1.0.9.1 | server | 8 towers and keeps, including an undead castle and pillager towers | — | — | testing |
| **ChoiceTheorem's Overhauled Village (CTOV)** | 3.6.4 | server | **Replaces the vanilla villages** (owner: "no classic vanilla villages"): 21 biome variants in small, medium and large sizes, fortified versions, + pillager outposts | Lithostitched | vanilla villages disabled in Structurify; 7 dead *Wares*-compat loot tables disabled | tuned |
| Towns and Towers | 1.13.11 | both | Extra village styles and biome pillager outposts (24 outpost + 15 village variants), alongside CTOV | Cristel Lib | Cristel's auto-config for *other* mods turned off | tuned |
| Sky Villages | 1.0.6 | server | Floating villages high above the land | Architectury | — | testing |
| Ember's Floating Islands | 1.5.3 | server | 17 sky islands (amethyst, cemetery, cherry shrine, camps) | — | — | testing |
| Sky Whale Ship | 1.0.3 | both | Giant flying whale ships with an arena | — | — | testing |
| Eternal Nether | v21.1.3 | both | Nether exploration: Citadel, Piglin Manor, Catacombs (+ mobs) | Puzzles Lib | — | testing |

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
| YetAnotherConfigLib (YACL) | 3.8.2 | both | Structurify | No | needed |
| Resourceful Config | 3.0.11 | server | Structure Layout Optimizer | No | needed |
| Cristel Lib | 3.1.7 | both | Towns and Towers. **Auto-config disabled** (`config/cristellib/auto_config_settings.json5`) so it doesn't fight Structurify | No | needed |
| Cloth Config API | 15.0.140 | both | Cristel Lib | No | needed |
| Architectury API | 13.0.11 | server | Sky Villages | No | needed |
| Puzzles Lib | v21.1.66 | both | Eternal Nether | No | needed |

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
| Structure Layout Optimizer | 1.0.12 | server | Faster generation of big jigsaw structures (WDA, D&T, T&T) | Resourceful Config | testing |

### Gameplay
| Mod | Version | Side | What it improves | Depends on | Status |
|---|---|---|---|---|---|
| Jade | 15.10.6 | both | Shows what you're looking at: block or mob, health, which mod it's from | (JEI, optional) | testing |
| AppleSkin | 3.0.9 | both | Shows food and saturation values | none | testing |
| AttributeFix | 21.1.3 | both | Removes vanilla stat caps (armor, damage, …) so RPG gear can go higher | Bookshelf, Prickle | testing |
| Controlling | 19.0.5 | client | Searchable keybind menu that shows conflicts. Needed once dozens of mods add keys | Searchables | testing |
| Mouse Tweaks | 2.26.1 | client | Drag and scroll-wheel item moving in inventories | none | testing |
| Traveler's Titles | 5.1.3 | client | RPG-style title on screen when you enter a new biome or dimension | YUNG's API | testing |
| Lootr | 1.11.38 | both | **Every player gets their own loot** from each structure chest, so friends don't loot-steal | none | testing |

---

## On deck (planned, not installed)
| Mod | Category | Waiting for |
|---|---|---|
| AllTheLeaks | QoL · performance | CurseForge-only. We can't checksum-verify CurseForge files without an API key, so add it by hand once the pack is big |
| Configured + Catalogue | QoL | CurseForge-only (same) |
| ProbeJS | Editing (dev machine only) | When we start writing KubeJS scripts (autocompletion in VS Code) |
| Castle in the Sky · Ancient Remnants · Illager Structures | Main · structures | CurseForge-only (we have the chinatown jars, unverified). Castle in the Sky is in the story (Violet). Illager Structures uses vanilla biome IDs only, so it needs a Structurify biome list first |
| *Considered and left out (2026-11-09)* | | Moog's Voyager Structures (130 mostly tiny decorations that clutter Terralith) · Trek (beta; overlaps D&T) · Repurposed Structures (vanilla variants that overlap YUNG's) · Awesome Dungeon ×3 (vanilla biome IDs only) · Explorify (vanilla-style) |
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
- `Error loading class: com/simibubi/create/…`: Lootr's optional Create compatibility. It goes away once Create is installed.
- `[spark] Timed out waiting for world statistics`: spark's stats timing out while the server is busy generating a world.
- **Known ERROR, explained:** `Block-attached entity at invalid position`.
  - **Cause:** a structure template hangs a painting or item frame where no wall survived, so the game drops it.
  - **Source:** traced with `tools/whatstructure.py` + `/locate` to **`philipsruins:ancient_dungeon`** (12 blocks from the error spot, 6× at spawn generation on our seed). Seen once from YUNG's on another seed.
  - **How it's reported:** `boottime.py` still **counts and shows** it as "known & explained". It's never hidden, and it doesn't fail a boot test.

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

#### Structure placement: Structurify (`server/config/structurify.json`)
Structurify is the **only** thing that controls placement. Cristel Lib's auto-config is switched off.

| Setting | Value | Why |
|---|---|---|
| `prevent_structure_overlap` | on | No structure may cut into another |
| Global spacing ×1.5 | on | ~15 structure mods at their default density would crowd every hill |
| `minecraft:villages` | exempt (default spacing) | The prologue needs a village at spawn; the Blue class lives in villages |
| `betterstrongholds:stronghold` | exempt | ×1.5 pushed the stronghold ring from ~2,400 to ~4,450 blocks; exempt brings it back to ~2,100 |
| Flatness check (AUTO) | `dungeons_arise:` illager_windmill, wishing_well, giant_mushroom, jungle_tree_house, shiraz_palace | Surface builds with no terrain adaptation. Instead of floating on Terralith slopes, they only spawn on flat ground |
| **Disabled** | `minecraft:village_plains`, `_desert`, `_savanna`, `_snowy`, `_taiga` | Owner wants no classic villages. CTOV only *outweighs* them and has no "vanilla off" switch. `/locate` now answers "structure is currently disabled" |

**Left alone on purpose:**
- WDA's fixed-height structures (Heavenly sky fortresses at y200, Mechanical Nest, Thornborn and Bandit Towers) are meant to float.
- WDA's deliberately sunk ones (Infested Temple, Kisegi Sanctuary at −32) have their own foundations.

**Tuning:** fly around in spectator mode. If something still floats or the land feels crowded or empty, add an entry here. Structurify's in-game screen (Mods → Structurify) edits the same file.

#### Dungeons and Taverns: repaired advancements
- `minecraft:wander_add_map` and `minecraft:give_quest_trader_trade` name a parent `minecraft:root` that doesn't exist, so the game dropped them.
- They're hidden triggers that make **wandering traders sell D&T structure maps** and enable **quest-trader trades**.
- `server/kubejs/data/minecraft/advancement/` ships them without the bad parent. They have no `display`, so they stay invisible.

#### When Dungeons Arise: repaired advancements
- *Guns and Roses* (`find_thornborn_towers`) and *Fishing In The Dark* (`find_fishing_hut`) point at the removed `find_small_prairie_house`.
- `server/kubejs/data/dungeons_arise/advancement/` re-attaches them to `dungeons_arise:wda_root`.

#### CTOV: villages
- **How it works:**
  - CTOV registers its villages in code and adds them to the `#minecraft:village` tag, so Village Spawn Point, village maps and raids treat them as villages.
  - Weights live in `config/ctov-common.toml`: small 10, medium 4, large 1, outposts 1, plus a list of enabled variants.
  - Its 1,040 Lithostitched modifiers are all *conditional* add-ons that put other mods' workstations into its villages when those mods are installed.
- **On our seed:** the nearest village to spawn is `ctov:medium/village_savanna_na` (226 blocks).
- **Dead data:** `server/kubejs/data/wares/loot_table/chests/village/*_warehouse.json` disables 7 loot tables CTOV ships for the *Wares* mod.
  - They use `minecraft:set_nbt`, which was removed in 1.20.5, so each logged an ERROR. Nothing in CTOV references them.
  - Delete the folder if we ever add Wares and CTOV updates them.
- D&T's extra pieces for vanilla taiga, jungle and swamp villages are unused now that vanilla villages are off. They're harmless.

#### Smaller notes
- D&T adds *extra* versions of structures that YUNG's also redesigns (Nether Keep, Witch Villa, Trident Trial Monument). They're additions, not replacements, so both coexist.
  - Its badlands miner outpost brings back the vanilla mesa mineshaft next to YUNG's. That's a minor duplicate; disable `minecraft:mineshaft_mesa` in Structurify if it bothers us.
- Towns and Towers' `exclusives/*` (culture-styled villages and outposts) aren't placed by default. Its normal biome villages and outposts are.
- The world was **regenerated 2026-11-09** with all structure mods. The terrain-only world (unplayed) is in `server/backups/`.

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
| 2026-11-09 | + Structurify, YACL | 34 | 19.9s | 0 |
| 2026-11-09 | + Structure Layout Optimizer, Resourceful Config | 36 | 19.9s | 0 |
| 2026-11-09 | + Lootr | 37 | 20.2s | 0 |
| 2026-11-09 | + Dungeons and Taverns | 38 | 21.8s → 21.1s | 1 → 0 (advancements repaired) |
| 2026-11-09 | + When Dungeons Arise | 39 | 25.3s → 25.9s | 1 → 0 (advancements repaired) |
| 2026-11-09 | + WDA Seven Seas | 40 | 25.7s | 0 |
| 2026-11-09 | + The Lost Castle | 41 | 26.4s | 0 |
| 2026-11-09 | + Philips Ruins | 42 | 26.8s | 0 |
| 2026-11-09 | + Grim Kingdoms | 43 | 25.8s | 0 |
| 2026-11-09 | + Ember's Castles and Keeps | 44 | 26.4s | 0 |
| 2026-11-09 | + Towns and Towers, Cristel Lib, Cloth Config | 47 | 27.8s | 0 |
| 2026-11-09 | + Sky Villages, Architectury | 49 | 27.8s | 0 |
| 2026-11-09 | + Ember's Floating Islands | 50 | 25.7s | 0 |
| 2026-11-09 | + Sky Whale Ship | 51 | 26.6s | 0 |
| 2026-11-09 | + Eternal Nether, Puzzles Lib | 53 | 27.5s | 0 |
| 2026-11-09 | Structurify config applied (overlap, ×1.5, flatness, exemptions) | 53 | 22.3–23.5s | 0 (+6 known) |
| 2026-11-09 | **New real world** with all structures | 53 | 58.9s (first generation) | 0 (+6 known), 20 TPS |
| 2026-11-09 | + CTOV | 54 | 23.3s | 7 → 0 (dead Wares loot disabled) (+6 known) |
| 2026-11-09 | Vanilla villages disabled (Structurify) | 54 | 23.4s | 0 (+6 known) |
| 2026-11-09 | **New real world** with CTOV villages (unplayed pre-CTOV world archived) | 54 | 23.5s | 0 (+6 known), 20 TPS |
