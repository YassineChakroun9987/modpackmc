# Story & Systems Design: *Blackest Night*

*Working design for the Green Lanterns modpack. Revision 2, 2026-11-09.*

**What changed in revision 2** (owner's decisions):
- New colour map for the classes.
- White and Black rings now come from **one key boss**, depending on how you kill it.
- The final boss is an **existing OP boss from a mod**, not Nekron.
- Create: Lanterns may be **modified freely**: the pack is for personal use only and won't be published.

> **How to read this:**
> - Every mod named here was checked for a NeoForge 1.21.1 build (versions in §11).
> - **(verify)** means the idea depends on a detail not tested in-game yet.
> - **Decision** marks choices still open (§12).

## Contents
1. [The story in one page](#1-the-story-in-one-page)
2. [The backbone: Create: Lanterns, and how we change it](#2-the-backbone-create-lanterns-and-how-we-change-it)
3. [The journey: acts and chapters](#3-the-journey-acts-and-chapters)
4. [Prologue: The Seventh Dawn](#4-prologue-the-seventh-dawn)
5. [The classes (the seven lights)](#5-the-classes-the-seven-lights)
6. [Leveling and the talent tree](#6-leveling-and-the-talent-tree)
7. [Gear ladder](#7-gear-ladder)
8. [Boss ladder](#8-boss-ladder)
9. [The corruption (the enemy grows)](#9-the-corruption-the-enemy-grows)
10. [The Crossroads (White / Black) and the finale](#10-the-crossroads-white--black-and-the-finale)
11. [Mods needed, by build phase](#11-mods-needed-by-build-phase)
12. [Decisions for you](#12-decisions-for-you)
13. [Implementation map (what builds what)](#13-implementation-map-what-builds-what)

---

## 1. The story in one page

**The threat.** Something is corrupting the universe. Undead, monsters and twisted creatures pour out of the dark between the stars, killing innocents and swallowing whole worlds. Now the corruption has reached Earth. *(The force behind it is the final boss, chosen in §10.)*

**The order.** On the planet **Oa**, the Guardians lead an alliance of seven Lantern Corps, each wielding one light of the spectrum. Earth needs warriors worthy of a ring, so the Guardians are watching.

**You.** You and your friends are young adventurers who wake up in a small village. A **pillager warband** camps on the ridge, and in **seven days** they'll attack. On the night you save the village, a Lantern ship crashes in the hills, and its dying pilot tells you what's coming.

**The road.** You grow in a **talent tree** and can follow one class or mix several. Each class is one **light**: an element, a fighting style, an aspect (the mods it focuses on), its own questline, gear, enemies and mount. As your class grows, its light **whispers** to you, then you **dream** of it. At the end of your class's road comes the **ring trial**, and the ring chooses you.

**The Crossroads.** One key boss stands between the ring-bearers and the end. *How* you kill it changes you forever:
- you keep your ring and it grows stronger, or
- the **White Light** claims you, or
- the **Black** does.

**The end.** All the paths join. Every ring-bearer, of every colour, stands together against the corruption's master: one of the most brutal bosses in the modded game.

---

## 2. The backbone: Create: Lanterns, and how we change it

**Create: Lanterns** (`createlanterns` alpha 20.11, by "The Team") and its HUD add-on **Spectral Hub** are in the chinatown instance. It gives us:
- **Rings:** a ring for each light, with 2 powers each plus an ultimate, flight, a hard-light suit, grip, and constructs you can ride.
- **Lanterns and power batteries.**
- **The calling:** whisper → dream → worthy → the ring comes.
- **Planets:** **Oa** (Citadel, Guardian Outpost, Lantern Spire, Central Power Battery) and **Korugar** (Dread Plains, Fear Bogs, Fear Spire, Sinestro's Watchtower), reached by **Create Aeronautics ships**.
- **Commands:**

| Command | What it does |
|---|---|
| `/createlanterns spectrum …` | show or **set** a player's deed points per light |
| `/createlanterns call …` | send a ring to a player |
| `/createlanterns crash …` | bring a Lantern ship down nearby |
| `/createlanterns battery small\|medium\|biggest` | build a Central Power Battery |
| `/createlanterns config` | list non-default settings |

**Because the pack is personal, we reshape the mod to fit our classes:**

| Change | How (verify exact syntax in-game) |
|---|---|
| **Natural deeds off**, because the mod's emotions (Yellow = fear, …) no longer match our classes | server config `deedWorth = 0` |
| **Class progress drives the light** | KubeJS mirrors each class's Pufferfish XP into that light's deed points with `/createlanterns spectrum set <player> <light> <points>`, so the mod's own story beats fire at our milestones |
| Whisper at **class level 10**, dream at **level 25** | map levels to `whisperAt` / `dreamAt` |
| **The ring never arrives on its own**; the ring trial delivers it | `ringAt` set very high; trial reward runs `/createlanterns call <player> <light>` |
| The ring still **rejects the unworthy** (e.g. someone else's class ring) | keep `ringsChoose = true` |
| **White and Black** only from the Crossroads boss (§10) | not called by deeds; given by script, and `whiteNeedsTheSeven` off |
| Joke lights (Xbox / PlayStation / Steam / WhatsApp) **off**. Ultraviolet / Gold off unless we keep secret classes | `lights.<colour>.enabled = false` |
| **Prologue crash** at the village | `/createlanterns crash green` after the Warlord falls |
| **Re-theme each light** to its class (names, Corps titles, power names, whispers) | language override in `kubejs/assets/createlanterns/lang/en_us.json`. For example, Yellow *Terror* → **Thunderclap**, *Cage* → **Storm Cage** |
| Later, if needed: a tiny **bridge mod** of ours for anything commands can't do (e.g. reading deed points) | "Our own mods" category |

---

## 3. The journey: acts and chapters

| Act | Name | Gear tier (Apotheosis world tier, verify) | What happens | Ring status |
|---|---|---|---|---|
| Prologue | **The Seventh Dawn** | Haven | Village, 7-day raid countdown, the Warlord, the crashed Lantern | none |
| I | **Proving Ground** | Haven → Frontier | First dungeons and bosses, first spells. **Choose your class(es)** | whispers (class level 10) |
| II | **The Seven Paths** | Frontier → Ascent | Each class's own chapter: aspect mods, class gear, mount, mid bosses. Corruption gets worse | dreams (class level 25) |
| III | **Worthy** | Summit | Late bosses, space travel to Oa / Korugar, the **ring trial** | **ring** |
| IV | **The Crossroads** | Summit → Pinnacle | The key boss. Your ring powers up, or turns **White**, or **Black** | ring+ / White / Black |
| V | **The Last Light** | Pinnacle | All paths join against the **final boss** | — |
| Epilogue | **Afterglow** | Pinnacle+ | Extreme optional bosses, secrets, building | — |

**Quest-book layout (FTB Quests):**
- Prologue
- Act I: shared by everyone
- **one chapter per class** (7), with Act III ring trials inside them
- Act IV and Act V: shared
- Epilogue
- A **Lore** tab linked to Modonomicon

Target: about 400 quests, built chapter by chapter.

---

## 4. Prologue: The Seventh Dawn

**Setting.** Players spawn in a **CTOV village** (*Village Spawn Point*). Vanilla villages are disabled pack-wide. On our seed, the village nearest spawn is a medium CTOV savanna village. About 150–250 blocks away stands a **pillager outpost**. Vanilla never places one near a village, so a script places it on first load; a CTOV or Towns and Towers fortified outpost suits the Warlord.

A boss bar at the top of the screen reads: **"The Warband marches in 7 days"**.

| # | Quest | Goal | Teaches |
|---|---|---|---|
| P1 | *A Horn on the Ridge* | Talk to the village elder (Easy NPC) | The threat, the countdown |
| P2 | *Make Ready* | Craft a sword, shield and armor; build a bed | Basics |
| P3 | *Walls and Watchfires* | Light the village at night | Defense |
| P4 | *Hire Spears* | Recruit 2 villagers (Villager Recruits) or wake the guards (Guard Villagers) | Allies |
| P5 | *Scout the Camp* | Spot the outpost; kill a patrol | Combat |
| P6 | *First Spell* | Find a scroll / an Iron's Spells starter book | Magic exists |
| P7 | *Day Seven* | **The raid**: survive every wave | Teamwork |
| P8 | *Head of the Snake* | Storm the outpost and kill **Warlord Vex**, the pillager leader | First boss |
| P9 | *Hero of the Village* | Get the vanilla Hero effect | Reward |
| P10 | *Fire in the Sky* | That night a **Lantern ship crashes** (`/createlanterns crash green`). Reach the wreck | The hook |
| P11 | *The Last Words* | The dying Green Lantern (Easy NPC) warns of the corruption and the seven lights. His ring flies off to look for someone worthy. *Not you. Not yet.* | Main quest |
| P12 | *The Book of Oa* | Get the lore book (Modonomicon). Act I opens | Lore |

**How it's built:**
- **Countdown:** KubeJS keeps the start tick and updates a `/bossbar`.
- **Day 7:** the vanilla 1.21.1 method `setRaidOmenPosition(village)` + Raid Omen, so the raid hits *that* village. Vanilla has no usable `/raid` command.
  - **Warning:** a raid needs living villagers (P4 matters).
- **Raid flavour:** Illager Invasion and Raids:Enhanced.
- **Warlord Vex:** a scripted, named, buffed pillager captain (300 HP) with a boss bar, or a FIW Bosses JSON boss (phases, horn summons, dialogue).

---

## 5. The classes (the seven lights)

**Rules:**
- Each class = **one light** = element + combat style + aspect.
- You **choose** at a Lantern shrine in Act I (an Easy NPC Guardian Envoy). You can pick **more than one**; each has its own XP bar and talent tree.
- Classes share bosses. A boss can be one class's *nemesis* and another's optional fight.
- The **mount** is how a class travels *before* the ring. **After the ring, every Lantern flies** and can ride their constructs.

**Overview:**

| Light | Class | Element (magic) | Combat style | Aspect (focus mods) | Mount | Ring trial world |
|---|---|---|---|---|---|---|
| 🔴 Red | **Bloodfire Berserker** | **Fire** (+ Blood) | Two-handed berserker | Nether, fire dragons, forges | Ice and Fire **fire dragon** | Nether / Lost Citadel |
| 🟠 Orange | **Hoardwarden** | **Earth** | Heavy knight / tank | Mining, treasure, gems, dungeon loot | Overworld Drake → **Gronckle** | Cursed Pyramid |
| 🟡 Yellow | **Stormwright** | **Lightning** | Speed duelist | **Technology**: Create, Aeronautics, Mekanism, Draconic | **Its own aircraft** (balloon → plane → starship) | **Korugar** |
| 🟢 Green | **Lightwarden** | **Evocation** (+ Holy support) | **Paladin** | **Villages**, raids, trading, defense | Armored warhorse → white **hippogryph** | **Oa** |
| 🔵 Blue | **Frostbinder** | **Ice** / crystal | **Battlemage** | Frozen lands, sky islands, exploration | Ice and Fire **ice dragon** (raised from an egg) | End: Crystal Peaks |
| 🟣 Indigo | **Wildheart** | **Summoning** | Ranger / beast master | Taming, breeding, farming, familiars | **Bonded Book of Dragons dragons** + Wyrmroost | wherever the beasts are |
| 💜 Violet | **Voidblade** | **Void** (Ender + Eldritch) | **Assassin** | Night, undead hunting, stealth, the End | Book of Dragons **Night Fury** | End: Shadowlands |

**Magic schools by class.** Iron's Spells' per-spell config lets us **reassign spells to schools**, and isskjs can create new schools:
- **Earth** (Orange): a new school made from Iron's Earthquake, Stomp, Oakskin and Touch Dig, or GTBC's Geomancy Plus.
- **Summoning** (Indigo): a new school made from Iron's summon spells (Summon Vex, Raise Dead, Summon Polar Bear, …) plus Alshanex's Familiars.
- **Evocation** (Green): keeps Fang Strike, Fang Ward, Shield, Gust and **Summon Horse** (the paladin's steed). It loses Summon Vex to Summoning.
- **Void** (Violet): Iron's Ender + Eldritch, plus Fire's Ender Expansion and Discerning the Eldritch.
- **Holy** has no class of its own. It's Green's support branch (heals), and anyone can dabble.

---

### 🔴 Red: The Bloodfire Berserker
*"The closer to death you are, the harder you hit."*

| | |
|---|---|
| **Magic** | Iron's **Fire** (Fireball, Raise Hell, Flaming Barrage, Burning Dash) + **Blood** (Blood Slash, Devour, Sacrifice); later Cataclysm: Spellbooks fire spells |
| **Combat** | Better Combat greatweapons: Simply Swords greatswords; Dungeons Weapons claymore, great hammer, double axe |
| **Aspect mods** | The Nether (Jaden's Nether Expansion, YUNG's Better Nether Fortresses, Eternal Nether) · Cataclysm fire bosses · Ice and Fire fire dragons |
| **Talent XP** | Kills with two-handers · damage dealt below 40% health · Nether kills · boss kills · raid captains |
| **Mount** | A fire dragon hatched from an egg won from a stage-4 cave dragon |
| **Nemeses** | Ignis · Netherite Monstrosity · Nether Gauntlet (BOMD) · Lord Pumpkinhead · **Echo of Tyros** |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Bone or iron greatweapon, Wandering Magician robes |
| Mid | **Pyromancer** armor, Blaze Instruction Manual |
| Late | **Ignitium** armor (Ignis), **Infernal Forge**, fire dragonsteel |
| Extreme | Mythic Apotheosis gear with fire gems, **Decrepit Scythe** (Tyros), the Red ring |

**Questline: Path of Rage**

| Tier | Quests |
|---|---|
| Early | *First Blood* (50 kills with a two-hander) · *Kindling* (Fireball) · *Burn Them Out* (a YUNG's dungeon) · *Bonecaller* (Supreme Bonescaller) |
| Mid | *Into the Inferno* (a JNE Sanctum) · *The Pyromancer's Mantle* · *Fortress Breaker* · *The Gauntlet* · *Ash and Embers* (stage-3 fire dragon) |
| Late | *The Blacksmith's Wrath* (Netherite Monstrosity) · *Burning Arena* (Ignis) · *Firebrood* (egg → hatch → ride) · *Pumpkin King* |
| **Ring trial** | ***The Crucible of Rage***: slay the **Echo of Tyros** (1000 HP) while below half health |

**Ring powers:** Blood Plasma → **Hellbolt** · Eruption → **Inferno** (renamed).

---

### 🟠 Orange: The Hoardwarden
*"Mine."*

| | |
|---|---|
| **Magic** | **Earth** (custom school, see above) |
| **Combat** | Heavy knight: Shield Expansion (parry, shield tiers), Epic Knights and Knight Quest armor, hammers and maces |
| **Aspect mods** | Mining (YUNG's Better Mineshafts + our Terralith patch, a veinminer, Create Ore Excavation) · treasure (Lootr, archaeology, D&T and WDA loot) · **Apotheosis gems** · Kings & Monsters (the Ogre King locks Bog Iron) |
| **Talent XP** | Ores mined (high), stone (tiny) · loot chests opened · archaeology finds · emeralds from trades · gems socketed |
| **Mount** | Wyrmroost **Overworld Drake** (armored ground mount) → Book of Dragons **Gronckle** (the rock-eating dragon) |
| **Nemeses** | Ferrous Wroughtnaut · Tongbi the Sculptor · **Ogre King** · Void Blossom · **Ancient Remnant** |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Epic Knights plate + kite shield, **Axe of a Thousand Metals** |
| Mid | Knight Quest sets, **King's Club + Crown**, **Earthrend Gauntlet**, Iron's Paladin chestplate |
| Late | **Gauntlet of Guard**, Netherite Battlemage |
| Extreme | Mythic gear socketed with perfect gems, the Orange ring |

**Questline: Path of the Mountain**

| Tier | Quests |
|---|---|
| Early | *Shiny* (veinmine 64 iron) · *Grave Goods* (archaeology) · *Shaft Raider* (5 Better Mineshafts) · *The Iron Ghost* (Wroughtnaut) |
| Mid | *Ogre Country* · *Crown of the Ogre King* · *Earthrend* (Tongbi) · *Gem Cutter* · *The Deep Bloom* (Void Blossom) |
| Late | *Pyramid of Greed* (Ancient Remnant) · *The Hoard* (9 gold + 9 diamond + 9 emerald blocks) · *The Guardian's Fist* (Ender Guardian) |
| **Ring trial** | ***Mine, All Mine***: survive a treasure gateway (Gateways to Eternity), then defeat the reborn **Ancient Remnant** in its pyramid |

**Ring powers:** Covet → **Lodestone Pull** · Plunder → **Shatterplunder**. Lit passive: kills drop more.

---

### 🟡 Yellow: The Stormwright
*"Faster than thunder, brighter than lightning."*

| | |
|---|---|
| **Magic** | Iron's **Lightning** (Lightning Bolt, Thunderstorm, Ball Lightning, Volt Strike) + Cataclysm: Spellbooks *Technomancy* + Create: Wizardry |
| **Combat** | Speed duelist: rapiers and katanas (Simply Swords, Spartan Weaponry Unofficial), Combat Roll, Iron's Boots of Speed |
| **Aspect mods** | **Technology**: Create (+ New Age electricity, Crafts & Additions) · **Create Aeronautics** (balloons, planes, airships, **the ships that reach Oa and Korugar**) · Mekanism (MekaSuit) · **Draconic Evolution** (extreme tier, beta) |
| **Talent XP** | Create / Mekanism / Aeronautics milestones · crafting machines · first flights · kills with lightning · kills while outnumbered |
| **Mount** | **No dragon: they build their own.** Hot-air balloon → propeller plane → Levitite airship → Lantern starship. *In co-op, Yellow builds the team's fleet* |
| **Nemeses** | **The Harbinger** (Cataclysm war machine) · **Scylla** (storm) · rival **lightning dragons** (Ice and Fire) |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Create goggles + Extendo Grip, copper/iron rapier |
| Mid | **Electromancer** armor, New Age power, first plane |
| Late | **MekaSuit**, lightning dragonsteel, Witherite (Harbinger) |
| Extreme | **Draconic** (Wyvern → Draconic → Chaotic) armor, the Yellow ring |

**Questline: Path of the Storm**

| Tier | Quests |
|---|---|
| Early | *Cog and Copper* · *Static* (Lightning Bolt) · *The Duelist* (rapier) · *Spark Plug* (first powered machine) |
| Mid | *Lift-Off* (balloon) · *New Age* (electricity) · *Electromancer* · *Iron Prophet* (the Harbinger) |
| Late | *Propeller* (plane) · *MekaSuit* · *Storm Rival* (stage-4 lightning dragon) · *Starship* (a ship that reaches another planet) |
| **Ring trial** | ***The Storm Spire***: fly your own ship to **Korugar** (re-themed as the storm world), climb the spire through the Dread Plains and Fear Bogs, and defeat the **Scylla** that guards the yellow lantern |

**Ring powers:** Terror → **Thunderclap** (nearby enemies flee, weakened) · Cage → **Storm Cage** (lock a target in yellow lightning).

---

### 🟢 Green: The Lightwarden
*"In brightest day, in blackest night…"*

| | |
|---|---|
| **Magic** | Iron's **Evocation** (Fang Strike, Fang Ward, Shield, Gust, Summon Horse) + **Paladin Spells** (tank spells that scale with armor) · Holy as a support branch (Heal, Fortify) |
| **Combat** | Paladin: sword and shield, heavy armor, protecting allies |
| **Aspect mods** | **Villages**: Guard Villagers, Villager Recruits, Towns and Towers, Easy NPC villagers · **raids**: Illager Invasion, Raids:Enhanced · trading |
| **Talent XP** | **Raids won (big)** · villager trades · zombie villagers cured · allies healed · iron golems built · illagers slain |
| **Mount** | Armored **warhorse** (Summon Horse spell + horse armor) → a white Ice and Fire **hippogryph** |
| **Nemeses** | Raid bosses (Golem of Last Resort, Zapper, **Raider Blimp**) · **the Invoker** (Illager Invasion) · **the Archevoker** (Iron's) · **the Dead King** |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Kite shield + chainmail, first Evocation scroll |
| Mid | **Archevoker** armor, **Grimoire of Evokation**, Paladin chestplate, Hallowed Gem (Invoker) |
| Late | Netherite Battlemage, the Dead King's spoils |
| Extreme | Mythic holy gear, the Green ring |

**Questline: Path of the Shield**

| Tier | Quests |
|---|---|
| Early | *Recruits* (hire 3 soldiers) · *Mercy* (cure a zombie villager) · *Fang and Ward* (first Evocation spells) · *Watchman* (keep a village lit) |
| Mid | *Iron Guardians* (build 2 golems) · *The Archevoker* (Iron's Evoker Fort) · *The Invoker* · *Rally* (win an Omen III raid) |
| Late | *The Dead King* (Iron's Catacombs) · *Bastion* (win an Omen V raid with the Raider Blimp) · *Hippogryph* |
| **Ring trial** | ***The Central Power Battery***: reach **Oa**, the Green Lantern Corps' homeworld. Defend the Guardian Outpost through the Trial of Will (waves) and recharge the **Central Power Battery** |

**Ring powers:** Resolve → **Aegis** (shrug off harm, shield) · Fist → **Hammer of Light**. Lit passive: constructs cost a quarter less.

---

### 🔵 Blue: The Frostbinder
*"Winter keeps what it loves."*

| | |
|---|---|
| **Magic** | Iron's **Ice** (Ice Tomb, Blizzard, Ray of Frost, Frostwave) + **Galosphere: Spellbooks** (crystal) |
| **Combat** | Battlemage: sword + spell (Iron's imbued weapons), Netherite Battlemage armor |
| **Aspect mods** | Frozen lands and the **sky**: Terralith Skylands and frozen biomes, Sky Villages, Floating Islands, Sky Whale Ship · Nullscape **Crystal Peaks** · co-op exploration |
| **Talent XP** | Spell kills in cold biomes · kills shared with party members · distance flown · sky structures explored |
| **Mount** | Ice and Fire **ice dragon**, raised from an egg (a bond, not a conquest) |
| **Nemeses** | **Frostmaw** · **Night Lich** (frost undead) · **Maledictus** (Frosted Prison) · wild ice dragons |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Cryomancer robes, Frostbranded Book |
| Mid | **Cryomancer** armor, Galosphere crystal gear |
| Late | **Cursium** (Maledictus), Netherite Battlemage, **ice dragonsteel** |
| Extreme | Mythic crystal gear, the Blue ring |

**Questline: Path of Winter**

| Tier | Quests |
|---|---|
| Early | *First Frost* · *Cold Hands* (10 spell kills in snow) · *Skyward* (reach a floating island) · *Ice Spider Den* (Iron's) |
| Mid | *Cryomancer* · *The White Beast* (Frostmaw) · *The Lich of the North* (Night Lich) · *Skylands* (visit 3 sky islands) |
| Late | *Prison of Curses* (Maledictus) · *Ice Brood* (raise an ice dragon) · *Whale Rider* (clear a Sky Whale Ship) · *Laputa* (craft a levitation stone and conquer the **Castle in the Sky**) |
| **Ring trial** | ***Heart of Winter***: fly your ice dragon to the End's **Crystal Peaks** and take the frozen heart from its guardians |

**Ring powers:** Hope → **Frost Ward** (heals you and allies) · Sanctuary → **Glacial Sanctum** (allies inside take half damage). Lit passive: **charges nearby Green rings**, a Blue + Green synergy.

---

### 🟣 Indigo: The Wildheart
*"No beast fights alone."*

| | |
|---|---|
| **Magic** | **Summoning** (custom school, see above) + **Alshanex's Familiars** (13 spell-casting familiars) + Conjurer's Talisman |
| **Combat** | Ranger: bows and crossbows (Iron's Autoloader Crossbow); summons, pets and familiars fight beside you |
| **Aspect mods** | **Taming and breeding**: Book of Dragons (bonding levels), Wyrmroost (breeding), Alex's Mobs, Redomesticate (pet beds, pet respawn), Companions! · **farming**: Farmer's Delight + addons |
| **Talent XP** | Animals bred · mobs tamed · crops harvested · damage dealt by your summons and pets · familiars bonded |
| **Mount** | **Bonded Book of Dragons dragons** (any species) + Wyrmroost drakes |
| **Nemeses** | **Umvuthi** (Mowzie's sun-tribe beast-caller) · Ice and Fire **Hydra** and **Sea Serpent** · **Leviathan** (Cataclysm) · corrupted beast-binders |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Leather + bow, Druidic Tome |
| Mid | **Plagued** armor + Conjurer's Talisman, familiars |
| Late | Drake armor (Wyrmroost), dragon bonding gear, **Tidal Claws** (Leviathan) |
| Extreme | Mythic bow, **the Indigo Staff** (Create: Lanterns), the Indigo ring |

**Questline: Path of the Pack**

| Tier | Quests |
|---|---|
| Early | *Friend of the Wild* (tame a wolf, cat and horse) · *New Life* (breed 10 animals) · *Harvest Feast* · *First Summon* |
| Mid | *Familiar* · *Plagued Robes* · *Drake Breeder* · *Sun and Mask* (Umvuthi) |
| Late | *Dragon Whisperer* (max bond) · *The Many Heads* (Hydra) · *Leviathan* · *Set Them Free* (free a chained dragon from a corrupted camp) |
| **Ring trial** | ***The Staff of Compassion***: tend wounded creatures across five biomes. When the corrupted beast-boss falls, **spare it** and set it free |

**Ring powers:** Blink → **Pack Leap** (teleport) · Exchange → **Swap with your beast**. Lit passive: can charge from a Lantern of any colour.

---

### 💜 Violet: The Voidblade
*"The void doesn't see you coming. Neither will they."*

| | |
|---|---|
| **Magic** | **Void**: Iron's Ender (Shadow Slash, Teleport, Echoing Strikes, Black Hole) + Eldritch late (Sonic Boom, Sculk Tentacles, Pocket Dimension) + Fire's Ender Expansion + Discerning the Eldritch |
| **Combat** | Assassin: daggers (Dungeons Weapons), Combat Roll, **Attract to Sound** (mobs hear you, so stealth matters), sneak-attack bonuses |
| **Aspect mods** | Night and undead hunting: Born in Chaos, The Graveyard, Mutant Monsters · **the End**: Nullscape Shadowlands and Void Barrens, YUNG's Better End Island |
| **Talent XP** | Kills at night · kills while sneaking (×2) · undead kills · kills in the End |
| **Mount** | Book of Dragons **Night Fury**, the stealth dragon |
| **Nemeses** | Nightmare Stalker · **Corrupted Champion** (Graveyard) · **Ender Guardian** · **Obsidilith** · the **Warden** |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Leather + daggers, a Born in Chaos charm |
| Mid | **Shadowwalker** armor, Dragonskin Spell Book |
| Late | Warden battlemage gear (Deeper & Darker: Spellbooks, optional), Gauntlet of Guard |
| Extreme | **Signet of the Betrayer** (Eldritch), Mythic daggers, the Violet ring |

**Questline: Path of the Void**

| Tier | Quests |
|---|---|
| Early | *Strike from Shadow* (20 sneak kills) · *Nightwalker* (survive 3 nights in the wild) · *Silent Steel* · *The Stalker* |
| Mid | *Shadowwalker* · *Grave Robber* (Corrupted Champion) · *Blink* (Teleport) · *Into the Deep Dark* (outlast a Warden) |
| Late | *Night Fury* (bond) · *The Black Monolith* (Obsidilith) · *Void Touched* (learn an Eldritch spell) |
| **Ring trial** | ***The Void Walk***: cross Nullscape's **Shadowlands** unseen, infiltrate the Ruined Citadel, and assassinate the **Ender Guardian** |

**Ring powers:** Enthrall → **Void Lure** (details when installed).

---

### Secret lights (optional, decision 5)
Ultraviolet (*The Unseen*) and Gold (*The Bard*, Tunes n' Tomes) stay possible as hidden extras. If we drop them, their lights get switched off.

---

## 6. Leveling and the talent tree

**Engine: Pufferfish's Skills** 0.19.2 (all 0.x builds are tagged beta). Add-ons:
- **Unofficial Additions:** `harvest_crops`, `fishing` and `spell_casting` sources.
- **Pufferfish's Attributes:** extra stats to use as rewards.

**Categories:**
- **Adventurer**: always open. Generic XP: mobs, bosses, raids, exploration.
- **Seven class categories**, locked until chosen. The class quest unlocks one with `/puffish_skills category unlock <player> gl:<class>`.

**Each class tree has three branches and a capstone:**
1. **Element:** spell power for its school, mana, cooldowns.
2. **Style:** weapon stats.
3. **Aspect:** utility. It also unlocks recipes early through KubeJS stages.
4. **Capstone:** needs the ring.

**XP per class.** Starting values for tuning:

| Class | Main XP sources (Pufferfish) |
|---|---|
| 🔴 Red | `kill_entity` with a two-hander (×1.5 in the Nether) · `deal_damage` while health < 40% · boss kills |
| 🟠 Orange | `mine_block`: ores 8, stone 0.2 · traded emeralds · loot chests |
| 🟡 Yellow | `criterion` on Create/Mekanism/Aeronautics advancements · `craft_item` on machine tags · lightning kills |
| 🟢 Green | `increase_stat` raid won (200) · trades (6) · `heal` on allies · illager kills |
| 🔵 Blue | `spell_casting` ice spells · kills in cold biomes · `shared_kill_entity` · distance flown |
| 🟣 Indigo | `increase_stat` animals bred (5) · tamed · `harvest_crops` · summon kills |
| 💜 Violet | `kill_entity` at night ×1.5, sneaking ×2, undead ×1.5, in the End ×1.5 |

**How the levels feed the rest:**
- **Anti-farming** limits are built in.
- **Bridge to the rings:** a KubeJS script copies each class level into that light's deed points (`/createlanterns spectrum set`). Class **level 10 brings the whisper**, **level 25 the dream**, and finishing the ring trial brings the ring.

---

## 7. Gear ladder

| Tier | Act | Source |
|---|---|---|
| **Early** | Prologue–I | Crafted class kits (Epic Knights, Dungeons Weapons), Wandering Magician robes, first spellbooks |
| **Mid** | II | **Iron's school armor** (Pyromancer, Cryomancer, Electromancer, Archevoker, Shadowwalker, Plagued), Knight Quest, mid-boss uniques |
| **Late** | III | **Cataclysm boss gear**, **dragonsteel**, MekaSuit, Netherite Battlemage |
| **Extreme** | IV–V | **Apotheosis Mythic** affixed items + perfect gems, Tyros' Scythe, Draconic, the **rings** |

**How it's controlled:**
- **Apotheosis** is the global loot-quality dial; its world tiers line up with the acts (verify).
- **LootJS** injects class gear into boss and dungeon loot.
- **Iron's Spellbooks Tweaks** caps spell rarity per act.
- **Lootr** gives every player their own structure loot.

---

## 8. Boss ladder

| Tier | Bosses (mod) | Class nemesis |
|---|---|---|
| **Prologue** | **Warlord Vex** (custom) | all |
| **Early** | Ferrous Wroughtnaut, Umvuthi, Tongbi (Mowzie's) · Supreme Bonescaller, Nightmare Stalker (Born in Chaos) · Iron's school mages, Ancient Knight · Cataclysm dungeon minis · Invoker | Orange, Indigo, Red, Violet, Green |
| **Mid** | **Ogre King** · **Night Lich**, Nether Gauntlet, Void Blossom (BOMD) · **Frostmaw** · **Corrupted Champion** · **The Harbinger** · Archevoker · stage-3 dragons | Orange, Blue, Red, Violet, Yellow, Green |
| **Late** | Netherite Monstrosity, **Ignis**, **Ancient Remnant**, **Maledictus**, **Ender Guardian**, **Leviathan**, **Scylla** (Cataclysm) · **Dead King** · Lord Pumpkinhead · **Obsidilith** · Hydra · stage-4/5 dragons | each class (§5) |
| **Extreme** | **Echo of Tyros** · Discerning the Eldritch's Ascended One · Dark Doppelganger · Ender Dragon (Better End Island) | ring trials, post-game |
| **Key boss** | **The Crossroads**: your **Dark Doppelganger** (proposed, §10) | everyone with a ring, alone |
| **Gate** | **Chaos Guardian** (Draconic Evolution) | everyone |
| **Final** | **Devourer of Gods** (proposed, §10); backup: **The Obliterator** | everyone |

**Optional extra dimensions with their own boss ladders** (decision 6): Twilight Forest, The Aether, Eternal Starlight, Deeper and Darker.

---

## 9. The corruption (the enemy grows)

| Act | Pressure | Mods / how |
|---|---|---|
| Prologue | Pillager warband | the raid |
| I | Rare **Blackened elites**: mobs with a corruption affix | Champions-Unofficial + a KubeJS "Blackened" affix |
| II | **Blood Moons** every ~10 nights with undead hordes · difficulty grows with distance | Enhanced Celestials (v1 or v2; their add-ons aren't cross-compatible) · Scaling Difficulty · Born in Chaos |
| III | **Corruption rifts** near ring-trial sites that slowly blight the land · corrupted patrols | KubeJS "corruption nodes" (spreading `/fillbiome` + block swaps) · The Hordes |
| IV–V | **The final boss's shadow**: every night is a Blood Moon until it falls | KubeJS world event |

---

## 10. The Crossroads (White / Black) and the finale

### The Crossroads: the key boss
Once a player has their ring, one **key boss** awaits. **How you kill it** decides what you become:

| Outcome | You become | Idea (to design later) |
|---|---|---|
| **Power-up** | You keep your ring and it **grows stronger**: an upgraded ring, a permanent *Heightened* effect, or extra talent points | the "normal" kill |
| **White** | The **White Lantern** (Life) | e.g. a merciful or protective kill: nobody in your party falls, healing or holy finishing blow, … |
| **Black** | The **Black Lantern** (Death) | e.g. a ruthless kill: in the Deep Dark, with blood or void, while sacrificing allies or summons, … |

*We'll design the exact conditions later.*

**How it's built:**
- A KubeJS `EntityEvents.death` check reads how the boss died (killer, location, weapon or spell, party state).
- It then runs `/createlanterns call <player> white|black` or applies the power-up.
- In the mod, White and Black are switched to "commands only", so deeds never trigger them.

**Key-boss candidates.** Research done 2026-11-09; numbers read from the jars:

| Candidate | Why | Notes |
|---|---|---|
| **Dark Doppelganger** (Dark Doppelganger 4.0.0, Iron's addon) · **recommended** | It **copies the summoner's own armor, weapon and spell power**: you fight *your own corrupted shadow*. It's a solo fight that every player faces individually, which suits a "who will you become?" moment. How you defeat yourself decides White / Black / power-up | 4 phases, adapts to repeated attacks, steals buffs, makes clones; `hard_mode`; HP 1–100,000 in config. ⚠ Copying Draconic armor is untested: put it on `banned_armor` until tested |
| Iron's **Dead King** | Undead lord, respawnable with a phylactery | 500 HP, too weak for ring-bearers unless buffed |
| Goety **Apostle** | Necromancer; caps hits at 20; immune at half HP and heals back to full | Big mod; its 1.21.1 port is from July 2026 |

### The gate before the finale: the Chaos Guardian
**Draconic Evolution's Chaos Guardian** is already planned, since Draconic is Yellow's tech line, and the research confirmed Chaos Island exists in the 1.21.1 build.
- **Stats:** 1000 HP plus a **16,000-point shield**. Crystal shields must be broken first, its damage **ignores armor and Resistance**, and it summons Guardian Withers.
- **What it drops:** Chaos Shards (Chaotic-tier gear), and in our design a **key ingredient for summoning the final boss**.
- It has no multiplayer scaling (KubeJS can add it). Draconic is beta.

### Act V: The Last Light (the finale)
All ring-bearers (powered-up, White and Black alike) unite for the last fight.

**Final boss: an existing, very OP mod boss.**

Each candidate was compared on HP and armor from the jars, damage caps, healing, phases, immunities and theme. The bar is Cataclysm's 333–600 HP bosses, plus endgame Draconic and Mythic gear.

| Rank | Boss | Mod (version) | Stats (from the jar) | Signature mechanics | Theme | Risk |
|---|---|---|---|---|---|---|
| 🥇 **recommended** | **Devourer of Gods** | Devourer of Gods 1.2.0 | 2000 base HP; configurable to 30 armor and 20 toughness | **340-block worm**, 2 phases (phase 2: ×1.5 damage, ×1.3 speed), lasers, Cosmic Flame. Config can **ignore armor and Protection, stop your regeneration, eat enchant levels off your gear to heal itself**, and reduce your damage to it. **Built-in co-op scaling** (+50% HP and +15% damage per extra player). An aerial fight, perfect for ring flight | **Cosmic god-eater**; its summon fragment drops when it *devours the Ender Dragon* | Small new mod (All Rights Reserved; fine for personal use). 102 body segments, so it's heavy, and Entity Culling must exclude it. **No drops by default** (we add a loot table). Defaults are tuned for vanilla gear, so it must be tuned up |
| 🥈 | **The Obliterator** | Legendary Monsters 2.2.4 | 550 HP / 14 armor, 4 toughness | **Max 20 damage per hit**, adapts to your damage, heals and resets its phase if left alone, immune to projectiles in phase 1, attacks that deal a percentage of your HP. Health and damage multipliers up to 1000× | Space Station in the End | Low (8.3M downloads, no dependencies). ⚠ **Invulnerable while you fly or hold high ground**, which cancels the Lantern rings' flight |
| 🥉 | Dark Doppelganger | 4.0.0 | 600 by default (up to 100,000) | Copies your gear (best used as the **Crossroads** boss above) | The hero's shadow | Needs Iron's ≥ 3.15 |
| — | Not strong enough or not suitable | | Bosses'Rise (200–500), Eternal Starlight Solar Creeper (250), Herobrine (500), Remnants' Hollow Sovereign (720), Wither Reincarnated (600), Luxtructosaurus (600). DivineRPG's Lady Luna is fought with a separate inventory, so your endgame gear doesn't count. AoA's 1.21.1 build only has early and mid bosses. Twilight Forest has no final boss. Wither Storm has no 1.21.1 build | | | |

**Proposed end-game chain** (decision 2):
1. **The Crossroads**: face your **Dark Doppelganger**. How you defeat your own shadow makes you **White**, **Black**, or keeps your ring and powers it up.
2. **The Gate**: the **Chaos Guardian** in the End drops Chaos Shards and the *Chaos Core* (our recipe change) needed for the summon.
3. **The Devouring**: the **Devourer of Gods** devours the Ender Dragon, and its fragment + the Chaos Core summon it.
4. **The Last Light**: every ring-bearer flies against the Devourer.

**Starting tune for the Devourer** (to test):
- `maxHealth` 6000+ · player damage multiplier ≈ 0.2 · armor pierce ≈ 20 · enchantment pierce ≈ 10 · regen halt on.
- Keep its co-op scaling.
- Add our own loot table.
- Summon recipe: also requires the Chaos Core.

| Step | Quest | What happens |
|---|---|---|
| V-1 | *The Shadow Falls* | Every night is a Blood Moon; corrupted versions of fallen bosses roam |
| V-2 | *Recharge* | Fly to **Oa** and recharge every ring at the Central Power Battery |
| V-3 | *The Gathering* | All seven colours (and any White or Black) answer the call |
| V-4 | *The Last Light* | The final boss. Each colour has a job: Green shields, Blue protects, Indigo's beasts tank adds, Yellow and Red burst damage, Orange holds the line, Violet strikes weak points |
| V-5 | *Afterglow* | Credits; the Epilogue opens |

---

## 11. Mods needed, by build phase

All versions are NeoForge 1.21.1, checked 2026-11-08/09. **β** = beta/alpha. ⚠ = risk noted.

### Phase A: Story backbone (first)
| Mod | Version | Notes |
|---|---|---|
| **Create: Lanterns** + Spectral Hub | alpha 20.11 / v4 | Personal use, so we modify it freely. Needs Create, Sable, Simulated, Aeronautics |
| Create · Sable · Simulated · Create Aeronautics | 6.0.10 · 2.0.6 · 1.3.2 · 1.3.2 | Simulated and Aeronautics are CurseForge-only (we have the jars) |
| Curios | 9.5.1 | ring slot |
| FTB Quests + FTB Library + FTB Teams · FTB XMod Compat | 2101.1.38 · .39 · .12 · 21.1.14 | quest book + KubeJS hooks |
| Easy NPC (+ FTB Quests compat) | 7.18.0 (+1.0.2) | NPCs, dialogue |
| Modonomicon | 1.123.0 | lore book |
| Pufferfish's Skills + Unofficial Additions + Attributes | 0.19.2 β · 2.2.8 · 0.8.3 | talent trees |
| Village Spawn Point (+ Collective) | 6.0 | spawn in a village |

### Phase B: Magic and combat
| Mod | Version | Notes |
|---|---|---|
| **Iron's Spells 'n Spellbooks** (+ Iron's Lib, GeckoLib, playerAnimator) | 3.16.3 | ⚠ raycast and teleport bugs on Aeronautics ships (#1142) |
| Iron's Spellbooks Tweaks | 1.5.0 | gate spells by act |
| KubeJS Iron's Spells (isskjs) | 4.0.3 | **Earth** and **Summoning** schools. ⚠ test with ISS 3.16 |
| Cataclysm: Spellbooks | 1.1.11 | Technomancy (Yellow), fire |
| Discerning the Eldritch · Fire's Ender Expansion | 1.4.5 · 2.5.1 | Violet's void |
| Paladin Spells | 1.1.4 | Green |
| Galosphere: Spellbooks | 1.1.5 | Blue crystal |
| Alshanex's Familiars (+ FamiliarsLib) | v5.0 | Indigo. ⚠ past versions broke saves |
| *Earth alternative:* Geomancy Plus | 1.1.0 | ⚠ old, CurseForge-only |
| Better Combat + Combat Roll | 2.4.0 · 2.0.6 | not together with Epic Fight |
| Simply Swords · Dungeons Weapons · Shield Expansion · Epic Knights · Knight Quest · Attract to Sound | 1.70.2 · 9.0.1 · 1.4.3 · 10.17 · 1.9.4 · 7.0.2 | styles |
| Apotheosis (+ Apothic Attributes / Enchanting / Spawners) · Artifacts · Relics · Iron's Gems 'n Jewelry | 8.9.0 · 13.2.5 · 0.10.7.8 · 2.0.2 | gear |

### Phase C: Bosses
| Mod | Version | Notes |
|---|---|---|
| L_Ender's Cataclysm · Bosses of Mass Destruction · Mowzie's Mobs · Born in Chaos | 3.33 · 1.3.3 · 1.8.2 · 1.7.6 | ⚠ Cataclysm uses vanilla biome IDs only, so it needs a Structurify biome list |
| Kings & Monsters (CurseForge) | 1.2.2 | ⚠ plains/swamp only: needs a biome list |
| The Graveyard · Mutant Monsters · Illager Invasion | 4.0.1 · 21.1.1 · 21.1.6 | |
| FIW Bosses | 1.3.1 | Warlord Vex |
| **Devourer of Gods** | 1.2.0-hotfix1 | proposed final boss. ⚠ heavy (102 segments), so exclude it from Entity Culling; add a loot table |
| Dark Doppelganger | 4.0.0 | proposed Crossroads boss. Needs Iron's ≥ 3.15, GeckoLib, playerAnimator |
| *Backup final:* Legendary Monsters | 2.2.4 | The Obliterator (+ 15 other bosses) |

### Phase D: Dragons and mounts
| Mod | Version | Notes |
|---|---|---|
| **Ice and Fire CE** (+ Uranus, Jupiter) | 2.0 | fire (Red), ice (Blue), lightning (Yellow's rival) dragons, hippogryph (Green), hydra |
| **Book of Dragons** | 1.4.1 | Night Fury (Violet), Gronckle (Orange), bonding (Indigo). ⚠ check the Fauna Engine dependency |
| Wyrmroost | 1.4.1 | drakes (Orange, Indigo) |
| Alex's Mobs Continued · Redomesticate · Companions! | 2.3.0 · 2.0.0 · 1.3.7 | animals, pets |

### Phase E: Aspect mods
| Mod | Version | Class |
|---|---|---|
| Create: New Age · Create Crafts & Additions · Mekanism · **Draconic Evolution** (β) | 1.2.0 · 1.7.2 · 10.7.19 · 3.1.4 | 🟡 Yellow |
| VeinMiner or FTB Ultimine · Create Ore Excavation | 2.11.2 · 1.6.8 | 🟠 Orange |
| Guard Villagers · Villager Recruits · Raids:Enhanced · Raided · Gateways to Eternity | 2.4.12 · 1.15.2 · 1.0.2 · 0.1.6 · 5.1.0 | 🟢 Green (+ the Prologue) |
| Farmer's Delight + addons | 1.3.4 | 🟣 Indigo |

### Phase F: Corruption
Enhanced Celestials (v1 + add-ons **or** v2 + Chaos Moon 2) · Champions-Unofficial 21.1.1.7 · Scaling Difficulty 1.1.0 · The Hordes 1.6.3f.

### Already installed (worldgen, structures)
Terralith · Jaden's Nether Expansion · Nullscape + YUNG's Better End Island · all YUNG's · Dungeons and Taverns · When Dungeons Arise + Seven Seas · The Lost Castle · Philips Ruins · Grim Kingdoms · Castles and Keeps · Towns and Towers · Sky Villages · Floating Islands · Sky Whale Ship · Eternal Nether · Structurify · Lootr (see MODLIST.md).

---

## 12. Decisions for you
| # | Decision | Status |
|---|---|---|
| 1 | Create: Lanterns permission | ✅ **Resolved:** personal use, modify freely |
| 2 | Final boss | ⏳ Proposed: **Devourer of Gods** (final) · **Dark Doppelganger** (Crossroads) · Chaos Guardian (gate). Pick or swap (§10) |
| 3 | How White works solo vs party | ✅ **Resolved:** White and Black come from the Crossroads boss |
| 4 | Black ring for players | ✅ **Resolved:** from the Crossroads boss; conditions later |
| 5 | Secret classes (Ultraviolet, Gold) | open |
| 6 | Extra dimensions (Twilight Forest / Aether / Eternal Starlight / Deeper and Darker) | open |
| 7 | Spell Engine (RPG Series) for extra class skills | open (recommend keeping it out) |
| 8 | Book of Dragons or Berk's Dragon Academy | open (recommend Book of Dragons) |
| 9 | Earth school: KubeJS-made or Geomancy Plus | open |
| 10 | Rename lights and powers to match the classes (Yellow "Sinestro Corps" → a storm Corps, …) | open (recommended) |
| 11 | Key-boss conditions for White / Black / power-up | later, as you said |

---

## 13. Implementation map (what builds what)

| Mechanic | Built with |
|---|---|
| Spawn in a village · outpost nearby | Village Spawn Point · KubeJS `place structure` on first load |
| 7-day countdown + raid | KubeJS: `/bossbar` + `setRaidOmenPosition` + Raid Omen |
| Warlord Vex | FIW Bosses, or a scripted buffed captain |
| Crashed Lantern | `/createlanterns crash green` + Easy NPC |
| Quest book | FTB Quests (+ FTB XMod Compat) |
| Choosing a class | FTB Quests command reward → `/puffish_skills category unlock` |
| Talent trees, per-class XP | Pufferfish's Skills datapack (`kubejs/data/…`) |
| **Class level → the light's whisper/dream** | KubeJS → `/createlanterns spectrum set` |
| **Ring trial → the ring** | FTB Quests reward → `/createlanterns call <player> <light>` |
| Earth and Summoning schools | isskjs custom schools + Iron's per-spell school reassignment |
| Re-themed lights and powers | `kubejs/assets/createlanterns/lang/en_us.json` |
| Recipe / spell gating | KubeJS stages · Iron's Spellbooks Tweaks |
| Lore | Modonomicon |
| Loot by tier | Apotheosis + LootJS (+ Lootr) |
| Corruption | Champions affix, Enhanced Celestials, KubeJS world events |
| **The Crossroads outcome** | KubeJS `EntityEvents.death` → power-up / `call … white` / `call … black` |
| Final boss | Devourer of Gods config (HP, pierce, regen halt) + our loot table + KubeJS recipe change (Chaos Core) |
| Crossroads boss | Dark Doppelganger (`hard_mode`, HP raised) + KubeJS death check → outcome |
| Our own mods (later) | **lantern-bridge**, only if commands can't do something (e.g. read deed points) |

**Suggested next step:** Phase A, the backbone. Install Create → Sable → Simulated → Aeronautics → **Create: Lanterns**, one at a time. Read its full config, test `spectrum set`, `call` and `crash`, and switch off the lights we don't use.
