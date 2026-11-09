// ============================================================================
//  Green Lanterns: tiered, cross-mod chest loot (LootJS 3.7, NeoForge 1.21.1)
// ============================================================================
//
//  What it does
//  - Every structure chest/barrel/vault table below gets ONE extra roll of
//    greenlanterns:chests/injected_tier_<N> (N = 1..5). The original loot is kept.
//  - The tier comes from the table id (rules below, first match wins), then is
//    raised by the dimension (Nether/End >= 3) and by the structure the chest
//    is in (for mods whose structures reuse vanilla tables, e.g. Grim Kingdoms).
//  - Luck matters: the injected tables use `quality` (weight + quality * luck)
//    and `bonus_rolls` (extra rolls per point of luck). Junk and blanks have
//    negative quality, rare items positive quality.
//
//  How it is wired (LootJS docs: https://docs.almostreliable.com/lootjs/1.21.x/)
//  1. LootJS.lootTables  -> event.getLootTableIds(), event.hasLootTable(),
//                           event.create(id).createPool(...)   (missing tables)
//     Classifies every loot table id once per (re)load.
//  2. LootJS.modifiers   -> event.addTableModifier(/^(id|id|...)$/).pool(...)
//     A loot modifier runs only for the table the chest itself rolled (not for
//     tables pulled in through "minecraft:loot_table" references), so a When
//     Dungeons Arise chest that also references a vanilla table still gets
//     exactly one injected roll.
//     (lootTables runs while the loot registry loads; modifiers runs later, when
//     the global loot modifiers load, on every start and every /reload.)
//
//  Chests are shared (Lootr was removed 2026-11-09): a chest rolls once, when it's first opened,
//  with the opener's luck. glue/chest_loot.js then caps scroll rarity and stack count by tier.
//
//  Tuning: edit the data block below, then /reload.
//  The server log prints "[greenlanterns/loot]" lines with table counts per tier.
// ============================================================================

// ---------------------------------------------------------------- DATA BLOCK

var GL_LOOT_INJECT = 'greenlanterns:chests/injected_tier_'

// Never injected (checked before the tier rules).
var GL_LOOT_SKIP = [
  // block/mob/fishing/key/map/pot/brush tables (the WDA Coliseum chest table sits in entities/, so it is exempt)
  /^(?!dungeons_arise:entities\/gladiator_loot$)[a-z0-9_.-]+:(blocks|entities|entity|gameplay|equipment|entity_equipment|spawners|spawner_projectile|keys|maps|mob|pots|archaeology|archeology|archaelogy|special_items|shearing|dispensers|items|inject|magic_items|test|chronicle|additions)\//,
  /^greenlanterns:/,
  /^lootr:/, /^wares:/, /^monobank:/, /^alexsmobs:/, /^apothic_/, /^ae2:/, /^dog:/, /^sophisticatedbackpacks:/,
  /^farmersdelight:chests\/fd_/,                  // Farmer's Delight adds these to vanilla chests itself
  /^artifacts:(?!chests\/campsite_(chest|barrel)$)/,
  /\/inserts\//, /\/additional_[a-z_]+$/,          // loot other mods add into vanilla chests
  /(^|\/|_)pot$/, /_urn$/, /dispenser/, /tavern_quest$/,
  /^irons_spellbooks:chests\/trial_chambers\//,
  /^discerning_the_eldritch:chests\/(city_items|rift_ripper_emblem|trial_chambers\/)/,
  /^twilightforest:(useless|items\/|quest_grove_dropper|darktower_key|fallen_trunk_loot)/,
  /^terralith:(royal_jelly|underground\/giant_bee_hive|mage\/small_common_flowers)$/,
  /^minecraft:chests\/spawn_bonus_chest$/
]

