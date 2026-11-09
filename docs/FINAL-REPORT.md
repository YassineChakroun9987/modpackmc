# Green Lanterns: final report (2026-11-09)

What I built overnight, every decision I made for you, and what still needs a real player to
check. Everything is committed to git, so any decision can be undone (`git log --oneline`).

> **Phase: development.** The world may be regenerated whenever a worldgen change needs it (you
> said so on 2026-11-09). Tell me when you start playing for real, and from then on it won't be.

---

## 1. Status in one look

| | |
|---|---|
| **Server** | Boots in ~45 s with **0 errors** and **0 unreviewed warnings** (2 known, harmless and explained) |
| **Mods** | 149 server jars + 9 client-only; the `greenlanterns` client is **in sync** |
| **World** | Fresh world `greenlanterns`, pre-generated 1,200 blocks around the spawn village. Older worlds are in `server/backups/` |
| **Quest book** | "The Book of Oa": **27 chapters, 660 quests** (story, 7 classes, finale, 17 mod guides) |
| **Space** | Oa, Korugar, the Moon and deep space are real places (Create Cosmonautics) |
| **Classes** | 8 skill trees (Adventurer + 7 lights): 22 + 7 × 34 nodes |
| **Loot** | 747 chest tables sorted into 5 difficulty tiers, items from every gear/magic mod, scaled by Luck |
| **Self-test** | `/gl_dev selftest`: **49/49 checks pass** on a fresh world (IDs, skill categories, trial scoring, the outpost, Warlord Vex, the crash site, both NPCs, corpse quick-loot) |

## 2. Before you play (5 minutes)

1. **Lower TLauncher's RAM.** It is set to **21 GB**. The server now uses up to 10 GB, and the
   PC has 32 GB. Running both at once won't fit. Set TLauncher to **8–10 GB** (Settings → memory).
2. **Start the server:** double-click `server\start.bat`. Wait for `Done`.
3. **Join** `127.0.0.1` with the `greenlanterns` instance. The story starts on your first login.
4. **Inviting friends** needs two changes, because the server is locked to this PC on purpose:
   - Clear `server-ip=` in `server.properties`.
   - Use a VPN such as **Tailscale, Radmin VPN or ZeroTier** rather than port forwarding. With
     `online-mode=false` (needed for TLauncher), anyone who can reach the server can log in as
     any name, **including yours (op)**. A VPN keeps strangers out.
   - Turn on the whitelist (`/whitelist on`, `/whitelist add <name>`) as well.
   - Change the RCON password in `server.properties` if the port is ever reachable.
5. Friends need the same mods: copy your `greenlanterns` instance's `mods` folder to them.

## 3. How a playthrough goes

**Prologue: The Seventh Dawn** (≈ 2–3 hours)
- You wake in a village (Village Spawn Point picks one). Elder Maren (gold name, right-click
  to talk) explains the situation.
- A pillager outpost stands on a ridge ~190 blocks north-east, led by **Warlord Vex** (300 HP,
  his own boss bar).
- A boss bar counts down **7 days** to the Warband's raid. The countdown only runs while someone
  is online.
- Quests teach the basics: wood, tools, food, bed, light, the first spell, arming villagers
  (Guard Villagers), an iron golem.
- On day 7 the raid starts as soon as a player is in the village. Winning gives Hero of the
  Village.
- Kill Vex (at any time) and, 10 seconds later, a **green star falls**: Kaelen's crashed Lantern
  ship lands ~70 blocks south-west. The dying Green Lantern tells the story of the corruption,
  the seven lights and the ring, and Act I opens.

**Act I: Proving Ground**
- Gear up (Better Combat weapons, shields, armour), find a waystone, a backpack, your first
  dungeon, a tavern and a shrine.
