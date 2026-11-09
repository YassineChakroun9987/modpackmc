// Builds docs/Green-Lanterns-Mod-List.docx: every mod in the pack, in MODLIST.md's five categories,
// with the main mods split by what they add. Side (Both / Server / Client) comes from mods-manifest.txt,
// and the script warns about any jar in the manifest that no row covers.
//
// Needs the `docx` npm package (not kept in the repo):
//   cd <scratch dir> && npm install docx@9
//   NODE_PATH=<scratch dir>/node_modules node tools/modlist_doc.js
const fs = require('fs')
const path = require('path')
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, HeadingLevel, Footer, PageNumber, VerticalAlign, TableLayoutType,
} = require('docx')

const ROOT = path.resolve(__dirname, '..')
const OUT = path.join(ROOT, 'docs', 'Green-Lanterns-Mod-List.docx')

// ---------------------------------------------------------------- data
// [name, version, description, jar regex (null = no jar of its own), side override]
const CATEGORIES = [
  {
    title: '1. Editing mods',
    intro: 'Tools we use to change the other mods: recipes, loot, tags, structure placement. Players see JEI; the rest works behind the scenes.',
    groups: [{ rows: [
      ['Just Enough Items (JEI)', '19.69.0.457', 'Recipe and item browser: look up any item, how to make it and what it\'s used for.', /^jei-/],
      ['KubeJS', '2101.7.2', 'Scripting tool: we use it to change recipes, tags and items, and to run the whole story engine.', /^kubejs-/],
      ['LootJS', '3.7.0', 'KubeJS add-on for editing loot tables and drops. Powers our tiered chest loot.', /^lootjs-/],
      ['Almost Unified', '1.4.2', 'Merges the same material from different mods (one copper, one tin, one steel...), so there are no duplicate items.', /^almostunified-/],
      ['Structurify', '2.0.43', 'Controls where structures spawn: stops them overlapping, spaces them out and checks for flat ground.', /^structurify-/],
    ] }],
  },
  {
    title: '2. Main mods',
    intro: 'The mods the pack is built around, split by what they add to the game.',
    groups: [
      { title: '2.1 Story, quests and classes', rows: [
        ['Create: Lanterns', '20.11-alpha', 'The heart of the story: power rings for every light of the emotional spectrum, lanterns, the crashed Lantern ship, and the planets Oa and Korugar. Private build.', /^createlanterns-/],
        ['Spectral Hub', 'v4', 'Create: Lanterns add-on: the spectrum screen (press J) that shows your light.', /^spectral_hub-/],
        ['FTB Quests', '2101.1.38', 'The quest book, "The Book of Oa": the story, the 7 class paths, the finale and a guide for each big mod.', /^ftb-quests-/],
        ['FTB Teams', '2101.1.12', 'Parties: team up with friends to share quest progress. Land claims use the same teams.', /^ftb-teams-/],
        ['FTB XMod Compat', '21.1.14', 'Connects the quest book to our story scripts, so story events complete quests.', /^ftb-xmod-compat-/],
        ['Pufferfish\'s Skills', '0.19.2', 'Skill trees (press K): an Adventurer tree for everyone plus one tree per class, levelled with class XP.', /^puffish_skills-/],
        ['Pufferfish\'s Unofficial Additions', '2.2.8', 'More ways to earn skill XP and more reward types for the skill trees.', /^pufferfish_unofficial_additions-/],
        ['Pufferfish\'s Attributes', '0.8.3', 'Extra stats that skill-tree nodes can give: sprint speed, mining speed, healing and more.', /^puffish_attributes-/],
      ] },
      { title: '2.2 Combat and gear', rows: [
        ['Better Combat', '2.4.0', 'Weapon movesets: combos, sweeping swings, two-handed weapons and dual wielding.', /^bettercombat-/],
        ['Combat Roll', '2.0.6', 'A dodge roll with a cooldown, which enchantments can improve.', /^combat_roll-/],
        ['Simply Swords', '1.70.2', '15 weapon types in every material, plus about 40 unique legendary weapons found in loot.', /^simplyswords-/],
        ['Dungeons Weapons', '9.0.1', 'Weapons from Minecraft Dungeons: the Stormlander, the Soul Scythe and many more.', /^minecraftdungeonsv1-/],
        ['Epic Knights', '10.17', 'Medieval armour (plate, chainmail, light), shields, lances and flails. Armour can be dyed and decorated.', /^epic-knights-/],
        ['Shield Expansion', '1.4.3', 'Shields can parry, use stamina and come in tiers.', /^shieldexp-/],
        ['Apotheosis', '8.9.0', 'Gear progression: loot with random bonuses and rarities, gems and sockets, elite bosses, and world tiers that raise the challenge.', /^Apotheosis-/],
        ['Apothic Attributes', '2.11.0', 'The stat system behind Apotheosis (critical hits, life steal, armour piercing) with a full stats screen.', /^ApothicAttributes-/],
        ['Apothic Enchanting', '1.6.4', 'Reworked enchanting: bookshelves with their own stats and higher enchantment levels.', /^ApothicEnchanting-/],
        ['Apothic Spawners', '1.4.0', 'Mob spawners can be mined, moved and upgraded.', /^ApothicSpawners-/],
        ['Artifacts', '13.2.5', 'About 40 rare trinkets worn in accessory slots, found in chests. Watch out for Mimics.', /^artifacts-/],
      ] },
      { title: '2.3 Magic', rows: [
        ['Iron\'s Spells \'n Spellbooks', '3.16.3', 'The magic system: spellbooks, scrolls, mana, the inscription table, mage armour, wizard towers and boss mages. Each class draws on its own schools of magic.', /^irons_spellbooks-/],
        ['Cataclysm: Spellbooks', '1.1.11', 'Spells, spellbooks and armour made from Cataclysm boss materials.', /^cataclysm_spellbooks-/],
        ['Discerning the Eldritch', '1.4.5', 'Expands the Eldritch school: the Violet path\'s late-game spells and gear.', /^discerning_the_eldritch-/],
        ['Alshanex\'s Familiars', '5.0', 'Summonable familiars that fight beside you and level up. The core of the Indigo beast master.', /^alshanex_familiars-/],
        ['Galosphere Spellbooks', '1.1.5', 'Spellbooks and gear made from Galosphere\'s crystals.', /^galosphere_spellbooks-/],
      ] },
      { title: '2.4 Bosses', rows: [
        ['L_Ender\'s Cataclysm', '3.33', 'Huge bosses in their own structures: Ignis, the Netherite Monstrosity, the Leviathan, Scylla and more. The Harbinger is the Yellow trial boss.', /^L_Enders-Cataclysm-/],
        ['Bosses of Mass Destruction', '1.3.3', 'Four big bosses: the Night Lich (Blue trial), the Nether Gauntlet (Red trial), the Obsidilith and the Void Blossom.', /^BOMD-/],
        ['Mowzie\'s Mobs', '1.8.2', 'Memorable bosses and creatures: Frostmaw, the Ferrous Wroughtnaut, Umvuthi, the Sculptor and more.', /^mowziesmobs-/],
        ['Kings & Monsters', '1.2.2', 'Ogre country and the Ogre King (Orange trial).', /^kingsandmonsters/],
        ['The Graveyard', '4.0.1', 'Graveyards, crypts and the undead. Its Lich is "the Corrupted Champion" (Violet trial).', /^graveyard-/],
        ['Legendary Monsters', '2.2.4', 'Legendary bosses in their own arenas. Its guide book tells you where to find them.', /^legendary_monsters-/],
        ['Mutant Monsters', '21.1.1', 'Mutant zombie, skeleton, creeper and enderman mini-bosses.', /^MutantMonsters-/],
        ['DarkDoppelganger', '4.0.0', 'A boss that copies you and casts your own spells back at you.', /^darkdoppelganger-/],
        ['Devourer of Gods', '1.2.0', 'The final boss: a cosmic worm about 335 blocks long, summoned with a Cosmic Worm.', /^dog-/],
      ] },
      { title: '2.5 Mobs, dragons and pets', rows: [
        ['Alex\'s Mobs Continued', '2.3.0', 'About 90 animals and creatures, many of them tameable.', /^alexsmobs-/],
        ['Born in Chaos', '1.7.6', 'Dark-fantasy monsters and bosses, such as Lord Pumpkinhead and the Supreme Bonescaller.', /^born_in_chaos_/],
        ['Ice and Fire: Community Edition', '2.0', 'Fire, ice and lightning dragons you can tame and ride, plus the Hydra (Indigo trial), sea serpents and more.', /^iceandfire-/],
        ['Book of Dragons', '1.4.1', 'Tameable dragons from the How to Train Your Dragon world: Night Fury, Gronckle and more.', /^bookofdragons-/],
        ['Companions!', '1.3.7', 'New companion creatures you can tame.', /^companions-/],
        ['Redomesticate', '2.0.0', 'Better pets: pet beds, pet enchantments and pet commands.', /^redomesticate-/],
      ] },
      { title: '2.6 World: terrain, dimensions and events', rows: [
        ['Terralith', '2.6.2', 'New Overworld terrain and about 99 biomes (Skylands, Moonlight Grove, Amethyst Canyon...), built from vanilla blocks.', /^Terralith_/],
        ['Nullscape', '1.2.14', 'A surreal End: tall floating islands and 3 new biomes.', /^Nullscape_/],
        ['Jaden\'s Nether Expansion', '2.4.1', 'Reworked Nether biomes with new blocks, mobs and structures.', /^Jadens-Nether-Expansion-/],
        ['Galosphere', '1.5.5', 'New caves (Crystal Canyons, Lichen Caves, Pink Salt) with silver ore and magic crystals.', /^Galosphere-/],
        ['The Twilight Forest', '4.8.3345', 'A whole new dimension with a chain of bosses (Naga, Lich, Minoshroom, Hydra, Ur-Ghast, Snow Queen...). Part of the finale.', /^twilightforest-/],
        ['Enhanced Celestials 2 (Core + Default Lunar Events)', '2.0.3.4 · 2.0.1.4', 'Blood, blue, harvest and super moons that change what happens at night.', /^Enhanced-Celestials-2-/],
      ] },
      { title: '2.7 Structures and dungeons', rows: [
        ['YUNG\'s Better Dungeons', '5.1.4', 'Redesigned spawner dungeons.', /^YungsBetterDungeons-/],
        ['YUNG\'s Better Mineshafts', '5.1.1', '13 mineshaft styles that match the biome around them.', /^YungsBetterMineshafts-/],
        ['YUNG\'s Better Strongholds', '5.1.3', 'Huge redesigned strongholds with more than 15 room types.', /^YungsBetterStrongholds-/],
        ['YUNG\'s Better Nether Fortresses', '3.1.5', 'Redesigned Nether fortresses.', /^YungsBetterNetherFortresses-/],
        ['YUNG\'s Better Ocean Monuments', '4.1.2', 'Redesigned ocean monuments.', /^YungsBetterOceanMonuments-/],
        ['YUNG\'s Better Desert Temples', '4.1.5', 'Desert temples with puzzles.', /^YungsBetterDesertTemples-/],
        ['YUNG\'s Better Jungle Temples', '3.1.2', 'Jungle temples with traps.', /^YungsBetterJungleTemples-/],
        ['YUNG\'s Better Witch Huts', '4.1.1', 'Redesigned witch huts and witch circles.', /^YungsBetterWitchHuts-/],
        ['YUNG\'s Better End Island', '3.1.2', 'A redesigned main End island. The dragon is summoned at a bell tower.', /^YungsBetterEndIsland-/],
        ['YUNG\'s Extras', '5.1.1', 'Small Overworld structures and decorations.', /^YungsExtras-/],
        ['YUNG\'s Bridges', '5.1.1', 'Bridges over rivers.', /^YungsBridges-/],
        ['Dungeons and Taverns', 'v4.4.4', '97 structures: taverns, crypts, combat-trial shrine towers, illager manors and a Nether keep.', /^dungeons-and-taverns-/],
        ['When Dungeons Arise', '2.1.68', '40 huge dungeons: sky fortresses, the Mechanical Nest, the Foundry, the Coliseum and more.', /^DungeonsArise-/],
        ['When Dungeons Arise: Seven Seas', '1.0.4', 'Pirate and naval ships to raid at sea.', /^DungeonsAriseSevenSeas-/],
        ['The Lost Castle', '2.1.0', 'One huge, rare castle dungeon far from spawn.', /^tlc-/],
        ['Philips Ruins', '2.0', '17 kinds of ruins with loot: crypts, dungeons and towers.', /^Philips-Ruins/],
        ['Grim Kingdoms (Vanilla Edition)', '2.0.0', '65 lost-kingdom ruins, watchtowers and camps.', /^grim-kingdoms-/],
        ['Ember\'s Castles and Keeps', '1.0.9.1', 'Towers and keeps, including an undead castle and pillager towers.', /^castles_and_keeps-/],
        ['Ember\'s Floating Islands', '1.5.3', '17 kinds of floating sky islands.', /^floating_islands-/],
        ['Sky Whale Ship', '1.0.3', 'Giant flying whale ships with an arena on board.', /^sky_whale_ship-/],
        ['Castle in the Sky', '1.21.1.1', 'One floating castle dungeon with coloured keys and doors, found with a levitation stone.', /^castle_in_the_sky-/],
        ['Eternal Nether', '21.1.3', 'Nether exploration: a citadel, a piglin manor and catacombs, plus new mobs.', /^EternalNether-/],
      ] },
      { title: '2.8 Villages', rows: [
        ['Epic Structures: Villages', '2.0.0', 'Rebuilds the classic villages as large medieval towns with churches, windmills and walls. The story starts in one.', /^epic-structures-villages-/],
        ['ChoiceTheorem\'s Overhauled Village (CTOV)', '3.6.4', 'Overhauled villages for 21 biomes in small, medium and large sizes, some fortified, plus pillager outposts.', /^\[neoforge\]ctov-/],
        ['Towns and Towers', '1.13.11', 'Extra village styles and pillager outposts for many biomes.', /^t_and_t-/],
        ['Sky Villages', '1.0.6', 'Floating villages high above the land.', /^SkyVillages-/],
        ['Village Spawn Point', '6.0', 'Starts new worlds in a village. Our story script then moves you to the nearest medieval town.', /^villagespawnpoint-/],
        ['Guard Villagers', '2.4.12', 'Give a villager a sword or crossbow and it becomes a guard. Your defence in the prologue\'s raid.', /^guardvillagers-/],
      ] },
      { title: '2.9 Tech, Create and space', rows: [
        ['Create', '6.0.10', 'Machines, conveyors and trains built from moving parts. The Yellow path\'s home mod.', /^create-1\.21\.1-/],
        ['Sable', '2.0.6', 'The physics engine that airships and Create: Lanterns\' planets are built on.', /^sable-/],
        ['Create Aeronautics', '1.3.2', 'Airships: propellers, balloons and levitite. Includes Create: Simulated and Create: Offroad.', /^create-aeronautics-bundled-/],
        ['Create Cosmonautics', '26.08.307 (beta)', 'Space: rockets, thrusters, titanium ore, the Moon and deep space. Makes Oa and Korugar real worlds you can fly to.', /^cosmonautics-/],
        ['Create Crafts & Additions', '1.7.2', 'Electricity for Create: generators, motors and wires.', /^createaddition-/],
        ['Mekanism + Generators', '10.7.19', 'Ore processing (up to 5 times the output), power generation and the MekaSuit.', /^Mekanism(Generators)?-/],
        ['Applied Energistics 2', '19.2.18', 'Digital storage networks.', /^appliedenergistics2-/],
        ['Draconic Evolution', '3.1.4', 'Endgame tech and armour. Its Chaos Guardian drops the shards that unlock the final boss.', /^Draconic-Evolution-/],
      ] },
      { title: '2.10 Farming and food', rows: [
        ['Farmer\'s Delight', '1.3.4', 'Cooking: new crops, the cooking pot and skillet, meals and feasts.', /^FarmersDelight-/],
      ] },
    ],
  },
  {
    title: '3. Dependencies',
    intro: 'Libraries that are only here because another mod needs them. They add nothing by themselves.',
    groups: [{ rows: [
      ['Rhino', '2101.2.7', 'The JavaScript engine KubeJS runs on.', /^rhino-/],
      ['mezz_config', '0.6.6', 'Settings library. It ships inside the JEI jar.', null, 'Both'],
      ['Better Advanced Tooltips', '2101.1.0', 'Extra tooltip details for KubeJS.', /^better-advanced-tooltips-/],
      ['Bookshelf', '21.1.81', 'Shared code for AttributeFix and Enchantment Descriptions.', /^bookshelf-/],
      ['Prickle', '21.1.11', 'Settings library for AttributeFix and Enchantment Descriptions.', /^prickle-/],
      ['Searchables', '1.0.2', 'Search library for Controlling.', /^Searchables-/],
      ['Lithostitched', '1.8.1', 'World-generation library for Terralith and CTOV.', /^lithostitched-/],
      ['YUNG\'s API', '5.1.9', 'Shared code for all YUNG\'s mods and Traveler\'s Titles.', /^YungsApi-/],
      ['Lodestone', '1.8.2', 'Effects library for Jaden\'s Nether Expansion.', /^lodestone-/],
      ['Elysium API', '2.0.1', 'Library for Jaden\'s Nether Expansion.', /^ElysiumAPI-/],
      ['YetAnotherConfigLib', '3.8.2', 'Settings screens for Structurify.', /^yet_another_config_lib_v3-/],
      ['Resourceful Config', '3.0.11', 'Settings library for Structure Layout Optimizer.', /^resourcefulconfig-/],
      ['Cristel Lib', '3.1.7', 'Library for Towns and Towers.', /^cristellib-/],
      ['Cloth Config API', '15.0.140', 'Settings screens for Better Combat, Bosses of Mass Destruction, Epic Knights and others.', /^cloth-config-/],
      ['Architectury API', '13.0.11', 'Shared code for the FTB mods, Sky Villages, Simply Swords and Epic Knights.', /^architectury-/],
      ['Puzzles Lib', '21.1.66', 'Library for Eternal Nether and Mutant Monsters.', /^puzzleslib-/],
      ['Curios API', '9.5.1', 'Accessory slots (rings, necklace, back, spellbook...) used by many mods, including the Lantern rings.', /^curios-/],
      ['GeckoLib', '4.9.3', 'Animation engine for many creature and boss mods.', /^geckolib-/],
      ['Player Animator', '2.0.4', 'Player animations for Better Combat, Combat Roll and Iron\'s Spells.', /^player-animation-lib-/],
      ['AzureLib', '3.2.7', 'Animation library for Cataclysm: Spellbooks and Discerning the Eldritch.', /^azurelib-/],
      ['Iron\'s Lib', '2.3.0', 'Shared code for Iron\'s Spells.', /^irons_lib-/],
      ['Ace\'s Spell Utils', '1.2.7.5', 'Spell helpers for Iron\'s Spells add-ons.', /^aces_spell_utils-/],
      ['FamiliarsLib', '2.0', 'Library for Alshanex\'s Familiars.', /^familiarslib-/],
      ['Lionfish API', '3.1', 'Library for L_Ender\'s Cataclysm.', /^lionfishapi-/],
      ['Cerbons API', '1.3.0', 'Library for Bosses of Mass Destruction.', /^CerbonsAPI-/],
      ['CodxLib', '1.6.1', 'Library for Alex\'s Mobs Continued.', /^codxlib-/],
      ['Jupiter + Uranus', '2.3.7 · 2.4.1', 'Libraries for Ice and Fire.', /^(jupiter|uranus)-/],
      ['FAUNA Engine', '1.1', 'Creature engine for Book of Dragons.', /^faunaengine-/],
      ['Knight Lib', '2.0.5', 'Library for Companions!.', /^knightlib-/],
      ['VillagersTradingPlus', '1.1.1', 'Villager trading library needed by The Graveyard.', /^villagertradingplus-/],
      ['Patchouli', '93', 'In-game guide books (used by Kings & Monsters).', /^Patchouli-/],
      ['Placebo', '9.9.4', 'Shared code for Apotheosis and the Apothic mods.', /^Placebo-/],
      ['Fzzy Config', '0.7.7', 'Settings library for Simply Swords.', /^fzzy_config-/],
      ['Kotlin for Forge', '5.12.0', 'Kotlin language support, needed by Fzzy Config.', /^kotlinforforge-/],
      ['Collective', '8.84', 'Shared code for Village Spawn Point.', /^collective-/],
      ['CorgiLib + Data Anchor', '5.0.0.10 · 2.0.0.18', 'Libraries for Enhanced Celestials 2.', /^(Corgilib|Data_Anchor)-/],
      ['GuideME', '21.1.22', 'The in-game guide for Applied Energistics 2.', /^guideme-/],
      ['Brandon\'s Core + CodeChicken Lib', '3.2.1 · 4.6.1', 'Libraries for Draconic Evolution.', /^(BrandonsCore|CodeChickenLib)-/],
      ['Sophisticated Core', '1.5.31', 'Shared code for Sophisticated Backpacks.', /^sophisticatedcore-/],
      ['Balm', '21.0.67', 'Library for Waystones.', /^balm-/],
      ['FTB Library', '2101.1.39', 'Shared code for all the FTB mods.', /^ftb-library-/],
      ['Simply Tooltips', '0.1.5', 'Tooltips for Simply Swords.', /^SimplyTooltips-/],
    ] }],
  },
  {
    title: '4. Our own mods',
    intro: 'What we built ourselves to tie the pack together. These are scripts and data on the server, not separate mod files.',
    groups: [{ rows: [
      ['Green Lanterns story engine', 'KubeJS scripts', 'The prologue (7-day raid, Warlord Vex, the crashed Lantern), the story NPCs, joining classes, the ring trial (class, White or Black ring), the story town and the /gl commands.', null, 'Server'],
      ['Class skill trees', 'data pack', 'The Adventurer tree and the 7 class trees for Pufferfish\'s Skills.', null, 'Server'],
      ['Tiered loot', 'data pack + KubeJS', 'Structure chests get loot by difficulty (5 tiers), with items from every gear and magic mod, and better rolls with Luck.', null, 'Server'],
      ['The Book of Oa', 'FTB Quests chapters', '26 chapters and 646 quests: the story, the classes, the finale and the mod guides.', null, 'Server'],
      ['Pack glue', 'KubeJS', 'Fixes and small features: tag fixes, hidden unused items, the Cosmic Worm recipe, party sync, and corpse quick-loot.', null, 'Server'],
    ] }],
  },
  {
    title: '5. Quality of life',
    intro: 'Makes playing smoother without adding content. Several of these are only in the players\' games.',
    groups: [
      { title: '5.1 Performance', rows: [
        ['ModernFix', '5.27.27', 'Faster startup, lower memory use and many bug fixes.', /^modernfix-/],
        ['FerriteCore', '7.0.3', 'Cuts memory use a lot.', /^ferritecore-/],
        ['Packet Fixer', '3.3.1', 'Raises network limits so big modded data doesn\'t kick players.', /^packetfixer-/],
        ['spark', '1.10.124', 'Performance profiler for tracking down lag.', /^spark-/],
        ['Chunky', '1.4.23', 'Pre-generates the world so exploring doesn\'t lag.', /^Chunky-/],
        ['Structure Layout Optimizer', '1.0.12', 'Generates big structures faster.', /^structure_layout_optimizer-/],
        ['Clumps', '19.0.0.1', 'Merges XP orbs into one: less lag after big fights.', /^Clumps-/],
        ['Sodium', '0.8.13', 'A new renderer: much higher FPS.', /^sodium-/],
        ['ImmediatelyFast', '1.6.15', 'Faster rendering of the HUD, text and entities.', /^ImmediatelyFast-/],
        ['Entity Culling', '1.11.3', 'Skips drawing mobs and blocks you can\'t see.', /^entityculling-/],
      ] },
      { title: '5.2 Gameplay', rows: [
        ['Jade', '15.10.6', 'Shows what you\'re looking at: the block or mob, its health and which mod it comes from.', /^Jade-/],
        ['AppleSkin', '3.0.9', 'Shows how much hunger and saturation food gives.', /^appleskin-/],
        ['AttributeFix', '21.1.3', 'Removes vanilla stat caps so RPG gear can go higher.', /^attributefix-/],
        ['Lootr', '1.11.38', 'Every player gets their own loot from each structure chest: no loot stealing.', /^lootr-/],
        ['Waystones', '21.1.46', 'Teleport between the waystones you\'ve found.', /^waystones-/],
        ['Xaero\'s Minimap + World Map', '26.6.0 · 1.47.0', 'A minimap with waypoints and a full world map (press M).', /^xaero(minimap|worldmap)-/],
        ['Open Parties and Claims', '0.33.0', 'Claim land so nobody can grief it. Uses your FTB party.', /^open-parties-and-claims-/],
        ['Sophisticated Backpacks', '3.26.20', 'Upgradeable backpacks: pickup, magnet, feeding, crafting and more.', /^sophisticatedbackpacks-/],
        ['Corpse', '1.1.22', 'When you die, your items stay in your body. Right-click your own body to get everything back in place; Shift + right-click to open it.', /^corpse-/],
        ['FTB Ultimine', '2101.1.15', 'Hold ` to mine a whole ore vein or tree at once.', /^ftb-ultimine-/],
        ['Polymorph', '1.1.0', 'Pick which result you get when two mods\' recipes overlap.', /^polymorph-/],
        ['Enchantment Descriptions', '21.1.11', 'Every enchantment explains itself in its tooltip.', /^enchdesc-/],
        ['Controlling', '19.0.5', 'Searchable key-binding menu that shows conflicts.', /^Controlling-/],
        ['Mouse Tweaks', '2.26.1', 'Drag and scroll to move items in inventories.', /^MouseTweaks-/],
        ['Traveler\'s Titles', '5.1.3', 'An RPG-style title on screen when you enter a new biome or dimension.', /^TravelersTitles-/],
      ] },
    ],
  },
]

