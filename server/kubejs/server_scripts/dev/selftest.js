// Dev tool: /gl_dev selftest  (op only). Exercises the story engine without a player:
// IDs, skill categories, ring-trial scoring, and the real world placement of
// the outpost, Warlord Vex, the crash site and the NPCs. Results go to the console.
ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('selftest').executes(function (ctx) {
      var server = ctx.source.getServer(), ok = 0, bad = 0
      function check(name, cond) { if (cond) { ok++ } else { bad++; console.error('[selftest] FAIL ' + name) } }
      var reg = server.registryAccess()
      var $Reg = Java.loadClass('net.minecraft.core.registries.Registries')
      var ents = reg.registryOrThrow($Reg.ENTITY_TYPE), items = reg.registryOrThrow($Reg.ITEM)
      GL_CLASS_IDS.forEach(function (id) {
        var c = GL_CLASSES[id]
        check(id + ' ring item ' + c.ring, items.containsKey($ResourceLocation.parse(c.ring)))
        check(id + ' trial boss ' + c.boss, ents.containsKey($ResourceLocation.parse(c.boss)))
        var cat = $SkillsAPI ? $SkillsAPI.getCategory($ResourceLocation.parse('greenlanterns:' + id)) : null
        check(id + ' skill category greenlanterns:' + id, cat && cat.isPresent())
      })
      check('white ring', items.containsKey($ResourceLocation.parse('createlanterns:white_power_ring')))
      check('black ring', items.containsKey($ResourceLocation.parse('createlanterns:black_power_ring')))
      check('adventurer category', $SkillsAPI && $SkillsAPI.getCategory($ResourceLocation.parse('greenlanterns:adventurer')).isPresent())
      check('FTB Teams API for party teams', $FTBTeamsAPI !== null && $FTBTeamsAPI.api().getManager() !== null)
      check('cold-biome test works', (function () {
        try { return server.overworld().getBiome(new $BlockPos(0, 64, 0)).value().getBaseTemperature() > -10 } catch (e) { console.error('[selftest] ' + e); return false }
      })())
      // Ring-trial scoring: every 4-answer combination
      var counts = { white: 0, black: 0, own: 0 }
      for (var a = 0; a < 81; a++) {
        var life = 0, death = 0, x = a
        for (var q = 0; q < 4; q++) { var k = x % 3; x = Math.floor(x / 3); if (k === 0) life++; if (k === 2) death++ }
        var o = glTrialOutcome(life, death, 'red')
        if (o === 'white') counts.white++; else if (o === 'black') counts.black++; else counts.own++
      }
      console.info('[selftest] trial outcomes over all 81 answer paths: own=' + counts.own + ' white=' + counts.white + ' black=' + counts.black)
      check('trial outcomes balanced', counts.own > counts.white && counts.white === counts.black && counts.white > 0)
      // World placement (prologue + crash), as if the first player had logged in and Vex had died
      try {
      glPrologueInit(server)
      var d = glData(server)
      check('prologue init', d.getBoolean('init'))
      check('raid countdown starts at 7 days', glRaidLeft(d) === GL_RAID_DAYS * GL_DAY)
      var ox = d.getInt('ox'), oz = d.getInt('oz')
      glRun(server, 'execute in minecraft:overworld run forceload add ' + (ox - 8) + ' ' + (oz - 8) + ' ' + (ox + 8) + ' ' + (oz + 8))
      check('outpost ground height found', d.getInt('oy') > 0)
      glCrash(server)
      check('crash placed', d.getBoolean('crashPlaced'))
      // The ship template (createlanterns:oa/crashed_lantern_ship, 47x19x29) really landed: count its quartz hull.
      var hull = 0, cy0 = d.getInt('cy') - 2, $BP = Java.loadClass('net.minecraft.core.BlockPos')
      for (var sx = 0; sx < 47; sx++) for (var sy = 0; sy < 19; sy++) for (var sz = 0; sz < 29; sz++) {
        var bs = server.overworld().getBlockState(new $BP(d.getInt('shipX') + sx, cy0 + sy, d.getInt('shipZ') + sz))
        if (String(bs.getBlock().getDescriptionId()).indexOf('quartz') >= 0) hull++
      }
      console.info('[selftest] crashed ship: ' + hull + ' quartz hull blocks at ' + d.getInt('shipX') + ',' + cy0 + ',' + d.getInt('shipZ'))
      check('crashed ship is built (quartz hull present)', hull > 300)
      var cx = d.getInt('cx'), cz = d.getInt('cz')
      glRun(server, 'execute in minecraft:overworld run forceload add ' + (cx - 8) + ' ' + (cz - 8) + ' ' + (cx + 8) + ' ' + (cz + 8))
      // Entities in freshly loaded chunks appear a moment later: check after 5 s.
      server.scheduleInTicks(100, function () {
        console.info('[selftest] (delayed) Warlord Vex present: ' + glCountTagged(server.overworld(), 'gl_warlord'))
        console.info('[selftest] (delayed) dying Lantern NPC present: ' + glCountTagged(server.overworld(), 'gl_npc_lantern'))
        console.info('[selftest] (delayed) elder present: ' + glCountTagged(server.overworld(), 'gl_npc_elder'))
      })
      glNpcSpawnElder(server)
      check('elder spawned', d.getBoolean('elderSpawned'))
      console.info('[selftest] village ' + d.getInt('vx') + ',' + d.getInt('vz') + ' outpost ' + ox + ',' + d.getInt('oy') + ',' + oz + ' crash ' + cx + ',' + d.getInt('cy') + ',' + cz)
      } catch (err) { bad++; console.error('[selftest] world placement threw: ' + err); if (err.javaException) console.error('[selftest]   ' + err.javaException) }
      check('NPC talk handler present', typeof glNpcTalk === 'function')
      var missingBosses = Object.keys(GL_BOSS_LIST).filter(function (id) { return !ents.containsKey($ResourceLocation.parse(id)) })
      check('every quest boss exists (' + Object.keys(GL_BOSS_LIST).length + ')' + (missingBosses.length ? ': missing ' + missingBosses.join(', ') : ''), missingBosses.length === 0)
      try {
        var $FPF = Java.loadClass('net.neoforged.neoforge.common.util.FakePlayerFactory')
        var gp = $FPF.get(server.overworld(), new (Java.loadClass('com.mojang.authlib.GameProfile'))(Java.loadClass('java.util.UUID').fromString('00000000-0000-4000-8000-00000000901d'), 'gl_guide_test'))
        check('guide: no class -> no boss', glNextBoss(gp) === null)
        var nb = glNextBoss(gp, function (s) { return s === 'gl_class_red' })
        check('guide: Red recruit gets an early Red boss (' + (nb ? nb.name : 'none') + ')', nb !== null && GL_CLASS_BOSSES.red.some(function (r) { return r[0] === nb.id && r[1] === '' }))
        var lm = glLairMap(gp, 'kingsandmonsters:ogre_outpost_plains', 'Lair test')
        check('guide: lair map made for an ogre outpost' + (lm ? ' at ' + lm.x + ',' + lm.z : ''), lm !== null && String(lm.map.id) === 'minecraft:filled_map')
      } catch (err) { bad++; console.error('[selftest] guide threw: ' + err) }
      try {
        var z = Java.loadClass('net.minecraft.world.entity.EntityType').ZOMBIE.create(server.overworld())
        check('scaling: a fresh zombie is scalable', glShouldScale(z))
        check('scaling: area power with nobody near is null (and does not throw)', glAreaPower(server.overworld(), 0, 64, 0) === null)
        var elite = glApplyMobScale(z, 50, true)
        var A = Java.loadClass('net.minecraft.world.entity.ai.attributes.Attributes')
        var hp = z.getMaxHealth(), dmg = z.getAttributeValue(A.ATTACK_DAMAGE), arm = z.getAttributeValue(A.ARMOR)
        console.info('[selftest] scaling: power-50 elite zombie hp=' + hp + ' dmg=' + dmg.toFixed(2) + ' armour=' + arm)
        check('scaling: power-50 elite zombie has 72 hp (20 x 3.6)', elite && Math.abs(hp - 72) < 0.01)
        check('scaling: damage x2.55 (3 -> 7.65)', Math.abs(dmg - 7.65) < 0.01)
        check('scaling: +10 armour (2 -> 12)', Math.abs(arm - 12) < 0.01)
        check('scaling: never scaled twice', !glShouldScale(z))
        z.discard()
      } catch (err) { bad++; console.error('[selftest] scaling threw: ' + err) }
      try {
        // A stand-in container (glCapChest only needs these four methods; SimpleContainer's constructor is
        // overloaded and Rhino can't pick one).
        var slots = []; for (var bs = 0; bs < 27; bs++) slots.push($ItemStack.EMPTY)
        var box = { getContainerSize: function () { return 27 }, getItem: function (i) { return slots[i] },
                    setItem: function (i, s) { slots[i] = s }, setChanged: function () {} }
        for (var bi = 0; bi < 22; bi++) box.setItem(bi, Item.of(bi % 2 ? 'minecraft:rotten_flesh' : 'minecraft:string', 3))
        box.setItem(22, Item.of('minecraft:diamond_sword')); box.setItem(23, Item.of('minecraft:golden_apple'))
        box.setItem(24, Item.of('minecraft:diamond', 2))
        var capped = glCapChest(box, 1), left = 0, keptSword = false
        for (var bj = 0; bj < 27; bj++) { if (!box.getItem(bj).isEmpty()) left++; if (String(box.getItem(bj).id) === 'minecraft:diamond_sword') keptSword = true }
        check('chest cap: tier 1 chest trimmed to 9 stacks (' + left + ')', left === 9)
        check('chest cap: junk goes first, the sword stays', keptSword && capped.stacksRemoved === 16)
        check('chest tier: a village chest is tier 1, a Nether chest at least 3',
          glChestTier('minecraft:chests/village/village_plains_house', 'minecraft:overworld') === 1 && glChestTier('minecraft:chests/village/village_plains_house', 'minecraft:the_nether') >= 3)
      } catch (err) { bad++; console.error('[selftest] chest cap threw: ' + err) }
      try {
        var lvl = server.overworld(), VT = Java.loadClass('net.minecraft.world.entity.EntityType').VILLAGER
        var npc = VT.create(lvl), plain = VT.create(lvl)
        npc.addTag('gl_npc'); npc.setPos(0, 200, 0); plain.setPos(2, 200, 0)
        lvl.addFreshEntity(npc); lvl.addFreshEntity(plain)
        npc.attack(lvl.damageSources().generic(), 10); plain.attack(lvl.damageSources().generic(), 10)
        check('story NPCs take no damage (npc ' + npc.getHealth() + ', plain villager ' + plain.getHealth() + ')', npc.getHealth() === npc.getMaxHealth() && plain.getHealth() < plain.getMaxHealth())
        npc.discard(); plain.discard()
      } catch (err) { bad++; console.error('[selftest] npc damage threw: ' + err) }
      try { glCorpseSelftest(server, check) } catch (err) { bad++; console.error('[selftest] corpse quick-loot threw: ' + err); if (err.javaException) console.error('[selftest]   ' + err.javaException) }
      console.info('[selftest] DONE: ' + ok + ' passed, ' + bad + ' failed')
      return bad === 0 ? 1 : 0
    })))
  // /gl_dev villageweights: the live "minecraft:villages" structure set (after every mod changed it).
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('villageweights').executes(function (ctx) {
      var $Reg = Java.loadClass('net.minecraft.core.registries.Registries')
      var set = ctx.source.getServer().registryAccess().registryOrThrow($Reg.STRUCTURE_SET).get($ResourceLocation.parse('minecraft:villages'))
      var total = 0, lines = []
      set.structures().forEach(function (e) {
        var key = e.structure().unwrapKey()
        lines.push(e.weight() + '  ' + (key.isPresent() ? key.get().location() : '?'))
        total += e.weight()
      })
      lines.forEach(function (l) { console.info('[villageweights] ' + l) })
      console.info('[villageweights] ' + lines.length + ' entries, total weight ' + total + ', placement ' + set.placement())
      // Which biomes may hold a classic (Epic) village, and the biome at spawn.
      var server = ctx.source.getServer(), level = server.overworld()
      var biomes = server.registryAccess().registryOrThrow($Reg.BIOME)
      var $TagKey = Java.loadClass('net.minecraft.tags.TagKey')
      var here = String(level.getBiome(level.getSharedSpawnPos()).unwrapKey().get().location())
      console.info('[villageweights] spawn biome: ' + here)
      ;['plains', 'desert', 'savanna', 'snowy', 'taiga'].forEach(function (b) {
        var tag = $TagKey.create($Reg.BIOME, $ResourceLocation.parse('minecraft:has_structure/village_' + b))
        var names = []
        var it = biomes.getTagOrEmpty(tag).iterator()
        while (it.hasNext()) names.push(String(it.next().unwrapKey().get().location()))
        console.info('[villageweights] village_' + b + ' biomes (' + names.length + '): ' + names.join(' ') + (names.indexOf(here) >= 0 ? '   <-- includes spawn' : ''))
      })
      return 1
    })))
  // /gl_dev corpsetest: only the corpse quick-loot round trip.
  event.register(Commands.literal('gl_dev').requires(function (s) { return s.hasPermission(2) })
    .then(Commands.literal('corpsetest').executes(function (ctx) {
      var ok = 0, bad = 0
      function check(name, cond) { if (cond) { ok++ } else { bad++; console.error('[corpsetest] FAIL ' + name) } }
      try { glCorpseSelftest(ctx.source.getServer(), check) } catch (err) { bad++; console.error('[corpsetest] threw: ' + err) }
      console.info('[corpsetest] DONE: ' + ok + ' passed, ' + bad + ' failed')
      return bad === 0 ? 1 : 0
    })))
})
