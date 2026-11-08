// ============================================================================
//  Prologue: The Seventh Dawn
//  First login places an outpost near the spawn village, posts the Warlord,
//  and starts a 7-day boss-bar countdown. On day 7 the Warband raids the
//  village. Killing Warlord Vex brings down a Lantern ship nearby.
//  Late joiners are caught up automatically.
// ============================================================================

var GL_DAY = 24000
var GL_RAID_DAYS = 7
var GL_OUTPOST_DIST = 190
var GL_CRASH_DIST = 70

function glPrologueInit(server) {
  var d = glData(server)
  if (d.getBoolean('init')) return
  var level = server.overworld()
  var spawn = level.getSharedSpawnPos()
  var vx = spawn.getX(), vz = spawn.getZ()
  d.putInt('vx', vx); d.putInt('vz', vz); d.putInt('vy', spawn.getY())
  // The outpost goes on a ridge to the north-east, the crash site to the south-west.
  var ox = vx + Math.round(GL_OUTPOST_DIST * 0.7), oz = vz - Math.round(GL_OUTPOST_DIST * 0.7)
  var cx = vx - Math.round(GL_CRASH_DIST * 0.7), cz = vz + Math.round(GL_CRASH_DIST * 0.7)
  d.putInt('ox', ox); d.putInt('oz', oz); d.putInt('cx', cx); d.putInt('cz', cz)
  glRun(server, 'execute in minecraft:overworld run forceload add ' + (ox - 32) + ' ' + (oz - 32) + ' ' + (ox + 32) + ' ' + (oz + 32))
  glEnsureChunks(level, ox, oz, 3)
  glRun(server, 'execute in minecraft:overworld run place structure minecraft:pillager_outpost ' + ox + ' 64 ' + oz)
  var oy = glSurfaceY(level, ox + 3, oz + 3)
  d.putInt('oy', oy)
  glRun(server, 'execute in minecraft:overworld run summon minecraft:pillager ' + (ox + 3) + ' ' + (oy + 1) + ' ' + (oz + 3) +
    ' {CustomName:\'{"text":"Warlord Vex","color":"dark_red","bold":true}\',CustomNameVisible:1b,PersistenceRequired:1b,Tags:["gl_warlord"],' +
    'attributes:[{id:"minecraft:generic.max_health",base:300.0d},{id:"minecraft:generic.armor",base:10.0d},{id:"minecraft:generic.attack_damage",base:9.0d},{id:"minecraft:generic.follow_range",base:40.0d}],Health:300.0f,' +
    'HandItems:[{id:"minecraft:crossbow",count:1},{}],ArmorItems:[{id:"minecraft:iron_boots",count:1},{id:"minecraft:iron_leggings",count:1},{id:"minecraft:iron_chestplate",count:1},{id:"minecraft:iron_helmet",count:1}]}')
  glRun(server, 'execute in minecraft:overworld run forceload remove ' + (ox - 32) + ' ' + (oz - 32) + ' ' + (ox + 32) + ' ' + (oz + 32))
  d.putLong('raidStart', glGameTime(level))
  d.putBoolean('init', true)
  glRun(server, 'bossbar add gl:warband {"text":"The Warband marches in 7 days","color":"red"}')
  glRun(server, 'bossbar set gl:warband color red')
  glRun(server, 'bossbar set gl:warband max ' + (GL_RAID_DAYS * GL_DAY))
  glRun(server, 'bossbar add gl:warlord {"text":"Warlord Vex","color":"dark_red"}')
  glRun(server, 'bossbar set gl:warlord color red')
  glRun(server, 'bossbar set gl:warlord max 300')
  console.info('[gl] prologue initialised: village ' + vx + ',' + vz + ' outpost ' + ox + ',' + oy + ',' + oz + ' crash ' + cx + ',' + cz)
}

function glDirection(fromX, fromZ, toX, toZ) {
  var dx = toX - fromX, dz = toZ - fromZ
  var ns = dz < -20 ? 'north' : (dz > 20 ? 'south' : '')
  var ew = dx > 20 ? 'east' : (dx < -20 ? 'west' : '')
  return (ns + (ns && ew ? '-' : '') + ew) || 'nearby'
}

PlayerEvents.loggedIn(function (event) {
  var player = event.player, server = event.server
  glPrologueInit(server)
  var d = glData(server)
  if (glGiveStage(player, 'gl_started')) {
    glRun(server, 'give ' + player.username + ' ftbquests:book')
    var dir = glDirection(d.getInt('vx'), d.getInt('vz'), d.getInt('ox'), d.getInt('oz'))
    glSpeak(server, player, [
      '§7§o...You wake to the smell of woodsmoke and the sound of a horn.',
      '§6An old voice:§f "Easy, traveller. You\'re safe, for now. This village took you in."',
      '§6"But listen. That horn came from the ridge to the §c' + dir + '§6. A §cpillager warband§6 has made camp there."',
      '§6"Their scouts say they march in §cseven days§6. We have no soldiers. Only farmers... and now you."',
      '§e✦ Open your quest book (§fthe book in your inventory§e, or the quest key) to begin: §6The Seventh Dawn§e.'
    ], 50)
  }
  // Late joiners: catch them up on story beats the server has already lived through.
  if (d.getBoolean('raidWon') && glGiveStage(player, 'gl_raid_won'))
    glSay(player, '§7§oThe village is scarred but standing. The Warband\'s raid was beaten back before you arrived.')
  if (d.getBoolean('warlordSlain') && glGiveStage(player, 'gl_warlord_slain'))
    glSay(player, '§7§oVillagers still talk about the night Warlord Vex fell.')
})