// ---------------------------------------------------------------- sides from the manifest
const SIDE_LABEL = { both: 'Both', server: 'Server', client: 'Client' }
const manifest = fs.readFileSync(path.join(ROOT, 'mods-manifest.txt'), 'utf8').split(/\r?\n/)
  .filter(l => l.trim() && !l.startsWith('#')).map(l => { const p = l.trim().split(/\s+/); return { side: p[0], jar: p[1] } })
const used = new Set()
let problems = 0
for (const cat of CATEGORIES) for (const g of cat.groups) for (const r of g.rows) {
  const [name, , , re, override] = r
  if (!re) { r.side = override; continue }
  const hits = manifest.filter(m => re.test(m.jar))
  if (!hits.length) { console.warn('NO JAR for', name); problems++; r.side = '?'; continue }
  const sides = [...new Set(hits.map(h => h.side))]
  if (sides.length > 1) console.warn('mixed sides for', name, sides)
  hits.forEach(h => used.add(h.jar))
  r.side = SIDE_LABEL[sides[0]] || sides[0]
}
for (const m of manifest) if (!used.has(m.jar)) { console.warn('NOT IN DOC:', m.jar); problems++ }

// ---------------------------------------------------------------- layout
const GREEN = '1E6B3A', LIGHT = 'EEF6F0', GREY = '6B7280', LINE = 'C9D6CD'
const W = { mod: 2750, desc: 5788, side: 1100 }          // = 9638 DXA: A4 minus 2 cm margins
const TOTAL = W.mod + W.desc + W.side
const border = { style: BorderStyle.SINGLE, size: 4, color: LINE }
const borders = { top: border, bottom: border, left: border, right: border }
const pad = { top: 70, bottom: 70, left: 110, right: 110 }

