// ============================================================================
//  Green Lanterns: story engine, shared core
//  Names (classes, stages, commands) follow docs/CONTRACT.md. Rhino rules:
//  `var` inside functions, no computed object keys.
// ============================================================================

var $BlockPos = Java.loadClass('net.minecraft.core.BlockPos')
var $MobEffects = Java.loadClass('net.minecraft.world.effect.MobEffects')
var $HeightTypes = Java.loadClass('net.minecraft.world.level.levelgen.Heightmap$Types')
var $ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')

// The seven lights. `light` = Create: Lanterns' own colour key (its whisper/dream lang lines).
var GL_CLASSES = {
  red:    { name: 'Bloodfire Berserker', light: 'red',    color: '§c', ring: 'createlanterns:red_power_ring',    boss: 'bosses_of_mass_destruction:gauntlet', bossName: 'the Nether Gauntlet',
            corps: 'Red Lantern Corps', motto: 'Rage, turned against the dark.' },
  orange: { name: 'Hoardwarden',         light: 'orange', color: '§6', ring: 'createlanterns:orange_power_ring', boss: 'kingsandmonsters:ogre_lord',         bossName: 'the Ogre King',
            corps: 'Orange Lantern Corps', motto: 'What is mine, I protect.' },
  yellow: { name: 'Stormwright',         light: 'yellow', color: '§e', ring: 'createlanterns:yellow_power_ring', boss: 'cataclysm:the_harbinger',            bossName: 'the Harbinger',
            corps: 'Yellow Lantern Corps', motto: 'Faster than thunder, brighter than lightning.' },
  green:  { name: 'Lightwarden',         light: 'green',  color: '§a', ring: 'createlanterns:power_ring',        boss: 'irons_spellbooks:dead_king',         bossName: 'the Dead King',
            corps: 'Green Lantern Corps', motto: 'In brightest day, in blackest night.' },
  blue:   { name: 'Frostbinder',         light: 'blue',   color: '§b', ring: 'createlanterns:blue_power_ring',   boss: 'bosses_of_mass_destruction:lich',    bossName: 'the Night Lich',
            corps: 'Blue Lantern Corps', motto: 'Winter keeps what it loves.' },
  indigo: { name: 'Wildheart',           light: 'indigo', color: '§9', ring: 'createlanterns:indigo_power_ring', boss: 'iceandfire:hydra',                   bossName: 'the Hydra',
            corps: 'Indigo Tribe', motto: 'No beast fights alone.' },
  violet: { name: 'Voidblade',           light: 'violet', color: '§d', ring: 'createlanterns:violet_power_ring', boss: 'graveyard:lich',                     bossName: 'the Corrupted Champion',
            corps: 'Star Sapphires of the Void', motto: 'The void does not see you coming.' }
}
var GL_CLASS_IDS = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
var GL_PARTY_RADIUS = 64

function glData(server) {
  var root = server.persistentData
  if (!root.contains('gl')) root.put('gl', NBT.compoundTag())
  return root.getCompound('gl')
}

function glSay(player, text) { player.tell(Text.of(text)) }

function glSayAll(server, text) { server.players.forEach(function (p) { glSay(p, text) }) }

// Speak several lines with a pause between them, like a character talking.
function glSpeak(server, player, lines, gapTicks) {
  var gap = gapTicks || 40
  for (var i = 0; i < lines.length; i++) {
    (function (line, delay) {
      server.scheduleInTicks(delay, function () { glSay(player, line) })
    })(lines[i], 1 + i * gap)
  }
  return lines.length * gap
}

function glGiveStage(player, stage, announce) {
  if (player.stages.has(stage)) return false
  player.stages.add(stage)
  if (announce) glSay(player, announce)
  return true
}

// Players within GL_PARTY_RADIUS of an entity, in the same dimension (party credit).
function glNearbyPlayers(entity) {
  var out = []
  var dim = String(entity.level.dimension)
  entity.server.players.forEach(function (p) {
    if (String(p.level.dimension) === dim && p.distanceToSqr(entity.getX(), entity.getY(), entity.getZ()) <= GL_PARTY_RADIUS * GL_PARTY_RADIUS) out.push(p)
  })
  return out
}

// Generate (synchronously) the chunks around x,z so heights and /place work right now.
function glEnsureChunks(level, x, z, r) {
  var cx = x >> 4, cz = z >> 4
  for (var dx = -r; dx <= r; dx++) for (var dz = -r; dz <= r; dz++) level.getChunk(cx + dx, cz + dz)
}

function glSurfaceY(level, x, z) {
  glEnsureChunks(level, x, z, 0)
  return level.getHeight($HeightTypes.WORLD_SURFACE, x, z)
}

function glRun(server, cmd) { return server.runCommandSilent(cmd) }

// Pufferfish's Skills: a player's level in greenlanterns:<id>, or -1.
var $SkillsAPI = null
try { $SkillsAPI = Java.loadClass('net.puffish.skillsmod.api.SkillsAPI') } catch (e) { console.warn('[gl] Pufferfish API not available: ' + e) }

function glClassLevel(player, id) {
  if (!$SkillsAPI) return -1
  try {
    var cat = $SkillsAPI.getCategory($ResourceLocation.parse('greenlanterns:' + id))
    if (!cat.isPresent()) return -1
    var exp = cat.get().getExperience()
    if (!exp.isPresent()) return -1
    return exp.get().getLevel(player)
  } catch (e) { return -1 }
}

// World game time (ticks). KubeJS's ServerLevel wrapper doesn't expose getGameTime() directly.
function glGameTime(level) {
  try { return level.getLevelData().getGameTime() } catch (e) {}
  try { return level.levelData.gameTime } catch (e) {}
  return level.time
}

// How many loaded entities in a level carry a tag. (Commands run from scripts don't return
// pass/fail in 1.21, so `execute if entity` can't be used as a check.)
function glCountTagged(level, tag) {
  var n = 0
  level.getEntities().forEach(function (e) { if (e.getTags().contains(tag)) n++ })
  return n
}
