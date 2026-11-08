# Research: terrain generation (Overworld, Nether, End)

*Compiled 2026-11-08 for NeoForge 1.21.1.*

**Sources:**
- Versions come from the Modrinth API (`tools/modrinth.py`) and CurseForge.
- Compatibility facts come from reading the structure and biome JSON **inside every chinatown jar**, plus mod pages, GitHub issues and three other packs installed on this PC (ATM10, SUPERIOR-RPG, BMC4).
- Reddit was unreachable, so community opinion is second-hand.
- Fantasy ratings are our judgement (1 = realistic, 5 = high fantasy).

> **Why this matters:** terrain can't be swapped later. Terralith "cannot be removed from an existing world", and changing biome mods means a new world. So we decide here, test in throwaway worlds, then lock it in.

---

## 1. Verdict at a glance

| Dimension | Recommended (safe, locked) | Fantasy upgrade to test before locking | Avoid |
|---|---|---|---|
| **Overworld** | **Terralith** | + **Tectonic** (huge mountains); + Regions Unexplored (more biomes) | Biomes O' Plenty or Oh The Biomes We've Gone together with Terralith (tiny biomes / freezes); Lithosphere |
| **Nether** | **Vanilla + Jaden's Nether Expansion** | + Amplified Nether (taller Nether, no new biomes) | Incendium (1.21.1 is an old *alpha*, and it stops other Nether biome mods) |
| **End** | **Nullscape + YUNG's Better End Island** | + Unusual End (biomes, mobs, structures) | **Enderscape** (NeoForge version abandoned, clashes with Nullscape); Stellarity (final version, clashes with Better End Island) |
| **Underground** | (Terralith's 14 cave biomes) | YUNG's Better Caves · Alex's Caves (port) | n/a |

**Needed alongside any choice:**
- **Structurify** fixes structure density, overlap, biome lists and floating dungeons.
- **Structure Layout Optimizer** makes big dungeons generate faster.
- A small **biome-tag patch** lets mods that only know vanilla biomes spawn in Terralith/Nullscape biomes (§6).

---

## 2. Overworld

| Mod | What it does | Biomes | Fantasy | Compatibility | 1.21.1 NeoForge | Verdict |
|---|---|---|---|---|---|---|
| **Terralith** *(have)* | New biomes + terrain shaping; **vanilla blocks only**; adds Mage Towers and Fortified Villages | **~99** (85 surface incl. 5 Skylands + 14 cave). Modrinth says "95+" | 3: "light fantasy". Skylands, Moonlight Grove, Amethyst Canyon, Mirage Isles, crystal caves | Fills 42 `c:` tags + vanilla tags, so tag-based structures and mobs find its biomes. Keeps all 53 vanilla biomes (they just get rarer). No per-biome toggle. Needs Lithostitched | 2.6.2 release | **Base pick** |
| **Tectonic** | Terrain shape only: giant mountains, islands, jungle pillars, lava tunnels | 0 | 2 (but makes dragon flights spectacular) | Official Terralith support built in (no Terratonic needed). Option `increased_height` raises the build limit to y640. **Makes floating/buried dungeons worse** (When Dungeons Arise has no terrain adaptation on 27/40 structures; Tectonic #217). Sky structures (Sky Villages, Floating Islands, Castle in the Sky, Sky Whales, Hollowmarch airship) can clip into peaks unless `increased_height` is on | 3.0.28 release | **Test it.** Beautiful, but costs structure quality |
| **Regions Unexplored** | Biomes + new blocks; Prismachasm, Bioshroom caves, Wisteria, Magnolia | 64 (Overworld + Nether) | 3 | Lithostitched-based since 0.6; per-biome weights. Untested with Terralith | 0.6.3 release | Optional add-on, test |
| Biomes O' Plenty | Biomes + new woods; Mystic Grove, Ominous Woods, Origin Valley | 61 | 3 | TerraBlender. With Terralith: **"very small biomes"**. Every build tagged beta | 21.1.0.14 beta | Instead of Terralith, never with it |
| Oh The Biomes We've Gone | Biomes, blocks, mobs; Enchanted Tangle, Weeping Witch Forest | 53 | **4** | Worldgen **freezes** on NeoForge 1.21.1 with BoP/RU (#405, #430); feature-cycle crashes | 2.6.3 release | Most magical, too risky |
| Atmospheric / Environmental / Autumnity | Flavour biomes | 14 / ~5 / ~3 | 2 | Need the *Terrabnormals* datapack with Terralith | 7.0.1 / 5.0.1 / 6.0.1 | Optional flavour |
| WWOO · Nature's Spirit · Geophilic | Realistic vanilla+ | 0 / 67 / 0 | 1–2 | n/a | releases | Skip (not fantasy) |
| Lithosphere | Terrain only | 0 | 1 | **Incompatible with Terralith** (Terralith #271) | 1.8.2 | Avoid |
| Wilder Wild | Vanilla+ | n/a | 2 | **No NeoForge 1.21.1** | none | Not possible |
| *Ember's Floating Islands (have)* | Sky-island **structures**, not terrain | 0 | 4 | Fixed sky height | 1.5.3 | Keep (doesn't affect this choice) |
| *Hollowmarch (have)* | **Structures**, mobs, enchants (Cloudbreaker airship) | 0 | 3 | Terralith support since 1.1.0. Check its Create/Supplementaries dependency claim | 1.3.0 | Keep (structures) |

### Underground options
| Mod | What | Fantasy | 1.21.1 |
|---|---|---|---|
| Terralith (built in) | 14 cave biomes (crystal, frostfire, …) | 3 | included |
| **YUNG's Better Caves** | Overhauls cave *carving* (lava caverns, underground rivers) | 2 | 3.1.6 release |
| YUNG's Cave Biomes | 2 cave biomes (Frosted, Lost Caves) | 2 | 3.1.1 release |
| **Alex's Caves (unofficial port)** | 5 huge themed cave biomes with bosses (magnetic, toxic, primordial, abyssal, candy) | **5** | 2.0.10 (community port, test) |

---

## 3. Nether

| Mod | What it does | New biomes | Fantasy | Compatibility | 1.21.1 NeoForge | Verdict |
|---|---|---|---|---|---|---|
| **Jaden's Nether Expansion** *(have)* | Reworks the 5 vanilla biomes; new blocks, mobs; Sanctum, Chapel, Mega Fossil structures | 0 new (4 planned) | 4 | Keeps vanilla biome IDs, so everything else still spawns | 2.4.1 release | **Keep** |
| Amplified Nether | Terrain only: Nether 256 tall, dramatic cliffs | 0 | 3 | Not with Incendium; untested with JNE | 1.2.16 release | Test |
| Incendium | Terrain + 8 biomes + 9 structures + *Hovering Inferno* boss + magic gear | 8 | **5** | 1.21.1 build is **5.4.4 alpha from Dec 2024** ("Incendium Legacy", only game-breaking fixes). **Blocks other Nether biome mods.** Makes Cataclysm's Ignis arena and JNE's sub-biomes rarer | 5.4.4 **alpha** | Most fantasy, too risky to lock in |
| Luminous: Nether | 2 biomes, 16 mobs, **6 bosses** | 2 | 4 | Not documented | 1.3.4 release | Interesting for boss content, test |
| Eternal Nether | Structures (Manor, Citadel, Catacombs), mobs | 0 | 4 | Uses vanilla biomes, safe | 21.1.3 release | Good structure add |
| Nether Depths Upgrade | Lava-sea fish, enchant, potion | 0 | 2 | Safe | 3.3 release | Safe add |
| BoP / Regions Unexplored Nether parts | ~5 biomes each | 5 | 3 | Come with their Overworld mods | n/a | Only if we take those mods |
| BetterNether: New Dawn | ~20 biomes, many blocks | ~20 | 4 | Unofficial port, BCLib stack | 21.0.30 | Too heavy |
| Cinderscapes · Infernal Expansion (original) | n/a | n/a | n/a | No NeoForge 1.21.1 | none | Not possible |

---

## 4. End

| Mod | What it does | End biomes | Fantasy | Compatibility | 1.21.1 NeoForge | Verdict |
|---|---|---|---|---|---|---|
| **Nullscape** | Terrain: surreal 384-tall islands, vanilla blocks | 4 | 4 | Works with Better End Island (ATM10 ships the pair). End cities rarer. **Awesome Dungeon End and Cataclysm's Ruined Citadel only find highlands**, so they need a tag patch | 1.2.14 release | **Pick** |
| **YUNG's Better End Island** | Redesigned main island; the dragon is summoned at a bell tower | 0 | 4 | With Nullscape: ✅. With Stellarity: ❌ | 3.1.2 release | **Pick** |
| Unusual End | ~4 biomes, ~11 mobs, ~9 structures | ~4 | 4 | "No known incompatibility". One crash report only when combined with *End's Phantasm* too. Needs Blueprint | 2.3.1b release | Optional, test |
| Stellarity | Full overhaul: 23 biomes, 40+ items, reworked dragon, new strongholds/cities | 23 | **5** | Not with Better End Island or BetterEnd. 3.1.0 is **the final 1.21.1 version** | 3.1.0 final | Fantasy, but a dead end |
| **Enderscape** *(have)* | Terrain + biomes + blocks | 4 | 4 | Replaces the End biome layout, so it **clashes with Nullscape** (#71, #135). The maintainer **stopped NeoForge/1.21.1 support (Oct 2026)**, so 1.0.9 beta is final | 1.0.9 **beta, EOL** | **Drop** |
| BetterEnd: New Dawn | Custom generator, 24+ biomes | 24+ | 5 | Unofficial, heavy BCLib stack | 21.0.39 | Too heavy |
| End Remastered | 16 custom Eyes of Ender; changes portal progression | 0 | 4 | Compatible with YUNG's Better Strongholds | 6.3.0 release | **Story candidate** (eyes as quest rewards) |
| The Outer End | n/a | n/a | n/a | No NeoForge 1.21.1 | none | Not possible |

---

## 5. YUNG's catalogue (all NeoForge 1.21.1 releases, all need YUNG's API 5.1.9)

**Does YUNG make terrain generators?** Yes, two, both Overworld underground only: **Better Caves** (cave carving) and **Cave Biomes** (2 biomes). Everything else is structures. YUNG makes no Nether or End *terrain* mod.

| Mod | What it changes | Version | Have? |
|---|---|---|---|
| Better Caves | **Cave terrain**: lava caverns, underground rivers, varied tunnels | 3.1.6 | – |
| Cave Biomes | **2 cave biomes** (Frosted Caves, Lost Caves) + blocks/mobs | 3.1.1 | – |
| Better Dungeons | Redesigned dungeons | 5.1.4 | ✔ |
| Better Mineshafts | Redesigned mineshafts | 5.1.1 | – |
| Better Strongholds | Redesigned strongholds (15+ room types) | 5.1.3 | ✔ |
| Better Nether Fortresses | Redesigned fortresses (Keep, Lava Halls) | 3.1.5 | ✔ |
| Better Ocean Monuments | Redesigned monuments | 4.1.2 | – |
| Better Desert Temples | Redesigned desert temples | 4.1.5 | – |
| Better Jungle Temples | Redesigned jungle temples | 3.1.2 | – |
| Better Witch Huts | Redesigned witch huts | 4.1.1 | – |
| Better End Island | Redesigned main End island + dragon summon | 3.1.2 | – |
| Extras | Small Overworld structures and decorations | 5.1.1 | – |
| Bridges | Bridges over rivers | 5.1.1 | – |
| Traveler's Titles | RPG-style "you entered <biome>" titles (great for immersion) | 5.1.3 | – |
| Ribbits | Frog villages in swamps | 4.1.6 | – |
| Menu Tweaks | Client menu UI | 2.1.2 | – |

**YUNG's conflicts:** Better End Island ✕ Stellarity. Better Strongholds probably overlaps with stronghold overhauls from Stellarity/Enderscape (unverified). Better Nether Fortresses is fine with Incendium and Nether biome mods.

---

## 6. Compatibility with your chinatown structure/boss mods

How each mod chooses where to spawn (read from the JSON inside every jar):
- **Biome tags (safe with any terrain mod):**
  - Structure mods: When Dungeons Arise (37/40), YUNG's ×3, Sky Villages, Sky Whale Ship, Floating Islands, Ancient Remnants, Castle in the Sky, Hollowmarch.
  - Mobs: Mowzie's, Mobs of Mythology, Fangs 'n Claws.
  - Berk's Dragon Academy.
- **Knows modded biomes already:** Dungeons and Taverns (Terralith, BoP, WWOO, RU) and Trek (Terralith, BoP, RU).
- **Vanilla biome IDs only, so they become *rarer* (not missing) in Terralith/Nullscape:**
  - Awesome Dungeon (+ Ocean, + End), Cataclysm (14/15 structures), Illager Structures (37/37) and Born in Chaos structures (25/31).
  - BOMD's Lich Tower and Obsidilith arena.
  - **Kings & Monsters** (outposts plains/swamp only; the Ogre King fort is swamp only).
  - **Fix:** add the matching Terralith/Nullscape biomes per structure in Structurify, or with a small tag datapack (we'll do this in `kubejs/data`).

| Mod | Terralith | Terralith + Tectonic | Incendium | Nullscape | Enderscape |
|---|---|---|---|---|---|
| When Dungeons Arise | ⚠ floats on slopes | ⚠ worse | – | – | – |
| Dungeons and Taverns, Trek, YUNG's | ✅ | ✅ (Trek ⚠ on slopes) | ✅ | ✅ | ✅ |
| Awesome Dungeon (+Ocean) | ⚠ rarer | ⚠ rarer | – | – | – |
| Awesome Dungeon End | – | – | – | ⚠ patch tags | ✅ |
| Sky Villages, Floating Islands, Castle in the Sky, Sky Whale | ✅ | ⚠ clips peaks | – | – | – |
| Cataclysm | ⚠ rarer | ⚠ rarer | ⚠ Ignis arena rarer | ⚠ patch Citadel tags | ✅ |
| BOMD, Born in Chaos, Kings & Monsters, Illager Structures | ⚠ rarer | ⚠ rarer | ✅ | ? | ✅ |
| Mowzie's, Hollowmarch, Mobs of Mythology, Fangs, Berk's, Waystones | ✅ | ✅ | ✅ | ✅ | ✅ |
| Jaden's Nether Expansion | – | – | ⚠ rarer | – | – |

✅ works · ⚠ works with a caveat · ❌ broken · ? unknown · – not that dimension

**Other notes:**
- Waystones' village waystones only appear in vanilla/supported villages, so not in Terralith's fortified villages.
- **Structure density with ~15 structure mods:**
  - Use **Structurify** alone, not with Sparse Structures, since both multiply spacing. SUPERIOR-RPG uses a ×1.8 spacing multiplier.
  - It also prevents overlap, can override terrain adaptation per structure (fixes floating dungeons), and checks flatness.
- **Performance:**
  - Pregenerate with Chunky.
  - Add Structure Layout Optimizer (1.0.12).
  - Lithium later.
  - Avoid C2ME (alpha on NeoForge).

---

## 7. What the CurseForge-only chinatown jars are
| Jar | What it is |
|---|---|
| castle_in_the_sky 1.21.1.1 | A floating Laputa-style castle dungeon with keys and puzzles. Found with a levitation stone from a master Cartographer; ≥10k blocks from spawn |
| kingsandmonsters 1.2.2 | Kings & Monsters: Ogre tribe with faction anger, **Ogre King boss**, ogre outposts and fort. Needs GeckoLib, Curios, Patchouli |
| ancient_remnants 1.0.2.2 | Ember's Ancient Remnants: 14 decorative megastructures (giant hand, pillars, aqueducts), no loot |
| illagerstructures 0.1.3 | 37 illager forts, galleons, ocean citadels, a monastery (Dawn of Time team) |
| fangs_n_claws 1.2.5 | ~20 RPG creatures, no structures |
| trek B0.6.2 | 139 structures incl. vanilla variants; Terralith/BoP/RU aware (beta) |
| Berk's Dragon Academy V0.5 BETA | `bda`, needs BlueLib; **Hooligan villages** and the **Red Death volcano**; dragons spawn by biome tags |
| **createlanterns alpha 20.11** | **Create: Lanterns**, the Lantern ring mod (see `docs/STORY-design.md`). Adds planets **Oa** and **Korugar** reached by Aeronautics ships |
| spectral_hub v4 | HUD showing per-light deed points for Create: Lanterns |

---

## 8. Test plan before locking in
1. **Make throwaway test worlds** on the dev server. Set `level-name` to `test_A` / `test_B` / `test_C`, one per combo; the real `world` stays untouched:
   - **A, safe:** Terralith · JNE · Nullscape + Better End Island.
   - **B, dramatic:** A + Tectonic (`increased_height` on).
   - **C, max biomes:** A + Regions Unexplored (+ Alex's Caves).
2. In each, fly around in spectator mode. Use `/locate structure` for When Dungeons Arise, Cataclysm, Sky Villages and Castle in the Sky, and visit them to check for floating or clipping.
3. Pick one, delete the test worlds, lock it in. The terrain jars then join MODLIST under **Main**, with status `locked`.
4. After the structure mods are in and tuned: pregenerate with Chunky.