function cell(children, width, fill, opts = {}) {
  return new TableCell({
    children, width: { size: width, type: WidthType.DXA }, borders, margins: pad,
    verticalAlign: opts.vAlign || VerticalAlign.TOP,
    shading: fill ? { fill, type: ShadingType.CLEAR, color: 'auto' } : undefined,
  })
}
const p = (runs, opts = {}) => new Paragraph({ children: runs, spacing: { before: 0, after: 0 }, ...opts })

function headerRow(first) {
  const h = t => p([new TextRun({ text: t, bold: true, color: 'FFFFFF', size: 19 })])
  return new TableRow({ tableHeader: true, cantSplit: true, children: [
    cell([h(first)], W.mod, GREEN), cell([h('What it does')], W.desc, GREEN), cell([h('Side')], W.side, GREEN),
  ] })
}

function modTable(rows, first) {
  return new Table({
    width: { size: TOTAL, type: WidthType.DXA }, columnWidths: [W.mod, W.desc, W.side], layout: TableLayoutType.FIXED,
    rows: [headerRow(first), ...rows.map((r, i) => {
      const fill = i % 2 ? LIGHT : undefined
      return new TableRow({ cantSplit: true, children: [
        cell([p([new TextRun({ text: r[0], bold: true, size: 19 })]), p([new TextRun({ text: r[1], size: 15, color: GREY })])], W.mod, fill),
        cell([p([new TextRun({ text: r[2], size: 19 })])], W.desc, fill),
        cell([p([new TextRun({ text: r.side, size: 18 })])], W.side, fill),
      ] })
    })],
  })
}

