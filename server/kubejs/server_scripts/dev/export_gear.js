// Dev: /gl_dev exportgear (op only) -> kubejs/exported/gear.json
// Every armour piece and weapon in the pack with its real stats, read from the game itself:
// attribute modifiers (after every mod's hooks), durability, enchantability, armour slot and
// material, Better Combat moveset (category, two-handed, reach). tools/gear_doc.js turns it into
// docs/Green-Lanterns-Armour-and-Weapons.docx. Skips items hidden from JEI (c:hidden_from_recipe_viewers).
var $GearReg = Java.loadClass('net.minecraft.core.registries.Registries')
var $GearTagKey = Java.loadClass('net.minecraft.tags.TagKey')
var $ArmorItem = Java.loadClass('net.minecraft.world.item.ArmorItem')
var $ProjectileWeaponItem = Java.loadClass('net.minecraft.world.item.ProjectileWeaponItem')
var $TridentItem = Java.loadClass('net.minecraft.world.item.TridentItem')
var $MaceItem = Java.loadClass('net.minecraft.world.item.MaceItem')
var $ShieldItem = Java.loadClass('net.minecraft.world.item.ShieldItem')
var $BCWeapons = null
try { $BCWeapons = Java.loadClass('net.bettercombat.logic.WeaponRegistry') } catch (e) { console.warn('[gl_dev exportgear] Better Combat registry not available: ' + e) }

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('exportgear').executes(function (ctx) {
      var server = ctx.source.getServer()
      // Run on the next tick: errors there are logged with a full stack trace.
      server.scheduleInTicks(1, function () { glExportGear(server) })
      return 1
    })))
})

// The item ids in a tag, as a JS set (ItemStack.is(...) is overloaded and Rhino can't pick one).
function glGearTag(reg, id) {
  var set = {}
  var opt = reg.getTag($GearTagKey.create($GearReg.ITEM, $ResourceLocation.parse(id)))
  if (opt.isPresent()) {
    var it = opt.get().iterator()
    while (it.hasNext()) set[String(it.next().unwrapKey().get().location())] = true
  }
  return set
}

function glExportGear(server) {
  var reg = server.registryAccess().registryOrThrow($GearReg.ITEM)
  var T = {
    hidden: glGearTag(reg, 'c:hidden_from_recipe_viewers'), swords: glGearTag(reg, 'minecraft:swords'), axes: glGearTag(reg, 'minecraft:axes'),
    pickaxes: glGearTag(reg, 'minecraft:pickaxes'), shovels: glGearTag(reg, 'minecraft:shovels'), hoes: glGearTag(reg, 'minecraft:hoes'),
    melee: glGearTag(reg, 'c:tools/melee_weapon'), ranged: glGearTag(reg, 'c:tools/ranged_weapon'),
  }
  var out = [], skipped = 0, bcHits = 0
  reg.keySet().forEach(function (key) {
    var id = String(key)
    var item = reg.get(key)
    var stack = item.getDefaultInstance()
    if (!!T.hidden[id] || /(^|[_:])(debug|creative|example|test)([_]|$)/.test(id)) { skipped++; return }
    var mods = []
    try {
      stack.getAttributeModifiers().modifiers().forEach(function (e) {
        var a = e.attribute().unwrapKey()
        mods.push({
          attr: a.isPresent() ? String(a.get().location()) : '?',
          amount: Number(e.modifier().amount()),
          op: String(e.modifier().operation()),
          slot: String(e.slot()),
        })
      })
    } catch (err) { /* items without modifiers */ }
    var isArmor = item instanceof $ArmorItem
    var isRanged = item instanceof $ProjectileWeaponItem || !!T.ranged[id]
    var isShield = item instanceof $ShieldItem
    var hasDamage = mods.some(function (m) { return m.attr === 'minecraft:generic.attack_damage' && m.amount > 0 })
    var isTool = (!!T.pickaxes[id] || !!T.shovels[id] || !!T.hoes[id]) && !T.swords[id]
    var isMelee = !isArmor && !isTool && (hasDamage || !!T.swords[id] || !!T.melee[id] || item instanceof $TridentItem || item instanceof $MaceItem)
    if (!isArmor && !isMelee && !isRanged && !isShield) return
    var e = {
      id: id, kind: isArmor ? 'armor' : isShield ? 'shield' : isRanged && !hasDamage ? 'ranged' : 'melee',
      durability: stack.getMaxDamage(), enchantability: Number(stack.getEnchantmentValue()),
      rarity: String(stack.getRarity()), mods: mods,
      tags: { sword: !!T.swords[id], axe: !!T.axes[id] },
      trident: item instanceof $TridentItem, mace: item instanceof $MaceItem,
    }
    if (isArmor) {
      e.slot = String(item.getType())
      try { e.material = String(item.getMaterial().unwrapKey().get().location()) } catch (err) { e.material = '?' }
    }
    if ($BCWeapons && !isArmor) {
      try {
        var wa = $BCWeapons.getAttributes(stack)
        if (wa) {
          bcHits++
          e.bc = { category: String(wa.category() || ''), twoHanded: !!wa.isTwoHanded(), range: Number(wa.attackRange()) }
        }
      } catch (err) { /* not a Better Combat weapon */ }
    }
    out.push(e)
  })
  JsonIO.write('kubejs/exported/gear.json', { gear: out })
  var n = { armor: 0, melee: 0, ranged: 0, shield: 0 }
  out.forEach(function (e) { n[e.kind]++ })
  console.info('[gl_dev exportgear] armor=' + n.armor + ' melee=' + n.melee + ' ranged=' + n.ranged + ' shields=' + n.shield +
    ' (Better Combat movesets: ' + bcHits + ', hidden/dev items skipped: ' + skipped + ')')
}
