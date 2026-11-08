// Dev tool: /gl_dev export  (op only) -> writes every ID the quest/loot/skill files may use
// to kubejs/exported/*.json, so content is written against REAL ids, never guessed ones.
const $Registries = Java.loadClass('net.minecraft.core.registries.Registries')

function step(name, fn) {
  try { return fn() } catch (e) { console.error(`[gl_dev export] ${name} failed: ${e}`); return [] }
}

function keysOf(server, key) {
  var out = []
  server.registryAccess().registryOrThrow(key).keySet().forEach(k => out.push(String(k)))
  out.sort()
  return out
}

function writeJson(name, value) {
  var o = {}
  o[name] = value
  step(`write ${name}`, () => JsonIO.write(`kubejs/exported/${name}.json`, o))
}

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event
  event.register(Commands.literal('gl_dev').requires(s => s.hasPermission(2))
    .then(Commands.literal('export').executes(ctx => { try {
      console.log('[gl_dev export] start')
      var srv = ctx.source.getServer()
      var regs = {
        items: $Registries.ITEM, entity_types: $Registries.ENTITY_TYPE, structures: $Registries.STRUCTURE,
        biomes: $Registries.BIOME, dimensions: $Registries.LEVEL_STEM, attributes: $Registries.ATTRIBUTE,
        mob_effects: $Registries.MOB_EFFECT, potions: $Registries.POTION, enchantments: $Registries.ENCHANTMENT,
      }
      var counts = []
      var items = []
      for (var name in regs) {
        var ids = step(name, () => keysOf(srv, regs[name]))
        if (name === 'items') items = ids
        writeJson(name, ids)
        counts.push(`${name}=${ids.length}`)
      }
      var adv = step('advancements', () => {
        var out = []
        srv.getAdvancements().getAllAdvancements().forEach(h => {
          if (h.value().display().isPresent()) out.push(String(h.id()))
        })
        return out.sort()
      })
      writeJson('advancements_visible', adv); counts.push(`advancements_visible=${adv.length}`)
      var loot = step('loot_tables', () => {
        var out = []
        srv.reloadableRegistries().getKeys($Registries.LOOT_TABLE).forEach(k => out.push(String(k)))
        return out.sort()
      })
      writeJson('loot_tables', loot); counts.push(`loot_tables=${loot.length}`)
      var names = {}
      items.forEach(id => { try { names[id] = String(Item.of(id).getHoverName().getString()) } catch (e) {} })
      step('write item_names', () => JsonIO.write('kubejs/exported/item_names.json', names))
      console.log(`[gl_dev export] ${counts.join(' ')}`)
      ctx.source.sendSystemMessage(Text.of(`Exported: ${counts.join(' ')}`))
      return 1
    } catch (e) { console.error(`[gl_dev export] FAILED: ${e}`); if (e.javaException) e.javaException.printStackTrace(); return 0 } })))
})
