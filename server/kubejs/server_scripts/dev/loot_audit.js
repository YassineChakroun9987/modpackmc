// Dev: /gl_dev lootaudit (op only). Rolls real chest loot tables (with every mod's global loot modifiers,
// as when a chest is filled) 200 times each and logs: average stacks per chest, items per mod, how many
// Iron's scrolls and what spells/rarities they rolled. Results: "[lootaudit] ..." in the log.
var GL_AUDIT_TABLES = [
  'minecraft:chests/village/village_savanna_house', 'minecraft:chests/village/village_plains_house',
  'minecraft:chests/random', 'minecraft:chests/wood', 'minecraft:chests/mineral', 'minecraft:chests/stone',
  'minecraft:chests/trash', 'minecraft:chests/dye', 'minecraft:chests/simple_dungeon', 'minecraft:chests/abandoned_mineshaft',
  'trek:village/village_library', 'trek:overworld/common/', 'trek:overworld/medium/',
]

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('lootaudit').executes(function (ctx) {
      var server = ctx.source.getServer()
      server.scheduleInTicks(1, function () { glLootAudit(server) })
      return 1
    })))
})

function glLootAudit(server) {
  var level = server.overworld()
  var $Reg = Java.loadClass('net.minecraft.core.registries.Registries')
  var $Key = Java.loadClass('net.minecraft.resources.ResourceKey')
  var $LPB = Java.loadClass('net.minecraft.world.level.storage.loot.LootParams$Builder')
  var $P = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParams')
  var $Sets = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParamSets')
  var $Vec = Java.loadClass('net.minecraft.world.phys.Vec3')
  var all = []
  server.reloadableRegistries().getKeys($Reg.LOOT_TABLE).forEach(function (k) { all.push(String(k)) })
  var ids = []
  GL_AUDIT_TABLES.forEach(function (t) {
    if (t.endsWith('/')) { all.filter(function (a) { return a.indexOf(t) === 0 }).slice(0, 3).forEach(function (a) { ids.push(a) }) }
    else if (all.indexOf(t) >= 0) ids.push(t)
  })
  var N = 200
  ids.forEach(function (id) {
    var table = server.reloadableRegistries().getLootTable($Key.create($Reg.LOOT_TABLE, $ResourceLocation.parse(id)))
    var stacks = 0, byMod = {}, scrolls = 0, rar = {}, legend = {}
    for (var i = 0; i < N; i++) {
      var params = new $LPB(level).withParameter($P.ORIGIN, new $Vec(0, 64, 0)).withLuck(0).create($Sets.CHEST)
      var items = table.getRandomItems(params)
      stacks += items.size()
      items.forEach(function (s) {
        var ns = String(s.id).split(':')[0]
        byMod[ns] = (byMod[ns] || 0) + 1
        if (String(s.id) === 'irons_spellbooks:scroll') {
          scrolls++
          var txt = String(s.getComponentsPatch())
          var r = (txt.match(/rarity[^A-Za-z]*([A-Za-z]+)/) || [])[1] || String(s.getRarity())
          var spell = (txt.match(/([a-z_]+:[a-z_]+)[^a-z_:]*level/) || txt.match(/"?id"?[=:]"?([a-z_]+:[a-z_]+)/) || [])[1] || '?'
          rar[r] = (rar[r] || 0) + 1
          if (/legend|epic/i.test(r)) legend[spell] = (legend[spell] || 0) + 1
        }
      })
    }
    var mods = Object.keys(byMod).sort(function (a, b) { return byMod[b] - byMod[a] }).map(function (m) { return m + '=' + (byMod[m] / N).toFixed(2) })
    console.info('[lootaudit] ' + id + ': ' + (stacks / N).toFixed(1) + ' stacks/chest; per mod ' + mods.join(' ') +
      '; scrolls ' + (scrolls / N).toFixed(2) + '/chest ' + JSON.stringify(rar) + (Object.keys(legend).length ? ' high-rarity: ' + JSON.stringify(legend) : ''))
  })
  // One example scroll's raw data, to see how rarity and spell are stored.
  console.info('[lootaudit] DONE')
}
