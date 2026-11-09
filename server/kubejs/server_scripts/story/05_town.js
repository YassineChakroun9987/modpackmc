// ============================================================================
//  The story town
//  The classic village types are rebuilt as medieval towns by Epic Structures:
//  Villages (CTOV keeps its own villages next to them). On a brand-new world,
//  before the prologue starts, the world spawn moves to the nearest such town,
//  so the prologue (Elder Maren, the 7-day raid) always happens in one.
//  Village Spawn Point has already put spawn in *a* village; this picks a town.
//  Runs once per world (flag gl.townPicked). Logs "[gl] story town: ...",
//  which tools/pregen.py waits for before it pre-generates around spawn.
// ============================================================================
var GL_TOWN_TAG = 'greenlanterns:story_town'   // kubejs/data/greenlanterns/tags/worldgen/structure/story_town.json
var GL_TOWN_RADIUS = 100                        // chunks, the same as /locate

function glPickStoryTown(server) {
  var d = glData(server)
  if (d.getBoolean('init') || d.getBoolean('townPicked')) return
  var level = server.overworld()
  var $TagKey = Java.loadClass('net.minecraft.tags.TagKey')
  var $Reg = Java.loadClass('net.minecraft.core.registries.Registries')
  var tag = $TagKey.create($Reg.STRUCTURE, $ResourceLocation.parse(GL_TOWN_TAG))
  var from = level.getSharedSpawnPos()
  var pos = level.findNearestMapStructure(tag, from, GL_TOWN_RADIUS, false)
  d.putBoolean('townPicked', true)
  if (pos == null) {
    console.warn('[gl] story town: none within ' + (GL_TOWN_RADIUS * 16) + ' blocks, spawn stays at ' + from.getX() + ',' + from.getZ())
    return
  }
  var y = glSurfaceY(level, pos.getX(), pos.getZ())
  level.setDefaultSpawnPos(new $BlockPos(pos.getX(), y, pos.getZ()), 0)
  console.info('[gl] story town: spawn moved from ' + from.getX() + ',' + from.getZ() + ' to ' + pos.getX() + ',' + y + ',' + pos.getZ())
}

ServerEvents.loaded(function (event) { glPickStoryTown(event.server) })
