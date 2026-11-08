# Story & Systems Design: *Blackest Night*

*Working design for the Green Lanterns modpack. Written 2026-11-08 from the owner's story pitch, with the mods researched for NeoForge 1.21.1. It's a living document: change anything.*

> **How to read this:**
> - Every mod named here was checked for a NeoForge 1.21.1 build (version in §11).
> - **(verify)** means the idea depends on a detail we haven't tested in-game yet.
> - **Decision** marks a choice that's yours to make (all collected in §12).

## Contents
1. [The story in one page](#1-the-story-in-one-page)
2. [The backbone: Create: Lanterns](#2-the-backbone-create-lanterns)
3. [The journey: acts and chapters](#3-the-journey-acts-and-chapters)
4. [Prologue: The Seventh Dawn](#4-prologue-the-seventh-dawn)
5. [The classes (the seven lights)](#5-the-classes-the-seven-lights)
6. [Leveling and the talent tree](#6-leveling-and-the-talent-tree)
7. [Gear ladder](#7-gear-ladder)
8. [Boss ladder](#8-boss-ladder)
9. [The corruption (the enemy grows)](#9-the-corruption-the-enemy-grows)
10. [Finale: Blackest Night](#10-finale-blackest-night)
11. [Mods needed, by build phase](#11-mods-needed-by-build-phase)
12. [Decisions for you](#12-decisions-for-you)
13. [Implementation map (what builds what)](#13-implementation-map-what-builds-what)

---

## 1. The story in one page

**The threat.** Death is spreading across the universe. Nekron, Lord of the Unliving, has woken. His **Black Lanterns** raise the dead, and the monsters they command are wiping out whole worlds. The corruption has reached Earth: undead hordes, blighted beasts, bosses that should have stayed dead.

**The order.** On the planet **Oa**, the Guardians lead an alliance of the **seven Lantern Corps**. Each Corps draws on one emotion of the *emotional spectrum*. No single Corps can stop the dead. Only all seven lights together, the **White Light of Life**, can. So the Guardians are searching every world for people worthy of a ring.

**You.** You and your friends are young adventurers who wake up in a small village. A **pillager warband** is camped on the ridge, and their war-horns say they march in **seven days**. Saving the village is the first test. On the night you win, a Lantern ship crashes in the hills, and its dying pilot tells you what's coming.

**The road.** Every deed you do is seen by the spectrum: the fights you pick, the ores you hoard, the animals you save, the friends you stand beside. You grow in a **talent tree** and can follow one class or mix several. Each class is one **light**, with its own:
- element (a school of magic)
- combat style
- aspect: the mods it focuses on, such as tech, dragons, mining or villages
- questline, gear, enemies and mount

Near the end of the road, your light's **ring** chooses you.

**The end.** With rings on their hands, the players reunite. Nekron raises the bosses you killed as Black Lanterns. Your seven lights must become one, and a single champion wears the **White Light**. Then you face Nekron in the void at the edge of the End.

> *Lore note:* names like Oa, Korugar, Nekron and Sinestro come from DC Comics, and Create: Lanterns already uses them. That's fine on a private server. If the pack is ever published, check what's allowed (or rename).

---

## 2. The backbone: Create: Lanterns

The chinatown instance contains **Create: Lanterns** (`createlanterns`, *alpha 20.11*, by "The Team": Xeon, Phazeau, Lycoris, Clara eclipse, Neves) and its HUD add-on **Spectral Hub**. It already *is* the system from the original pitch: **what you do on the server builds an attribute, and a threshold brings your ring.** The whole design builds on it rather than re-inventing it.

What it contains (read from its jar and config):

| Feature | What it does |
|---|---|
| **The full spectrum** | Red (Rage), Orange (Avarice), Yellow (Fear / Sinestro Corps), Green (Will), Blue (Hope), Indigo (Compassion / Indigo Tribe), Violet (Love / Star Sapphires), plus Ultraviolet (Shame), Gold (Joy), **Black (Death)**, **White (Life)**. Also 4 joke lights (Xbox, PlayStation, Steam, WhatsApp) that we'll switch off |
| **Deeds** | ~80 tracked deeds, grouped by light (table below). Every player has deed points per light |
| **The calling** | As points grow, the light **whispers** (60 pts) → you **dream** of it (180) → you're **worthy** (225) → the **ring comes looking** (450). Steps are 7 in-game days apart. All of it is configurable: per-deed worth, decay, extra rings cost ×4 |
| **Special lights** | **White** picks only someone carrying rings of all seven lights. **Black** takes only someone who died in the Deep Dark, and needs ×N deeds |
| **Ring powers** | Two per light, plus an ultimate. Red: Blood Plasma, Eruption. Orange: Covet, Plunder. Yellow: Terror, Cage. Green: Resolve, Fist. Blue: Hope, Sanctuary. Indigo: Blink, Exchange. Violet: Enthrall. Each light also has a "lit" passive |
| **Ring abilities** | Flight · a hard-light suit · grip (grab mobs, items, contraptions) · **constructs you can design, summon and ride** |
| **Planets** | **Oa** (Verdant Plains, Guardian Highlands, Spire Fields, Emerald Sea, Willpower River; Citadel, Guardian Outpost, Lantern Spire, **Central Power Battery**, crashed Lantern ship). **Korugar** (Dread Plains, Blackstone Crags, Fear Bogs, The Murk, River of Fear; Fear Spire, Sinestro's Watchtower) |
| **Travel** | Ships built with **Create Aeronautics** (it requires Create, Sable, Simulated and Aeronautics) |
| **Crafting** | Liquid light and dust for each emotion, Lantern frames, ring bands, and a **Great Foundry** where rings are forged ("Forged in Light") |
| **Commands** | Show or set a player's deed points per light |

**Deeds by light.** We read this from the mod's code; the grouping follows the code's order, so treat it as (verify):

| Light | Deeds |
|---|---|
| Red, Rage | berserk · rampage · slaughter · vengeance · avenge a companion / villager · burning fury · bare-handed · fight through the pain · punish raiders · slay a captain |
| Orange, Avarice | treasure · plunder · strike it rich (ores) · hoard · profit · ransack a village · dig up treasure · fish up treasure |
| Yellow, Fear | terrorise · slay the fleeing / young / trapped · strike from shadow · crush eggs |
| Green, Will | slay the mighty · slay while desperate · slay a terror · hold the line · outnumbered · endure the night · face the dark · brave the deep dark |
| Blue, Hope | hero of the village · cure · rescue · rally · plant · light the dark · build a guardian · keep watch · tend · mend a golem |
| Indigo, Compassion | give · set free · kindness · nurture · tame · breed · name · defend a companion |
| Violet, Love | company · grief · befriend an allay · give a flower · armour a companion · together |
| Ultraviolet, Shame | unseen · skulk · unseen kill · hide away · hide one's face · flee the fight · pilfer |
| Gold, Joy | music · dance · celebrate · feast · soar · victory · play a note · sound a horn · swim with dolphins |
| Black, Death | die · die in the dark · toll · slay / raise the Wither · brush with death · eat the dead · return to the grave · cheat death |
| White, Life | grow · sow · compost · keep bees · root |

**How we use it:**
- **The spectrum is the story's narrator.** Whispers and dreams become quest beats: "A green light notices you" can open a quest that explains it.
- **The ring arrives at the end of your class questline, not before.** We raise `ringAt` so rings never show up early on their own. The class's **ring trial** (§5) is the moment the ring comes. The mod's own worthiness check stays: a ring still rejects anyone whose deeds don't show its emotion.
- **Pufferfish's Skills XP (§6) mirrors the same deeds.** A Red player's actions fill both their Red talent tree and their Red deed points, so the two systems agree.
- **White and Black are the finale** (§10).

> ⚠ **Before anything else:** Create: Lanterns is *alpha*, licensed **All Rights Reserved**, and its GitHub repo is private. The whole story leans on it, so we need to know how you got it, whether we may use and tune it, and whether "The Team" can expose deed points to scripts (§12, decision 1).

---

## 3. The journey: acts and chapters

| Act | Name | Gear tier (Apotheosis world tier, verify) | What happens | Ring status |
|---|---|---|---|---|
| Prologue | **The Seventh Dawn** | Haven | Village, 7-day raid countdown, the Warlord, the crashed Lantern | none |
| I | **Proving Ground** | Haven → Frontier | Learn the world, first dungeons and bosses, first spells. The spectrum starts whispering. **Choose your class(es)** | whispers |
| II | **The Seven Paths** | Frontier → Ascent | Each class's own chapter: aspect mods, class gear, mount, mid bosses. Corruption gets worse | dreams |
| III | **Worthy** | Summit | Late bosses, space travel to Oa / Korugar, **the ring trial**, *the ring chooses you* | **ring** |
| IV | **Blackest Night** | Pinnacle | All paths join. The dead rise as Black Lanterns, the seven lights unite, **Nekron** | White Light |
| Epilogue | **Afterglow** | Pinnacle+ | Extreme optional bosses, secret lights (Ultraviolet, Gold), building | — |

**Quest-book layout (FTB Quests):**
- Prologue
- Act I: shared by everyone
- **one chapter per class** (7 + 2 secret)
- Act III ring trials: inside each class chapter
- Act IV: shared
- Epilogue
- A **Lore** tab that links to Modonomicon entries

Rough size: ~15 prologue + ~40 Act I + ~45 per class + ~35 Act IV = about 400 quests at full build. We'll build it chapter by chapter.

---

## 4. Prologue: The Seventh Dawn

**Setting.** Players spawn in a village (*Village Spawn Point*). Over the ridge, about 150–250 blocks away, sits a **pillager outpost**. Vanilla never places outposts within 10 chunks of a village, so a script places one there the first time the world loads.

A boss bar at the top of the screen reads: **"The Warband marches in 7 days"**, and it counts down in-game days.

| # | Quest | Goal | Teaches |
|---|---|---|---|
| P1 | *A Horn on the Ridge* | Talk to the village elder (Easy NPC) | The threat, the countdown |
| P2 | *Make Ready* | Craft a sword, shield and armor; build a bed | Basics |
| P3 | *Walls and Watchfires* | Light the village at night (Blue "light the dark" deed) | Defense, the spectrum |
| P4 | *Hire Spears* | Recruit 2 villagers (Villager Recruits) or wake the guards (Guard Villagers) | Allies |
| P5 | *Scout the Camp* | Spot the outpost; kill a patrol (Red "punish raiders") | Combat |
| P6 | *First Spell* | Find a scroll / Iron's Spells starter book | Magic exists |
| P7 | *Day Seven* | **The raid**: survive every wave | Teamwork |
| P8 | *Head of the Snake* | Storm the outpost and kill **Warlord Vex**, the pillager leader boss | First boss |
| P9 | *Hero of the Village* | Get the vanilla Hero effect | Reward |
| P10 | *Fire in the Sky* | That night a **Lantern ship crashes** in the hills. Reach the wreck | The hook |
| P11 | *The Last Words* | The dying Lantern (Easy NPC) tells you about the Black Lanterns, Oa, and the seven lights. His ring flies off to look for someone worthy. *Not you. Not yet.* | Main quest |
| P12 | *The Book of Oa* | Get the lore book (Modonomicon). Act I opens | Lore |

**How it's built:**
- **Countdown:** KubeJS keeps the start tick in the server's saved data and updates a `/bossbar` every second.
- **Day 7:** the script calls the vanilla 1.21.1 method `setRaidOmenPosition(village)` and gives Raid Omen, so the raid hits *that* village even if players are elsewhere. Vanilla has no usable `/raid` command; we checked the 1.21.1 server code.
  - **Warning:** a raid needs living villagers. If every villager dies there's no raid, so P4 matters.
- **Raid flavour:** Illager Invasion (new illagers that join raids) and Raids:Enhanced (raid mini-bosses at higher omen levels). We use them again in Act II.
- **Warlord Vex:**
  - **Easy:** a scripted, named, buffed pillager captain (300 HP) with a boss bar.
  - **Better:** a FIW Bosses JSON boss shaped like a vindicator, with phases, horn summons and dialogue.
- **The crash:**
  - Create: Lanterns ships a `crashed_lantern_ship` structure and has its own "wreck" mechanic (a ring waits in a crashed ship for someone worthy) (verify how to trigger it).
  - Fallback: `/place template createlanterns:oa/crashed_lantern_ship` at a scripted spot.

---

## 5. The classes (the seven lights)

**Rules:**
- Each class = **one light** = element + combat style + aspect.
- You **choose** a class at a Lantern shrine in Act I (an Easy NPC Guardian Envoy). You can pick **more than one**. Each class has its own XP bar and talent tree, so mixing two or three works, but focusing gets you to your ring faster.
- Classes **share bosses**. A boss can be one class's *nemesis* and another class's optional fight.
- The **mount** is the class's way to travel *before* the ring. **After the ring, every Lantern flies** and can ride their constructs.

**Overview:**

| Light | Class | Element (magic) | Combat style | Aspect (focus mods) | Mount |
|---|---|---|---|---|---|
| 🔴 Red | **Bloodfire Berserker** | Fire + Blood | Two-handed berserker | Nether, fire dragons, forges | Ice and Fire **fire dragon** |
| 🟠 Orange | **Hoardwarden** | Earth | Heavy knight / tank | Mining, treasure, gems, dungeon loot | Wyrmroost Overworld Drake → **Gronckle** (Book of Dragons) |
| 🟡 Yellow | **Nightblade** | Ender / Shadow | Assassin | Night, undead hunting, Korugar | **Night Fury** (Book of Dragons) |
| 🟢 Green | **Stormwright** | Lightning | Speed duelist | **Technology**: Create, Aeronautics, Mekanism, Draconic | **Its own aircraft** (balloon → plane → starship) |
| 🔵 Blue | **Dawnwarden** | Holy + Water | Paladin / support | Villages, trading, raid defense, healing | Ice and Fire **hippocampus** + white **hippogryph** |
| 🟣 Indigo | **Wildheart** | Nature | Ranger / beast master | Taming, breeding, farming, familiars | **Bonded dragons** (Book of Dragons) + Wyrmroost |
| 💜 Violet | **Starheart** | Ice / Crystal | Battlemage | Co-op bonds, sky islands, exploration | Ice and Fire **ice dragon** (raised from an egg) |
| ⚫ Ultraviolet | *The Unseen* (secret) | Ender / Eldritch | Stealth | Hidden lore, secrets | — |
| 🟡 Gold | *The Bard* (secret) | Melodic (sound) | Support | Music, feasts, celebration | — |

---

### 🔴 Red: The Bloodfire Berserker
*"The closer to death you are, the harder you hit."*

| | |
|---|---|
| **Corps · emotion** | Red Lantern Corps · Rage |
| **Magic** | Iron's **Fire** (Fireball, Raise Hell, Flaming Barrage, Burning Dash) and **Blood** (Blood Slash, Devour, Sacrifice). Later: Cataclysm: Spellbooks fire spells |
| **Combat** | Better Combat greatweapons: Simply Swords greatswords; Dungeons Weapons claymore, great hammer, double axe |
| **Aspect mods** | The Nether (Jaden's Nether Expansion, YUNG's Better Nether Fortresses) · L_Ender's Cataclysm fire bosses · Ice and Fire fire dragons |
| **Talent XP** | Kills with two-handers, damage dealt while below 40% health, Nether kills, boss kills, raid captains |
| **Spectrum deeds** | berserk, rampage, slaughter, vengeance, burning fury, bare-handed, punish raiders, slay a captain |
| **Mount** | A fire dragon you hatch from an egg won from a stage-4 cave dragon |
| **Nemeses** | Ignis · Netherite Monstrosity · Nether Gauntlet (BOMD) · Lord Pumpkinhead · **Echo of Tyros** (ring trial) |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Iron/bone greatweapon, leather + Wandering Magician robes, first fire scroll |
| Mid | **Pyromancer** armor, Blaze Instruction Manual, Simply Swords greatsword |
| Late | **Ignitium** armor (Ignis), **Infernal Forge** (Netherite Monstrosity), fire **dragonsteel** |
| Extreme | Mythic Apotheosis gear with fire gems, **Decrepit Scythe** (Tyros), the Red ring |

**Questline: Path of Rage**

| Tier | Quests |
|---|---|
| Early | *First Blood* (50 kills with a two-hander) · *Kindling* (learn Fireball) · *Burn Them Out* (clear a YUNG's dungeon) · *Bonecaller* (kill the Supreme Bonescaller, Born in Chaos) |
| Mid | *Into the Inferno* (find a JNE Sanctum) · *The Pyromancer's Mantle* · *Fortress Breaker* (YUNG's Keep) · *The Gauntlet* (BOMD Nether Gauntlet) · *Ash and Embers* (slay a stage-3 fire dragon) |
| Late | *The Blacksmith's Wrath* (Netherite Monstrosity) · *Burning Arena* (Ignis) · *Firebrood* (egg → hatch → ride) · *Pumpkin King* (Lord Pumpkinhead) |
| **Ring trial** | ***The Crucible of Rage***: at "worthy", descend to the Lost Citadel and slay the **Echo of Tyros** (1000 HP) below 50% health. Then forge your ring in the Great Foundry with **Liquid Rage** |

**Ring powers:** Blood Plasma (a burning bolt that hits harder the closer you are to death) · Eruption (a blast of blood plasma around you).

---

### 🟠 Orange: The Hoardwarden
*"Mine."*

| | |
|---|---|
| **Corps · emotion** | Orange Lantern Corps · Avarice |
| **Magic** | **Earth.** Iron's has no Earth school, so: **(a)** move Iron's earth-flavoured Nature spells (Earthquake, Stomp, Oakskin, Touch Dig) into a custom KubeJS "Earth" school with Iron's per-spell config, or **(b)** GTBC's Geomancy Plus (13 Geo spells; old build, needs testing) |
| **Combat** | Heavy knight: Shield Expansion (parry, shield tiers), Epic Knights and Knight Quest armor, hammers and maces |
| **Aspect mods** | Mining (YUNG's Better Mineshafts + our Terralith patch, a veinminer, Create Ore Excavation) · treasure (Lootr, archaeology) · **Apotheosis gems** · Kings & Monsters (the Ogre King locks Bog Iron) |
| **Talent XP** | Ores mined (high), stone (tiny), loot chests opened, archaeology finds, emeralds earned from trades, gems socketed |
| **Spectrum deeds** | treasure, plunder, strike it rich, hoard, profit, dig up / fish up treasure, ransack a village |
| **Mount** | Wyrmroost **Overworld Drake** (an armored ground mount) → Book of Dragons **Gronckle** (the rock-eating dragon) |
| **Nemeses** | Ferrous Wroughtnaut · Tongbi the Sculptor · **Ogre King** · Void Blossom · **Ancient Remnant** |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Epic Knights plate + kite shield, **Axe of a Thousand Metals** (Wroughtnaut) |
| Mid | Knight Quest sets, **King's Club + Crown** (Ogre King), **Earthrend Gauntlet** (Tongbi), Iron's Paladin chestplate |
| Late | **Gauntlet of Guard** (Ender Guardian), Netherite Battlemage, Remnant gear |
| Extreme | Mythic gear socketed with perfect gems, the Orange ring |

**Questline: Path of Avarice**

| Tier | Quests |
|---|---|
| Early | *Shiny* (veinmine 64 iron) · *Grave Goods* (archaeology finds) · *Shaft Raider* (loot 5 Better Mineshafts) · *The Iron Ghost* (Ferrous Wroughtnaut) |
| Mid | *Ogre Country* (Kings & Monsters outposts) · *Crown of the Ogre King* · *Earthrend* (Tongbi) · *Gem Cutter* (5 gem types) · *The Deep Bloom* (Void Blossom) |
| Late | *Pyramid of Greed* (Ancient Remnant) · *The Hoard* (vault 9 gold + 9 diamond + 9 emerald blocks) · *The Guardian's Fist* (Ender Guardian) |
| **Ring trial** | ***Mine, All Mine***: bring the Hoard to the Ogre King's vault. Survive a **treasure gateway** (Gateways to Eternity waves). Then defeat the corrupted **Ancient Remnant** reborn in its pyramid. The orange light can't resist you |

**Ring powers:** Covet (pull in loot and XP) · Plunder (rip off everything a target holds and wears). Lit passive: kills drop more.

---

### 🟡 Yellow: The Nightblade
*"Fear, mastered, is a blade the dead can't parry."*

| | |
|---|---|
| **Corps · emotion** | Sinestro Corps · Fear. The Guardians distrust them, but the dead fear them, so the alliance needs them |
| **Magic** | Iron's **Ender** (Shadow Slash, Teleport, Echoing Strikes, Black Hole) + Fire's Ender Expansion. Late game: Eldritch (Signet of the Betrayer) |
| **Combat** | Assassin: daggers (Dungeons Weapons), Combat Roll, **Attract to Sound** (mobs hear you, so stealth matters), sneak-attack bonuses |
| **Aspect mods** | Night and undead hunting: Born in Chaos, The Graveyard, BOMD Night Lich, Mutant Monsters · **Korugar** (Fear Spire, Sinestro's Watchtower) |
| **Talent XP** | Kills at night, kills while sneaking, undead kills, kills of fleeing mobs |
| **Spectrum deeds** | terrorise, slay the fleeing / trapped, strike from shadow |
| **Mount** | Book of Dragons **Night Fury**, the stealth dragon |
| **Nemeses** | Nightmare Stalker · **Night Lich** · **Corrupted Champion** (Graveyard) · **Maledictus** · Sinestro's Watcher (custom) |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Leather + daggers, a Born in Chaos charm |
| Mid | **Shadowwalker** armor, Dragonskin Spell Book |
| Late | **Cursium** armor (Maledictus), Warden battlemage gear (Deeper & Darker: Spellbooks, optional) |
| Extreme | **Signet of the Betrayer**, Mythic daggers, the Yellow ring |

**Questline: Path of Fear**

| Tier | Quests |
|---|---|
| Early | *Strike from Shadow* (20 sneak kills) · *Nightwalker* (survive 3 nights in the wild) · *Silent Steel* (daggers) · *The Stalker* (Nightmare Stalker) |
| Mid | *Shadowwalker* · *The Lich of the North* (Night Lich) · *Grave Robber* (Corrupted Champion) · *Blink* (learn Teleport) |
| Late | *Prison of Curses* (Maledictus) · *Night Fury* (bond with a Night Fury) · *Into the Deep Dark* (outlast a Warden) |
| **Ring trial** | ***The Fear Spire***: get a ship to **Korugar**, climb the Fear Spire through Dread Plains and Fear Bogs, and **cage** the Watcher at Sinestro's Watchtower |

**Ring powers:** Terror (nearby mobs flee, weakened) · Cage (lock a target in yellow light).

---

### 🟢 Green: The Stormwright
*"You were chosen to overcome fear."* (from Create: Lanterns)

| | |
|---|---|
| **Corps · emotion** | Green Lantern Corps · Will. The Guardians' own Corps, and the heart of the alliance |
| **Magic** | Iron's **Lightning** (Thunderstorm, Ball Lightning, Volt Strike) + Cataclysm: Spellbooks *Technomancy* + Create: Wizardry |
| **Combat** | Speed duelist: rapiers and katanas (Simply Swords, Spartan Weaponry Unofficial), Combat Roll, Iron's Boots of Speed |
| **Aspect mods** | **Technology**: Create (+ New Age electricity, Crafts & Additions) · **Create Aeronautics** (balloons, planes, airships, **ships to Oa**) · Mekanism (MekaSuit) · **Draconic Evolution** (extreme tier, beta) · AE2 (optional) |
| **Talent XP** | Create/Mekanism milestone advancements, crafting machines, first flights, kills while outnumbered, wave defense |
| **Spectrum deeds** | slay the mighty, hold the line, outnumbered, endure the night, face the dark |
| **Mount** | **No dragon. They build their own:** hot-air balloon → propeller plane → Levitite airship → Lantern starship. *In co-op, Green builds the team's fleet* |
| **Nemeses** | **The Harbinger** (Cataclysm war machine) · Scylla (storm) · rival **lightning dragons** (Ice and Fire) · Chaos Guardian (Draconic, extreme) |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Create goggles + Extendo Grip, copper/iron rapier |
| Mid | **Electromancer** armor, New Age power, first plane |
| Late | **MekaSuit**, lightning dragonsteel, Witherite (Harbinger) |
| Extreme | **Draconic** (Wyvern → Draconic → Chaotic) armor, the Green ring |

**Questline: Path of Will**

| Tier | Quests |
|---|---|
| Early | *Cog and Copper* (first Create machines) · *Static* (Lightning Bolt) · *The Duelist* (a rapier) · *Hold the Line* (survive a Gateway wave) |
| Mid | *Lift-Off* (balloon) · *New Age* (generate electricity) · *Electromancer* · *Iron Prophet* (the Harbinger) |
| Late | *Propeller* (a plane) · *MekaSuit* · *Storm Rival* (stage-4 lightning dragon) · *Starship* (a ship that reaches Oa) |
| **Ring trial** | ***The Central Power Battery***: fly to **Oa**, restore the Guardian Outpost, and recharge the **Central Power Battery** while holding the line against the Trial of Will (waves on Oa) |

**Ring powers:** Resolve (shrug off all harm, steady, shield) · Fist (a giant hard-light fist). Lit passive: constructs cost a quarter less.

---

### 🔵 Blue: The Dawnwarden
*"All will be well."*

| | |
|---|---|
| **Corps · emotion** | Blue Lantern Corps · Hope |
| **Magic** | Iron's **Holy** (Greater Heal, Healing Circle, Divine Smite, Fortify) + Paladin Spells. **Water**: Cataclysm: Spellbooks *Abyssal*, or Somake Spells' *Aqua* school (heavy dependencies) |
| **Combat** | Paladin: sword and shield, healing allies, holy damage against undead |
| **Aspect mods** | **Villages**: Guard Villagers, Villager Recruits, Illager Invasion, Raids:Enhanced, Easy NPC villagers · trading · healing |
| **Talent XP** | **Raids won (big)**, villager trades, zombie villagers cured, healing done, iron golems built |
| **Spectrum deeds** | hero of the village, cure, rescue, rally, light the dark, build a guardian, keep watch, mend a golem |
| **Mount** | Ice and Fire **hippocampus** (sea) + a white **hippogryph** (the holy flier) |
| **Nemeses** | Raid bosses (Golem of Last Resort, Zapper, **Raider Blimp**) · the Invoker · **the Dead King** · Leviathan |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Kite shield + Iron's Priest's robes, Villager Bible |
| Mid | **Priest** armor, Paladin chestplate, Hallowed Gem (Invoker) |
| Late | **Tidal Claws** (Leviathan), Blood Staff / Necronomicon taken from the Dead King |
| Extreme | Mythic holy gear, the Blue ring |

**Questline: Path of Hope**

| Tier | Quests |
|---|---|
| Early | *Recruits* (hire 3 soldiers) · *Mercy* (cure a zombie villager) · *Light the Dark* · *Holy Light* (Heal) |
| Mid | *Iron Guardians* (build 2 golems) · *Vestments* (Priest armor) · *The Invoker* · *Rally* (win an Omen III raid) |
| Late | *The Dead King* (Iron's Catacombs) · *Sanctuary of the Deep* (Leviathan) · *Hippocampus* |
| **Ring trial** | ***The Long Night***: defend your **first village** through a Blood Moon horde and an **Omen V raid** (Raider Blimp) without losing a single villager. At dawn, the blue light rises |

**Ring powers:** Hope (heal you and allies) · Sanctuary (allies inside take half damage, hostiles are pushed out). Lit passive: slow heal, and **charges nearby Green rings**.

---

### 🟣 Indigo: The Wildheart
*"Nok."*

| | |
|---|---|
| **Corps · emotion** | Indigo Tribe · Compassion |
| **Magic** | Iron's **Nature** + **Alshanex's Familiars** (13 spell-casting familiars) |
| **Combat** | Ranger: bows and crossbows (Iron's Autoloader Crossbow); pets and familiars fight beside you |
| **Aspect mods** | **Taming and breeding**: Book of Dragons (bonding levels), Wyrmroost (breeding), Alex's Mobs, Redomesticate (pet beds, pet respawn), Companions! · **Farming**: Farmer's Delight + addons |
| **Talent XP** | Animals bred, mobs tamed, crops harvested, pets fed and healed, familiars bonded |
| **Spectrum deeds** | tame, breed, nurture, name, give, set free, kindness, defend a companion |
| **Mount** | **Bonded Book of Dragons dragons** (any species) + Wyrmroost drakes |
| **Nemeses** | Poachers and binders (Hollowmarch Reavers, Black Lantern beast-binders) · Frostmaw · Void Blossom |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Leather + bow, Druidic Tome |
| Mid | **Plagued** armor + Conjurer's Talisman, familiars |
| Late | Drake armor (Wyrmroost), dragon bonding gear (Book of Dragons) |
| Extreme | Mythic bow, **the Indigo Staff** (Create: Lanterns), the Indigo ring |

**Questline: Path of Compassion**

| Tier | Quests |
|---|---|
| Early | *Friend of the Wild* (tame a wolf, cat and horse) · *New Life* (breed 10 animals) · *Harvest Feast* (Farmer's Delight) · *Nature's Voice* (first Nature spell) |
| Mid | *Familiar* · *Plagued Robes* · *Drake Breeder* (Wyrmroost) · *Free the Beast* (calm Frostmaw) |
| Late | *Dragon Whisperer* (max bond) · *Set Them Free* (free a chained dragon from a Black Lantern camp) |
| **Ring trial** | ***The Staff of Compassion***: tend wounded creatures across five biomes. Then, when a corrupted beast-boss is beaten, **spare it** and set it free |

**Ring powers:** Blink (teleport where you look) · Exchange (swap places with a target). Lit passive: **can charge from a Lantern of any colour**, so Indigo supports mixed teams.

---

### 💜 Violet: The Starheart
*"You have been chosen for love."* (from Create: Lanterns)

| | |
|---|---|
| **Corps · emotion** | Star Sapphire Corps · Love |
| **Magic** | Iron's **Ice** (Ice Tomb, Blizzard, Ray of Frost) + **Galosphere: Spellbooks** (crystal) |
| **Combat** | Battlemage: sword + spell (Iron's imbued weapons), Netherite Battlemage armor |
| **Aspect mods** | **Bonds**: party play, protecting a companion · **The sky**: Terralith Skylands, Sky Villages, Floating Islands, Castle in the Sky, Nullscape **Crystal Peaks** |
| **Talent XP** | **Kills shared with party members (×2)**, distance flown, sky structures explored, allays befriended |
| **Spectrum deeds** | together, company, grief, give a flower, befriend an allay, armour a companion |
| **Mount** | Ice and Fire **ice dragon**, raised from an egg (a bond, not a conquest) |
| **Nemeses** | Frostmaw · Night Lich · wild ice dragons · the Castle in the Sky's guardians |

**Gear ladder:**

| Tier | Gear |
|---|---|
| Early | Cryomancer robes, Frostbranded Book |
| Mid | **Cryomancer** armor, Galosphere crystal gear |
| Late | Netherite Battlemage, **ice dragonsteel** |
| Extreme | Mythic crystal gear, the Violet ring |

**Questline: Path of Love**

| Tier | Quests |
|---|---|
| Early | *Together* (5 quests with a partner nearby) · *A Flower for You* · *Allay* · *First Frost* |
| Mid | *Cryomancer* · *The White Beast* (Frostmaw) · *Skylands* (visit 3 sky islands) |
| Late | *Castle in the Sky* · *Ice Brood* (raise an ice dragon) |
| **Ring trial** | ***Heart of the Sapphire***: fly your bonded dragon (or travel with a partner) to the End's **Crystal Peaks**, protect them through the climb, and take the violet crystal heart |

**Ring powers:** Enthrall (from the config; details to read once installed).

---

### Secret lights (Epilogue, optional)
- **Ultraviolet, *The Unseen* (Shame):** unlocks *only* when the spectrum whispers ultraviolet: unseen kills, skulking, hiding, fleeing. It's a hidden chapter of secrets, told in Modonomicon lore.
- **Gold, *The Bard* (Joy):** a support class built on Tunes n' Tomes (Melodic school, Bard armor) and joy deeds: music, dance, feasts, celebrations.

---

## 6. Leveling and the talent tree

**Engine: Pufferfish's Skills** (0.19.2). It's tagged beta, as every 0.x build is. Add-ons:
- **Unofficial Additions:** XP sources `harvest_crops`, `fishing` and `spell_casting`.
- **Pufferfish's Attributes:** extra stats to use as rewards.

**Categories:**
- **Adventurer**: always open. Generic XP: mobs, bosses, raids, exploration. Gives general stats.
- **Seven class categories**, locked until chosen. Choosing one is a quest whose reward runs `/puffish_skills category unlock <player> gl:<class>`.
- Two **secret** categories, unlocked by their own hidden quests.

**Each class tree has three branches and a capstone:**
1. **Element:** spell power for that school, mana, cooldowns.
2. **Style:** weapon stats such as attack speed, crit, armor, dodge.
3. **Aspect:** utility (mining speed, taming, flight fuel, …). It also **unlocks recipes early** through KubeJS stages.
4. **Capstone:** needs the ring.

**XP per class.** Each category only counts its own actions. Numbers are starting values for tuning:

| Class | Main XP sources (Pufferfish) |
|---|---|
| Red | `kill_entity` with a two-hander (×1.5 in the Nether) · `deal_damage` while health < 40% · boss kills |
| Orange | `mine_block`: ores 8, stone 0.2 · `increase_stat` traded emeralds · loot chests opened |
| Yellow | `kill_entity` at night ×1.5, undead ×1.5, while sneaking ×2 |
| Green | `criterion` on Create/Mekanism/Aeronautics advancements · `craft_item` on machine tags |
| Blue | `increase_stat` raid won (200) · trades (6) · `heal` |
| Indigo | `increase_stat` animals bred (5) · tamed · `harvest_crops` |
| Violet | `shared_kill_entity` ×2 · distance flown · sky structures |

- **Anti-farming** (per-chunk / per-entity limits) is built in, so mob grinders and trading halls can't level you.
- **Multipliers:** every expression gets `* (1 + mult/100)`, where `mult` is a scoreboard value. Quests raise it ("the spectrum has noticed you"). Once your ring is on, its Curios modifier raises it further.

---

## 7. Gear ladder

| Tier | Act | Source of gear |
|---|---|---|
| **Early** | Prologue–I | Crafted class kits (Epic Knights, Dungeons Weapons), Iron's Wandering Magician robes, first spellbooks |
| **Mid** | II | **Iron's school armor** (Pyromancer, Cryomancer, Electromancer, Priest, Shadowwalker, Plagued), Knight Quest sets, mid-boss uniques |
| **Late** | III | **Cataclysm boss gear** (Ignitium, Cursium, Infernal Forge, Gauntlet of Guard, Tidal Claws), **dragonsteel**, MekaSuit, Netherite Battlemage |
| **Extreme** | IV | **Apotheosis Mythic** affixed items + perfect gems, Tyros' Scythe, Draconic, the **rings** |

**How it's controlled:**
- **Apotheosis** (affixes, rarities, gems) is the global "loot quality" dial. Its world tiers line up with the acts (verify how tiers unlock).
- **LootJS** injects class gear into boss and dungeon loot.
- **Iron's Spellbooks Tweaks** caps spell rarity until the matching act.

---

## 8. Boss ladder

| Tier | Bosses (mod) | Class nemesis |
|---|---|---|
| **Prologue** | **Warlord Vex** (custom) | all |
| **Early** | Ferrous Wroughtnaut, Umvuthi, Tongbi (Mowzie's) · Supreme Bonescaller, Nightmare Stalker, Lifestealer (Born in Chaos) · Iron's school mages, Ancient Knight · Cataclysm dungeon minis · Mutant Zombie/Skeleton · Invoker | Orange, Red, Yellow, Blue |
| **Mid** | **Ogre King** (Kings & Monsters) · **Night Lich**, Nether Gauntlet, Void Blossom (BOMD) · Frostmaw · **Corrupted Champion** (Graveyard) · **The Harbinger** · Sir Pumpkinhead · stage-3 dragons | Orange, Yellow, Red, Indigo, Violet, Green |
| **Late** | Netherite Monstrosity, **Ignis**, **Ancient Remnant**, **Maledictus**, Ender Guardian, **Leviathan**, Scylla (Cataclysm) · **Dead King** (Iron's) · **Lord Pumpkinhead** · Obsidilith · stage-4/5 dragons | each class (see §5) |
| **Extreme** | **Echo of Tyros** (Iron's, 1000 HP) · Chaos Guardian (Draconic, verify) · Dark Doppelganger · The Ascended One (Discerning the Eldritch) · Ender Dragon (Better End Island) | ring trials, post-game |
| **Final** | **Nekron** + the Black Lantern Revenants (custom, §10) | everyone |

**Optional extra dimensions with their own boss ladders** (decision 6):
- Twilight Forest (Naga → Lich → Minoshroom → Hydra → Ur-Ghast → Snow Queen)
- The Aether (Slider → Valkyrie Queen → Sun Spirit)
- Eternal Starlight
- Deeper and Darker (the Otherside)

---

## 9. The corruption (the enemy grows)

The Black Lanterns' plague escalates with the acts, so the world feels like it's losing:

| Act | Pressure | Mods / how |
|---|---|---|
| Prologue | Pillager warband | the raid |
| I | Rare **Blackened elites**: mobs with a black-light affix | Champions-Unofficial + a KubeJS-registered "Blackened" affix |
| II | **Blood Moons** every ~10 nights with undead hordes · difficulty grows with distance from spawn | Enhanced Celestials (pick v1 or v2; their add-ons aren't cross-compatible) · Scaling Difficulty · Born in Chaos undead |
| III | **Corruption rifts** near ring-trial sites that slowly blight the land · Black Lantern patrols | a KubeJS "corruption node" (spreading `/fillbiome` + block swaps) · The Hordes (datapack horde nights) |
| IV | **The Black Moon**: every night until Nekron falls; fallen bosses rise | KubeJS world event + Revenant bosses |

**The Deep Dark temptation (decision 4).** In Create: Lanterns, the **Black ring** only takes someone who **died in the Deep Dark**. We can turn that into a story beat: a player who dies there hears Nekron's whisper. Either they resist, or (optionally) they take a *Fallen* path. Or we simply switch Black off for players.

---

## 10. Finale: Blackest Night

**Trigger:** the first player (or party) to hold a ring and finish Act III's last quest, *The Guardians' Summons*.

| Step | Quest | What happens |
|---|---|---|
| IV-1 | *The Dead Walk* | The Black Moon rises. Nekron's rings reanimate **seven Revenants**: Black Lantern versions of each class's nemesis (Black Ignis, Black Ancient Remnant, Black Maledictus, Black Harbinger, Black Dead King, Black Frostmaw, Black Night Lich). Each class hunts its own Revenant |
| IV-2 | *Recharge* | Fly to **Oa** and recharge at the Central Power Battery |
| IV-3 | *The Seven* | All seven lights must be carried by **one champion**. In co-op, players hand their rings to one bearer; the mod's `whiteNeedsTheSeven` rule does the rest, and the **White ring** chooses them |
| IV-4 | *The Void Throne* | In the End, Nekron's gate opens at YUNG's dragon bell tower. A **Black Lantern Ender Dragon** guards it |
| IV-5 | ***Nekron*** | Phase 1: Nekron + Black Lantern guard. Phase 2: he absorbs the Revenants' power. Phase 3: **only White Light can hurt him**, while the others keep the champion alive with Blue Sanctuary, Green Resolve, Indigo Blink and so on |
| IV-6 | *Life* | Nekron falls, the dead rest, and the White Lantern restores the land. Credits, then the Epilogue |

**How Nekron gets built** (decision 2: the "big guy"):
- **Now:** FIW Bosses (JSON phases, minions, dialogue, disguise as any mob) or a reskinned, buffed existing boss: Dead King, Apostle (Goety) or Maledictus, with phases scripted in KubeJS.
- **Later, in "Our own mods":** a proper Nekron entity (GeckoLib, scripted attacks, `ServerBossEvent`).
- **"Only White can hurt him":** a KubeJS `beforeHurt` check cancels damage unless the attacker wears the White ring.

---

## 11. Mods needed, by build phase

All versions are NeoForge 1.21.1, checked 2026-11-08. **R** = release, **β** = beta/alpha. ⚠ = risk noted.

### Phase A: Story backbone (first)
| Mod | Version | Notes |
|---|---|---|
| **Create: Lanterns** + Spectral Hub | alpha 20.11 / v4 | ⚠ ARR, private, alpha. Needs Create, Sable, Simulated, Aeronautics |
| Create · Sable · Simulated · Create Aeronautics | 6.0.10 · 2.0.6 · 1.3.2 · 1.3.2 | Simulated and Aeronautics are CurseForge-only |
| Curios | 9.5.1 | ring slot |
| FTB Quests + FTB Library + FTB Teams | 2101.1.38 · .39 · .12 | quest book |
| FTB XMod Compat | 21.1.14 | KubeJS ↔ FTB Quests |
| Easy NPC (+ FTB Quests compat) | 7.18.0 (+1.0.2) | NPCs, dialogue |
| Modonomicon | 1.123.0 | lore book that unlocks with the story |
| Pufferfish's Skills + Unofficial Additions + Attributes | 0.19.2 β · 2.2.8 · 0.8.3 | talent trees |
| Village Spawn Point (+ Collective) | 6.0 | spawn in a village |

### Phase B: Magic and combat
| Mod | Version | Notes |
|---|---|---|
| **Iron's Spells 'n Spellbooks** (+ Iron's Lib, GeckoLib, playerAnimator) | 3.16.3 | Its toml requires these even though Modrinth lists none. ⚠ raycast and teleport bugs on Aeronautics ships (#1142) |
| Iron's Spellbooks Tweaks | 1.5.0 | gate spells by act or boss |
| Cataclysm: Spellbooks | 1.1.11 | Abyssal (water) + Technomancy |
| Discerning the Eldritch | 1.4.5 | endgame Eldritch + boss |
| Paladin Spells · Fire's Ender Expansion · Galosphere: Spellbooks | 1.1.4 · 2.5.1 · 1.1.5 | Blue/Orange · Yellow · Violet |
| Alshanex's Familiars (+ FamiliarsLib) | v5.0 | Indigo. ⚠ past versions broke saves |
| KubeJS Iron's Spells (isskjs) | 4.0.3 | custom Earth school. ⚠ built before ISS 3.16; test |
| *Earth:* Geomancy Plus | 1.1.0 | ⚠ old, CurseForge-only, test. Or the KubeJS Earth school instead |
| Better Combat + Combat Roll | 2.4.0 · 2.0.6 | Use **instead of** Epic Fight, not with it |
| Simply Swords · Dungeons Weapons · Shield Expansion · Epic Knights · Knight Quest · Attract to Sound | 1.70.2 · 9.0.1 · 1.4.3 · 10.17 · 1.9.4 · 7.0.2 | weapons and styles |
| Apotheosis (+ Apothic Attributes / Enchanting / Spawners) | 8.9.0 | gear quality dial |
| Artifacts · Relics · Iron's Gems 'n Jewelry | 13.2.5 · 0.10.7.8 · 2.0.2 | trinkets |

### Phase C: Bosses and dungeons
| Mod | Version | Notes |
|---|---|---|
| L_Ender's Cataclysm | 3.33 | ⚠ vanilla biome IDs only, so it needs a Structurify/tag patch for Terralith |
| Bosses of Mass Destruction · Mowzie's Mobs · Born in Chaos | 1.3.3 · 1.8.2 · 1.7.6 | |
| Kings & Monsters (CurseForge) | 1.2.2 | ⚠ plains/swamp only: needs a biome patch |
| The Graveyard · Mutant Monsters · Illager Invasion · Goety | 4.0.1 · 21.1.1 · 21.1.6 · 3.2.2 | |
| FIW Bosses | 1.3.1 | Warlord Vex + Nekron (new mod) |
| Structurify (+ YACL) · Structure Layout Optimizer | 2.0.43 · 1.0.12 | density, overlap, Terralith biome fixes |
| When Dungeons Arise · Dungeons and Taverns · Castle in the Sky · Sky Villages · Floating Islands · Hollowmarch | (chinatown) | add one by one |

### Phase D: Dragons and mounts
| Mod | Version | Notes |
|---|---|---|
| **Ice and Fire CE** (+ Uranus, Jupiter) | 2.0 | fire, ice and lightning dragons, hippogryph, hippocampus, dragonsteel |
| **Book of Dragons** | 1.4.1 | HTTYD-style bonding (Night Fury, Gronckle, …). ⚠ CurseForge lists Fauna Engine as a dependency |
| Wyrmroost | 1.4.1 | drakes, breeding |
| Alex's Mobs Continued (+ CodxLib) · Redomesticate · Companions! | 2.3.0 · 2.0.0 · 1.3.7 | animals, pets |
| *Berk's Dragon Academy* | V0.5 beta | ⚠ overlaps Book of Dragons (pick one), thin docs. Its draw is the **Red Death** boss |

### Phase E: Aspect mods
| Mod | Version | Class |
|---|---|---|
| Create: New Age · Create Crafts & Additions · Mekanism · **Draconic Evolution** (β) · AE2 | 1.2.0 · 1.7.2 · 10.7.19 · 3.1.4 · 19.2.18 | Green |
| VeinMiner or FTB Ultimine · Create Ore Excavation · Lootr | 2.11.2 · 1.6.8 | Orange |
| Guard Villagers · Villager Recruits · Raids:Enhanced · Raided · Gateways to Eternity | 2.4.12 · 1.15.2 · 1.0.2 · 0.1.6 · 5.1.0 | Blue (+ the Prologue) |
| Farmer's Delight + addons | 1.3.4 | Indigo |
| Tunes n' Tomes | 1.1.0 | Gold (secret) |

### Phase F: Corruption
Enhanced Celestials (v1 + Horde/Destructive Moon, **or** v2 + Chaos Moon 2) · Champions-Unofficial 21.1.1.7 · Scaling Difficulty 1.1.0 · The Hordes 1.6.3f.

### Not available, or avoid
- **Not on NeoForge 1.21.1:** MCDW · T.O Magic 'n Extras · Ice and Fire: Spellbooks · Botania · Passive Skill Tree · Soulslike Weaponry · Cracker's Wither Storm · Illager Revolution.
- **Avoid:**
  - Epic Fight together with Better Combat.
  - Spell Engine / RPG Series: a second magic system next to Iron's (decision 7).
  - More than one HTTYD dragon mod.
  - MCA Reborn: its latest version isn't backwards compatible.

---

## 12. Decisions for you
1. **Create: Lanterns.** Where does it come from, and do we have permission to use and tune it? Can "The Team" give us a way to read deed points from scripts (KubeJS or a command)? That's the one missing link between quests and deeds.
2. **The big guy.** **Nekron** (recommended: it matches "the universe corrupted by the undead", and the mod already has the Black and White lights). Alternatives: **Parallax** (fear), **Krona**, or an original villain.
3. **Solo vs party for the White Light.** The rule "carry all seven rings" suits a party. For solo play, either let a solo player collect all seven (very long), or switch `whiteNeedsTheSeven` off and gate White behind a quest.
4. **The Black ring for players.** Off (enemies only), or an optional *Fallen* path for players who die in the Deep Dark.
5. **Secret classes** (Ultraviolet, Gold): in or out?
6. **Extra dimensions:** Twilight Forest / Aether / Eternal Starlight / Deeper and Darker?
7. **Spell Engine (RPG Series)** for extra class skills: keep it out, so Iron's stays the only magic?
8. **Dragons:** Book of Dragons (recommended) or Berk's Dragon Academy (for its Red Death)?
9. **Earth magic:** a KubeJS-made Earth school (more control) or Geomancy Plus (more spells, but old)?

---

## 13. Implementation map (what builds what)

| Mechanic | Built with |
|---|---|
| Spawn in a village | Village Spawn Point |
| Outpost next to the village | KubeJS on first load: `forceload add` → `place structure minecraft:pillager_outpost` → `forceload remove` |
| 7-day countdown + raid | KubeJS: saved start tick, `/bossbar`, `setRaidOmenPosition` + Raid Omen on day 7 |
| Warlord Vex, Nekron, Revenants | FIW Bosses (later our own mod) + KubeJS phases |
| Crashed Lantern | Create: Lanterns wreck / `place template createlanterns:oa/crashed_lantern_ship` + Easy NPC |
| Quest book | FTB Quests (+ FTB XMod Compat for KubeJS hooks) |
| Choosing a class | FTB Quests command reward → `/puffish_skills category unlock` |
| Talent trees and per-class XP | Pufferfish's Skills datapack (`kubejs/data/…`) |
| Recipe gating | KubeJS stages, set by skill nodes and quests |
| Spell gating | Iron's Spellbooks Tweaks + Iron's per-spell datapack config |
| Earth school | isskjs custom school + Iron's per-spell "school" reassignment |
| Rings, deeds, powers, planets | Create: Lanterns (config: `ringAt` raised, joke lights off) |
| Reading deeds in quests | **Missing.** Needs an API from the mod team, or a small bridge mod of ours |
| Lore | Modonomicon entries unlocked by quests and advancements |
| Loot by tier | Apotheosis + LootJS |
| Blackened elites | Champions-Unofficial + KubeJS affix |
| Black Moon, corruption rifts | Enhanced Celestials + KubeJS world events |
| "Only White can hurt Nekron" | KubeJS `beforeHurt` |
| Our own mods (later) | **lantern-bridge** (deed points ↔ quests/skills) · **nekron** (final boss) · **blackened** (corruption mobs and rifts) |

**Suggested next step:** Phase A, the backbone. Install Create → Sable → Simulated → Aeronautics → **Create: Lanterns**, one at a time as usual. Read its full config and test the calling in-game. Everything else in this document depends on how that mod behaves.
