// ============================================================================
//  Raiders glow red through walls during a raid, so players can find the last few.
//  Every second: for each active raid near an online player (the prologue's Warband or any later
//  village raid), every living raider gets Glowing (3 s, refreshed while the raid lasts) and joins
//  the scoreboard team "gl_raiders", whose red colour makes the outline red. When the raid ends the
//  glow fades within 3 seconds.
// ============================================================================
var GL_RAID_TEAM_MADE = false

ServerEvents.tick(function (event) {
  var server = event.server
  if (server.tickCount % 20 !== 0) return
  var seen = {}
  server.players.forEach(function (p) {
    var level = p.level
    if (typeof level.getRaidAt !== 'function') return
    var raid = level.getRaidAt(p.blockPosition())
    if (!raid || !raid.isActive()) return
    var key = String(level.dimension) + ':' + raid.getId()
    if (seen[key]) return
    seen[key] = true
    if (!GL_RAID_TEAM_MADE) {
      glRun(server, 'team add gl_raiders')
      glRun(server, 'team modify gl_raiders color red')
      GL_RAID_TEAM_MADE = true
    }
    raid.getAllRaiders().forEach(function (r) {
      if (!r.isAlive()) return
      var id = String(r.getUuid())
      glRun(server, 'effect give ' + id + ' minecraft:glowing 3 0 true')
      if (!r.getTeam() || String(r.getTeam().getName()) !== 'gl_raiders') glRun(server, 'team join gl_raiders ' + id)
    })
  })
})
