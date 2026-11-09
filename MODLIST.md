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
| Almost Unified | 1.4.2 | both | **No duplicate items:** one copper, tin, silver, steel… for every mod. Picks a preferred mod per material (`config/almostunified/`), swaps the rest in recipes, loot and drops | testing |
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
| Castle in the Sky | 1.21.1.1 | both | One floating Laputa-style castle dungeon with coloured keys, doors and a Laputa core. Found with the **levitation stone** (craftable, or from a master Cartographer). ≥10k blocks from spawn (14,484 on our seed). CurseForge-only, **verified**: identical SHA-1 to CurseForge's CDN file 8200620 | — | levitation stone recipe fixed; exempt from the ×1.5 spacing | tuned |
| Eternal Nether | v21.1.3 | both | Nether exploration: Citadel, Piglin Manor, Catacombs (+ mobs) | Puzzles Lib | — | testing |

### Magic (added 2026-11-09)
Each class draws its spells from one or two Iron's Spells schools (see `docs/CONTRACT.md` and each class chapter of the quest book).

| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| Iron's Spells 'n Spellbooks | 3.16.3 | both | **The magic system:** spellbooks, scrolls, mana, inscription table, mage armour sets, wizard towers and boss mages (Dead King, Echo of Tyros, Archevoker). Schools per class: Fire (Red), Nature (Orange), Lightning (Yellow), Holy + Evocation (Green), Ice (Blue), Nature + familiars (Indigo), Ender + Eldritch (Violet) | Iron's Lib, Curios, GeckoLib, Player Animator | — | testing |
| Cataclysm: Spellbooks | 1.1.11 | both | Iron's spells, spellbooks and an armour set made from Cataclysm boss materials (e.g. Bloom Stone, Cursium) | Ace's Spell Utils, AzureLib | — | testing |
| Discerning the Eldritch | 1.4.5 | both | Deepens the Eldritch school: Violet's late-game spells and gear | Iron's Spells, Ace's Spell Utils, AzureLib | Echo Greatsword taken out of `minecraft:swords` (its tag entry broke the whole tag) | tuned |
| Alshanex's Familiars | 5.0 | both | Summonable familiars that fight beside you and level up: the core of Indigo's beast-master kit | Iron's Spells, FamiliarsLib | — | testing |
| DarkDoppelganger | 4.0.0 | both | An Iron's boss that copies you and casts your own spells back | Iron's Spells, GeckoLib, Player Animator | — | testing |
| Galosphere | 1.5.5 | both | Crystal Canyons, Lichen Caves and Pink Salt caves, silver ore, allurite / lumiere crystals | — | — | testing |
| Galosphere Spellbooks | 1.1.5 | both | Iron's spellbooks and gear from Galosphere materials | Galosphere, Iron's Spells | — | testing |

### Classes, quests and levelling (added 2026-11-09)
| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| FTB Quests | 2101.1.38 | both | **The quest book ("The Book of Oa")**: the story, 7 class paths, the finale and the mod guides. Written as JSON in `quests/src/`, built by `tools/questgen.py` into `server/config/ftbquests/quests/` | FTB Library, FTB Teams, Architectury | all chapters are ours | tuned |
| FTB Teams | 2101.1.12 | both | **Parties.** A team shares quest progress; Open Parties and Claims uses the same teams | FTB Library | — | tuned |
| FTB XMod Compat | 21.1.14 | both | Lets FTB Quests see KubeJS stages (`gl_*`), which is how the story drives the quest book | — | — | tuned |
| Pufferfish's Skills | 0.19.2 | both | **Class skill trees:** an Adventurer tree for everyone + one tree per class, levelled by class XP. Datapack: `server/kubejs/data/greenlanterns/puffish_skills/` | — | all trees are ours | tuned |
| Pufferfish's Unofficial Additions | 2.2.8 | both | Extra XP sources and reward types for the skill trees | Pufferfish's Skills | — | testing |
| Pufferfish's Attributes | 0.8.3 | both | Extra attributes that skill nodes give (e.g. sprint speed, mining speed, healing) | — | — | testing |
| Village Spawn Point | 6.0 | server | New worlds spawn in the centre of a village: the Prologue's village | Collective | — | tuned |

