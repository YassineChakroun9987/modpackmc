// ---------------------------------------------------------------------------
// Tag repairs. A tag that references an item that doesn't exist fails to load
// ENTIRELY, and so does every tag that includes it. Each fix says why.
// ---------------------------------------------------------------------------
ServerEvents.tags('item', event => {
  // Discerning the Eldritch 1.4.5 lists discerning_the_eldritch:echo_greatsword in
  // #minecraft:swords, but never registers that item (only its model/texture ship).
  // Without this, #minecraft:swords fails, and with it enchantable/sword, /weapon,
  // /sharp_weapon, /durability, c:tools ... i.e. no sword in the pack can be enchanted.
  event.remove('minecraft:swords', 'discerning_the_eldritch:echo_greatsword')
})

// Dungeons Weapons' bone_cudgel_scythe_repair_items tag (lists the block-only minecraft:twisting_vines_plant)
// is replaced outright in kubejs/data/minecraftdungeonsv1/tags/item/ - KubeJS can't remove an entry that never resolved.
