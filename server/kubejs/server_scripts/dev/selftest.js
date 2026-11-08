// Dev tool: /gl_dev selftest  (op only). Exercises the story engine without a player:
// IDs, skill categories, ring-trial scoring, and the real world placement of
// the outpost, Warlord Vex, the crash site and the NPCs. Results go to the console.
ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('selftest').executes(function (ctx) {
      var server = ctx.source.getServer(), ok = 0, bad = 0
      function check(name, cond) { if (cond) { ok++ } else { bad++; console.error('[selftest] FAIL ' + name) } }
      var reg = server.registryAccess()
      var $Reg = Java.loadClass('net.minecraft.core.registries.Registries')
      var ents = reg.registryOrThrow($Reg.ENTITY_TYPE), items = reg.registryOrThrow($Reg.ITEM)
      GL_CLASS_IDS.forEach(function (id) {
        var c = GL_CLASSES[id]
        check(id + ' ring item ' + c.ring, items.containsKey($ResourceLocation.parse(c.ring)))
        check(id + ' trial boss ' + c.boss, ents.containsKey($ResourceLocation.parse(c.boss)))
        var cat = $SkillsAPI ? $SkillsAPI.getCategory($ResourceLocation.parse('greenlanterns:' + id)) : null
        check(id + ' skill category greenlanterns:' + id, cat && cat.isPresent())
      })
      check('white ring', items.containsKey($ResourceLocation.parse('createlanterns:white_power_ring')))
      check('black ring', items.containsKey($ResourceLocation.parse('createlanterns:black_power_ring')))
      check('adventurer category', $SkillsAPI && $SkillsAPI.getCategory($ResourceLocation.parse('greenlanterns:adventurer')).isPresent())
      // Ring-trial scoring: every 4-answer combination
      var counts = { white: 0, black: 0, own: 0 }
      for (var a = 0; a < 81; a++) {
        var life = 0, death = 0, x = a
        for (var q = 0; q < 4; q++) { var k = x % 3; x = Math.floor(x / 3); if (k === 0) life++; if (k === 2) death++ }
        var o = glTrialOutcome(life, death, 'red')
        if (o === 'white') counts.white++; else if (o === 'black') counts.black++; else counts.own++
      }
      console.info('[selftest] trial outcomes over all 81 answer paths: own=' + counts.own + ' white=' + counts.white + ' black=' + counts.black)
      check('trial outcomes balanced', counts.own > counts.white && counts.white === counts.black && counts.white > 0)
      // World placement (prologue + crash), as if the first player had logged in and Vex had died
      try {
      glPrologueInit(server)
      var d = glData(server)
      check('prologue init', d.getBoolean('init'))
      var ox = d.getInt('ox'), oz = d.getInt('oz')
      glRun(server, 'execute in minecraft:overworld run forceload add ' + (ox - 8) + ' ' + (oz - 8) + ' ' + (ox + 8) + ' ' + (oz + 8))
      check('outpost ground height found', d.getInt('oy') > 0)
      glCrash(server)
      check('crash placed', d.getBoolean('crashPlaced'))
      var cx = d.getInt('cx'), cz = d.getInt('cz')
      glRun(server, 'execute in minecraft:overworld run forceload add ' + (cx - 8) + ' ' + (cz - 8) + ' ' + (cx + 8) + ' ' + (cz + 8))
      // Entities in freshly loaded chunks appear a moment later: check after 5 s.
      server.scheduleInTicks(100, function () {
        console.info('[selftest] (delayed) Warlord Vex present: ' + glCountTagged(server.overworld(), 'gl_warlord'))
        console.info('[selftest] (delayed) dying Lantern NPC present: ' + glCountTagged(server.overworld(), 'gl_npc_lantern'))
        console.info('[selftest] (delayed) elder present: ' + glCountTagged(server.overworld(), 'gl_npc_elder'))
      })
      glNpcSpawnElder(server)
      check('elder spawned', d.getBoolean('elderSpawned'))
      console.info('[selftest] village ' + d.getInt('vx') + ',' + d.getInt('vz') + ' outpost ' + ox + ',' + d.getInt('oy') + ',' + oz + ' crash ' + cx + ',' + d.getInt('cy') + ',' + cz)
      } catch (err) { bad++; console.error('[selftest] world placement threw: ' + err); if (err.javaException) console.error('[selftest]   ' + err.javaException) }
      console.info('[selftest] DONE: ' + ok + ' passed, ' + bad + ' failed')
      return bad === 0 ? 1 : 0
    })))
})