const count = cat => cat.groups.reduce((n, g) => n + g.rows.length, 0)
const total = CATEGORIES.reduce((n, c) => n + count(c), 0)

const children = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun('Green Lanterns: Mod List')] }),
  p([new TextRun({ text: 'Every mod in the pack, grouped by what it\'s for. Updated 9 November 2026.', color: GREY, size: 21 })], { spacing: { after: 200 } }),
  p([new TextRun({ text: `The pack has ${total} entries in five categories (${manifest.length} mod files; a few entries cover two files that belong together). The main mods are split by what they add to the game.`, size: 21 })], { spacing: { after: 120 } }),
  p([new TextRun({ text: 'The Side column says where a mod is installed: ', size: 21 }),
     new TextRun({ text: 'Both', bold: true, size: 21 }), new TextRun({ text: ' = the server and every player\'s game; ', size: 21 }),
     new TextRun({ text: 'Server', bold: true, size: 21 }), new TextRun({ text: ' = only the server, players don\'t need it; ', size: 21 }),
     new TextRun({ text: 'Client', bold: true, size: 21 }), new TextRun({ text: ' = only in players\' games (graphics, controls, performance).', size: 21 })],
    { spacing: { after: 240 } }),
  new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun('At a glance')] }),
  new Table({
    width: { size: TOTAL, type: WidthType.DXA }, columnWidths: [W.mod, W.desc, W.side], layout: TableLayoutType.FIXED,
    rows: [
      new TableRow({ tableHeader: true, children: [
        cell([p([new TextRun({ text: 'Category', bold: true, color: 'FFFFFF', size: 19 })])], W.mod, GREEN),
        cell([p([new TextRun({ text: 'What\'s in it', bold: true, color: 'FFFFFF', size: 19 })])], W.desc, GREEN),
        cell([p([new TextRun({ text: 'Entries', bold: true, color: 'FFFFFF', size: 19 })])], W.side, GREEN),
      ] }),
      ...CATEGORIES.map((c, i) => new TableRow({ children: [
        cell([p([new TextRun({ text: c.title.replace(/^\d+\.\s*/, ''), bold: true, size: 19 })])], W.mod, i % 2 ? LIGHT : undefined),
        cell([p([new TextRun({ text: c.groups.length > 1 ? c.groups.map(g => g.title.replace(/^[\d.]+\s*/, '')).join(' · ') : c.intro, size: 19 })])], W.desc, i % 2 ? LIGHT : undefined),
        cell([p([new TextRun({ text: String(count(c)), size: 19 })])], W.side, i % 2 ? LIGHT : undefined),
      ] })),
    ],
  }),
]

for (const cat of CATEGORIES) {
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun(cat.title)] }))
  children.push(p([new TextRun({ text: cat.intro, size: 21, color: '374151' })], { spacing: { after: 160 } }))
  const first = cat.title.startsWith('3.') ? 'Library' : 'Mod'
  for (const g of cat.groups) {
    if (g.title) children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(g.title)] }))
    children.push(modTable(g.rows, first))
  }
}

const doc = new Document({
  creator: 'Green Lanterns', title: 'Green Lanterns: Mod List',
  styles: {
    default: { document: { run: { font: 'Calibri', size: 21 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal', run: { font: 'Calibri', size: 52, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 80 }, keepNext: true } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 34, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 100 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 25, bold: true, color: '2E7D4F' }, paragraph: { spacing: { before: 280, after: 100 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: 'Green Lanterns: Mod List  ·  page ', size: 16, color: GREY }),
      new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
    ] })] }) },
    children,
  }],
})

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf)
  console.log(`wrote ${path.relative(ROOT, OUT)}: ${total} entries, ${manifest.length} jars in the manifest, ${problems} problem(s)`)
})
