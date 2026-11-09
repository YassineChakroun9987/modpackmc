// ============================================================================
//  Chest loot caps and the loot-chest counter (no Lootr: an opened chest is opened for everyone)
//
//  A structure chest rolls its loot the first time someone opens it, and on top of its own table
//  many mods add their loot (Iron's scrolls, Artifacts, Apotheosis, our tiers...). That piled up:
//  ~25 stacks and a Legendary scroll in a starter chest. So, right after a FRESH loot chest opens:
//   - its tier (1-5) is worked out like the tiered loot does (table id + Nether/End minimum);
//   - Iron's scrolls above the tier's rarity become ink of the allowed rarity, extra scrolls go;
//   - if it still holds more stacks than the tier allows, the cheapest stacks are removed
//     (junk first, gear and rare items last).
//  The first player to open a fresh loot chest also gets it counted: stages gl_loot_1 / 10 / 25 for
//  the quests, and +15 Orange class XP if they follow the Orange light.
//  Tuning: GL_CHEST_CAPS below.
// ============================================================================
var GL_CHEST_CAPS = {
  //   max scroll rarity (0 common .. 4 legendary), max scrolls, max stacks
  1: { rarity: 1, scrolls: 1, stacks: 9 },
  2: { rarity: 2, scrolls: 2, stacks: 11 },
  3: { rarity: 3, scrolls: 2, stacks: 13 },
  4: { rarity: 4, scrolls: 3, stacks: 15 },
  5: { rarity: 4, scrolls: 3, stacks: 18 },
}
var GL_INK = ['irons_spellbooks:common_ink', 'irons_spellbooks:uncommon_ink', 'irons_spellbooks:rare_ink',
              'irons_spellbooks:epic_ink', 'irons_spellbooks:legendary_ink']
var GL_JUNK = /^minecraft:(rotten_flesh|bone|string|stick|spider_eye|gunpowder|wheat_seeds|beetroot_seeds|paper|feather|flint|coal|torch|arrow|iron_nugget|gold_nugget|leather|book|bread|wheat)$/
var GL_PENDING_CHEST = {}   // player uuid -> { tier, until }
var $GLSpells = null
try { $GLSpells = Java.loadClass('io.redspace.ironsspellbooks.api.spells.ISpellContainer') } catch (e) { console.warn('[gl] Iron\'s spell API not available: ' + e) }

// Tier of a loot table, as the tiered loot sees it (0 = unclassified -> treated as tier 2).
function glChestTier(tableId, dimension) {
  var t = (typeof glLootTierOf === 'function') ? glLootTierOf(tableId) : 0
  if (!t) t = 2
  if (typeof GL_LOOT_DIMENSION_MIN_TIER !== 'undefined') GL_LOOT_DIMENSION_MIN_TIER.forEach(function (d) { if (d[0] === dimension) t = Math.max(t, d[1]) })
  return Math.min(5, Math.max(1, t))
}

// Rarity of an Iron's scroll (0..4), or -1 if it isn't one.
function glScrollRarity(stack) {
  if (!$GLSpells || String(stack.id) !== 'irons_spellbooks:scroll') return -1
  try {
    var data = $GLSpells.get(stack).getSpellAtIndex(0)
    return data.getSpell().getRarity(data.getLevel()).ordinal()
  } catch (e) { return -1 }
}

// How much a stack is worth keeping (higher = keep).
function glStackValue(stack) {
  var id = String(stack.id)
  var v = stack.getRarity().ordinal() * 10
  if (stack.getMaxStackSize() === 1) v += 6                       // tools, gear, books, unique items
  if (stack.isEnchanted() || id === 'minecraft:enchanted_book') v += 8
  if (GL_JUNK.test(id)) v -= 10
  if (glScrollRarity(stack) >= 0) v += 4 + glScrollRarity(stack) * 3
  return v
}

// Apply the tier's caps to an opened container. Returns a short summary.
function glCapChest(inv, tier) {
  var cap = GL_CHEST_CAPS[tier]
  var changed = { inked: 0, scrollsRemoved: 0, stacksRemoved: 0 }
  var scrollSlots = []
  for (var i = 0; i < inv.getContainerSize(); i++) {
    var s = inv.getItem(i)
    var r = glScrollRarity(s)
    if (r < 0) continue
    if (r > cap.rarity) { inv.setItem(i, Item.of(GL_INK[cap.rarity])); changed.inked++ }
    else scrollSlots.push({ slot: i, r: r })
  }
  scrollSlots.sort(function (a, b) { return b.r - a.r })
  scrollSlots.slice(cap.scrolls).forEach(function (x) { inv.setItem(x.slot, $ItemStack.EMPTY); changed.scrollsRemoved++ })
  var filled = []
  for (var j = 0; j < inv.getContainerSize(); j++) if (!inv.getItem(j).isEmpty()) filled.push({ slot: j, v: glStackValue(inv.getItem(j)) })
  if (filled.length > cap.stacks) {
    filled.sort(function (a, b) { return a.v - b.v })
    filled.slice(0, filled.length - cap.stacks).forEach(function (x) { inv.setItem(x.slot, $ItemStack.EMPTY); changed.stacksRemoved++ })
  }
  inv.setChanged()
  return changed
}

function glCountLootChest(player) {
  var n = player.persistentData.getInt('gl_loot_opened') + 1
  player.persistentData.putInt('gl_loot_opened', n)
  ;[1, 10, 25].forEach(function (k) { if (n >= k) glGiveStage(player, 'gl_loot_' + k) })
  if (player.stages.has('gl_class_orange')) glRun(player.server, 'puffish_skills experience add ' + player.username + ' greenlanterns:orange 15')
}

// 1. Right-click: if the block still has a loot table (never opened), remember its tier for this player.
BlockEvents.rightClicked(function (event) {
  var be = event.block.entity
  if (!be || typeof be.getLootTable !== 'function') return
  var key = be.getLootTable()
  if (!key) return
  var player = event.player
  GL_PENDING_CHEST[String(player.getUuid())] = { tier: glChestTier(String(key.location()), String(event.level.dimension)), until: event.server.tickCount + 10 }
})

// 2. The container opened with its loot rolled: cap it and count it.
PlayerEvents.chestOpened(function (event) {
  var player = event.player
  var k = String(player.getUuid())
  var p = GL_PENDING_CHEST[k]
  if (!p) return
  delete GL_PENDING_CHEST[k]
  if (p.until < event.server.tickCount) return
  glCapChest(event.inventory, p.tier)
  glCountLootChest(player)
})
