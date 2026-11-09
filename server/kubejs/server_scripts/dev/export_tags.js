// Dev: /gl_dev exporttags (op only) -> kubejs/exported/c_tags.json
// Every item tag in the c: namespace with its members, to audit duplicate materials across mods
// (what Almost Unified merges, and what it misses).
ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('exporttags').executes(function (ctx) {
      var server = ctx.source.getServer()
      server.scheduleInTicks(1, function () {
        var reg = server.registryAccess().registryOrThrow(Java.loadClass('net.minecraft.core.registries.Registries').ITEM)
        var out = {}
        reg.getTags().forEach(function (pair) {
          var id = String(pair.getFirst().location())
          if (id.indexOf('c:') !== 0) return
          var members = []
          var it = pair.getSecond().iterator()
          while (it.hasNext()) members.push(String(it.next().unwrapKey().get().location()))
          out[id] = members
        })
        JsonIO.write('kubejs/exported/c_tags.json', out)
        console.info('[gl_dev exporttags] ' + Object.keys(out).length + ' c: item tags')
      })
      return 1
    })))
})
