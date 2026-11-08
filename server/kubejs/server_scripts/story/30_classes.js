// ============================================================================
//  Classes: joining a light, and the light noticing you as you grow.
//  /gl class join <player> <id>  (from the class quest's reward)
//    -> unlocks Pufferfish's Skills category greenlanterns:<id>, stage gl_class_<id>
//  Every 5 s: class level 10 -> the light whispers (gl_whisper_<id>),
//             class level 25 -> you dream of it (gl_dream_<id>).
//  The whisper and dream lines are Create: Lanterns' own text.
// ============================================================================

function glClassJoin(server, player, id) {
  var c = GL_CLASSES[id]
  if (!c) return 0
  glRun(server, 'puffish_skills category unlock ' + player.username + ' greenlanterns:' + id)
  if (!glGiveStage(player, 'gl_class_' + id)) {
    glSay(player, c.color + 'You already walk the path of the ' + c.name + '.')
    return 1
  }
  glSpeak(server, player, [
    c.color + '§l✦ You walk the path of the ' + c.name + ' ✦',
    '§7§o' + c.motto,
    '§7Your §f' + c.name + '§7 talent tree is open: press §f[K]§7 (Pufferfish\'s Skills) to spend points.',
    '§7Grow by doing what a ' + c.name + ' does. At class level §f10§7 the light will notice you... at §f25§7 you will dream of it.',
    '§7When you are ready, face §f' + c.bossName + '§7. The ring will judge you after.'
  ], 40)
  return 1
}

ServerEvents.tick(function (event) {
  var server = event.server
  if (server.tickCount % 100 !== 50) return
  server.players.forEach(function (p) {
    GL_CLASS_IDS.forEach(function (id) {
      if (!p.stages.has('gl_class_' + id)) return
      var lvl = glClassLevel(p, id)
      if (lvl < 0) return
      var c = GL_CLASSES[id]
      if (lvl >= 10 && glGiveStage(p, 'gl_whisper_' + id)) {
        p.tell(Text.of(c.color + '✦ ').append(Text.translatable('calling.createlanterns.whisper.' + c.light).italic()))
        glRun(server, 'execute at ' + p.username + ' run playsound minecraft:block.amethyst_block.chime master ' + p.username + ' ~ ~ ~ 0.8 0.7')
      }
      if (lvl >= 25 && glGiveStage(p, 'gl_dream_' + id)) {
        p.tell(Text.of(c.color + '☾ ').append(Text.translatable('calling.createlanterns.dream.' + c.light).italic()))
        glSay(p, '§7§oThe dream fades, but the feeling stays. You are almost ready for ' + c.bossName + '.')
      }
    })
  })
})
