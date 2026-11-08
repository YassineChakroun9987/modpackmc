# Quest sources

Write chapters as JSON in `quests/src/<chapter>.json`. Then run `python -I tools/questgen.py`, which writes
`server/config/ftbquests/quests/` (chapters, groups and the `lang/en_us.snbt` text). Check with `--check` first: it
validates every item, mob, structure, biome, dimension and advancement ID against `server/kubejs/exported/`.

```json
{
  "id": "prologue",                 // file name and chapter key: lowercase, unique
  "title": "&6Prologue: The Seventh Dawn",
  "subtitle": "A horn on the ridge...",
  "icon": "minecraft:bell",         // must be a real item id
  "group": "story",                 // story | classes | mods
  "order": 0,                       // order inside the group
  "quests": [
    {
      "key": "horn",                // unique in this chapter; referenced as "prologue:horn" elsewhere
      "title": "A Horn on the Ridge",
      "subtitle": "short line under the title",
      "desc": ["Paragraph one. &eColour codes&r work.", "", "Paragraph two."],
      "icon": "minecraft:goat_horn",
      "x": 0, "y": 0,                // grid position (1 unit = one quest width)
      "shape": "hexagon",            // circle square rsquare diamond pentagon hexagon octagon heart gear
      "size": 1.5,                   // optional, 1 = normal
      "deps": ["other_key", "act1:choose_path"],   // same-chapter key, or "chapter:key"
      "dep_mode": "one",             // optional: "one" = any one dependency is enough
      "optional": false,
      "tasks": [
        {"type": "item", "item": "minecraft:iron_sword", "count": 1, "consume": false},
        {"type": "kill", "entity": "minecraft:pillager", "count": 1, "custom_name": "Warlord Vex"},
        {"type": "advancement", "advancement": "minecraft:story/mine_stone"},
        {"type": "structure", "structure": "minecraft:village_plains"},
        {"type": "dimension", "dimension": "minecraft:the_nether"},
        {"type": "biome", "biome": "terralith:moonlight_grove"},
        {"type": "stage", "stage": "gl_warlord_slain", "team": true},
        {"type": "checkmark"}
      ],
      "rewards": [
        {"type": "item", "item": "minecraft:bread", "count": 8},
        {"type": "xp", "xp": 100},
        {"type": "xp_levels", "levels": 3},
        {"type": "skill_xp", "category": "adventurer", "amount": 50},
        {"type": "loot", "table": "greenlanterns:rewards/tier_1"},
        {"type": "command", "command": "/gl class join {p} red"},
        {"type": "stage", "stage": "gl_something"}
      ]
    }
  ]
}
```
Names to use for stages, commands, skill categories, reward tables and anchor quests are in `docs/CONTRACT.md`.
