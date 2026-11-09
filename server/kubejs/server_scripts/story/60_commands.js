// ============================================================================
//  /gl commands (see docs/CONTRACT.md)
//    /gl class join <player> <id>     op/quest
//    /gl trial begin <player> <id>    op/quest
//    /gl lore <player> <entry>        op/quest
//    /gl choose <n>                   any player (answers the ring trial)
//    /gl status                       any player (your classes, levels, ring, story)
//    /gl raid now                     op: end the 7-day countdown (the raid starts when someone is in the village)
//    /gl raid days <n>                op: set the countdown to n days
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
  // Debug: skip or shorten the Warband countdown. The normal prologue tick still starts the raid
  // (when a player is within 96 blocks of the village), so this tests the real trigger.
  var raidSet = function (ctx, daysLeft) {
    var server = ctx.source.getServer(), d = glData(server)
    var say = function (t) { ctx.source.sendSystemMessage(Text.of(t)) }
    if (!d.getBoolean('init')) { say("§cThe prologue hasn't started yet: someone has to log in first."); return 0 }
    if (d.getBoolean('raidTriggered')) { say('§eThe raid has already started.'); return 0 }
    d.putLong('raidElapsed', Math.max(0, GL_RAID_DAYS * GL_DAY - daysLeft * GL_DAY))
    say(daysLeft > 0 ? '§aWarband countdown set to §f' + daysLeft + '§a day(s).'
                     : '§aCountdown ended. §7The raid starts as soon as someone is within 96 blocks of the village (' + d.getInt('vx') + ', ' + d.getInt('vz') + ').')
    return 1
  }
  var raid = Commands.literal('raid').requires(op)
    .then(Commands.literal('now').executes(function (ctx) { return raidSet(ctx, 0) }))
    .then(Commands.literal('days').then(Commands.argument('n', Arguments.INTEGER.create(event))
      .executes(function (ctx) { return raidSet(ctx, Math.max(0, Math.min(GL_RAID_DAYS, Arguments.INTEGER.getResult(ctx, 'n')))) })))

  event.register(Commands.literal('gl')
    .then(raid)
    .then(Commands.literal('class').requires(op).then(classJoin))
    .then(Commands.literal('trial').requires(op).then(trialBegin))
    .then(lore).then(choose).then(status))
})