// Ordered tier rules: [regex, tier]. First match wins. Tier 1 = small ruin/village ... 5 = huge castle/End.
var GL_LOOT_TIER_RULES = [
  // ---- tables that live in other folders but are real structure chests
  [/^dungeons_arise:entities\/gladiator_loot$/, 4],                       // WDA Coliseum

  // ---- Vanilla (and Born in Chaos / D&T tables in the minecraft namespace)
  [/^minecraft:chests\/village\//, 1],
  [/^minecraft:chests\/(village_desert_house|wood|random|mineral|dye|stone|trash)$/, 1],   // Epic Villages' chests; created below if missing (Cataclysm / Grim Kingdoms)
  [/^minecraft:chests\/(igloo_chest|shipwreck_supply|shipwreck_map|underwater_ruin_small|ruined_portal)$/, 1],
  [/^minecraft:chests\/(basic_chest|chest_level_1|farm_drop)$/, 1],              // Born in Chaos
  [/^minecraft:chests\/(chest_level_2|firewell_d|shater)$/, 2],                  // Born in Chaos
  [/^minecraft:chests\/chest_level_3$/, 3],                                      // Born in Chaos
  [/^minecraft:chests\/(simple_dungeon|abandoned_mineshaft|pillager_outpost|desert_pyramid|jungle_temple|buried_treasure|shipwreck_treasure|underwater_ruin_big)$/, 2],
  [/^minecraft:chests\/trial_chambers\/(corridor|entrance|intersection|intersection_barrel|supply)$/, 2],
  // vault tables; the *_common/_rare/_unique parts only fire when a structure uses them directly (Grim Kingdoms)
  [/^minecraft:chests\/trial_chambers\/reward_common$/, 2],
  [/^minecraft:chests\/trial_chambers\/(reward|reward_rare|reward_ominous_common)$/, 3],
  [/^minecraft:chests\/trial_chambers\/(reward_unique|reward_ominous|reward_ominous_rare|reward_ominous_unique)$/, 4],
  [/^minecraft:chests\/(stronghold_corridor|stronghold_crossing|stronghold_library|woodland_mansion|ancient_city_ice_box|nether_bridge|bastion_bridge|bastion_other|bastion_hoglin_stable)$/, 3],
  [/^minecraft:chests\/nether_fortress\//, 3],                                   // D&T Nether Keep
  [/^minecraft:chests\/illager_mansion\/(secret_room|evoker_chest|ancient_city_raid_chest)$/, 4], // D&T Illager Manor
  [/^minecraft:chests\/illager_mansion\//, 3],
  [/^minecraft:chests\/(ancient_city|bastion_treasure)$/, 4],
  [/^minecraft:chests\/end_city_treasure$/, 5],

  // ---- YUNG's
  [/^betterdungeons:small_dungeon\//, 1],
  [/^betterdungeons:small_nether_dungeon\//, 3],
  [/^betterdungeons:/, 2],
  [/^betterdeserttemples:chests\/(tomb_pharaoh|pharaoh_hidden)$/, 4],
  [/^betterdeserttemples:chests\/tomb$/, 3],
  [/^betterdeserttemples:chests\//, 2],
  [/^betterjungletemples:chests\/campsite$/, 1],
  [/^betterjungletemples:chests\/treasure$/, 3],
  [/^betteroceanmonuments:chests\//, 3],
  [/^betterstrongholds:chests\/treasure$/, 4],
  [/^betterstrongholds:chests\//, 3],
  [/^betterfortresses:chests\/(keep|obsidian|beacon)$/, 4],
  [/^betterfortresses:chests\//, 3],
  [/^betterwitchhuts:chests\//, 1],
  [/^yungsextras:desert\/(chillzone|ruins)$/, 1],

  // ---- Dungeons and Taverns (nova_structures)
  [/^nova_structures:chests\/shrine\/combat_treasure_1$/, 1],
  [/^nova_structures:chests\/shrine\/combat_treasure_2$/, 2],
  [/^nova_structures:chests\/shrine\/combat_treasure_3$/, 3],
  [/^nova_structures:chests\/shrine\/combat_treasure_4$/, 4],
  [/^nova_structures:chests\/shrine\/combat_treasure_5$/, 5],
  [/^nova_structures:chests\/shrine\/shrine_lesser_treasure$/, 2],
  [/^nova_structures:chests\/shrine\/shrine_lesser_ominous$/, 3],
  [/^nova_structures:chests\/shrine\/vault_shrine_ominous$/, 4],
  [/^nova_structures:chests\/end_castle\/(greater_loot|treasure_lighthouse|vault_[a-z]+)$/, 5],
  [/^nova_structures:chests\/end_castle\//, 4],
  [/^nova_structures:chests\/end_lighthouse\/vault_lighthouse$/, 5],
  [/^nova_structures:chests\/end_lighthouse\//, 4],
  [/^nova_structures:chests\/lone_citadel\/(c_vault|c_vault_boss)$/, 4],
  [/^nova_structures:chests\/lone_citadel\//, 3],
  [/^nova_structures:chests\/(nether_keep\/vault_keep|piglin_donjon\/vault_piglin_donjon|piglin_outstation\/vault_piglin_outstation)$/, 4],
  [/^nova_structures:chests\/(nether_keep|nether_port|nether_skeleton_tower|piglin_camp|piglin_donjon|piglin_outstation)\//, 3],
  [/^nova_structures:chests\/toxic_lair\/(toxic_boss_vault|toxic_ominous_vault)$/, 4],
  [/^nova_structures:chests\/toxic_lair\/toxic_vault$/, 3],
  [/^nova_structures:chests\/toxic_lair\//, 2],
  [/^nova_structures:chests\/trident_trial_monument\/ttm_boss_vault_/, 4],
  [/^nova_structures:chests\/trident_trial_monument\//, 3],
  [/^nova_structures:chests\/creeping_crypt\/vault_creeping$/, 3],
  [/^nova_structures:chests\/(jungle_ruins\/jungle_ruins_main_temple(_wild)?|desert_ruins\/desert_ruin_main_temple|bunker_altar|stray_fort_tresure|illager_hideout_(tresure|heart_loot)|conduit_ruin\/conduit_ruin_big)$/, 3],
  [/^nova_structures:chests\/(dungeon_[1-7]|ruin_loot_master|ruin_loot_[1-7]|creeping_crypt\/|undead_crypts_grave|desert_ruins\/desert_ruin_lesser_treasure|conduit_ruin\/|illager_hideout_|stray_fort_|hamlet\/hamlet_tresure|pillager_outpost_treasure|witch_villa\/(lab|library|potion_brewing)$)/, 2],
  [/^nova_structures:chests\//, 1],

  // ---- When Dungeons Arise (treasure rooms first, then the rest of each build)
  [/^dungeons_arise:chests\/(heavenly_challenger|heavenly_conqueror|heavenly_rider)\/[a-z_]+_treasure$/, 5],
  [/^dungeons_arise:chests\/(shiraz_palace\/shiraz_palace_treasure|mechanical_nest\/mechanical_nest_treasure|typhon\/typhon_treasure|infested_temple\/infested_temple_vault_(ominous|treasure)|kisegi_sanctuary\/kisegi_sanctuary_vault_ominous(_treasure)?)$/, 5],
  [/^dungeons_arise:chests\/(aviary|foundry|illager_fort|illager_corsair|illager_galley|keep_kayra|monastery|plague_asylum|scorched_mines|thornborn_towers|undead_pirate_ship|mining_complex|infested_temple|kisegi_sanctuary|ceryneian_hind|shiraz_palace|mechanical_nest|heavenly_challenger|heavenly_conqueror|heavenly_rider|typhon)\/[a-z_]+(_treasure|_elite|_equipment|_vault_normal|_theater)$/, 4],
  [/^dungeons_arise:chests\/(aviary|foundry|illager_fort|illager_corsair|illager_galley|keep_kayra|monastery|plague_asylum|scorched_mines|thornborn_towers|undead_pirate_ship|mining_complex|infested_temple|kisegi_sanctuary|ceryneian_hind|shiraz_palace|mechanical_nest|heavenly_challenger|heavenly_conqueror|heavenly_rider|typhon)\//, 3],
  [/^dungeons_arise:chests\/mines_treasure_big$/, 4],
  [/^dungeons_arise:chests\/mines_treasure_medium$/, 3],
  [/^dungeons_arise:chests\/(small_blimp|mushroom_house|mushroom_village|bathhouse|bandit_village|bandit_towers|jungle_tree_house|illager_windmill|abandoned_temple|mining_system|mushroom_mines|giant_mushroom)\/[a-z_]+(_treasure|_top)$/, 3],
  [/^dungeons_arise:chests\/(fishing_hut|merchant_campsite|illager_campsite|greenwood_pub)\//, 1],
  [/^dungeons_arise:chests\//, 2],

  // ---- WDA: Seven Seas
  [/^dungeons_arise_seven_seas:chests\/small_yacht\/[a-z_]+_treasure$/, 3],
  [/^dungeons_arise_seven_seas:chests\/small_yacht\//, 2],
  [/^dungeons_arise_seven_seas:chests\/(unicorn_galleon|victory_frigate)\/[a-z_]+_treasure$/, 5],
  [/^dungeons_arise_seven_seas:chests\/[a-z_]+\/[a-z_]+_treasure$/, 4],
  [/^dungeons_arise_seven_seas:chests\//, 3],

  // ---- Philips Ruins (several of its tables are missing in the jar; created below)
  [/^philipsruins:chest\/(level_one_ruins_loot|ruin_loot)$/, 1],
  [/^philipsruins:chest\/(level_three_ruins_loot|ocean_ruin_fortress|lost_soul_city_loot|badlands_dungeon_loot_high|sculk_dungeon_loot|nether_ruins_low|nether_lava_ruins_loot)$/, 3],
  [/^philipsruins:chest\/end_ruins_loot$/, 4],
  [/^philipsruins:chest\//, 2],

  // ---- Trek (loot folders are its own rarity tiers)
  [/^trek:(overworld\/(very_common|common)|village)\//, 1],
  [/^trek:(overworld\/medium|pillagers)\//, 2],
  [/^trek:overworld\/rare\//, 3],
  [/^trek:overworld\/very_rare\//, 4],
  // ---- Towns and Towers, CTOV, Sky Villages, Terralith villages
  [/^kaisyn:outpost\/common\/armory$/, 2],
  [/^kaisyn:(outpost|village)\//, 1],
  [/^wythers:chests\/village\//, 1],
  [/^ctov:chests\//, 1],
  [/^skyvillages:chests\//, 2],
  [/^terralith:village\/(treasure\/|(desert|fortified)\/(treasure|smith\/expert)$)/, 2],
  [/^terralith:(village\/|desert_outpost$|igloo$|witch_hut$|lodge_drinkables$)/, 1],
  [/^terralith:mage\/treasure$/, 3],
  [/^terralith:mage\//, 2],
  [/^terralith:spire\/(treasure|rare)$/, 3],
  [/^terralith:spire\//, 2],
  [/^terralith:ruin\/glacial\/main_cs$/, 2],
  [/^terralith:ruin\//, 1],
  [/^terralith:underground\//, 2],

  // ---- The Lost Castle (one huge, rare castle)
  [/^tlc:chests\/(treasure|throne)$/, 5],
  [/^tlc:chests\/(hided|lab|dungeon|biblio)$/, 4],
  [/^(tlc|lostcastle):chests\//, 3],

  // ---- Nether mods
  [/^eternalnether:chests\//, 4],
  [/^netherexp:(chests|brazier_chest)\//, 3],

  // ---- Boss / mob mods
  [/^cataclysm:chests\/(acropolis_treasure|frosted_prison_treasure|desert_treasure|abandoned_treasure)$/, 4],
  [/^cataclysm:chests\//, 3],
  [/^bosses_of_mass_destruction:chests\//, 4],
  [/^legendary_monsters:chests\/space_station_loot_table_luxury$/, 5],
  [/^legendary_monsters:chests\/[a-z_]+luxury[a-z_]*$/, 4],
  [/^legendary_monsters:chests\//, 3],
  [/^mowziesmobs:chests\//, 3],
  [/^kingsandmonsters:chests\/ogre_kings_fort_(king|king_hut|tribute)$/, 4],
  [/^kingsandmonsters:chests\/ogre_kings_fort/, 3],
  [/^kingsandmonsters:chests\//, 2],
  [/^graveyard:chests\/(great_crypt_loot|large_graveyard_loot|large_loot|crypt_loot)$/, 3],
  [/^graveyard:chests\/(medium_graveyard_loot|medium_loot|desert_graveyard_loot|swamp_graveyard_loot|totem_loot|ore_loot|brewing_loot)$/, 2],
  [/^graveyard:chests\//, 1],

  // ---- Dragons
  [/^iceandfire:chest\/((fire|ice|lightning)_dragon_(female|male)_cave|(fire|ice|lightning)_dragon_roost|hydra_cave|cyclops_cave)$/, 4], // dragon hoards, roosts, lairs
  [/^iceandfire:chest\/(mausoleum_chest|graveyard)$/, 3],
  [/^iceandfire:chest\//, 1],
  [/^bookofdragons:chests\//, 3],

  // ---- Magic mods
  [/^irons_spellbooks:chests\/(catacombs\/dead_king_vault|citadel\/citadel_vault)$/, 4],
  [/^irons_spellbooks:chests\/(citadel|catacombs|battleground)\//, 3],
  [/^irons_spellbooks:chests\/(generic_magic_treasure|magic_bookshelf_loot)$/, 3],
  [/^irons_spellbooks:chests\//, 2],
  [/^discerning_the_eldritch:chests\/cultist_base\/ascended_vault$/, 5],
  [/^discerning_the_eldritch:chests\/cultist_base\/(cultist_vault|quality_treasure_loot|treasure_loot)$/, 4],
  [/^discerning_the_eldritch:chests\/(cultist_base\/|electromancer_tower\/|blood_cultist_hut\/bloody_chest$)/, 3],
  [/^discerning_the_eldritch:chests\//, 2],
  [/^alshanex_familiars:chests\/end_laboratory\//, 4],
  [/^alshanex_familiars:chests\/(summoner_lab\/|graveyard\/treasure$)/, 3],
  [/^alshanex_familiars:chests\/hunter_campsite\//, 1],
  [/^alshanex_familiars:chests\//, 2],
  [/^apotheosis:chests\/(tome_tower|chest_valuable)$/, 3],
  [/^apotheosis:chests\//, 2],

  // ---- Twilight Forest (its tables sit in the namespace root)
  [/^twilightforest:(troll_vault|troll_vault_with_lamp|labyrinth_vault_jackpot)$/, 5],
  [/^twilightforest:(labyrinth_vault|darktower_cache|darktower_boss|aurora_cache|aurora_room|troll_garden|hill_3)$/, 4],
  [/^twilightforest:(labyrinth_room|labyrinth_dead_end|stronghold_cache|stronghold_room|chests\/tower_[a-z_]+)$/, 3],
  [/^twilightforest:(hill_2|hedge_maze|graveyard|chests\/basement)$/, 2],
  [/^twilightforest:(hill_1|well|fancy_well|tree_cache|foundation_basement|camp_[a-z_]+|chests\/(hut_junk|casket_loot)|hedge_cloth)$/, 1],

  // ---- Small stuff
  [/^galosphere:chests\//, 2],
  [/^artifacts:chests\/campsite_(chest|barrel)$/, 1],
  [/^(redomesticate|pet_home):chests\/petshop_chest$/, 1]
]

// Minimum tier by the dimension the chest is in.
var GL_LOOT_DIMENSION_MIN_TIER = [
  ['minecraft:the_nether', 3],
  ['minecraft:the_end', 3]
]

// Minimum tier by structure: for mods whose structures reuse vanilla tables.
var GL_LOOT_STRUCTURE_MIN_TIER = [
  [['castle_in_the_sky:castle_in_the_sky'], 4],
  [['castles_and_keeps:undead_castle', 'castles_and_keeps:villager_keep', 'castles_and_keeps:two_towers'], 3],
  [['castles_and_keeps:desert_tower', 'castles_and_keeps:medium_tower', 'castles_and_keeps:pillager_tower',
    'castles_and_keeps:small_abandoned_tower', 'castles_and_keeps:zombie_villager_tower'], 2],
  [['grim_kingdoms:shardspire_castle', 'grim_kingdoms:silentgale_citadel', 'grim_kingdoms:silentgale_citadel_plains',
    'grim_kingdoms:snowgrave_citadel', 'grim_kingdoms:winterhold_citadel', 'grim_kingdoms:winterhold_citadel_taiga',
    'grim_kingdoms:glacierfall_keep', 'grim_kingdoms:glacierfall_keep_plains', 'grim_kingdoms:whitewarden_keep',
    'grim_kingdoms:grain_sack_keep', 'grim_kingdoms:glimmervault_fortress', 'grim_kingdoms:glimmervault_fortress_plains',
    'grim_kingdoms:frostbloom_bastion', 'grim_kingdoms:weathered_colosseum', 'grim_kingdoms:zweiberg',
    'grim_kingdoms:zweiberg_plains', 'grim_kingdoms:zweiberg_taiga', 'grim_kingdoms:eldermoor'], 3],
  [['grim_kingdoms:blackridge_watch', 'grim_kingdoms:blackridge_watch_taiga', 'grim_kingdoms:chill_hallmanor',
    'grim_kingdoms:chillhall_plains_refuge', 'grim_kingdoms:frozen_onion_fort', 'grim_kingdoms:frozen_onion_fort_taiga',
    'grim_kingdoms:grain_sack_fort', 'grim_kingdoms:grain_sack_hold', 'grim_kingdoms:east_spur_tower',
    'grim_kingdoms:west_spur_tower', 'grim_kingdoms:north_spur_tower', 'grim_kingdoms:south_spur_tower',
    'grim_kingdoms:high_spur_tower', 'grim_kingdoms:tor_tower', 'grim_kingdoms:decrown_monolith',
    'grim_kingdoms:decrown_monolith_taiga', 'grim_kingdoms:sandfell_outpost', 'grim_kingdoms:stonyfell_outpost',
    'grim_kingdoms:stonyfell_outpost_plains', 'grim_kingdoms:old_timber_watch', 'grim_kingdoms:river_bend_watch',
    'grim_kingdoms:gnome_tall_tower'], 2],
  [['sky_whale_ship:whale', 'sky_whale_ship:whaleship', 'sky_whale_ship:frozen_whale', 'sky_whale_ship:whalearena',
    'sky_whale_ship:whalelight'], 3],
  [['floating_islands:amethyst_island', 'floating_islands:camp_island', 'floating_islands:cemetery_island',
    'floating_islands:cherry_island_with_shrine', 'floating_islands:drifting_island', 'floating_islands:floating_rocks',
    'floating_islands:flower_island2', 'floating_islands:hut_with_waystone', 'floating_islands:paradise_island',
    'floating_islands:pillager_camp', 'floating_islands:shrine', 'floating_islands:spider_ruin',
    'floating_islands:steampunk_island', 'floating_islands:tower_island', 'floating_islands:villager_island',
    'floating_islands:witch_island'], 2],
  [['legendary_monsters:ancient_stronghold', 'legendary_monsters:ancient_tower_remains', 'legendary_monsters:cloudy_temple',
    'legendary_monsters:collapsed_kingdom', 'legendary_monsters:frostbitten_temple', 'legendary_monsters:lava_eater_spawn',
    'legendary_monsters:mossy_temple', 'legendary_monsters:ruined_pyramid', 'legendary_monsters:shulker_tower',
    'legendary_monsters:skeletosaurus_nest', 'legendary_monsters:soul_fortress_remains', 'legendary_monsters:space_station',
    'legendary_monsters:warped_fungussus_nest'], 3],
  [['cataclysm:abandoned_spire', 'cataclysm:abandoned_temple', 'cataclysm:acropolis', 'cataclysm:amethyst_nest',
    'cataclysm:ancient_factory', 'cataclysm:burning_arena', 'cataclysm:cursed_pyramid', 'cataclysm:desert_site',
    'cataclysm:desert_temple', 'cataclysm:frosted_prison', 'cataclysm:ruined_citadel', 'cataclysm:soul_black_smith',
    'cataclysm:sunken_city'], 3]
]

// Tables that structures in this pack point at but no mod ships (their chests would be empty).
// [missing id, existing table to copy from]. Skipped if the id exists or the source doesn't.
var GL_LOOT_MISSING_TABLES = [
  ['philipsruins:chest/desert_pyramid_loot', 'minecraft:chests/desert_pyramid'],
  ['philipsruins:chest/bone_dungeon_loot', 'minecraft:chests/simple_dungeon'],
  ['philipsruins:chest/badlands_dungeon_loot_low', 'minecraft:chests/abandoned_mineshaft'],
  ['philipsruins:chest/badlands_dungeon_loot_high', 'philipsruins:chest/level_three_ruins_loot'],
  ['philipsruins:chest/sculk_dungeon_loot', 'minecraft:chests/stronghold_corridor'],
  ['philipsruins:chest/nether_ruins_low', 'minecraft:chests/nether_bridge'],
  ['philipsruins:chest/nether_lava_ruins_loot', 'minecraft:chests/bastion_other'],
  ['philipsruins:chest/end_ruins_loot', 'minecraft:chests/end_city_treasure'],
  ['minecraft:chests/wood', 'minecraft:chests/village/village_plains_house'],        // Grim Kingdoms
  ['minecraft:chests/random', 'minecraft:chests/simple_dungeon'],                     // Grim Kingdoms
  ['minecraft:chests/mineral', 'minecraft:chests/abandoned_mineshaft'],               // Grim Kingdoms
  ['minecraft:chests/dye', 'minecraft:chests/village/village_shepherd'],              // Grim Kingdoms
  ['minecraft:chests/village_desert_house', 'minecraft:chests/village/village_desert_house'], // Cataclysm
  ['minecraft:chests/village/village_leatherworker', 'minecraft:chests/village/village_tannery'], // Towns and Towers
  ['kaisyn:village/village_birch_forest_house', 'minecraft:chests/village/village_plains_house'],
  ['kaisyn:village/village_forest_ruins/forest_ruins_butcher', 'minecraft:chests/village/village_butcher'],
  ['kaisyn:village/village_forest_ruins/forest_ruins_library', 'minecraft:chests/village/village_cartographer'],
  ['kaisyn:village/village_forest_ruins/forest_ruins_temple', 'minecraft:chests/village/village_temple'],
  ['wythers:chests/village/forest_ruins_big_house', 'minecraft:chests/village/village_plains_house'],
  ['terralith:village/desert/leatherworker', 'minecraft:chests/village/village_tannery'],
  ['lostcastle:chests/house', 'tlc:chests/house'],                                    // The Lost Castle
  ['lostcastle:chests/food', 'tlc:chests/food'],
  ['dungeons_arise:chests/giant_mushroom/red_giant_mushroom', 'dungeons_arise:chests/mushroom_house/mushroom_house_normal'],
  ['dungeons_arise:chests/giant_mushroom/twin_giant_mushroom', 'dungeons_arise:chests/mushroom_house/mushroom_house_normal'],
  ['dungeons_arise:chests/mushroom_house/mushroom_house_barrel', 'dungeons_arise:chests/mushroom_house/mushroom_house_barrels'],
  ['dungeons_arise:chests/mushroom_village/mushroom_village_normal', 'dungeons_arise:chests/mushroom_village/mushroom_village_barrels'],
  ['dungeons_arise:chests/mushroom_village/mushroom_village_weaponry', 'minecraft:chests/village/village_weaponsmith'],
  ['nova_structures:chests/illager_hideout_lesser_meat', 'nova_structures:chests/illager_hideout_meat'],
  ['nova_structures:chests/illager_hideout_raw_trash', 'nova_structures:chests/illager_hideout_trash'],
  ['nova_structures:chests/illager_hideout_raw_vegitarian', 'nova_structures:chests/illager_hideout_vegitarian'],
  ['nova_structures:chests/illager_hideout_raw_weaponry', 'nova_structures:chests/illager_hideout_weaponry'],
  ['nova_structures:chests/ruin_loot_1', 'nova_structures:chests/dungeon_1'],
  ['nova_structures:chests/ruin_loot_2', 'nova_structures:chests/dungeon_2'],
  ['nova_structures:chests/ruin_loot_3', 'nova_structures:chests/dungeon_3'],
  ['nova_structures:chests/ruin_loot_4', 'nova_structures:chests/dungeon_4'],
  ['nova_structures:chests/ruin_loot_5', 'nova_structures:chests/dungeon_5'],
  ['nova_structures:chests/ruin_loot_6', 'nova_structures:chests/dungeon_6'],
  ['nova_structures:chests/ruin_loot_7', 'nova_structures:chests/dungeon_7'],
  ['pet_home:chests/petshop_chest', 'redomesticate:chests/petshop_chest']               // Redomesticate
]

// ---------------------------------------------------------------- END OF DATA BLOCK

// Filled by LootJS.lootTables, read by LootJS.modifiers. Index = tier.
var GL_LOOT_IDS_BY_TIER = [[], [], [], [], [], []]

function glLootTierOf(id) {
  var i
  for (i = 0; i < GL_LOOT_SKIP.length; i++) {
    if (GL_LOOT_SKIP[i].test(id)) return 0
  }
  for (i = 0; i < GL_LOOT_TIER_RULES.length; i++) {
    if (GL_LOOT_TIER_RULES[i][0].test(id)) return GL_LOOT_TIER_RULES[i][1]
  }
  return 0
}

function glLootEscape(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function glLootCopyTable(event, id, source) {
  event.create(id).createPool(function (pool) {
    pool.addEntry(LootEntry.reference(source))
  })
}

function glLootCreateMissing(event) {
  var created = []
  var i, id, source
  for (i = 0; i < GL_LOOT_MISSING_TABLES.length; i++) {
    id = GL_LOOT_MISSING_TABLES[i][0]
    source = GL_LOOT_MISSING_TABLES[i][1]
    if (event.hasLootTable(id) || !event.hasLootTable(source)) continue
    try {
      glLootCopyTable(event, id, source)
      created.push(id)
    } catch (err) {
      console.error('[greenlanterns/loot] could not create ' + id + ': ' + err)
    }
  }
  return created
}

function glLootRef(tier) {
  return LootEntry.reference(GL_LOOT_INJECT + tier)
}

function glLootRefInDimension(tier, dimension) {
  return glLootRef(tier).when(function (c) {
    c.matchDimension(dimension)
  })
}

function glLootRefInStructures(tier, structures) {
  return glLootRef(tier).when(function (c) {
    c.matchCustomCondition({
      condition: 'minecraft:location_check',
      predicate: { structures: structures }
    })
  })
}

// One entry that rolls the right injected table: the first upgrade whose
// condition passes (highest tier first), otherwise the table's own tier.
// Built as nested two-child alternatives: alt(upgrade, alt(upgrade, base)).
function glLootRollEntry(tier) {
  var upgrades = []
  var up, i
  for (up = 5; up > tier; up--) {
    for (i = 0; i < GL_LOOT_DIMENSION_MIN_TIER.length; i++) {
      if (GL_LOOT_DIMENSION_MIN_TIER[i][1] === up) {
        upgrades.push(glLootRefInDimension(up, GL_LOOT_DIMENSION_MIN_TIER[i][0]))
      }
    }
    for (i = 0; i < GL_LOOT_STRUCTURE_MIN_TIER.length; i++) {
      if (GL_LOOT_STRUCTURE_MIN_TIER[i][1] === up) {
        try {
          upgrades.push(glLootRefInStructures(up, GL_LOOT_STRUCTURE_MIN_TIER[i][0]))
        } catch (err) {
          console.error('[greenlanterns/loot] structure rule skipped (' + GL_LOOT_STRUCTURE_MIN_TIER[i][0][0] + ' ...): ' + err)
        }
      }
    }
  }
  var result = glLootRef(tier)
  for (i = upgrades.length - 1; i >= 0; i--) {
    result = LootEntry.alternative(upgrades[i], result)
  }
  return result
}

// One modifier per batch of table ids (exact-match regex), so no pattern gets huge.
var GL_LOOT_BATCH = 60

function glLootAddBatch(event, tier, batch, n) {
  var pattern = '^(' + batch.map(glLootEscape).join('|') + ')$'
  event.addTableModifier(new RegExp(pattern)).pool(function (pool) {
    pool.name('greenlanterns_tier_' + tier + '_' + n)
    pool.rolls(1)
    pool.addEntry(glLootRollEntry(tier))
  })
}

function glLootAddTier(event, tier, ids) {
  var start, n = 0
  for (start = 0; start < ids.length; start += GL_LOOT_BATCH) {
    glLootAddBatch(event, tier, ids.slice(start, start + GL_LOOT_BATCH), n)
    n++
  }
  return n
}

LootJS.lootTables(function (event) {
  var created = glLootCreateMissing(event)
  var byTier = [[], [], [], [], [], []]
  var seen = {}
  var unclassified = []
  var it = event.getLootTableIds().iterator()
  var id, tier, i

  function classify(tableId) {
    if (seen[tableId]) return
    seen[tableId] = true
    tier = glLootTierOf(tableId)
    if (tier > 0) {
      byTier[tier].push(tableId)
    } else if (/chest/.test(tableId) && GL_LOOT_SKIP.every(function (r) { return !r.test(tableId) })) {
      unclassified.push(tableId)
    }
  }

  while (it.hasNext()) {
    id = String(it.next())
    classify(id)
  }
  for (i = 0; i < created.length; i++) classify(created[i])

  GL_LOOT_IDS_BY_TIER = byTier
  console.info('[greenlanterns/loot] created ' + created.length + ' missing tables; tier tables: ' +
    'T1=' + byTier[1].length + ' T2=' + byTier[2].length + ' T3=' + byTier[3].length +
    ' T4=' + byTier[4].length + ' T5=' + byTier[5].length)
  if (unclassified.length > 0) {
    console.info('[greenlanterns/loot] chest-like tables without a tier (not injected): ' + unclassified.join(', '))
  }
})

LootJS.modifiers(function (event) {
  var tier
  var total = 0
  var modifiers = 0
  for (tier = 1; tier <= 5; tier++) total += GL_LOOT_IDS_BY_TIER[tier].length
  if (total === 0) {
    console.error('[greenlanterns/loot] no classified tables: LootJS.lootTables did not run first, chest injection is off')
    return
  }
  for (tier = 1; tier <= 5; tier++) {
    modifiers += glLootAddTier(event, tier, GL_LOOT_IDS_BY_TIER[tier])
  }
  console.info('[greenlanterns/loot] chest injection active for ' + total + ' tables (' + modifiers + ' loot modifiers)')
})
