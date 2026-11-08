// ============================================================================
//  Create: Lanterns clean-up + end-game gate
// ============================================================================

// Lights this pack doesn't use: the 4 joke lights and the unused secret lights (Gold, Ultraviolet).
// Rings of these lights can't be obtained anyway (command/creative only); this hides every item of
// theirs from JEI so the recipe viewer only shows what's really in the story.
var GL_UNUSED_LIGHTS = ['xbox', 'playstation', 'steam', 'whatsapp', 'gold', 'ultraviolet']
var GL_LIGHT_ITEM_KINDS = ['dust', 'liquid_light_bucket', 'power_battery', 'power_ring']

ServerEvents.tags('item', function (event) {
  GL_UNUSED_LIGHTS.forEach(function (light) {
    GL_LIGHT_ITEM_KINDS.forEach(function (kind) {
      event.add('c:hidden_from_recipe_viewers', 'createlanterns:' + light + '_' + kind)
    })
  })
})

ServerEvents.recipes(function (event) {
  // The Devourer of Gods' summon also needs a Chaos Shard, so the Chaos Guardian is the gate
  // to the final fight (docs/STORY-design.md section 10).
  event.remove({ id: 'dog:cosmic_worm' })
  event.shapeless('dog:cosmic_worm', ['dog:draconic_soul_fragment', 'minecraft:nether_star', 'minecraft:echo_shard', 'draconicevolution:chaos_shard'])
    .id('greenlanterns:cosmic_worm')
})
