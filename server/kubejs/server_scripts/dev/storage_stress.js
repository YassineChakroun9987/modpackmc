// Dev: /gl_dev storagestress (op only). Lag test for Sophisticated Storage, for throwaway worlds only.
// Builds a worst realistic case 40 blocks from spawn, high in the air: 400 iron chests and barrels
// in two touching layers, half full, each with a magnet and a hopper upgrade (the two upgrades that
// work every tick), all linked to one controller, with a stream of loose items for the magnets to
// grab. It logs the server's average tick time before and after ("[storagestress] ...").
ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('storagestress').executes(function (ctx) {
      glStorageStress(ctx.source.getServer())
      return 1
    })))
})

function glStorageStress(server) {
  var level = server.overworld(), sp = level.getSharedSpawnPos()
  var x0 = sp.getX() + 40, z0 = sp.getZ() + 40, y0 = 230
  var ms = function () { return Number(server.getAverageTickTimeNanos()) / 1e6 }
  var log = function (t) { console.info('[storagestress] ' + t) }
  glRun(server, 'forceload add ' + (x0 - 8) + ' ' + (z0 - 8) + ' ' + (x0 + 28) + ' ' + (z0 + 18))
  var base = []
  for (var b = 1; b <= 3; b++) (function (k) { server.scheduleInTicks(100 + k * 100, function () { base.push(ms()) }) })(b)
  server.scheduleInTicks(420, function () {
    log('baseline (no storage): ' + base.map(function (v) { return v.toFixed(2) }).join(' / ') + ' ms per tick')
    var placed = 0
    for (var ly = 0; ly < 2; ly++) for (var i = 0; i < 200; i++) {
      var x = x0 + (i % 20), z = z0 + Math.floor(i / 20), y = y0 + ly
      glRun(server, 'setblock ' + x + ' ' + y + ' ' + z + ' sophisticatedstorage:' + (i % 2 ? 'iron_barrel' : 'iron_chest'))
      var w = level.getBlockEntity(new $BlockPos(x, y, z)).getStorageWrapper()
      w.getUpgradeHandler().setStackInSlot(0, Item.of('sophisticatedstorage:magnet_upgrade'))
      w.getUpgradeHandler().setStackInSlot(1, Item.of('sophisticatedstorage:hopper_upgrade'))
      var inv = w.getInventoryHandler()
      for (var s = 0; s < inv.getSlots() / 2; s++) inv.setStackInSlot(s, Item.of(s % 3 ? 'minecraft:cobblestone' : 'minecraft:iron_ingot', 64))
      placed++
    }
    glRun(server, 'setblock ' + (x0 - 1) + ' ' + y0 + ' ' + z0 + ' sophisticatedstorage:controller')
    level.getBlockEntity(new $BlockPos(x0 - 1, y0, z0)).searchAndAddBoundables()
    log('placed ' + placed + ' storages (magnet + hopper upgrade each, half full) and a controller')
    // Loose items for the magnets: 40 every second for 30 seconds.
    for (var t = 0; t < 30; t++) (function (k) {
      server.scheduleInTicks(40 + k * 20, function () {
        for (var j = 0; j < 40; j++) {
          var ix = x0 + Math.floor(Math.random() * 20), iz = z0 + Math.floor(Math.random() * 10)
          glRun(server, 'summon minecraft:item ' + ix + ' ' + (y0 + 3) + ' ' + iz + ' {Item:{id:"minecraft:dirt",count:1}}')
        }
      })
    })(t)
    var load = []
    for (var m = 1; m <= 5; m++) (function (k) { server.scheduleInTicks(200 + k * 100, function () { load.push(ms()) }) })(m)
    server.scheduleInTicks(760, function () {
      log('with storages: ' + load.map(function (v) { return v.toFixed(2) }).join(' / ') + ' ms per tick (budget: 50 ms)')
      var linked = 0
      try { linked = level.getBlockEntity(new $BlockPos(x0 - 1, y0, z0)).getStoragePositions().size() } catch (e) { linked = -1 }
      log('controller sees ' + linked + ' storages; item entities left near the grid: ' +
        level.getEntitiesOfClass(Java.loadClass('net.minecraft.world.entity.item.ItemEntity'),
          new (Java.loadClass('net.minecraft.world.phys.AABB'))(x0 - 2, y0 - 2, z0 - 2, x0 + 22, y0 + 8, z0 + 12)).size())
      // Breaking a full storage must drop ONE packed item (dropPacked = true), not hundreds of items.
      // Done on a lone chest 10 blocks from the grid, out of the magnets' reach.
      var bx = x0 - 10, by = y0, bz = z0 + 5
      glRun(server, 'setblock ' + bx + ' ' + by + ' ' + bz + ' sophisticatedstorage:iron_chest')
      var lone = level.getBlockEntity(new $BlockPos(bx, by, bz)).getStorageWrapper().getInventoryHandler()
      for (var s = 0; s < lone.getSlots(); s++) lone.setStackInSlot(s, Item.of('minecraft:cobblestone', 64))
      // Broken the way a player breaks it (dropPacked only applies to players and explosions, not /setblock).
      var breaker = Java.loadClass('net.neoforged.neoforge.common.util.FakePlayerFactory').getMinecraft(level)
      breaker.gameMode.destroyBlock(new $BlockPos(bx, by, bz))
      server.scheduleInTicks(5, function () {
        var drops = level.getEntitiesOfClass(Java.loadClass('net.minecraft.world.entity.item.ItemEntity'),
          new (Java.loadClass('net.minecraft.world.phys.AABB'))(bx - 3, by - 3, bz - 3, bx + 4, by + 3, bz + 4))
        var what = []
        drops.forEach(function (e) { what.push(e.getItem().getCount() + 'x ' + e.getItem().id) })
        log('broke a full chest: ' + drops.size() + ' item entit' + (drops.size() === 1 ? 'y' : 'ies') + ' dropped (' + what.slice(0, 3).join(', ') + ')')
        log('DONE')
      })
    })
  })
}