### Combat and gear (added 2026-11-09)
| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| Better Combat | 2.4.0 | both | Weapon movesets: combos, sweeping swings, two-handers, dual wielding | Player Animator, Cloth Config | — | testing |
| Combat Roll | 2.0.6 | both | Dodge roll (with cooldown; enchantable) | Player Animator | — | testing |
| Simply Swords | 1.70.2 | both | 15 weapon types in every material plus ~40 unique legendary weapons in loot | Architectury, Fzzy Config, Simply Tooltips | — | testing |
| Dungeons Weapons | 9.0.1 | both | Minecraft Dungeons-style weapons (Stormlander, Soul Scythe, …) | — | Stormlander moveset parent fixed; Bone Cudgel / Scythe repair tag rebuilt (it named blocks with no item) | tuned |
| Epic Knights | 10.17 | both | Medieval armour (plate, chainmail, light), shields, lances, flails; armour can be dyed and decorated | Architectury, Cloth Config | — | testing |
| Shield Expansion | 1.4.3 | both | Shields parry, have stamina, and come in tiers | — | — | testing |
| Apotheosis | 8.9.0 | both | **Gear progression:** affix loot with rarities, gems and sockets, Apotheotic bosses, **world tiers** (Haven → Frontier → Ascent → Summit → Pinnacle) | Placebo, Apothic Attributes | — | testing |
| Apothic Attributes | 2.11.0 | both | The attribute system behind Apotheosis (crit, life steal, armour pierce…) and a full attribute screen | Placebo | — | testing |
| Apothic Enchanting | 1.6.4 | both | Reworked enchanting: bookshelves with stats (Eterna, Quanta, Arcana), higher enchant levels | Placebo, Apothic Attributes | — | testing |
| Apothic Spawners | 1.4.0 | both | Spawners can be mined and upgraded with modifiers | Placebo | — | testing |
| Artifacts | 13.2.5 | both | ~40 rare trinkets (Curios slots) found in chests, and Mimics | — | — | testing |

### Creatures, dragons, pets and bosses (added 2026-11-09)
| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| L_Ender's Cataclysm | 3.33 | both | Big structure bosses: Netherite Monstrosity, Ignis, the Harbinger (**Yellow trial**), the Leviathan, Ender Guardian, Maledictus, Scylla, Ancient Remnant | Lionfish API, Curios | 2 missing tool tags added empty | testing |
| Bosses of Mass Destruction | 1.3.3 | both | Night Lich (**Blue trial**), Nether Gauntlet (**Red trial**), Obsidilith, Void Blossom | GeckoLib, Cerbons API, Cloth Config | — | testing |
| Mowzie's Mobs | 1.8.2 | both | Frostmaw, Ferrous Wroughtnaut, Umvuthi, Sculptor, Naga, foliaaths and more | GeckoLib | — | testing |
| Born in Chaos | 1.7.6 | both | Dark-fantasy mobs and bosses (Lord Pumpkinhead, Supreme Bonescaller) | — | — | testing |
| Alex's Mobs Continued | 2.3.0 | both | ~90 animals and creatures; many tameable | CodxLib | — | testing |
| Ice and Fire: Community Edition | 2.0 | both | Fire, ice and lightning dragons (tameable, rideable), the Hydra (**Indigo trial**), sea serpents, deathworms, hippogryphs, dragonsteel | Jupiter, Uranus | — | testing |
| Book of Dragons | 1.4.1 | both | Tameable dragons from the How-to-Train-Your-Dragon world (Night Fury, Gronckle, …) | FAUNA Engine | — | testing |
| Mutant Monsters | 21.1.1 | both | Mutant zombie, skeleton, creeper and enderman mini-bosses | Puzzles Lib | — | testing |
| The Graveyard | 4.0.1 | both | Graveyards, crypts, undead; its Lich is called **the Corrupted Champion** here (**Violet trial**) | GeckoLib, VillagersTradingPlus | — | testing |
| Legendary Monsters | 2.2.4 | both | A set of legendary bosses with their own arenas; its Guide Book says where | — | 1 missing tool tag added empty | testing |
| Kings & Monsters | 1.2.2 | both | Ogre country and the Ogre King (**Orange trial**) | GeckoLib, Curios, Patchouli | — | testing |
| Devourer of Gods (DoG) | 1.2.0 | both | **The final boss**: a cosmic worm about 335 blocks long, summoned with a Cosmic Worm | GeckoLib | tuned for the endgame (`dog-common.toml`); the Cosmic Worm also needs a Chaos Shard | tuned |
| The Twilight Forest | 4.8.3345 | both | The Twilight dimension and its boss chain (Naga → Lich → Minoshroom → Hydra → Ur-Ghast → Snow Queen …) | — | — | testing |
| Companions! | 1.3.7 | both | New tameable companion creatures | Knight Lib | — | testing |
| Redomesticate | 2.0.0 | both | Better pets: pet beds, pet enchantments, pet commands (a fork of Domestication Innovation) | — | — | testing |
| Guard Villagers | 2.4.12 | both | Give a villager a sword or crossbow and it becomes a guard: the Prologue's raid defence | — | — | testing |
| Enhanced Celestials 2: Core + Default Lunar Events | 2.0.3.4 · 2.0.1.4 | both | Blood, blue, harvest and super moons (replaced EC 1 6.0.2.6 on 2026-11-09: it showed an "EC 2 is here" popup on every world join, with no setting to turn it off. Shader Support add-on skipped: it needs Iris) | CorgiLib, Data Anchor | — | testing |

