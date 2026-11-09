// ============================================================================
//  Corpse quick-loot
//  Right-click your OWN body (Corpse mod) to take everything back at once:
//    - hotbar, inventory, armour and offhand go back into the exact slots they
//      were in (Corpse records those);
//    - Curios (backpack, spellbook, rings, necklace, ...) go back into the exact
//      curio slots they were in. Corpse doesn't record those, so we note them at
//      the moment of death (server persistent data "gl_corpse", last 8 deaths
//      per player) and match a body to its note by the time of death.
//    - Things picked up since respawning are moved aside to free slots; what
//      can't fit at all stays in the body, and you're told.
//  Shift + right-click opens the normal Corpse window. Other players' bodies,
//  and other players at yours, behave exactly as before (Corpse's own rules).
// ============================================================================

var $ItemStack = Java.loadClass('net.minecraft.world.item.ItemStack')
var $ListTag = Java.loadClass('net.minecraft.nbt.ListTag')
var $CuriosApi = null, $SlotContext = null
try {
  $CuriosApi = Java.loadClass('top.theillusivec4.curios.api.CuriosApi')
  $SlotContext = Java.loadClass('top.theillusivec4.curios.api.SlotContext')
} catch (e) { console.warn('[gl] Curios API not available: ' + e) }

var GL_CORPSE_KEEP = 8            // death notes kept per player
var GL_CORPSE_MATCH_MS = 120000   // a note belongs to a body if taken within 2 minutes of its death time

function glIsCorpse(e) { return !!e && typeof e.getDeath === 'function' && typeof e.getCorpseUUID === 'function' }

function glCorpseOwner(corpse, player) {
  var opt = corpse.getCorpseUUID()
  return opt.isPresent() && opt.get().equals(player.getUuid())
}

function glCurioHandler(player) {
  if (!$CuriosApi) return null
  var opt = $CuriosApi.getCuriosInventory(player)
  return opt.isPresent() ? opt.get() : null
}

// Every worn curio: [{id, index, cosmetic, stack}]
function glCurioSlots(player) {
  var out = [], h = glCurioHandler(player)
  if (!h) return out
  var curios = h.getCurios(), ids = curios.keySet().toArray()
  for (var k = 0; k < ids.length; k++) {
    var sh = curios.get(ids[k])
    var sets = [[sh.getStacks(), false]]
    if (sh.hasCosmetic()) sets.push([sh.getCosmeticStacks(), true])
    for (var s = 0; s < sets.length; s++) {
      var stacks = sets[s][0]
      for (var i = 0; i < stacks.getSlots(); i++) {
        var st = stacks.getStackInSlot(i)
        if (!st.isEmpty()) out.push({ id: String(ids[k]), index: i, cosmetic: sets[s][1], stack: st })
      }
    }
  }
  return out
}

// Put a stack into one exact curio slot, if that slot exists, is empty and accepts it.
function glCurioPut(h, player, id, index, cosmetic, stack) {
  var opt = h.getStacksHandler(id)
  if (!opt.isPresent()) return false
  var stacks = cosmetic ? opt.get().getCosmeticStacks() : opt.get().getStacks()
  if (index >= stacks.getSlots() || !stacks.getStackInSlot(index).isEmpty()) return false
  if (!$CuriosApi.isStackValid(new $SlotContext(id, player, index, cosmetic, true), stack)) return false
  stacks.setStackInSlot(index, stack)
  return true
}

// Put a stack into the first empty curio slot that accepts it.
function glCurioPutAnywhere(h, player, stack) {
  var ids = $CuriosApi.getItemStackSlots(stack, player).keySet().toArray()
  for (var k = 0; k < ids.length; k++) {
    var opt = h.getStacksHandler(ids[k])
    if (!opt.isPresent()) continue
    for (var i = 0; i < opt.get().getStacks().getSlots(); i++) {
      if (glCurioPut(h, player, String(ids[k]), i, false, stack)) return true
    }
  }
  return false
}

function glCorpseStore(server) {
  var root = server.persistentData
  if (!root.contains('gl_corpse')) root.put('gl_corpse', NBT.compoundTag())
  return root.getCompound('gl_corpse')
}

