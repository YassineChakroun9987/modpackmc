# Integration contract

The names every part of the pack agrees on. Quests (FTB Quests), skill trees (Pufferfish), loot (LootJS) and
the story scripts (KubeJS) all build against this. **Don't rename anything here without updating every user.**
Real IDs for items, mobs, structures and so on are in `server/kubejs/exported/*.json`, which `/gl_dev export` writes from the running server.
Never guess an ID.

## Classes
| id | Light | Class | Magic (Iron's school) | Trial boss (mid-game) | Ring item |
|---|---|---|---|---|---|
| `red` | Red | Bloodfire Berserker | fire (+ blood) | `bosses_of_mass_destruction:gauntlet` (Nether Gauntlet) | `createlanterns:red_power_ring` |
| `orange` | Orange | Hoardwarden (earth tank) | nature, earth-flavoured: Earthquake, Stomp, Oakskin | `kingsandmonsters:ogre_lord` (Ogre King) | `createlanterns:orange_power_ring` |
| `yellow` | Yellow | Stormwright (lightning, speed, tech) | lightning | `cataclysm:the_harbinger` | `createlanterns:yellow_power_ring` |
| `green` | Green | Lightwarden (paladin, villages) | evocation (+ holy support) | `irons_spellbooks:dead_king` | `createlanterns:power_ring` (Green has no prefix) |
| `blue` | Blue | Frostbinder (ice battlemage) | ice | `bosses_of_mass_destruction:lich` (Night Lich) | `createlanterns:blue_power_ring` |
| `indigo` | Indigo | Wildheart (beast master, summoning) | summon spells from any school + Alshanex's Familiars | `iceandfire:hydra` | `createlanterns:indigo_power_ring` |
| `violet` | Violet | Voidblade (assassin, void magic) | ender + eldritch | `graveyard:lich` (The Graveyard's Corrupted Champion) | `createlanterns:violet_power_ring` |

**Special rings:** `createlanterns:white_power_ring` and `createlanterns:black_power_ring`. You can only get them from the ring-trial *choice* (see Stages). Never give them directly in quests.

**End-game chain:**
1. **Chaos Guardian** `draconicevolution:draconic_guardian` (drops `draconicevolution:chaos_shard`).
2. **Ender Dragon**: the Devourer "devours" it and drops `dog:draconic_soul_fragment`.
3. **Summon item:** `dog:cosmic_worm`. Its recipe also needs a chaos shard.
4. **Final boss:** `dog:devourer_head` (Devourer of Gods).

Optional extreme bosses: `darkdoppelganger:dark_doppelganger`, `legendary_monsters:the_obliterator`.

## KubeJS stages (`player.stages`); quests read them with FTB Quests `stage` tasks
| Stage | Set when |
|---|---|
| `gl_started` | first login (prologue begins) |
| `gl_raid_won` | the player has *Hero of the Village* (won the Warband raid) |
| `gl_warlord_slain` | Warlord Vex died near the player (party credit, 64 blocks) |
| `gl_crash_seen` | the player reached the crashed Lantern ship |
| `gl_lantern_heard` | the player listened to the dying Lantern |
| `gl_class_<id>` | the player joined class `<id>` (via `/gl class join`) |
| `gl_whisper_<id>` / `gl_dream_<id>` | class `<id>` reached level 10 / level 25 (the light whispers, then you dream of it) |
| `gl_trial_<id>` | the player (or party member within 64 blocks) killed class `<id>`'s trial boss while in that class |
| `gl_ring_<id>` | the ring-trial choice gave the player their class ring |
| `gl_ring_white` / `gl_ring_black` | the ring-trial choice gave the player the White / Black ring instead |
| `gl_ringbearer` | any of the above ring outcomes (use this when "a ring" is enough) |
| `gl_chaos_slain` | Chaos Guardian killed nearby |
| `gl_devourer_slain` | Devourer of Gods killed nearby |

## Commands (KubeJS); use them in FTB Quests command rewards (`elevate_perms` is set by the generator)
| Command | Effect |
|---|---|
| `/gl class join {p} <id>` | unlocks Pufferfish category `greenlanterns:<id>`, adds stage `gl_class_<id>`, prints the light's welcome |
| `/gl trial begin {p} <id>` | starts the **ring-trial dialogue** (RP choices in chat). Needs `gl_trial_<id>`. It ends with the class ring, White or Black |
| `/gl lore {p} <entry>` | prints a lore passage in chat (entries: `crash`, `oa`, `corruption`, `devourer`) |

## Pufferfish's Skills categories
- `greenlanterns:adventurer`: unlocked by default, generic XP (mobs, bosses, exploration).
- `greenlanterns:red|orange|yellow|green|blue|indigo|violet`: locked until joined.
- Quest XP into a tree: reward `{"type":"skill_xp","category":"red","amount":100}`, which becomes
  `/puffish_skills experience add {p} greenlanterns:red 100`.

## Reward loot tables (the loot writer creates them; quests use `{"type":"loot","table":"..."}`)
| Table | Contents |
|---|---|
| `greenlanterns:rewards/tier_1` … `tier_5` | mixed goodies from all mods, scaling early → extreme |
| `greenlanterns:rewards/scrolls_1` … `scrolls_3` | random Iron's Spells scrolls, common → epic |
| `greenlanterns:rewards/class_<id>` | a class-themed mid-game bundle (one per class id) |

## Quest anchors (cross-chapter dependency keys)
- `prologue:finale`: the last prologue quest. Act I depends on it.
- `act1:choose_path`: unlocks every class chapter.
- `<id>:join`: first quest of each class chapter (reward `/gl class join {p} <id>`).
- `<id>:trial`: kill-the-trial-boss quest.
- `<id>:choice`: reward `/gl trial begin {p} <id>`.
- `<id>:ring`: task: stage `gl_ringbearer`.
- `finale:last_light`: the final boss quest.

## KubeJS / Rhino gotchas (from testing)
- Inside functions, use `var` (Rhino throws "redeclaration of var" for `const`/`let` in some blocks).
- No computed object keys (`{[k]: v}`). Build objects with `o[k] = v`.
- Every file in `kubejs/data` must have a lowercase path, or KubeJS crashes at startup.
