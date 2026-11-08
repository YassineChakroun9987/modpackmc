// ============================================================================
//  Story NPCs: the village elder and the dying Lantern at the crash site.
//  Invulnerable, no-AI villagers (nitwits, so they never trade). Right-click
//  to talk. Dialogue changes with the story's progress.
// ============================================================================

function glNpcSummon(server, x, y, z, tag, name, color) {
  glRun(server, 'execute in minecraft:overworld run summon minecraft:villager ' + x + ' ' + y + ' ' + z +
    ' {NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,Tags:["gl_npc","' + tag + '"],' +
    'CustomName:\'{"text":"' + name + '","color":"' + color + '"}\',CustomNameVisible:1b,' +
    'VillagerData:{profession:"minecraft:nitwit",level:1,type:"minecraft:plains"}}')
}

function glNpcSpawnElder(server) {
  var d = glData(server)
  if (d.getBoolean('elderSpawned')) return
  var level = server.overworld()
  var x = d.getInt('vx') + 2, z = d.getInt('vz') + 2
  glNpcSummon(server, x, glSurfaceY(level, x, z), z, 'gl_npc_elder', 'Elder Maren', 'gold')
  d.putBoolean('elderSpawned', true)
}

function glNpcSpawnLantern(server, x, y, z) {
  glNpcSummon(server, x, y, z, 'gl_npc_lantern', 'Kaelen, Lantern of Sector 2814', 'green')
  glRun(server, 'team add gl_lantern')
  glRun(server, 'team modify gl_lantern color green')
  glRun(server, 'execute in minecraft:overworld run team join gl_lantern @e[tag=gl_npc_lantern]')
  glRun(server, 'execute in minecraft:overworld run effect give @e[tag=gl_npc_lantern] minecraft:glowing infinite 0 true')
}

// The elder spawns as soon as a player is at the village (its chunk is loaded then).
PlayerEvents.loggedIn(function (event) {
  event.server.scheduleInTicks(40, function () { glNpcSpawnElder(event.server) })
})

var GL_TALKING = {}

ItemEvents.entityInteracted(function (event) {
  var t = event.target
  if (!t || !t.getTags || !t.getTags().contains('gl_npc')) return
  event.cancel()
  if (String(event.hand) !== 'MAIN_HAND') return
  var player = event.player, server = event.server
  var key = player.username
  if (GL_TALKING[key] && GL_TALKING[key] > server.tickCount) return
  var d = glData(server)
  var lines
  if (t.getTags().contains('gl_npc_elder')) {
    if (!d.getBoolean('raidTriggered')) {
      var left = Math.max(0, Math.ceil(glRaidLeft(d) / GL_DAY))
      lines = [
        '§6Elder Maren:§f "' + left + ' day' + (left === 1 ? '' : 's') + ' until they come. Every hour counts."',
        '§6"Light the village at night. Give our folk §fswords§6. Guards defend their homes, and a §fhired spear§6 is worth two farmers."',
        '§6"And find the Warband\'s camp. Their leader, §cWarlord Vex§6, rides with them. Cut off the head, and the body falls."',
        '§7(Tip: §fGuard Villagers§7: right-click a villager with a sword or crossbow to make them a guard.)'
      ]
    } else if (!d.getBoolean('warlordSlain')) {
      lines = ['§6Elder Maren:§f "Hold the walls! And if you can... end Vex. His camp is on the ridge."']
    } else if (!d.getBoolean('crashPlaced')) {
      lines = ['§6Elder Maren:§f "You did it. Rest, hero... the sky has been strange tonight."']
    } else {
      lines = [
        '§6Elder Maren:§f "That green star... it came down in the hills. People say a man walked out of the fire."',
        '§6"Whatever you are now, you\'re one of us. Go. Find out what fell from the sky."'
      ]
    }
  } else {
    if (!player.stages.has('gl_lantern_heard')) {
      lines = [
        '§2Kaelen:§a "...You. You\'re the one who held the village. Come closer. I don\'t have long."',
        '§a"I am a Green Lantern, of a Corps that keeps the peace between the stars. We were losing a war."',
        '§a"A §5corruption§a is spreading through the universe. The dead rise. Beasts twist. Whole worlds go dark."',
        '§a"It followed me here. To your world. Its creatures are already waking: in dungeons, in the deep places, in the sky."',
        '§a"Seven lights stand against it: §cRed§a, §6Orange§a, §eYellow§a, §2Green§a, §bBlue§a, §9Indigo§a, §dViolet§a. Each chooses its own."',
        '§a"Walk the path of a light. Grow. Prove yourself against the beasts the dark has claimed. And when you\'re ready..."',
        '§a"...a ring will judge you. Not by your strength. By your §fchoices§a."',
        '§2§oKaelen\'s ring rises from his hand, hovers... and streaks into the sky, searching.§r§a "Not you. Not yet. But maybe... soon."',
        '§e✦ The Lantern\'s tale is told. Your quest book has new pages: §6Act I: Proving Ground§e.'
      ]
      server.scheduleInTicks(lines.length * 60, function () {
        glGiveStage(player, 'gl_lantern_heard')
        glGiveStage(player, 'gl_crash_seen')
      })
    } else {
      lines = ['§2Kaelen:§a "The light is watching you. Make it proud... or make it afraid."']
    }
  }
  GL_TALKING[key] = server.tickCount + glSpeak(server, player, lines, 60)
})