// At death: note which curio slot every worn curio was in.
function glCorpseSnapshot(player) {
  var reg = player.server.registryAccess()
  var slots = new $ListTag()
  glCurioSlots(player).forEach(function (c) {
    var t = NBT.compoundTag()
    t.putString('id', c.id)
    t.putInt('i', c.index)
    t.putBoolean('c', c.cosmetic)
    t.put('item', c.stack.save(reg))
    slots.add(t)
  })
  var snap = NBT.compoundTag()
  snap.putLong('t', Date.now())
  snap.put('slots', slots)
  var store = glCorpseStore(player.server), key = String(player.getUuid())
  var old = store.getList(key, 10), hist = new $ListTag()
  for (var i = Math.max(0, old.size() - (GL_CORPSE_KEEP - 1)); i < old.size(); i++) hist.add(old.getCompound(i))
  hist.add(snap)
  store.put(key, hist)
}

function glCorpseFindSnapshot(server, uuid, deathTime) {
  var hist = glCorpseStore(server).getList(String(uuid), 10)
  var best = null, bestDiff = GL_CORPSE_MATCH_MS
  for (var i = 0; i < hist.size(); i++) {
    var s = hist.getCompound(i), diff = Math.abs(Number(s.getLong('t')) - deathTime)
    if (diff <= bestDiff) { best = s; bestDiff = diff }
  }
  return best
}

// Move everything from the body back onto the player. Returns counts for the message.
function glCorpseLoot(player, corpse) {
  var reg = player.server.registryAccess()
  var death = corpse.getDeath(), inv = player.getInventory()
  var res = { back: 0, curios: 0, moved: 0, left: 0 }
  var spill = []   // taken out of the body, not placed yet
  var extra = []   // the body's "additional items" (curios and other mods' drops)
  var add = death.getAdditionalItems()
  try {
    // 1. Hotbar/inventory, armour, offhand -> the slot they were in.
    var main = death.getMainInventory(), wanted = {}
    for (var w = 0; w < main.size(); w++) if (!main.get(w).isEmpty()) wanted[w] = true
    var freeSlot = function () {
      for (var j = 0; j < inv.items.size(); j++) if (!wanted[j] && inv.items.get(j).isEmpty()) return j
      return -1
    }
    var putBack = function (from, to) {
      for (var i = 0; i < from.size() && i < to.size(); i++) {
        var s = from.get(i)
        if (s.isEmpty()) continue
        from.set(i, $ItemStack.EMPTY)
        var cur = to.get(i)
        if (cur.isEmpty()) { to.set(i, s); res.back++; continue }
        if ($ItemStack.isSameItemSameComponents(cur, s)) {
          var n = Math.min(cur.getMaxStackSize() - cur.getCount(), s.getCount())
          if (n > 0) { cur.grow(n); s.shrink(n) }
          if (s.isEmpty()) res.back++
          else spill.push(s)
          continue
        }
        var j = freeSlot()   // something picked up since respawning sits here: move it aside
        if (j >= 0) { inv.items.set(j, cur); to.set(i, s); res.back++; res.moved++ }
        else spill.push(s)
      }
    }
    putBack(main, inv.items)
    putBack(death.getArmorInventory(), inv.armor)
    putBack(death.getOffHandInventory(), inv.offhand)

    // 2. Curios -> the exact slot they were in (first the identical item, then the same kind).
    for (var a = 0; a < add.size(); a++) if (!add.get(a).isEmpty()) extra.push(add.get(a))
    add.clear()
    var h = glCurioHandler(player)
    if (h) {
      var snap = glCorpseFindSnapshot(player.server, player.getUuid(), Number(death.getTimestamp()))
      if (snap) {
        var slots = snap.getList('slots', 10), used = {}
        for (var pass = 0; pass < 2; pass++) {
          for (var x = 0; x < extra.length; x++) {
            var st = extra[x]
            if (!st) continue
            for (var k = 0; k < slots.size(); k++) {
              if (used[k]) continue
              var e = slots.getCompound(k)
              var was = $ItemStack.parseOptional(reg, e.getCompound('item'))
              var same = pass === 0 ? $ItemStack.isSameItemSameComponents(was, st) : $ItemStack.isSameItem(was, st)
              if (same && glCurioPut(h, player, String(e.getString('id')), e.getInt('i'), e.getBoolean('c'), st)) {
                used[k] = true; extra[x] = null; res.curios++
                break
              }
            }
          }
        }
      } else {
        // No note for this body (it died before this script existed): wear whatever fits.
        for (var y = 0; y < extra.length; y++) {
          if (extra[y] && glCurioPutAnywhere(h, player, extra[y])) { extra[y] = null; res.curios++ }
        }
      }
    }
    extra.forEach(function (s) { if (s) spill.push(s) })
    extra = []

    // 3. The rest: any free slot. What doesn't fit stays in the body.
    for (var q = 0; q < spill.length; q++) {
      var s2 = spill[q]
      inv.add(s2)
      if (!s2.isEmpty()) { add.add(s2); res.left++ } else res.back++
      spill[q] = null
    }
  } catch (err) {
    // Never lose an item: anything in flight goes back into the body.
    spill.concat(extra).forEach(function (s) { if (s && !s.isEmpty()) add.add(s) })
    throw err
  }
  inv.setChanged()
  player.inventoryMenu.broadcastChanges()
  if (corpse.isEmpty()) corpse.discard()
  return res
}

