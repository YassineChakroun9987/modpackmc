// ============================================================================
//  Party and skill glue
//  1. FTB Teams parties -> vanilla scoreboard teams. Pufferfish's Skills only
//     shares class XP inside a vanilla team, and Iron's Spells / vanilla use
//     the same team to stop friendly fire. Each FTB party gets a team
//     "glp_<id>" with friendly fire off; leaving the party leaves the team.
//     Players in a vanilla team we didn't make are left alone.
//  2. Entity tags the skill trees read (puffish_skills:has_tag):
//       gl_sneaking    while crouching          (Violet: sneak-kill bonus)
//       gl_cold_biome  in a cold/snowy biome    (Blue: cold-land bonus)
// ============================================================================

var $FTBTeamsAPI = null
try { $FTBTeamsAPI = Java.loadClass('dev.ftb.mods.ftbteams.api.FTBTeamsAPI') } catch (e) { console.warn('[gl] FTB Teams API not available: ' + e) }

var GL_COLD_TEMP = 0.15   // vanilla: below this it snows (snowy plains 0.0, taiga 0.25, plains 0.8)
var GL_TEAMS_MADE = {}

function glPartyTeamName(player) {
  if (!$FTBTeamsAPI) return null
  try {
    var opt = $FTBTeamsAPI.api().getManager().getTeamForPlayer(player)
    if (!opt.isPresent() || !opt.get().isPartyTeam()) return null
    return 'glp_' + String(opt.get().getId()).replace(/-/g, '').substring(0, 12)
  } catch (e) { return null }
}

function glSyncPartyTeam(server, player) {
  var want = glPartyTeamName(player)
  var team = player.getTeam()
  var cur = team ? String(team.getName()) : null
  if (cur === want) return
  if (cur && cur.indexOf('glp_') !== 0 && !want) return   // someone else's team: hands off
  if (want) {
    if (!GL_TEAMS_MADE[want]) {
      glRun(server, 'team add ' + want)
      glRun(server, 'team modify ' + want + ' friendlyFire false')
      glRun(server, 'team modify ' + want + ' seeFriendlyInvisibles true')
      GL_TEAMS_MADE[want] = true
    }
    glRun(server, 'team join ' + want + ' ' + player.username)
  } else {
    glRun(server, 'team leave ' + player.username)
  }
}

function glSetTag(player, tag, on) {
  var has = player.getTags().contains(tag)
  if (on && !has) player.addTag(tag)
  else if (!on && has) player.removeTag(tag)
}

function glIsColdHere(player) {
  try {
    return player.level.getBiome(player.blockPosition()).value().getBaseTemperature() < GL_COLD_TEMP
  } catch (e) { return false }
}

PlayerEvents.tick(function (event) {
  var p = event.player
  glSetTag(p, 'gl_sneaking', p.isCrouching())
  var t = p.age
  if (t % 40 === 0) glSetTag(p, 'gl_cold_biome', glIsColdHere(p))
  if (t % 100 === 0) glSyncPartyTeam(event.server, p)
})

PlayerEvents.loggedIn(function (event) {
  event.server.scheduleInTicks(20, function () { glSyncPartyTeam(event.server, event.player) })
})