// Countdown, raid trigger, Warlord health bar, crash-site and hero detection. Once a second.
ServerEvents.tick(function (event) {
  var server = event.server
  if (server.tickCount % 20 !== 0) return
  var d = glData(server)
  if (!d.getBoolean('init')) return
  var level = server.overworld()
  var now = glGameTime(level)

  if (!d.getBoolean('raidTriggered')) {
    var left = d.getLong('raidStart') + GL_RAID_DAYS * GL_DAY - now
    if (left > 0) {
      var days = Math.ceil(left / GL_DAY)
      glRun(server, 'bossbar set gl:warband value ' + Math.max(0, Math.floor(left)))
      glRun(server, 'bossbar set gl:warband name {"text":"⚔ The Warband marches in ' + days + ' day' + (days === 1 ? '' : 's') + '","color":"red"}')
      glRun(server, 'bossbar set gl:warband players @a')
      glRun(server, 'bossbar set gl:warband visible true')
    } else {
      // Day seven: the raid starts as soon as someone is in the village to see it.
      var vx = d.getInt('vx'), vz = d.getInt('vz'), vy = glSurfaceY(level, vx, vz)
      var trigger = null
      server.players.forEach(function (p) {
        if (!trigger && String(p.level.dimension) === 'minecraft:overworld' && p.distanceToSqr(vx, vy, vz) < 96 * 96) trigger = p
      })
      glRun(server, 'bossbar set gl:warband name {"text":"⚔ The Warband is at the gates!","color":"dark_red"}')
      if (trigger) {
        trigger.setRaidOmenPosition(new $BlockPos(vx, vy, vz))
        glRun(server, 'effect give ' + trigger.username + ' minecraft:raid_omen 3 1 true')
        d.putBoolean('raidTriggered', true)
        glRun(server, 'bossbar set gl:warband visible false')
        glSayAll(server, '§4§l⚔ The Warband has come! §cDefend the village!')
      }
    }
  }

  // Warlord Vex's health bar, shown to anyone near him.
  if (!d.getBoolean('warlordSlain')) {
    glRun(server, 'execute in minecraft:overworld store result bossbar gl:warlord value run data get entity @e[tag=gl_warlord,limit=1] Health')
    glRun(server, 'bossbar set gl:warlord players')
    glRun(server, 'execute in minecraft:overworld at @e[tag=gl_warlord,limit=1] run bossbar set gl:warlord players @a[distance=..48]')
  }

  server.players.forEach(function (p) {
    // Won the raid: vanilla gives Hero of the Village.
    if (!p.stages.has('gl_raid_won') && p.hasEffect($MobEffects.HERO_OF_THE_VILLAGE)) {
      p.stages.add('gl_raid_won'); d.putBoolean('raidWon', true)
      glSay(p, '§a§l✔ The village is saved! §7The villagers will remember this.')
    }
    // Reached the crashed Lantern ship.
    if (d.getBoolean('crashPlaced') && !p.stages.has('gl_crash_seen') && String(p.level.dimension) === 'minecraft:overworld' &&
        p.distanceToSqr(d.getInt('cx'), d.getInt('cy'), d.getInt('cz')) < 20 * 20) {
      p.stages.add('gl_crash_seen')
      glSay(p, '§a§o The wreck still glows. Someone is moving inside it...§7 (right-click the wounded Lantern)')
    }
  })
})

// Warlord Vex falls: party credit, then a green star falls from the sky.
function glWarlordSlain(entity) {
  var server = entity.server, d = glData(server)
  glNearbyPlayers(entity).forEach(function (p) { glGiveStage(p, 'gl_warlord_slain', '§6§l✔ Warlord Vex is dead. §7The Warband scatters.') })
  if (d.getBoolean('warlordSlain')) return
  d.putBoolean('warlordSlain', true)
  glRun(server, 'bossbar remove gl:warlord')
  glRun(server, 'bossbar remove gl:warband')
  server.scheduleInTicks(200, function () { glCrash(server) })
}

function glCrash(server) {
  var d = glData(server)
  if (d.getBoolean('crashPlaced')) return
  var level = server.overworld()
  var cx = d.getInt('cx'), cz = d.getInt('cz')
  glRun(server, 'execute in minecraft:overworld run forceload add ' + (cx - 16) + ' ' + (cz - 16) + ' ' + (cx + 16) + ' ' + (cz + 16))
  glEnsureChunks(level, cx, cz, 2)
  var cy = glSurfaceY(level, cx, cz)
  glRun(server, 'execute in minecraft:overworld run place template createlanterns:oa/crashed_lantern_ship ' + cx + ' ' + (cy - 2) + ' ' + cz)
  d.putInt('cy', cy); d.putBoolean('crashPlaced', true)
  glNpcSpawnLantern(server, cx + 2, cy + 1, cz + 2)
  glRun(server, 'execute in minecraft:overworld run forceload remove ' + (cx - 16) + ' ' + (cz - 16) + ' ' + (cx + 16) + ' ' + (cz + 16))
  var dir = glDirection(d.getInt('vx'), d.getInt('vz'), cx, cz)
  server.players.forEach(function (p) {
    glRun(server, 'execute at ' + p.username + ' run playsound minecraft:entity.generic.explode ambient ' + p.username + ' ~ ~ ~ 0.6 0.5')
  })
  glSayAll(server, '§a§l✦ A green star falls from the sky!§r§a It crashes into the hills to the §2' + dir + '§a of the village (§2' + cx + ', ' + cz + '§a).')
}

EntityEvents.death(function (event) {
  var e = event.entity
  if (e.getTags().contains('gl_warlord')) glWarlordSlain(e)
})