- Magic basics: a spellbook and scrolls, the inscription table.
- Diamonds and enchanting, a mage tower, the first champion boss, Apotheosis' Frontier tier.
- **"The Seven Lights"** quest: join a class. Seven "taste" quests let you try each style first.
  You can join **several** classes; each has its own tree and its own way of earning XP.

**The seven class chapters** (40–43 quests each)
- Every light has its own gear road, school armour, mounts, structures and bosses.
- **Level 10:** the light *whispers* (Create: Lanterns' own lines).
- **Level 25:** you *dream* of it, and the **trial boss** quest opens.
- After the trial boss: **the ring trial**, then the ring. After that come the "true" content,
  mythic gear and a legend quest for after the final boss.

| Light | Class | Trial boss (mid-game) | Plays like |
|---|---|---|---|
| Red | Bloodfire Berserker | Nether Gauntlet (BOMD) | Fire + Blood magic, two-handers, stronger at low HP, the Nether |
| Orange | Hoardwarden | Ogre King (Kings & Monsters) | Earth/Nature tank, mining, gems, treasure |
| Yellow | Stormwright | The Harbinger (Cataclysm) | Lightning, speed, Create / Mekanism / airships |
| Green | Lightwarden | The Dead King (Iron's Spells) | Paladin: villages, raids, Holy + Evocation |
| Blue | Frostbinder | Night Lich (BOMD) | Ice battlemage, cold lands, the sky |
| Indigo | Wildheart | The Hydra (Ice and Fire) | Beasts, pets, familiars, dragons, summons |
| Violet | Voidblade | The Corrupted Champion (Graveyard Lich) | Assassin: night, undead, Ender + Eldritch void magic |

**The ring trial** (your White/Black ring idea)
- Kill your class's trial boss. Party members within 64 blocks who are in that class get credit.
- The quest book then offers "the ring's question". Claiming it starts **four questions in
  chat**, answered by clicking. Each answer leans *self*, *life* or *death*.
- **3+ "life" answers → White ring. 3+ "death" answers → Black ring. Anything else → your
  class ring.**
- Out of the 81 possible answer paths, 63 give your class ring, 9 White and 9 Black. White
  and Black are rare but reachable on purpose, never by accident.
- The ring is announced to the whole server. Each class's trial can be done once per player.

**Finale: The Last Light** (opens with any ring)
1. Apotheosis' Summit tier and the Wither.
2. The **Twilight Forest** boss chain (Naga → Lich → Minoshroom → Hydra → Knight Phantoms →
   Ur-Ghast → Alpha Yeti → Snow Queen → the Final Castle).
3. Cataclysm's great bosses.
4. Chaos Island and the **Chaos Guardian** (Draconic Evolution). Its shard is part of the
   **Cosmic Worm**.
5. The Ender Dragon, then the **Devourer of Gods**: the final boss, a god-eating worm about
   335 blocks long.
6. Epilogue: optional extreme bosses.

**Guides tab** (16 mini questlines, one per big mod)
- **From the start:** how to play this pack (keys, parties, claims, maps).
- **Once you've made tools:** gear, mining, farming.
- **After you choose a class:** exploration, creatures, Apotheosis, Iron's Spells, dragons,
  Twilight Forest, bosses, Create, airships + Lanterns, Mekanism, AE2, Draconic.
- Each one teaches by doing and pays out tiered loot and skill XP.

## 4. Decisions I made for you

The ones you're most likely to want to change are marked ★.

### Story and classes
| # | Decision | Why | To change |
|---|---|---|---|
| 1 | ★ **Class names:** Bloodfire Berserker, Hoardwarden, Stormwright, Lightwarden, Frostbinder, Wildheart, Voidblade | Each says element + role in one word | `story/00_core.js` (`GL_CLASSES`) + quest titles |
| 2 | ★ **Trial bosses** (table above) | Each is a mid-game boss that fits its light, and all 7 exist in the pack (checked by the self-test) | `GL_CLASSES[...].boss` + that chapter's `trial` quest |
| 3 | ★ **White/Black = 4 RP questions**, 3 of 4 answers needed | Your idea was "decisions with text". 3 of 4 makes them a deliberate choice, rare (9/81 each) but never luck | `story/40_trial.js` (`GL_QUESTIONS`, `glTrialOutcome`) |
| 4 | You **can join several classes** | Friends can try lights out. XP comes from playing that class's style, so a second class doesn't level for free. Each tree caps spending at 45 of 52 points | `/gl class join` is only run by the class `join` quests |
| 5 | **Final boss = Devourer of Gods** (DoG mod), tuned: 6,000 HP, armour 15, ×1.6 damage, players deal ×0.4, regenerates unless hit. It scales with every player present (+50% HP, +15% damage each), and the party shares a budget of 2 deaths per player | You wanted an existing, very OP mod boss, not Nekron. DoG is the most "end of the universe" boss available on 1.21.1 | `server/config/dog-common.toml` |
| 6 | The **Cosmic Worm** (DoG's summon) also needs a **Chaos Shard** | Makes the Chaos Guardian a gate, so the end-game is a chain, not one craft | `tweaks/lanterns_and_endgame.js` |
| 7 | **Prologue:** a 7-day countdown to a raid, an outpost led by Warlord Vex, the crash after Vex dies, Elder Maren and Kaelen as talking NPCs | Your story pitch (village, outpost, 7-day raid) made concrete. Vex can be killed early | `story/10_prologue.js`, `story/20_npcs.js` |
| 8 | The raid countdown only runs **while someone is online** | Otherwise a server left running overnight would spend your 7 days for you | `glRaidLeft` in `story/10_prologue.js` |
| 9 | **Create: Lanterns:** rings no longer choose players by themselves, natural "deeds" are off, 24 items of unused lights (4 joke lights, Gold, Ultraviolet) are hidden from JEI | Your story hands out rings through the trial; the mod's own emotion system (Yellow = fear…) doesn't match your colour map | `server/config/createlanterns-server.toml` |
| 10 | The class whisper at **level 10**, the dream at **level 25** | Spreads the light's "calling" across the class road | `story/30_classes.js` |

### Systems
| # | Decision | Why |
|---|---|---|
| 11 | **Iron's Spells** as the magic base, plus Cataclysm: Spellbooks, Discerning the Eldritch, Alshanex's Familiars, Galosphere Spellbooks and DarkDoppelganger | Iron's has a school for every light and the most add-ons on 1.21.1 |
| 12 | **Pufferfish's Skills** for class trees: Adventurer (everyone) + 7 classes, levels 40 / 50 | Real skill-tree screen, data-driven, has a KubeJS API the story uses |
| 13 | **FTB Quests + FTB Teams** for the book and parties | The standard; works with KubeJS stages |
| 14 | Parties: **FTB Teams** for everything; Open Parties and Claims uses the same parties. My glue script also puts each party in a vanilla team with **friendly fire off**, so allies' spells and swords don't hurt each other, and Pufferfish shares class XP inside the party | One party system instead of three |
| 15 | Boss credit for everyone **within 64 blocks** (trial bosses: same class only) | Co-op shouldn't mean only the last hitter progresses |
| 16 | **Apotheosis** for gear progression (affixes, gems, world tiers) | Gives every item a rarity ladder that fits the story's acts |
| 17 | **Loot: 5 tiers by structure difficulty**, injected into every structure chest, with items from all gear/magic mods. Luck matters: at Luck 5 a tier-3 chest's empty rolls drop from 33% to 11%, plus an extra roll. The Adventurer tree gives +2 Luck | Your "luck stat + difficulty + all mods" request |
| 18 | **Lootr**: every player gets their own copy of each chest | No loot-stealing between friends |
| 19 | **Almost Unified**: one copper, tin, silver, steel… across mods | Your "no duplicate items" request |
| 20 | Rings, Draconic gear, boss uniques and spawn eggs are **never** in loot | They belong to the story or the end-game |

### Quality of life (the "design choices waiting for you" from before)
| Choice | Picked |
|---|---|
| Map | Xaero's Minimap + World Map |
| Backpacks | Sophisticated Backpacks |
| Gravestone | Corpse (your items wait in your body). **Right-click your own body** and everything goes back where it was, Curios slots too; **Shift + right-click** opens the normal window (see §10) |
| Fast travel | Waystones |
| Land claims | Open Parties and Claims |
| Vein mining | FTB Ultimine (hold `` ` ``) |
| Recipe conflicts | Polymorph |

### Technical
| Decision | Why |
|---|---|
| Server heap 4–10 GB (was 2–6) | 147 mods |
| View distance 12 (was 10) | The Devourer is ~335 blocks long; clients only see entities inside the view distance, so at 10 he went invisible mid-fight |
| Mod guides unlock in stages | Keeps the start simple: only "how to play" at first |
| Dropped **Illager Invasion** | Needs a library (`extensibleenums`) that isn't published for 1.21.1 |
| ★ Added **Create Cosmonautics** (beta) | Without it, Create: Lanterns' Oa and Korugar don't exist. With it they're real worlds, and a lit ring can fly you into space (see §7) |

## 5. Please check in-game

Things that need a real player, so I couldn't test them headless:

**Story**
- [ ] First login: the book is given, the elder's lines appear, the countdown bar shows.
- [ ] Right-click Elder Maren and, later, Kaelen: dialogue appears and isn't repeated.
- [ ] Day 7: the raid starts when you're in the village; winning gives Hero of the Village.
- [ ] Killing Vex: the crash happens ~10 s later and Kaelen glows green.
- [ ] The ring trial: clickable answers in chat, a ring arrives, it can be worn (Curios ring
      slot). Test a White and a Black path too.
- [ ] Space: fly straight up with a lit, charged ring and check you reach deep space, can steer
      toward Oa, and land there.

**Systems**
- [ ] Skill trees: open the skills screen (default key **K**), check a class tree unlocks after
      its join quest, and that XP feels right. The curve is level 10 ≈ 1.9k XP, level 25 ≈ 13k XP.
- [ ] Parties: make an FTB party with a friend and check friendly fire is off and XP is shared.
- [ ] Loot: open the same kind of chest with and without `/effect give @s luck 60 5`.
- [ ] Corpse: die wearing a backpack, spellbook and ring, respawn, pick something up, then
      right-click your body: everything is back in its old slot and the body disappears.
      Shift + right-click opens the window instead. A friend right-clicking your body gets the
      normal window.
- [ ] Storage: put a Sophisticated chest and a controller down, break the full chest (it should
      drop as one packed chest), and search from the controller. The storage guide is right after
      *Arms and Armour* in the quest book.

**Quest hints to confirm**
- [ ] How Lord Pumpkinhead is summoned and where the Supreme Bonescaller spawns (Born in Chaos).
- [ ] Scylla's location (Cataclysm).
- [ ] Which dimension the Cosmic Worm works in.
- [ ] The Aeronautics item chain.

**Notes**
- `/loot give` (quest rewards) ignores Luck, so Luck only matters for chests.
- Pufferfish crafting XP counts crafting-table crafts only. Create mechanical crafting and
  Draconic fusion don't count.

## 6. Known limits

- Create Cosmonautics is a **beta**. It booted cleanly in every test, but space travel hasn't been
  tried by a player yet. If it causes trouble, remove its jar from the server and the client.
  The Oa / Korugar / deep-space quests then can't be completed; everything else is unaffected.
- Create: Lanterns has **no ring-forging recipes** in this alpha. Rings come only from the trial
  (or `/give` as op).
- Some guide quests are checkmarks, because the mod has no item or advancement to detect:
  Better Combat, Xaero's, OPAC, Jade and similar.
- Quest progress belongs to an **FTB team**. If you and a friend share a team, you share class
  progress too (and can both claim rewards). For separate class paths, keep separate teams. Boss
  credit works between teams anyway (the 64-block rule).

## 7. Create Cosmonautics, and two quest-book bugs caught at the end

**Cosmonautics.** The guide writer noticed that Create: Lanterns' Lantern worlds only exist with
**Create Cosmonautics**. It's on CurseForge for NeoForge 1.21.1, as beta 26.08.307: I checked
the file size against CurseForge, and its dependencies were already in the pack. With it:
- the server has 4 new dimensions: `createlanterns:oa`, `createlanterns:korugar`,
  `rocketnautics:moon` and `rocketnautics:deep_space`;
- a lit ring keeps flying past ~20,000 blocks up, into deep space, and keeps you breathing there
  (new `[cosmonautics]` section in the Lanterns config; our own settings were untouched);
- rockets, thrusters, a space helmet, jetpack and **titanium ore** are added.

Because titanium generates in the Overworld, I **generated the world again** after adding it. The
"Oa" and "Korugar" quests now require actually going there, after a new "Beyond the Sky" quest
(reach deep space by ring or rocket). Yellow's "Starship" quest ends in deep space.

**Two bugs FTB Quests hides completely.** Both were found by comparing the quest files before and
after a boot, and both are fixed and guarded against in `tools/questgen.py`:
1. FTB reads quest IDs as *signed* numbers. About half of our IDs started with 8–F, so FTB quietly
   gave those quests new IDs. Their titles and dependency lines no longer matched.
2. FTB's stage task is called `gamestage`, not `stage`. FTB deleted all 44 story stage tasks on
   load: the trials, the ring, the raid, the crash, the Lantern's tale.

Now: 646 quests, all titled, all 772 dependency links resolve, every task type and field survives
a boot, and a second boot leaves the files byte-for-byte unchanged.

## 8. Still yours to decide

- Shaders (Iris) and EMI next to JEI: both client-side taste. If you add Iris, also add
  **Enhanced Celestials 2: Shader Support** (both sides), or the moons look wrong with shaders.
- Whether anything in section 4 should change, especially ★ 1–3.
- When you'd like to publish the repo anywhere: change the RCON password first.

## 9. Where things live

| What | Where | How to change it |
|---|---|---|
| Story engine | `server/kubejs/server_scripts/story/` | edit, then `/reload` (or restart) |
| Party/tag glue, corpse quick-loot | `server/kubejs/server_scripts/glue/` | same |
| Quest book | `quests/src/*.json` | `python -I tools/questgen.py --check`, then without `--check` |
| Skill trees | `tools/skills/gen_skills.py` | run it, then `tools/skills/check_skills.py` |
| Loot | `tools/loot/gen_loot.py` + `server/kubejs/server_scripts/loot/` | run it, then `tools/loot/check_loot.py` |
| Names and stages | `docs/CONTRACT.md` | the contract every script and quest follows |
| Every mod and why | `MODLIST.md` | — |
| Word lists (mods; armour and weapons) | `docs/Green-Lanterns-Mod-List.docx`, `docs/Green-Lanterns-Armour-and-Weapons.docx` | mods: `node tools/modlist_doc.js`; gear: boot with `--cmd "gl_dev exportgear"`, then `python -I tools/gear_data.py`, then `node tools/gear_doc.js` (both need `npm install docx@9` in a scratch folder, see the script headers) |
| Test boots | `python -I tools/boottest.py --fresh --cmd "gl_dev selftest"` | results in the log |
| Pre-generate | `python -I tools/pregen.py --radius 1200` | server must be stopped |
| Admin commands | `/gl class join <p> <id>`, `/gl trial begin <p> <id>`, `/gl lore <p> <entry>` | op only |
| Player commands | `/gl status` (your classes and ring), `/gl choose <n>` (trial answers) | anyone |

## 10. Changes after the overnight build (2026-11-09, morning)

**Enhanced Celestials → Enhanced Celestials 2.** Version 6.0.2.6 showed an "Enhanced Celestials 2
is here!" screen every time you joined a world, and had no setting to turn it off. It's replaced
by **EC 2 Core + Default Lunar Events**: the same blood, blue, harvest and super moons, and the
version that's still maintained. Going back to 6.0.2.5 instead would probably have broken with
our newer Data Anchor library. Your friends' `mods` folders need the same swap: remove
`Enhanced-Celestials-NeoForge-1.21.1-6.0.2.6.jar` and add the two `Enhanced-Celestials-2-*` jars.

**Corpse quick-loot** (`glue/corpse_quickloot.js`). Right-click **your own** body:
- hotbar, inventory, armour and offhand items go back into the exact slots they were in;
- Curios (backpack, spellbook, rings, necklace...) go back into the exact curio slot they were
  in. Corpse doesn't record curio slots, so the script notes them at the moment you die;
- anything you picked up since respawning is moved to a free slot, not lost;
- if your pack is too full, the rest stays in the body and chat tells you so;
- the empty body disappears.

**Shift + right-click** still opens the normal Corpse window. Other people's bodies, and other
people at yours, work exactly as before. A body from before this script existed has no curio
note, so its curios go into whatever empty slot fits them. The self-test covers all of this with
a fake player (16 checks).

**Bug fix: the story NPCs never spoke.** In KubeJS 7, `event.cancel()` ends the script on the spot,
and the NPC script called it *before* the dialogue. So Elder Maren and Kaelen would have said
nothing. Worse, Kaelen's tale is what unlocks **Act I**, so the story would have stalled after the
crash. The dialogue now runs first and the cancel comes last. This is still on the in-game
checklist (§5): it needs a real right-click to confirm.

**Villages: Epic Structures towns + a story town.** CTOV is a "vanilla-plus" mod, and with its
default weights two-thirds of its villages were *small*. Your spawn village was a small savanna
one, which is why it didn't feel much better than vanilla. Now:
- **Epic Structures: Villages** rebuilds the 5 classic village types (plains, taiga, savanna,
  snowy, desert) as sprawling medieval towns: churches with spires, windmills, walled taiga towns,
  and a Roman-style savanna town with an arena. The classic villages are switched back on for it.
  It has no zombie variants, so nothing classic-looking appears.
- In those biomes about 60% of villages are Epic towns and 40% are CTOV villages. CTOV's small
  villages are much rarer (weight 10 → 3), and other biomes (jungle, swamp, beach, mesa...) keep
  CTOV's.
- **The story always starts in an Epic town:** on a new world, spawn moves to the nearest one
  before the prologue begins. On our seed it's a plains town at (-1040, 784).
- The world was regenerated for this (you said that's fine while we're in development). The
  old one is in `server/backups/world-ctov-spawn-2026-11-09`.

**Sophisticated Storage** (added at your request). Chests, barrels and shulker boxes that take
upgrades and tier up in place (27 to 132 slots), drawer-style limited barrels, and a controller
that turns a room of storage into one searchable network. It's the non-tech step before AE2.
- **No item explosions:** breaking a storage drops it *packed*, with everything inside, like a
  shulker box. The contents live in the world's save, not in the item, so carrying a full chest
  can't cause network trouble.
- **Lag:** tested with 400 storages, each with a magnet and a hopper upgrade, all linked to a
  controller, with 1,200 loose items dropped on them. The server stayed at about 5–6 ms per tick
  (the limit is 50), the same as without them.
- **Connected:** a new mod guide, *The Quartermaster's Ledger* (12 quests, right after *Arms and
  Armour*); two optional Orange quests for the Hoardwarden (*The Counting House*, *A Bottomless
  Hoard*); storage upgrades in chest loot, tiers 1 to 5. Your friends need the one new jar.

