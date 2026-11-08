# Research: how to build the pack + base mods for NeoForge 1.21.1

*Compiled 2026-11-08.*

**Sources:**
- Version numbers were read from the Modrinth API and CurseForge file lists.
- Background comes from the official NeoForge, KubeJS and Modrinth docs, GitHub repos and issue trackers, and modding blogs.
- Reddit blocked our fetchers, so community opinion comes second-hand and is marked *(2nd-hand)*.
- ✔ = we double-checked it ourselves.

---

## 1. The short version

1. **Lock the terrain/biome stack first.** Make a new world after every worldgen change. Terralith can't be removed from an existing world. [Terralith](https://modrinth.com/datapack/terralith)
2. **One mod per niche:** one map, one backpack, one gravestone, one biome overhaul. Stacking biome mods (Terralith + Biomes O' Plenty) gives tiny biomes. [CurseForge FAQ](https://blog.curseforge.com/terralith-mod-faqs/)
3. **Control structure density with one tool: Structurify.** We'll be stacking many dungeon/structure mods. [Structurify](https://modrinth.com/mod/structurify)
4. **Boot the dedicated server after every mod**, not just the client. A mod's declared side means nothing until the server actually starts with it. *(We already do this.)*
5. **A performance base goes in before content:** ModernFix, FerriteCore, AllTheLeaks, Packet Fixer, spark (both sides); Sodium, ImmediatelyFast, Entity Culling (client).
6. **KubeJS + LootJS is the editing core on 1.21.1.** Skip CraftTweaker.
7. **Story stack:** FTB Quests + Easy NPC (with its FTB Quests compat) + Modonomicon. The ring is a Curios item.
8. **RAM:** about 8 GB is right for most packs. Above about 14 GB, garbage collection gets *worse*. Your TLauncher client is set to 21 GB. [moddedmc wiki](https://moddedmc.net/wiki/outofmemoryerror-heap-space)
9. **Don't redistribute mod jars** if the pack ever goes public. Publish a pack that *references* mods (.mrpack / CurseForge).
10. **Decide online vs offline mode before friends play for real.** Offline player data is keyed to names. Switching later orphans inventories, quest progress and the Lantern attribute.

---

## 2. Workflow tips

### Planning
- Write a one-paragraph pitch and a progression spine, e.g. *explore → dungeons → dragons → bosses → the ring*. Any mod that doesn't serve the spine gets cut.
- Pick between overlapping mods instead of keeping both.

### Worldgen and structures
- **Order:** terrain/biomes → structures → mobs. A new test world each time worldgen changes.
- **Density:**
  - **Structurify** (needs YACL): global and per-set spacing/separation, per-structure disabling, biome allow-lists.
  - **Sparse Structures** is a simpler single-multiplier alternative.
  - Use one or the other, not both.
- **Overlap:** *No Structure Overlap* exists for NeoForge 21.1.207+. [modpackindex](https://www.modpackindex.com/mod/86085/no-structure-overlap)
- **Pregenerate** the server world with Chunky and set a world border before anyone plays. Modded chunk generation is slow.
- **Tectonic** (terrain shape) works with Terralith. Use the *mod* version, which has Terratonic built in. [Tectonic](https://modrinth.com/mod/tectonic)

### Balance (RPG)
- **Spawns:** NeoForge biome modifiers are datapack JSON, no code needed. `add_spawns` / `remove_spawns`, and `neoforge:none` overrides another mod's modifier. [NeoForge docs](https://docs.neoforged.net/docs/1.21.1/worldgen/biomemodifier/) For rule-based spawns, use In Control! (tagged beta).
- **Difficulty scaling:** *Scaling Difficulty*, a NeoForge 1.21.1 port of RpgDifficulty, scales mobs with distance from spawn and has stat caps. Bosses are detected through the `#c:bosses` tag. [Modrinth](https://modrinth.com/project/Aht35CBK) *(not yet checked by us)*
- **Loot:** LootJS. **Ore and ingot duplicates:** Almost Unified.
- **What players complain about:** grindy "hand in 500 items" quests, HUD clutter, duplicate ores, obscure mods with no in-game guide, and updates that wipe their settings.

### Configs on NeoForge 1.21.1
| Folder | What it does |
|---|---|
| `config/` | **All** config types live here now. Forge-era guides that say "edit serverconfig" are outdated. |
| `world/serverconfig/` | Per-world override for SERVER-type configs only. Those are synced to clients. |
| `defaultconfigs/` | Only copied in when a config file is **missing**. It seeds new installs but never overwrites edits. |

- The client and the server should carry the **same** `config/` and `kubejs/`.
- STARTUP and COMMON configs aren't synced, and mismatches cause desyncs.
- Never ship `options.txt`. Use **Default Options** to set default keybinds and video settings.

[NeoForge config docs](https://docs.neoforged.net/docs/1.21.1/misc/config/)

### Testing and debugging
- **Logs:**
  - `logs/latest.log` and `logs/debug.log` (more detail), plus `crash-reports/`.
  - Search for `Mixin apply for mod` or `.mixins.json` to find the mod at fault.
  - Copy the logs before relaunching, because they get overwritten. [Modrinth support](https://support.modrinth.com/en/articles/8792916-debugging-minecraft-crashes)
- **Bad mod hunt:** remove half the mods, test, and repeat on the half that still breaks. Keep each mod together with its dependencies.
- **Lag hunt (spark):**
  - `spark profiler start --timeout 120`; add `--thread *` for worldgen lag.
  - Also `spark health` and `spark tickmonitor`.
  - On the client the command is `sparkc`.
  - [spark docs](https://spark.lucko.me/docs/Command-Usage)

### Version control and publishing (later)
- **git:** put `config/`, `defaultconfigs/`, `kubejs/` and the mod manifests under git. Ignore jars, `world/`, `logs/` and `crash-reports/`.
- **packwiz:** keeps the mod list as small TOML files and exports `.mrpack` (Modrinth) or a CurseForge zip.
  - It works with NeoForge, but has no tagged releases and an open bug in CurseForge export.
  - [packwiz](https://github.com/packwiz/packwiz)
- **ServerPackCreator** 9.4.0 builds a server zip and leaves out client-only mods. [GitHub](https://github.com/Griefed/ServerPackCreator/releases)
- **CurseForge:** the rules want packs built in the CurseForge App. Exports from other tools are a grey area.

### Licensing
- **Link to mods; don't bundle jars.** CurseForge authors can turn off third-party distribution of their files.
- **Modrinth packs** may include a file only if one of these holds:
  1. it's hosted on Modrinth,
  2. it has an open licence that allows redistribution,
  3. the mod's description grants permission, or
  4. you have the author's written permission.
- [Modrinth rules](https://support.modrinth.com/en/articles/8797527)

---

## 3. Proposed base stack, by our categories

Nothing here has been added yet. Each mod still goes through the one-at-a-time test. *Side: both / client / server.*

### 1 · Editing
| Mod | Version (1.21.1 NeoForge) | Side | Why | Verdict |
|---|---|---|---|---|
| KubeJS | 2101.7.2-build.381 ✔ | both | Recipes, tags, items, events; `kubejs/data` replaces datapack loaders | **core** |
| LootJS | 1.21.1-3.7.0 | both | Loot table editing (separate from KubeJS 7) | **core** |
| Structurify | 2.0.43 | both | Structure spacing for many dungeon mods | **core** once structure mods arrive |
| ProbeJS | 8.0.3 | client (**dev only**) | VS Code autocompletion for KubeJS scripts | dev machine only, never shipped |
| MoreJS | 0.16.0 | both | Villager trades, structure and enchant events | optional |
| FTB XMod Compat | 21.1.14 | both | Lets KubeJS drive FTB Quests (custom tasks/rewards) | when FTB Quests is added |
| Almost Unified | 1.4.2 | server (+client) | Merges duplicate ores/ingots | if material mods overlap |
| Item Obliterator | 2.3.0 | both | Completely disable items | when needed (last update 2025-06) |
| In Control! | 10.3.1 (beta) | server | Rule-based mob spawns | only if biome modifiers aren't enough |
| JEI | ours 19.69.0.457 = **beta** ✔; latest release 19.64.0.455 | both | Already in | keep; versions must match on client and server |
| ~~CraftTweaker~~ | 21.0.38 | both | ZenScript | **skip**: KubeJS covers it, with more addons |

### 5 · Quality of life: performance
| Mod | Version | Side | Verdict |
|---|---|---|---|
| ModernFix | 5.27.27 | both | **must** (leave "dynamic resources" off) |
| FerriteCore | 7.0.3 | both | **must** |
| AllTheLeaks | 1.1.16 | both | **must** (memory-leak fixes, big-pack essential) |
| Packet Fixer | 3.3.1 | both | **must** (stops oversized-packet kicks in big packs) |
| spark | 1.10.124 | both | **must** (profiler) |
| Chunky | 1.4.23 | server | **must** (pregeneration); already in chinatown |
| Sodium | 0.8.13 | client | **must** (renderer; see gotchas) |
| ImmediatelyFast | 1.6.15 | client | **must** |
| Entity Culling | 1.11.3 | client | **must** (whitelist giant bosses if they vanish) |
| Lithium | 0.15.4 | both | good, **needs the Iron's Spellbooks fix** (gotchas) |
| More Culling · BadOptimizations · Dynamic FPS | 1.0.11 · 2.4.1 · 3.11.4 | client | good |
| Clumps · FastWorkbench · FastFurnace | 19.0.0.1 · 9.1.3 · 9.0.1 | both | good |
| Krypton Reno | 0.2.28.1 | server | good (network) |
| Iris (+ Iris Flywheel Compat if Create) | 1.8.14-beta.1 (+2.4.0) | client | only if you want shaders; beta |
| Distant Horizons | 3.3.3 | both | optional and heavy |

### 5 · Quality of life: gameplay
| Mod | Version | Side | Status |
|---|---|---|---|
| Jade | 15.10.6 | both | in chinatown (skip WTHIT) |
| AppleSkin | 3.0.9 | both | in chinatown |
| Controlling + Searchables | 19.0.5 / 1.0.2 | client | in chinatown |
| Xaero's Minimap + World Map | 26.6.0 / 1.47.0 | both | in chinatown (skip JourneyMap and FTB Chunks; they'd duplicate it) |
| Inventory Profiles Next | 2.2.5 | client | in chinatown (needs libIPN + Kotlin for Forge) |
| Corpse | 1.1.22 | both | in chinatown (don't add a second gravestone mod) |
| Traveler's Backpack | 10.1.41 | both | in chinatown (*or* Sophisticated Backpacks, not both) |
| Mouse Tweaks | 2.26.1 | client | **add** |
| Configured + Catalogue | 2.6.3 / 1.11.2 | client | **add** (in-game config editor and mod list) |
| Polymorph | 1.1.0 | both | **add** (choose between conflicting recipes) |
| Enchantment Descriptions | 21.1.11 | client | **add** (RPG gear) |
| AttributeFix | 21.1.3 | both | **add** (lifts vanilla attribute caps, needed for RPG stats) |
| Default Options | 21.1.8 | client | **add** (ship default keybinds/settings) |
| Crash Assistant | 1.11.12 | client | good (helps friends report crashes) |

### 2 · Main: story framework (suggested; these carry the Green Lantern storyline)
| Mod | Version | Side | Why |
|---|---|---|---|
| FTB Quests (+ FTB Library, FTB Teams) | 2101.1.38 | both | Quest book with hidden chapters; biggest ecosystem |
| Easy NPC (+ EasyNPC × FTB Quests compat) | 7.18.0 (+1.0.2) | both | NPCs, dialogue trees and trades; dialogue that reacts to quest progress |
| Modonomicon | 1.123.0 | both | Lore book whose entries unlock as the story moves on (better than Patchouli for this) |
| Curios | 9.5.1 | both | Ring slot for the Lantern ring; already in chinatown |
| ~~CustomNPCs~~ | | | **avoid**: the only NeoForge 1.21.1 build is from 2024-12 |

### 3 · Dependencies these would bring in
Rhino and Better Advanced Tooltips (KubeJS ✔) · YACL (Structurify) · FTB Library and FTB Teams (FTB Quests) · Balm (Default Options) · Necronomicon API (Item Obliterator) · mezz_config (JEI, bundled)

### 4 · Our own mods: what the research says
- Prototype the Lantern attribute in **KubeJS** first (section 5). Port it to a real mod once the design settles.
- 1.21.1 mod template: [MDK-1.21.1-ModDevGradle](https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle).
- Store per-player data with NeoForge **data attachments**.
  - They are **not** kept on death unless the attachment sets `copyOnDeath`.
  - In 1.21.1 you send the client-sync packets yourself.
  - [docs](https://docs.neoforged.net/docs/1.21.1/datastorage/attachments)

---

## 4. Skip list
| Mod | Why |
|---|---|
| Embeddium | Last updated Jan 2025; Sodium now has official NeoForge builds |
| Noisium | Archived Nov 2025 |
| C2ME (NeoForge) | Alpha; open worldgen crash/freeze issues; risky with our structure-heavy plan |
| Moonrise | Beta, unmaintained for a year, conflicts with C2ME |
| KryptonFoxified | 2024 alpha; never combine with Krypton Reno |
| WTHIT, JourneyMap, FTB Chunks, Gravestone Mod, Sophisticated Backpacks | Duplicate something already chosen |

---

## 5. Gotchas for mods already in chinatown

1. **Sodium 0.8.13 is a backport.**
   - It breaks *Sodium Options API* and all its add-ons.
   - It needs Create Aeronautics ≥ 1.3.0 (you have 1.3.2), Sable ≥ 2.0.0 (you have 2.0.6) and Iris ≥ 1.8.13. [release notes](https://github.com/CaffeineMC/sodium/releases/tag/mc1.21.1-0.8.12)
2. **Iris must match Sodium exactly.**
   - Your 1.8.14-beta.1 + 0.8.13 pair matches.
   - **Iris + Sodium + Lodestone can hang while loading.** The issue is still open. [Iris #3350](https://github.com/IrisShaders/Iris/issues/3350)
   - If startup freezes, remove Iris first.
3. **Create with shaders** needs *Iris Flywheel Compat*. Without it, Flywheel's GPU instancing switches off and frame rates drop.
4. **Lithium breaks Iron's Spellbooks shields:** entities walk straight through them.
   - Fix: put `mixin.entity.collisions.intersection=false` in `config/lithium.properties`.
   - [Lithium #723](https://github.com/CaffeineMC/lithium/issues/723)
5. **Dynamic Surroundings:** update 0.4.7 → **0.4.9**. It fixes 10–30 ms frame stalls and adds performance presets. It's client-only.
6. **mezz_config:**
   - JEI 19.69 carries a bundled 0.6.6 copy (✔ seen in our server log).
   - chinatown also has a standalone 0.6.8 jar. NeoForge loads the highest version, so that's harmless.
   - Keep at most one standalone copy.
7. **Chest Tracker** in chinatown is an *unofficial* NeoForge port. The original is Fabric-only.
8. **NeoForge 21.1.265** is out; we're on 264 to match the client. Update both sides together later. There's no rush.
9. **Already the latest builds:** Create 6.0.10, Curios 9.5.1, Geckolib 4.9.3, Terralith 2.6.2, Lithostitched 1.8.1.

---

## 6. The Green Lantern mechanic: how packs do this today

The common approach without writing Java:
1. **KubeJS** keeps a hidden `willpower` number in the player's `persistentData`. Script events (kills, bosses, protecting villagers, refusing fear, …) add to it.
2. A copy goes to a **scoreboard**, so **Easy NPC** dialogue can check it ("the old guardian senses something in you…").
3. Crossing the threshold adds a **stage**. That unlocks a hidden **FTB Quests** chapter: the calling and the trial.
4. Completing it rewards the **ring**, a KubeJS-created item tagged `curios:ring`.
5. **Modonomicon** lore entries unlock along the way.

```js
// sketch only: KubeJS 7, server script
function addWill(player, n) {
  const d = player.persistentData, w = d.getInt('willpower') + n
  d.putInt('willpower', w)
  player.server.runCommandSilent(`scoreboard players set ${player.username} willpower ${w}`)
  if (w >= 1000 && !player.stages.has('lantern_worthy')) player.stages.add('lantern_worthy')
}
EntityEvents.death(e => { if (e.source.player) addWill(e.source.player, 10) })
```

Later this can become **our own mod**: a data attachment with `copyOnDeath`, a real ring item with powers, and proper network sync.

---

## 7. Decisions for you

1. **Online vs offline mode.**
   - TLauncher "free" accounts force offline mode.
   - Offline is fine while it's only you on localhost.
   - If friends will play for real, choose before that starts: switching later orphans everyone's progress.
   - **About TLauncher, verified:**
     - Malwarebytes flags it as a "potentially unwanted program" (`PUP.Optional.TLauncher`). That label means a cracked launcher with a risk of bundled adware; it is not a malware finding.
     - It's closed-source and shows ads.
   - **About TLauncher, contested:**
     - The 2022 "spyware" claims never came with technical evidence.
     - A rebuttal found no malware, but did find it uploads hardware info. *(2nd-hand)*
   - The community-standard setup is Prism Launcher + owned accounts + `online-mode=true`.
2. **Recipe viewer:** stay on JEI, or add EMI on top (EMI hides JEI and reuses JEI's plugins).
3. **Shaders yes/no:** decides whether Iris and its compat mod come in.
4. **Terrain stack:** Terralith alone, Terralith + Tectonic, or something else. This must be settled **before** structure mods.

## 8. Suggested build order
1. **Foundation:** the performance core + KubeJS/LootJS + QoL basics. These are low-risk, and they make every later test faster.
2. **Terrain and biomes:** decide and lock.
3. **Structures and dungeons,** one at a time, with Structurify tuning density as they stack.
4. **Main content:** magic schools, dragons, bosses, mobs. Balance with spawns, loot and difficulty scaling.
5. **Story framework:** FTB Quests, Easy NPC, Modonomicon. Prototype the Lantern attribute in KubeJS.
6. **Our own mods:** turn the prototypes into real mods.
