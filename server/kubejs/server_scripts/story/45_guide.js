// ============================================================================
//  The boss guide: how players find their next boss.
//   - Kaelen (the Lantern at the crashed ship): right-click him holding an EMPTY MAP. He takes it and
//     gives back an explorer map with a red X on the lair of your next boss (if it has one in the
//     world you're in), and tells you how to find or summon it.
//   - /gl guide: "your ring whispers" the same directions anywhere, without a map.
//  "Next boss" = the first boss quest, in book order, of any light you've joined, that you haven't
//  beaten yet and have unlocked (class level 10 / 25 / a ring, by where it sits in the chapter).
//  Data: GL_BOSS_LIST and GL_CLASS_BOSSES in story/51_boss_list.js (generated from quests/bosses.json).
// ============================================================================
var GL_WORLD = {
  overworld: ['minecraft:overworld', 'the Overworld'], nether: ['minecraft:the_nether', 'the Nether'],
  end: ['minecraft:the_end', 'the End'], twilight: ['twilightforest:twilight_forest', 'the Twilight Forest'],
}
var GL_GUIDE_COOLDOWN = {}

// `has(stage)` defaults to the player's stages (the self-test passes its own: fake players can't hold stages).
function glNextBoss(player, has) {
  has = has || function (s) { return player.stages.has(s) }
  for (var i = 0; i < GL_CLASS_IDS.length; i++) {
    var c = GL_CLASS_IDS[i]
    if (!has('gl_class_' + c)) continue
    var list = GL_CLASS_BOSSES[c] || []
    for (var j = 0; j < list.length; j++) {
      var id = list[j][0], need = list[j][1], b = GL_BOSS_LIST[id]
      if (!b || has(b[0])) continue
      if (need && !has(need)) continue
      return { id: id, cls: c, stage: b[0], name: b[1], structure: b[2], world: b[3], where: b[4] }
    }
  }
  return null
}

function glGuideLines(player, next, voice) {
  if (!next) {
    var anyClass = GL_CLASS_IDS.some(function (c) { return player.stages.has('gl_class_' + c) })
    return [anyClass ? voice + '"Every enemy your light can face right now has fallen. Grow stronger: more will show themselves."'
                     : voice + '"Choose a light first (Act I in your quest book). Then I can show you its enemies."']
  }
  var w = GL_WORLD[next.world] || GL_WORLD.overworld
  return [voice + '"Your next quarry: §f' + next.name + '§a."',
          '§7' + next.where + ' (' + w[1] + ')']
}

// Explorer map with a red X on the nearest lair of `structure`, or null if none within ~1,000 blocks (64 chunks keeps the search short).
function glLairMap(player, structure, title) {
  var level = player.level
  var $Reg = Java.loadClass('net.minecraft.core.registries.Registries')
  var $Key = Java.loadClass('net.minecraft.resources.ResourceKey')
  var $HolderSet = Java.loadClass('net.minecraft.core.HolderSet')
  var $List = Java.loadClass('java.util.List')
  var reg = player.server.registryAccess().registryOrThrow($Reg.STRUCTURE)
  var holder = reg.getHolderOrThrow($Key.create($Reg.STRUCTURE, $ResourceLocation.parse(structure)))
  var found = level.getChunkSource().getGenerator().findNearestMapStructure(level, $HolderSet['direct(java.util.List)']($List.of(holder)), player.blockPosition(), 64, false)
  if (!found) return null
  var pos = found.getFirst()
  var $MapItem = Java.loadClass('net.minecraft.world.item.MapItem')
  var map = $MapItem.create(level, pos.getX(), pos.getZ(), 2, true, true)
  $MapItem.renderBiomePreviewMap(level, map)
  Java.loadClass('net.minecraft.world.level.saveddata.maps.MapItemSavedData').addTargetDecoration(map, pos, '+',
    Java.loadClass('net.minecraft.world.level.saveddata.maps.MapDecorationTypes').RED_X)
  map['set(net.minecraft.core.component.DataComponentType,java.lang.Object)'](
    Java.loadClass('net.minecraft.core.component.DataComponents').ITEM_NAME, Text.of(title))
  return { map: map, x: pos.getX(), z: pos.getZ() }
}

// Kaelen + empty map. Returns true if it handled the interaction.
function glLanternMap(server, player) {
  var hand = player.getMainHandItem()
  if (String(hand.id) !== 'minecraft:map') return false
  var key = player.username
  if (GL_GUIDE_COOLDOWN[key] && GL_GUIDE_COOLDOWN[key] > server.tickCount) return true
  GL_GUIDE_COOLDOWN[key] = server.tickCount + 100
  var next = glNextBoss(player)
  var voice = '§2Kaelen:§a '
  glGuideLines(player, next, voice).forEach(function (l) { glSay(player, l) })
  if (!next) return true
  if (!next.structure) {
    glSay(player, voice + '"That one has no lair I can mark. Hunt it as I said. Keep your map."')
    return true
  }
  var w = GL_WORLD[next.world] || GL_WORLD.overworld
  if (String(player.level.dimension().location()) !== w[0]) {
    glSay(player, voice + '"Its lair is in §f' + w[1] + '§a. Bring me your map there... or, well, I can\'t walk. Use §f/gl guide§a when you arrive, and ask me again with a map in hand next time you pass."')
    return true
  }
  var made = null
  try { made = glLairMap(player, next.structure, 'Lair of ' + next.name) } catch (e) { console.error('[gl] lair map failed: ' + e) }
  if (!made) {
    glSay(player, voice + '"I can\'t find its lair anywhere near. Travel further and ask again."')
    return true
  }
  hand.shrink(1)
  player.give(made.map)
  glSay(player, voice + '"There. The red mark is its lair, near §f' + made.x + ', ' + made.z + '§a. May your light hold."')
  return true
}

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl').then(Commands.literal('guide').executes(function (ctx) {
    var player = ctx.source.getPlayer()
    if (!player) return 0
    var next = glNextBoss(player)
    glGuideLines(player, next, '§6Your ring whispers:§e ').forEach(function (l) { glSay(player, l) })
    if (next && next.structure) glSay(player, '§7(Kaelen, at the crashed ship, can mark its lair on a map: bring him an empty map.)')
    return 1
  })))
})
