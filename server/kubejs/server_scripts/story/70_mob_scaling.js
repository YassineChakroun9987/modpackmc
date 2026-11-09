// ============================================================================
//  Mob scaling: monsters grow with the players near them.
//  A player's POWER LEVEL = the higher of their Adventurer level (0-40) and their best class level
//  (0-50) from the skill trees (not vanilla XP). When a hostile mob spawns, it takes the average power
//  of the players within 64 blocks (or the nearest one within 128) and gets, per power level:
//     +4% max health, +2.5% attack damage, +0.2 armour, +0.08 toughness, +0.4 follow range
//  (power 50: x3 health, x2.25 damage, +10 armour, +4 toughness). From power 1 there's also a chance
//  of an ELITE (0.5% per level, max 25%): another +60% health, +30% damage, faster, and named.
//  Not scaled: bosses (quests/bosses.json), story NPCs/mobs (gl_* tags), named, tamed or summoned mobs,
//  and anything already scaled (tag gl_scaled), so reloading a chunk never stacks it.
//  /gl power shows your power level and the level of the area you're in.
// ============================================================================
var GL_SCALE = { hp: 0.04, dmg: 0.025, armor: 0.2, tough: 0.08, follow: 0.4, eliteHp: 0.6, eliteDmg: 0.3,
                 eliteChancePerLevel: 0.005, eliteChanceMax: 0.25, radius: 64, fallbackRadius: 128 }
var $GLAttrs = Java.loadClass('net.minecraft.world.entity.ai.attributes.Attributes')
var $GLMod = Java.loadClass('net.minecraft.world.entity.ai.attributes.AttributeModifier')
var $GLOp = Java.loadClass('net.minecraft.world.entity.ai.attributes.AttributeModifier$Operation')
var GL_POWER = {}   // player uuid -> power level, refreshed every 5 s

function glPowerLevel(player) {
  var best = Math.max(0, glClassLevel(player, 'adventurer'))
  GL_CLASS_IDS.forEach(function (c) { best = Math.max(best, glClassLevel(player, c)) })
  return best
}

PlayerEvents.tick(function (event) {
  var p = event.player
  if (p.age % 100 === 0 || GL_POWER[String(p.getUuid())] === undefined) GL_POWER[String(p.getUuid())] = glPowerLevel(p)
})

// Average power of the players around a position (null if nobody is near).
function glAreaPower(level, x, y, z) {
  var near = [], nearest = null, nd = Infinity
  var dim = String(level.dimension)
  // server.players + a dimension check (level.players() isn't callable from KubeJS).
  level.getServer().players.forEach(function (p) {
    if (String(p.level.dimension) !== dim) return
    var d = p.distanceToSqr(x, y, z)
    var pw = GL_POWER[String(p.getUuid())]
    if (pw === undefined) pw = glPowerLevel(p)
    if (d <= GL_SCALE.radius * GL_SCALE.radius) near.push(pw)
    if (d < nd) { nd = d; nearest = pw }
  })
  if (near.length) return near.reduce(function (a, b) { return a + b }, 0) / near.length
  if (nearest !== null && nd <= GL_SCALE.fallbackRadius * GL_SCALE.fallbackRadius) return nearest
  return null
}

function glAddMod(e, attr, id, amount, op) {
  var inst = e.getAttribute(attr)
  if (!inst || amount === 0) return
  var rl = $ResourceLocation.parse('greenlanterns:' + id)
  if (inst.hasModifier(rl)) inst.removeModifier(rl)
  inst.addPermanentModifier(new $GLMod(rl, amount, op))
}

// Apply power level L to a mob. Returns true if it became an elite.
function glApplyMobScale(e, L, forceElite) {
  var MB = $GLOp.ADD_MULTIPLIED_BASE, ADD = $GLOp.ADD_VALUE
  var elite = forceElite === true || (forceElite !== false && Math.random() < Math.min(GL_SCALE.eliteChanceMax, L * GL_SCALE.eliteChancePerLevel))
  glAddMod(e, $GLAttrs.MAX_HEALTH, 'scale_hp', GL_SCALE.hp * L + (elite ? GL_SCALE.eliteHp : 0), MB)
  glAddMod(e, $GLAttrs.ATTACK_DAMAGE, 'scale_dmg', GL_SCALE.dmg * L + (elite ? GL_SCALE.eliteDmg : 0), MB)
  glAddMod(e, $GLAttrs.ARMOR, 'scale_armor', GL_SCALE.armor * L, ADD)
  glAddMod(e, $GLAttrs.ARMOR_TOUGHNESS, 'scale_tough', GL_SCALE.tough * L, ADD)
  glAddMod(e, $GLAttrs.FOLLOW_RANGE, 'scale_follow', GL_SCALE.follow * L, ADD)
  if (elite) glAddMod(e, $GLAttrs.MOVEMENT_SPEED, 'scale_elite_speed', 0.15, MB)
  e.setHealth(e.getMaxHealth())
  e.addTag('gl_scaled')
  if (elite) {
    e.addTag('gl_elite')
    e.setCustomName(Text.of('§6Elite ' + e.getName().getString()))
  }
  return elite
}

function glShouldScale(e) {
  if (!e.isLiving() || e.isPlayer()) return false
  var tags = e.getTags()
  if (tags.contains('gl_scaled')) return false
  var skip = false
  tags.forEach(function (t) { if (String(t).indexOf('gl_') === 0) skip = true })
  if (skip || e.hasCustomName()) return false
  if (String(e.getEntityType().getCategory()) !== 'MONSTER') return false
  if (GL_BOSS_LIST[String(e.type)]) return false
  if (typeof e.getOwner === 'function' && e.getOwner()) return false            // tamed / summoned (TamableAnimal, Iron's summons)
  if (typeof e.getSummoner === 'function' && e.getSummoner()) return false
  return true
}

EntityEvents.spawned(function (event) {
  var e = event.entity
  if (e.level.isClientSide() || !glShouldScale(e)) return
  var L = glAreaPower(e.level, e.getX(), e.getY(), e.getZ())
  if (L === null || L < 1) return   // nobody (or only level-0 players) near: leave it unscaled for now, it's checked again when it next loads
  glApplyMobScale(e, Math.round(L))
})

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl').then(Commands.literal('power').executes(function (ctx) {
    var p = ctx.source.getPlayer()
    if (!p) return 0
    var mine = glPowerLevel(p)
    GL_POWER[String(p.getUuid())] = mine
    var area = glAreaPower(p.level, p.getX(), p.getY(), p.getZ())
    var L = Math.round(area || 0)
    glSay(p, '§6Your power level: §f' + mine + '§7 (your best class or Adventurer level)')
    glSay(p, '§6This area: §f' + L + '§7 → monsters here spawn with §f+' + Math.round(GL_SCALE.hp * L * 100) + '% health§7, §f+' +
      Math.round(GL_SCALE.dmg * L * 100) + '% damage§7, §f+' + (GL_SCALE.armor * L).toFixed(1) + ' armour§7; elite chance §f' +
      Math.round(Math.min(GL_SCALE.eliteChanceMax, L * GL_SCALE.eliteChancePerLevel) * 100) + '%§7.')
    return 1
  })))
})
