# Create: Lanterns recipes

This folder is a data pack that every world of this game loads (a server's, or one played alone), always on and
above every other data pack: what is in it is how Create: Lanterns' recipes are made here.

* **Change a recipe**: copy it from `defaults/` to the same place under `data/` and edit the copy. For example,
  `defaults/data/createlanterns/recipe/foundry/great/green_ring.json` goes to
  `data/createlanterns/recipe/foundry/great/green_ring.json`.
* **Take a recipe away**: put a file of the same name and place under `data/` holding only

      {"neoforge:conditions": [{"type": "neoforge:false"}]}

* **Add a recipe**: put it under `data/createlanterns/recipe/` (or any other namespace's `recipe/` folder) with a
  name of its own.

Changes take effect as a world loads, or with `/reload`.

`defaults/` holds a copy of every recipe this version of the mod ships, written again each time the game starts:
it is there to copy from. It is not part of the pack, so editing it does nothing (and the edit is undone).

The heat (°C) a foundry must be at to make each thing is data too, and can be changed here a thing at a time:
`data/createlanterns/data_maps/fluid/foundry_heat.json` for its liquids and
`data/createlanterns/data_maps/item/foundry_heat.json` for the rings. This, as the first of them, lets a
Crucible that is only heated melt gold:

    {"values": {"createlanterns:molten_gold": 1000}}

Simpler switches, whether each way of making Lanterns and rings is on at all, are in
`config/createlanterns-common.toml` (`[recipes]`), read as the recipes load; the foundry's numbers (lava and
charge a ring takes, the bellows it needs, how fast its mixer and bellows must turn, how fast it heats, what
makes a ring Flawed or a Masterwork, what a forge started wrong does) are world settings, in
`config/createlanterns-server.toml` (`[foundry]`), which every world reads but one with a copy of its own in
its `serverconfig` folder.

The game's own rules for this version of the mod hold whatever a recipe here says: a version without the
foundry makes nothing of the foundry's in a basin and takes its makings away, and nothing of a light a version
does not have is ever kept.