function glCorpseQuickLoot(server, player, corpse) {
  // Someone else has this body's window open: close it first, so nobody takes the same item twice.
  server.players.forEach(function (p) {
    var m = p.containerMenu
    if (m && typeof m.getCorpse === 'function' && m.getCorpse() && m.getCorpse().getUuid().equals(corpse.getUuid())) p.closeContainer()
  })
  try {
    var r = glCorpseLoot(player, corpse)
    var name = player.username
    glRun(server, 'execute at ' + name + ' run playsound minecraft:entity.item.pickup player ' + name + ' ~ ~ ~ 0.8 0.8')
    if (r.left > 0) {
      glSay(player, '§eYour pack is full: §f' + r.left + '§e stack' + (r.left === 1 ? ' is' : 's are') +
        ' still in your body. Make room and right-click it again.')
    } else {
      player.displayClientMessage(Text.of('§aYou gather your belongings.' +
        (r.moved > 0 ? ' §7(What you picked up since was moved aside.)' : '')), true)
    }
  } catch (err) {
    console.error('[gl] corpse quick-loot failed: ' + err)
    glSay(player, '§cCouldn\'t take your things back automatically. Shift + right-click the body to open it.')
  }
}

EntityEvents.death(function (event) {
  var e = event.entity
  if (!e.isPlayer()) return
  try { glCorpseSnapshot(e) } catch (err) { console.error('[gl] corpse: could not note curio slots: ' + err) }
})

// event.cancel() THROWS in KubeJS 7 (it ends the handler), so it must be the last line.
ItemEvents.entityInteracted(function (event) {
  var t = event.target, player = event.player
  if (!glIsCorpse(t) || player.isShiftKeyDown() || !glCorpseOwner(t, player)) return
  if (String(event.hand) === 'MAIN_HAND') glCorpseQuickLoot(event.server, player, t)
  event.cancel()   // don't open the Corpse window
})

