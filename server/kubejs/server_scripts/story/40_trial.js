// ============================================================================
//  The ring trial: after the class trial boss falls, the ring judges you.
//  /gl trial begin <player> <id>  (from the <id>:choice quest's reward)
//  Four questions in chat. Each answer leans toward:
//    self  - your own light        -> your class ring
//    life  - mercy, sacrifice      -> 3+ of 4: the WHITE ring
//    death - power at any cost     -> 3+ of 4: the BLACK ring
//  Players click an answer, which runs /gl choose <n>.
// ============================================================================

var GL_QUESTIONS = [
  { q: 'The ring hangs in the air before you, humming. It asks: §fwhy do you fight?§7',
    a: [ ['life',  'To protect those who cannot protect themselves.'],
         ['self',  'Because the {LIGHT} light burns in me. It is who I am.'],
         ['death', 'To become so strong that nothing can ever hurt me again.'] ] },
  { q: 'A vision: {BOSS} lies broken at your feet, and its last servants are fleeing into the dark. §fWhat do you do?§7',
    a: [ ['death', 'Hunt them all down. Fear is the only lesson they understand.'],
         ['life',  'Let them go. Mercy is a kind of strength.'],
         ['self',  'Finish what I started, the way a {CLASS} would.'] ] },
  { q: 'A friend lies dying beside you. The ring offers to save them, but it will cost the ring its light. §fDo you accept?§7',
    a: [ ['self',  'I will find another way. I will not give up my light.'],
         ['death', 'Let them fall. Their death will make me harder.'],
         ['life',  'Yes. A life is worth more than any ring.'] ] },
  { q: 'Something in the dark whispers: §5"Join us, and you will never die."§7 §fHow do you answer?§7',
    a: [ ['life',  'Life is precious because it ends.'],
         ['death', '...Tell me more.'],
         ['self',  'My light answers for me.'] ] }
]

function glFill(text, c) {
  return text.replace('{LIGHT}', c.light).replace('{CLASS}', c.name).replace('{BOSS}', c.bossName)
}

function glTrialAsk(player, st) {
  var c = GL_CLASSES[st.getString('cls')]
  var qi = st.getInt('q'), Q = GL_QUESTIONS[qi]
  glSay(player, ' ')
  glSay(player, c.color + '§l✦ The Ring Trial §r§8(' + (qi + 1) + '/' + GL_QUESTIONS.length + ')')
  glSay(player, '§7' + glFill(Q.q, c))
  for (var i = 0; i < Q.a.length; i++) {
    player.tell(Text.of('  §e[' + (i + 1) + ']§r ' + glFill(Q.a[i][1], c))
      .clickRunCommand('/gl choose ' + (i + 1))
      .hover(Text.of('§7Click to answer')))
  }
}

function glTrialBegin(server, player, id) {
  var c = GL_CLASSES[id]
  if (!c) return 0
  if (!player.stages.has('gl_trial_' + id)) { glSay(player, '§7The ring will not answer yet. First defeat §f' + c.bossName + '§7.'); return 0 }
  if (player.stages.has('gl_trialdone_' + id)) { glSay(player, '§7The ' + c.light + ' light has already judged you.'); return 0 }
  var st = NBT.compoundTag()
  st.putString('cls', id); st.putInt('q', 0); st.putInt('life', 0); st.putInt('self', 0); st.putInt('death', 0)
  player.persistentData.put('gl_trial', st)
  var wait = glSpeak(server, player, [
    c.color + '§l✦ ' + c.bossName.charAt(0).toUpperCase() + c.bossName.slice(1) + ' is dead. And something has noticed.',
    '§7§oA ring of ' + c.light + ' light descends from the sky and stops in front of your eyes. It does not ask for your strength. It asks for your heart.',
    '§7(Answer honestly. There are no wrong answers, only different lights.)'
  ], 50)
  server.scheduleInTicks(wait + 10, function () { glTrialAsk(player, player.persistentData.getCompound('gl_trial')) })
  return 1
}

function glTrialChoose(server, player, n) {
  if (!player.persistentData.contains('gl_trial')) { glSay(player, '§7No ring is waiting for an answer.'); return 0 }
  var st = player.persistentData.getCompound('gl_trial')
  var qi = st.getInt('q'), Q = GL_QUESTIONS[qi]
  if (!Q || n < 1 || n > Q.a.length) return 0
  var lean = Q.a[n - 1][0]
  st.putInt(lean, st.getInt(lean) + 1)
  st.putInt('q', qi + 1)
  var c = GL_CLASSES[st.getString('cls')]
  glSay(player, '§8» §7' + glFill(Q.a[n - 1][1], c))
  if (qi + 1 < GL_QUESTIONS.length) {
    server.scheduleInTicks(30, function () { glTrialAsk(player, st) })
  } else {
    server.scheduleInTicks(40, function () { glTrialFinish(server, player, st) })
  }
  return 1
}

// 3+ answers leaning life -> White, 3+ leaning death -> Black, anything else -> your own light.
function glTrialOutcome(life, death, id) { return life >= 3 ? 'white' : (death >= 3 ? 'black' : id) }

function glTrialFinish(server, player, st) {
  var id = st.getString('cls'), c = GL_CLASSES[id]
  var life = st.getInt('life'), death = st.getInt('death')
  player.persistentData.remove('gl_trial')
  player.stages.add('gl_trialdone_' + id)
  var outcome = glTrialOutcome(life, death, id)
  var ring, lines, stage, title
  if (outcome === 'white') {
    ring = 'createlanterns:white_power_ring'; stage = 'gl_ring_white'; title = '§f§lWHITE LANTERN'
    lines = ['§f§oThe ' + c.light + ' light flickers... and is swallowed by something brighter.',
             '§f"You chose life, again and again. The White Light does not choose often. It has chosen you."',
             '§7The light of §fLife§7 is yours. Your ' + c.name + ' path is still yours too.']
  } else if (outcome === 'black') {
    ring = 'createlanterns:black_power_ring'; stage = 'gl_ring_black'; title = '§8§lBLACK LANTERN'
    lines = ['§8§oThe ' + c.light + ' light gutters out. Something cold takes its place.',
             '§8"You did not flinch from death. You embraced it. The Black Light remembers those who do."',
             '§7The light of §8Death§7 is yours. Use it against the dark... or become it.']
  } else {
    ring = c.ring; stage = 'gl_ring_' + id; title = c.color + '§l' + c.corps.toUpperCase()
    lines = [c.color + '§oThe ring slides onto your finger as if it had always been there.',
             c.color + '"You have the ' + c.light + ' light in you. You always did. Welcome to the ' + c.corps + '."',
             '§7§o' + c.motto]
  }
  var wait = glSpeak(server, player, lines, 50)
  server.scheduleInTicks(wait + 10, function () {
    glRun(server, 'give ' + player.username + ' ' + ring)
    glGiveStage(player, stage)
    glGiveStage(player, 'gl_ringbearer')
    glRun(server, 'title ' + player.username + ' title {"text":"' + title.replace(/§./g, '') + '"}')
    glRun(server, 'puffish_skills experience add ' + player.username + ' greenlanterns:' + id + ' 500')
    glSayAll(server, '§6✦ §f' + player.username + '§6 has been chosen. ' + title + '§r§6 ✦')
    glSay(player, '§e✦ Put the ring on (Curios ring slot or your hand). Rings fly, build constructs and need charge: recharge at a Lantern of your colour.')
  })
}
