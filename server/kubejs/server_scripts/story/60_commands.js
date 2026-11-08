// ============================================================================
//  /gl commands (see docs/CONTRACT.md)
//    /gl class join <player> <id>     op/quest
//    /gl trial begin <player> <id>    op/quest
//    /gl lore <player> <entry>        op/quest
//    /gl choose <n>                   any player (answers the ring trial)
//    /gl status                       any player (your classes, levels, ring, story)
// ============================================================================

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands, Arguments = event.arguments
  var op = function (s) { return s.hasPermission(2) }

  var classJoin = Commands.literal('join').then(Commands.argument('player', Arguments.PLAYER.create(event))
    .then(Commands.argument('id', Arguments.WORD.create(event)).executes(function (ctx) {
      return glClassJoin(ctx.source.getServer(), Arguments.PLAYER.getResult(ctx, 'player'), String(Arguments.WORD.getResult(ctx, 'id')))
    })))
  var trialBegin = Commands.literal('begin').then(Commands.argument('player', Arguments.PLAYER.create(event))
    .then(Commands.argument('id', Arguments.WORD.create(event)).executes(function (ctx) {
      return glTrialBegin(ctx.source.getServer(), Arguments.PLAYER.getResult(ctx, 'player'), String(Arguments.WORD.getResult(ctx, 'id')))
    })))
  var lore = Commands.literal('lore').requires(op).then(Commands.argument('player', Arguments.PLAYER.create(event))
    .then(Commands.argument('entry', Arguments.WORD.create(event)).executes(function (ctx) {
      var p = Arguments.PLAYER.getResult(ctx, 'player'), lines = GL_LORE[String(Arguments.WORD.getResult(ctx, 'entry'))]
      if (!lines) return 0
      glSpeak(ctx.source.getServer(), p, lines, 40)
      return 1
    })))
  var choose = Commands.literal('choose').then(Commands.argument('n', Arguments.INTEGER.create(event)).executes(function (ctx) {
    var p = ctx.source.getPlayer()
    if (!p) return 0
    return glTrialChoose(ctx.source.getServer(), p, Arguments.INTEGER.getResult(ctx, 'n'))
  }))
  var status = Commands.literal('status').executes(function (ctx) {
    var p = ctx.source.getPlayer()
    if (!p) return 0
    glSay(p, '§6§l✦ Your path ✦')
    var any = false
    GL_CLASS_IDS.forEach(function (id) {
      if (!p.stages.has('gl_class_' + id)) return
      any = true
      var c = GL_CLASSES[id], lvl = glClassLevel(p, id)
      var ring = p.stages.has('gl_ring_' + id) ? ' §a[ring]' : (p.stages.has('gl_trialdone_' + id) ? ' §7[judged]' : (p.stages.has('gl_trial_' + id) ? ' §e[trial ready]' : ''))
      glSay(p, c.color + c.name + '§7: level §f' + (lvl < 0 ? '?' : lvl) + ring)
    })
    if (!any) glSay(p, '§7No class yet. Your quest book (§fAct I: Choose Your Light§7) will guide you.')
    if (p.stages.has('gl_ring_white')) glSay(p, '§f§lYou bear the White Light.')
    if (p.stages.has('gl_ring_black')) glSay(p, '§8§lYou bear the Black Light.')
    return 1
  })
  event.register(Commands.literal('gl')
    .then(Commands.literal('class').requires(op).then(classJoin))
    .then(Commands.literal('trial').requires(op).then(trialBegin))
    .then(lore).then(choose).then(status))
})