// Dev: called by /gl_dev selftest. A fake player dies wearing curios, respawns,
// picks up dirt into an old slot, and takes everything back from the body.
function glCorpseSelftest(server, check) {
  var $Fake = Java.loadClass('net.neoforged.neoforge.common.util.FakePlayerFactory')
  var $Profile = Java.loadClass('com.mojang.authlib.GameProfile')
  var $UUID = Java.loadClass('java.util.UUID')
  var $Death = Java.loadClass('de.maxhenkel.corpse.corelib.death.Death')
  var $Corpse = Java.loadClass('de.maxhenkel.corpse.entities.CorpseEntity')
  var fp = $Fake.get(server.overworld(), new $Profile($UUID.fromString('00000000-0000-4000-8000-00000000c0b5'), 'gl_corpse_test'))
  var items = server.registryAccess().registryOrThrow(Java.loadClass('net.minecraft.core.registries.Registries').ITEM)
  var inv = fp.getInventory(), h = glCurioHandler(fp)
  inv.clearContent()
  check('corpse: fake player has curio slots', h !== null)
  if (!h) return
  inv.items.set(3, Item.of('minecraft:diamond_sword'))
  inv.items.set(20, Item.of('minecraft:bread', 7))
  inv.armor.set(3, Item.of('minecraft:iron_helmet'))
  inv.offhand.set(0, Item.of('minecraft:shield'))
  var worn = []
  ;['sophisticatedbackpacks:backpack', 'irons_spellbooks:iron_spell_book', 'artifacts:cross_necklace', 'createlanterns:power_ring'].forEach(function (id) {
    if (!items.containsKey($ResourceLocation.parse(id))) { check('corpse: test item ' + id + ' exists', false); return }   // Item.of throws on unknown ids
    var st = Item.of(id), ids = $CuriosApi.getItemStackSlots(st, fp).keySet().toArray()
    if (ids.length === 0) { console.info('[selftest] corpse: ' + id + ' has no curio slot'); return }
    var stacks = h.getStacksHandler(ids[0]).get().getStacks()
    for (var i = stacks.getSlots() - 1; i >= 0; i--) {   // the LAST free slot, to prove the exact index comes back
      if (stacks.getStackInSlot(i).isEmpty()) { stacks.setStackInSlot(i, st); worn.push({ id: id, slot: String(ids[0]), i: i }); break }
    }
  })
  console.info('[selftest] corpse: wearing ' + worn.map(function (w) { return w.id + '@' + w.slot + '#' + w.i }).join(', '))
  check('corpse: test curios worn', worn.length >= 2)
  // Death: our note, Corpse's record, then everything leaves the player (dropped into the body).
  glCorpseSnapshot(fp)
  var death = $Death.fromPlayer(fp)
  worn.forEach(function (w) {
    var s = h.getStacksHandler(w.slot).get().getStacks()
    death.getAdditionalItems().add(s.getStackInSlot(w.i))
    s.setStackInSlot(w.i, $ItemStack.EMPTY)
  })
  inv.clearContent()
  inv.items.set(3, Item.of('minecraft:dirt', 5))   // respawned and picked up dirt into the sword's slot
  var corpse = $Corpse.createFromDeath(fp, death)
  check('corpse: owner recognised', glIsCorpse(corpse) && glCorpseOwner(corpse, fp))
  var r = glCorpseLoot(fp, corpse)
  console.info('[selftest] corpse: back=' + r.back + ' curios=' + r.curios + ' moved=' + r.moved + ' left=' + r.left)
  check('corpse: sword back in slot 3', String(inv.items.get(3).id) === 'minecraft:diamond_sword')
  check('corpse: bread back in slot 20', String(inv.items.get(20).id) === 'minecraft:bread' && inv.items.get(20).getCount() === 7)
  check('corpse: helmet back on', String(inv.armor.get(3).id) === 'minecraft:iron_helmet')
  check('corpse: shield back in offhand', String(inv.offhand.get(0).id) === 'minecraft:shield')
  var dirt = 0
  for (var j = 0; j < inv.items.size(); j++) if (String(inv.items.get(j).id) === 'minecraft:dirt') dirt += inv.items.get(j).getCount()
  check('corpse: picked-up dirt moved aside, not lost', dirt === 5 && r.moved === 1)
  worn.forEach(function (w) {
    check('corpse: ' + w.id + ' back in ' + w.slot + ' #' + w.i, String(h.getStacksHandler(w.slot).get().getStacks().getStackInSlot(w.i).id) === w.id)
  })
  check('corpse: body empty and removed', corpse.isEmpty() && corpse.isRemoved())
  var other = $Fake.get(server.overworld(), new $Profile($UUID.fromString('00000000-0000-4000-8000-00000000c0b6'), 'gl_corpse_other'))
  check('corpse: someone else is not the owner', !glCorpseOwner(corpse, other))
  inv.clearContent()
  worn.forEach(function (w) { h.getStacksHandler(w.slot).get().getStacks().setStackInSlot(w.i, $ItemStack.EMPTY) })
  glCorpseStore(server).remove(String(fp.getUuid()))

  // Full pack: what can't fit stays in the body, nothing is lost.
  inv.items.set(5, Item.of('minecraft:golden_sword'))
  var death2 = $Death.fromPlayer(fp)
  inv.clearContent()
  for (var f = 0; f < inv.items.size(); f++) inv.items.set(f, Item.of('minecraft:cobblestone', 64))
  var corpse2 = $Corpse.createFromDeath(fp, death2)
  var r2 = glCorpseLoot(fp, corpse2)
  var kept = death2.getAdditionalItems()
  check('corpse: full pack keeps the item in the body', r2.left === 1 && !corpse2.isRemoved() && kept.size() === 1 && String(kept.get(0).id) === 'minecraft:golden_sword')
  inv.clearContent()

  // A body with no death note (died before this script): curios are worn wherever they fit.
  var death3 = $Death.fromPlayer(fp)
  death3.getAdditionalItems().add(Item.of('artifacts:cross_necklace'))
  var r3 = glCorpseLoot(fp, $Corpse.createFromDeath(fp, death3))
  check('corpse: no note -> necklace worn anyway', r3.curios === 1 && String(h.getStacksHandler('necklace').get().getStacks().getStackInSlot(0).id) === 'artifacts:cross_necklace')
  // Clean up the fake player and its notes.
  inv.clearContent()
  h.getStacksHandler('necklace').get().getStacks().setStackInSlot(0, $ItemStack.EMPTY)
  glCorpseStore(server).remove(String(fp.getUuid()))
}
