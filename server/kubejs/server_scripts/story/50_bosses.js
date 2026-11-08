// ============================================================================
//  Boss hooks: trial-boss credit (party-wide, class-gated), the end-game
//  chain (Chaos Guardian -> Devourer of Gods) and lore announcements.
// ============================================================================

var GL_TRIAL_BOSSES = {}
GL_CLASS_IDS.forEach(function (id) { GL_TRIAL_BOSSES[GL_CLASSES[id].boss] = id })

EntityEvents.death(function (event) {
  var e = event.entity
  var type = String(e.type)
  var cls = GL_TRIAL_BOSSES[type]
  if (cls) {
    var c = GL_CLASSES[cls]
    glNearbyPlayers(e).forEach(function (p) {
      if (p.stages.has('gl_class_' + cls) && glGiveStage(p, 'gl_trial_' + cls))
        glSay(p, c.color + '§l✦ ' + c.bossName.charAt(0).toUpperCase() + c.bossName.slice(1) + ' has fallen. §r§7The ' + c.light + ' light saw it. §eOpen your quest book: the ring trial awaits.')
    })
  }
  if (type === 'draconicevolution:draconic_guardian') {
    glNearbyPlayers(e).forEach(function (p) { glGiveStage(p, 'gl_chaos_slain', '§5§l✦ The Chaos Guardian is broken. §r§7Its shards hum with something older than chaos.') })
  }
  if (type === 'dog:devourer_head') {
    glNearbyPlayers(e).forEach(function (p) { glGiveStage(p, 'gl_devourer_slain') })
    glSayAll(e.server, '§6§l✦✦✦ THE DEVOURER OF GODS HAS FALLEN ✦✦✦')
    glSayAll(e.server, '§e§oAcross the stars, every lantern burns a little brighter. The corruption that hunted the universe has lost its master.')
  }
})

var GL_LORE = {
  crash: ['§2§lThe Fallen Lantern', '§aKaelen of Sector 2814 crashed here, chased across the stars by the corruption.', '§aHis ring left to find someone worthy. The seven lights will each choose their own.'],
  oa: ['§2§lOa', '§aThe homeworld of the Guardians, at the centre of the universe. Its Central Power Battery charges every green lantern.', '§aCreate: Lanterns lets you reach it, and Korugar, by ship (Create Aeronautics).'],
  corruption: ['§5§lThe Corruption', '§dNo one knows where it started. It wakes the dead, twists beasts, and swallows worlds.', '§dThe bosses of this world are its chosen. Every one you defeat weakens its hold.'],
  devourer: ['§6§lThe Devourer of Gods', '§eA cosmic worm that eats gods and stars. It has tasted the Ender Dragon and liked it.', '§eSummon it with a §fCosmic Worm§e, and only when every light you have is ready.']
}