### Create, airships and tech (added 2026-11-09)
| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| Create | 6.0.10 | both | Machines, conveyors, trains; Yellow's home mod | Flywheel, Ponder (bundled) | — | testing |
| Sable | 2.0.6 | both | Physics "sub-levels" that ships, and Create: Lanterns' planets (Oa, Korugar), are built on | — | — | testing |
| Create Aeronautics (bundled) | 1.3.2 | both | **Airships**: propellers, balloons, levitite. Includes Create: Simulated | Create, Sable | — | testing |
| **Create Cosmonautics** | 26.08.307 (**beta**, CurseForge-only; size matches CurseForge file 8612744) | both | **Space:** rockets, thrusters, titanium ore, the Moon and deep space. With it, Create: Lanterns creates **Oa** and **Korugar** as real worlds, and a lit ring can fly its bearer into space past ~20,000 blocks (with life support) | Create, Aeronautics, Sable (bundles Dimensional Sable 1.0.5) | added after the first pre-generation, so the world was generated again (titanium ore) | testing |
| Create Crafts & Additions | 1.7.2 | both | Electricity for Create (alternators, motors, wires) | Create | — | testing |
| **Create: Lanterns** | 20.11-alpha | both | **The heart of the story:** the power rings of every light, lanterns, power batteries, constructs, the crashed Lantern ship, Oa and Korugar. Private build, personal use | Create, Sable, Simulated, Aeronautics | server config tuned (rings don't choose on their own, deeds off); 24 items of unused lights hidden; 3 recipe categories fixed | tuned |
| Spectral Hub | 4 | both | Create: Lanterns add-on: press **J** for the spectrum screen. With our settings it says "Rings do not choose in this world" (the ring trial hands out rings) | Create: Lanterns | — | testing |
| Mekanism + Generators | 10.7.19 | both | Ore processing (up to ×5), power, the MekaSuit | — | — | testing |
| Applied Energistics 2 | 19.2.18 | both | Digital storage networks | GuideME | — | testing |
| Draconic Evolution | 3.1.4 | both | Endgame tech and armour; the **Chaos Guardian** on Chaos Island, whose shards unlock the final boss | Brandon's Core, CodeChicken Lib | — | testing |

### Farming (added 2026-11-09)
| Mod | Version | Side | Role in the pack | Depends on | Tweaks made | Status |
|---|---|---|---|---|---|---|
| Farmer's Delight | 1.3.4 | both | Cooking, new crops, the cooking pot and skillet, feasts | — | — | testing |

## 3. Dependencies

When a mod is dropped, check this table for libraries that become `orphaned`.

| Library | Version | Side | Required by | Bundled? | Status |
|---|---|---|---|---|---|
| mezz_config | 0.6.6 | both | JEI | Yes, inside the JEI jar | needed |
| Rhino | 2101.2.7-build.85 | both | KubeJS (needs ≥ 2101.2.7-build.81) | No | needed |
| Better Advanced Tooltips | 2101.1.0-build.5 | client | KubeJS (optional, client side) | No | needed |
| Bookshelf | 21.1.81 | both | AttributeFix, Enchantment Descriptions | No | needed |
| Prickle | 21.1.11 | both | AttributeFix, Enchantment Descriptions | No | needed |
| Searchables | 1.0.2 | client | Controlling | No | needed |
| Lithostitched | 1.8.1 | both | Terralith (needed on the client too, despite Modrinth's "server-only" label) | No | needed |
| YUNG's API | 5.1.9 | both | All YUNG's mods, Traveler's Titles | No | needed |
| Lodestone | 1.8.2 | both | Jaden's Nether Expansion | No | needed |
| Elysium API | 2.0.1 | both | Jaden's Nether Expansion | No | needed |
| YetAnotherConfigLib (YACL) | 3.8.2 | both | Structurify | No | needed |
| Resourceful Config | 3.0.11 | server | Structure Layout Optimizer | No | needed |
| Cristel Lib | 3.1.7 | both | Towns and Towers. **Auto-config disabled** (`config/cristellib/auto_config_settings.json5`) so it doesn't fight Structurify | No | needed |
| Cloth Config API | 15.0.140 | both | Cristel Lib, Better Combat, BOMD, Epic Knights | No | needed |
| Architectury API | 13.0.11 | both | Sky Villages, FTB mods, Simply Swords, Epic Knights, Uranus | No | needed |
| Puzzles Lib | v21.1.66 | both | Eternal Nether, Mutant Monsters | No | needed |
| Curios API | 9.5.1 | both | Iron's Spells, Cataclysm, Kings & Monsters (ring, necklace, charm slots; Artifacts and the Lantern rings use them too) | No | needed |
| GeckoLib | 4.9.3 | both | Iron's Spells, Iron's Lib, BOMD, Mowzie's Mobs, The Graveyard, Kings & Monsters, DoG, DarkDoppelganger | No | needed |
| Player Animator | 2.0.4 | both | Better Combat, Combat Roll, Iron's Spells, DarkDoppelganger | No | needed |
| AzureLib | 3.2.7 | both | Cataclysm: Spellbooks, Discerning the Eldritch | No | needed |
| Iron's Lib | 2.3.0 | both | Iron's Spells | No | needed |
| Ace's Spell Utils | 1.2.7.5 | both | Cataclysm: Spellbooks, Discerning the Eldritch | No | needed |
| FamiliarsLib | 2.0 | both | Alshanex's Familiars | No | needed |
| Lionfish API | 3.1 | both | L_Ender's Cataclysm | No | needed |
| Cerbons API | 1.3.0 | both | Bosses of Mass Destruction | No | needed |
| CodxLib | 1.6.1 | both | Alex's Mobs Continued (needed on the client too) | No | needed |
| Jupiter · Uranus | 2.3.7 · 2.4.1 | both | Ice and Fire CE | No | needed |
| FAUNA Engine | 1.1 | both | Book of Dragons | No | needed |
| Knight Lib | 2.0.5 | both | Companions! | No | needed |
| VillagersTradingPlus | 1.1.1 | both | The Graveyard | No | needed |
| Patchouli | 93 | both | Kings & Monsters (its guide book) | No | needed |
| Placebo | 9.9.4 | both | Apotheosis and the Apothic mods | No | needed |
| Fzzy Config | 0.7.7 | both | Simply Swords, Simply Tooltips | No | needed |
| Kotlin for Forge | 5.12.0 | both | Fzzy Config | No | needed |
| Collective | 8.84 | both | Village Spawn Point | No | needed |
| CorgiLib · Data Anchor | 5.0.0.10 · 2.0.0.18 | both | Enhanced Celestials 2 | No | needed |
| GuideME | 21.1.22 | both | Applied Energistics 2 (its in-game guide) | No | needed |
| Brandon's Core · CodeChicken Lib | 3.2.1 · 4.6.1 | both | Draconic Evolution | No | needed |
| Sophisticated Core | 1.5.31 | both | Sophisticated Backpacks | No | needed |
| Balm | 21.0.67 | both | Waystones | No | needed |
| FTB Library | 2101.1.39 | both | FTB Quests, FTB Teams, FTB Ultimine, FTB XMod Compat | No | needed |
| Simply Tooltips | 0.1.5 | client | Simply Swords (tooltips) | No | needed |

## 4. Our own mods

| Mod | Mod ID | Version | Side | What it stitches together | Source | Status |
|---|---|---|---|---|---|---|
| **Green Lanterns story engine** | (KubeJS scripts) | — | server | The Prologue (7-day raid, Warlord Vex, the crash), story NPCs (Elder Maren, Kaelen), class joining, the ring whispers and dreams, the **ring trial** (class / White / Black ring), boss hooks, `/gl` commands. `server/kubejs/server_scripts/story/` | ours | testing |
| **Class skill trees** | (datapack) | — | server | Pufferfish's Skills trees: Adventurer + 7 classes. `server/kubejs/data/greenlanterns/puffish_skills/` | ours | testing |
| **Tiered loot** | (datapack + KubeJS) | — | server | Five loot tiers injected into structure chests by difficulty, with items from every gear and magic mod, scaled by Luck; quest reward tables. `server/kubejs/data/greenlanterns/loot_table/`, `server/kubejs/server_scripts/loot/` | ours | testing |
| **The Book of Oa** | (FTB Quests) | — | both | The quest book: 10 story/class chapters + 16 mod guides. Source `quests/src/*.json`, built with `python -I tools/questgen.py` | ours | testing |
| **Pack glue** | (KubeJS) | — | server | Tag fixes, hidden items, the Cosmic Worm recipe, dead-data overrides (`docs/broken-data.md`) | ours | tuned |

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
| Waystones | 21.1.46 | both | Teleport network between waystones you've found (costs XP); waystones spawn in villages | Balm | testing |
| Xaero's Minimap + World Map | 26.6.0 · 1.47.0 | both | Minimap with waypoints and a full-screen world map (M) | — | testing |
| Open Parties and Claims | 0.33.0 | both | Claim land so friends and mobs can't grief it; **uses FTB Teams as its party system** | — | tuned |
| Sophisticated Backpacks | 3.26.20 | both | Upgradable backpacks (pickup, magnet, feeding, crafting…) | Sophisticated Core | testing |
| Corpse | 1.1.22 | both | When you die, your items stay in a corpse you can loot back (no despawn). Our `glue/corpse_quickloot.js`: right-click your own body = everything back in its old slot, Curios too; Shift + right-click = the normal window | — | testing |
| FTB Ultimine | 2101.1.15 | both | Hold the key (default `` ` ``) to mine a whole vein or tree at once (64 blocks) | FTB Library | testing |
| Polymorph | 1.1.0 | both | Pick which output you get when two mods' recipes overlap | — | testing |
| Enchantment Descriptions | 21.1.11 | both | Every enchantment explains itself in its tooltip | Bookshelf, Prickle | testing |
| Clumps | 19.0.0.1 | both | Merges XP orbs (less lag after big fights) | — | testing |

---

## On deck (planned, not installed)
| Mod | Category | Waiting for |
|---|---|---|
| AllTheLeaks | QoL · performance | CurseForge-only. We can't checksum-verify CurseForge files without an API key, so add it by hand once the pack is big |
| Configured + Catalogue | QoL | CurseForge-only (same) |
| ProbeJS | Editing (dev machine only) | When we start writing KubeJS scripts (autocompletion in VS Code) |
| Ancient Remnants · Illager Structures | Main · structures | CurseForge-only (we have the chinatown jars; can be verified against CurseForge's CDN like Castle in the Sky). Illager Structures uses vanilla biome IDs only, so it needs a Structurify biome list first |
| *Considered and left out (2026-11-09)* | | Moog's Voyager Structures (130 mostly tiny decorations that clutter Terralith) · Trek (beta; overlaps D&T) · Repurposed Structures (vanilla variants that overlap YUNG's) · Awesome Dungeon ×3 (vanilla biome IDs only) · Explorify (vanilla-style) |
| YUNG's Better Caves | Main · worldgen | **Held back on purpose.** It rewrites cave generation, which could limit cave mods we add later (e.g. Alex's Caves). Only via a test world |
| Lithium | QoL · performance | After the magic mods are chosen (needs the Iron's Spellbooks shield fix) |
| Default Options | QoL | When we package the pack for other players |
| More Culling · BadOptimizations · Dynamic FPS | QoL · performance | Nice-to-have client extras |

**Design choices made 2026-11-09** (see `docs/FINAL-REPORT.md`): map = Xaero's · backpacks = Sophisticated Backpacks · gravestone = Corpse · waystones = Waystones · claims = Open Parties and Claims on FTB Teams. **Still yours to decide:** shaders (Iris) · EMI on top of JEI.

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
- `Error loading class: …` / `@Mixin target … was not found`: optional compatibility mixins for mods we don't run (Lootr ↔ Create before Create arrived, many others). Also `org/jetbrains/annotations` (compile-time only).
- `JarSelector: Attempted to select a dependency jar for JarJar which was passed in as source`: a library is both bundled and installed; the installed file wins.
- `azurelib: Correcting config value` · `Jupiter: Notice: Jupiter cannot resolve`: libraries tidying their own configs.
- `draconicevolution: Reactor detonation initiated / Calculating explosion ETA / Explosion Imminent`: Draconic Evolution's startup self-test noise, not a real reactor.
- `Found loot table element validation problem`: loot entries naming items that aren't installed are skipped.
- `KubeJS: Failed to parse recipe … Falling back to vanilla`: KubeJS doesn't model some recipe formats (Dungeons Weapons' smithing); the game still loads them normally.
- `RecipeManager: Skipping recipe …, not a json object`: our own `neoforge:false` overrides that switch dead recipes off (`docs/broken-data.md`).
- `[spark] Timed out waiting for world statistics`: spark's stats timing out while the server is busy generating a world.
- **Known ERROR, explained:** `Block-attached entity at invalid position`.
  - **Cause:** a structure template hangs a painting or item frame where no wall survived, so the game drops it.
  - **Source:** traced with `tools/whatstructure.py` + `/locate` to **`philipsruins:ancient_dungeon`** (12 blocks from the error spot, 6× at spawn generation on our seed). Seen once from YUNG's on another seed.
  - **How it's reported:** `boottime.py` still **counts and shows** it as "known & explained". It's never hidden, and it doesn't fail a boot test.
- **Known ERROR, explained:** `Jupiter: Failed to load config: ./config/…`: Ice and Fire's config library reads its config before creating it. Only on the very first boot of a server.
- **Known ERROR, explained:** `RuntimeDistCleaner: Attempted to load class net/minecraft/client/…`: FamiliarsLib's client-only mixin is tried on the dedicated server and skipped (×2 every boot). Clients are unaffected.
- **Fixed, no longer shown:** Create: Lanterns display cases used an invalid recipe category; Cataclysm / Legendary Monsters reference 3 tool tags they never ship (we add them empty); DoG's view-distance notice (view distance is 12 now).

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
| `castle_in_the_sky:castle_in_the_sky` | exempt | A unique landmark, already rare by design (500/300 chunks) |
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

#### Castle in the Sky
- **How we verified it** (CurseForge-only): the cfwidget API gave the official file ID (8200620). Downloading that from `mediafilez.forgecdn.net` gave the same SHA-1 as the chinatown jar (`5cb283e4…`). Use the same method for other CurseForge-only jars.
- **Recipe fix:** the jar's 1.21.1 build ships the levitation stone recipe in the **1.21.2+ format** (plain-string ingredients), which 1.21.1 can't read.
  - `server/kubejs/data/castle_in_the_sky/recipe/levitation_stone.json` is the same recipe in 1.21.1 format: elytra in the middle, netherite ingots and phantom membranes around it.
  - The recipe count went from 1,624 to 1,625, confirming it loads.
- **Story:** it's a late-game sky dungeon for the 🔵 Blue (ice battlemage, sky) path. The recipe needs an elytra and netherite, so it naturally comes after the End.

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
| 2026-11-09 | + Castle in the Sky | 55 | 22.8s → 22.9s | 1 → 0 (recipe fixed) (+6 known) |
| 2026-11-09 | **The big build** (+92 jars: magic, combat, creatures, bosses, tech, quests, skills, QoL) | 147 | 43.9s | tag cascade (DtE), 2 broken Dungeons Weapons files, 35 dead recipes/loot tables → 0 (+2 known) |
| 2026-11-09 | + story engine, quest book (26 chapters, 645 quests), skill trees (8), tiered loot (747 tables), party glue | 147 | 44.5s | 0 (+2 known), 0 unreviewed warnings; selftest 32/32 |
| 2026-11-09 | Quest book fixes: ids kept below 8000…, stage tasks as `gamestage` (FTB had silently re-id'd ~half the quests and dropped all 44 stage tasks) | 147 | 44.4s | 0 (+2 known) |
| 2026-11-09 | + Create Cosmonautics (Oa, Korugar, Moon, deep space become real dimensions) | 148 | 44.2s | 0 (+2 known); Lanterns config gained a `[cosmonautics]` section |
| 2026-11-09 | **Final real world**, pre-generated 1,200 blocks around spawn (≈22,800 chunks, ~8 min) | 148 | — | 0 (+ known Philips Ruins item frames during generation) |
| 2026-11-09 | Enhanced Celestials 1 → EC 2 Core + Default Lunar Events (no join popup); real world loads fine (one-time "enhancedcelestials MISSING" version note) | 149 | 44.5s | 0 (+2 known); selftest 32/32 |
