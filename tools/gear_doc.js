// Builds docs/Green-Lanterns-Armour-and-Weapons.docx from tools/gear_rows.json.
// Pipeline: boot with `/gl_dev exportgear` -> python -I tools/gear_data.py -> this script.
//   NODE_PATH=<scratch dir>/node_modules node tools/gear_doc.js      (needs `npm install docx@9` there)
const fs = require('fs')
const path = require('path')
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, HeadingLevel, Footer, PageNumber, VerticalAlign, TableLayoutType, PageOrientation, LevelFormat,
} = require('docx')

const ROOT = path.resolve(__dirname, '..')
const OUT = path.join(ROOT, 'docs', 'Green-Lanterns-Armour-and-Weapons.docx')
const mods = JSON.parse(fs.readFileSync(path.join(__dirname, 'gear_rows.json'), 'utf8'))

const GREEN = '1E6B3A', LIGHT = 'EEF6F0', GREY = '6B7280', LINE = 'C9D6CD', BODY = 17
const WIDTH = 16838 - 2 * 850   // landscape A4 minus 1.5 cm margins = 15138 DXA
const border = { style: BorderStyle.SINGLE, size: 4, color: LINE }
const borders = { top: border, bottom: border, left: border, right: border }
const pad = { top: 50, bottom: 50, left: 90, right: 90 }
const p = (runs, opts = {}) => new Paragraph({ children: runs, spacing: { before: 0, after: 0 }, ...opts })

// cols: [header, key, width, align('l'|'c'), bold?]
function table(cols, rows) {
  const sum = cols.reduce((n, c) => n + c[2], 0)
  if (sum !== WIDTH) throw new Error(`columns sum to ${sum}, not ${WIDTH}`)
  const cell = (text, c, fill, head) => new TableCell({
    width: { size: c[2], type: WidthType.DXA }, borders, margins: pad, verticalAlign: VerticalAlign.CENTER,
    shading: fill ? { fill, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    children: [p([new TextRun({ text: String(text ?? ''), size: head ? 17 : BODY, bold: head || c[4], color: head ? 'FFFFFF' : undefined })],
      { alignment: c[3] === 'c' ? AlignmentType.CENTER : AlignmentType.LEFT })],
  })
  return new Table({
    width: { size: WIDTH, type: WidthType.DXA }, columnWidths: cols.map(c => c[2]), layout: TableLayoutType.FIXED,
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true, children: cols.map(c => cell(c[0], c, GREEN, true)) }),
      ...rows.map((r, i) => new TableRow({ cantSplit: true, children: cols.map(c => cell(r[c[1]], c, i % 2 ? LIGHT : undefined, false)) })),
    ],
  })
}

const ARMOUR = [['Armour set / piece', 'name', 3300, 'l', true], ['Head', 'head', 800, 'c'], ['Chest', 'chest', 800, 'c'], ['Legs', 'legs', 800, 'c'],
  ['Feet', 'feet', 800, 'c'], ['Armour', 'armor', 900, 'c', true], ['Toughness', 'toughness', 1000, 'c'], ['Knockback res.', 'kb', 1100, 'c'],
  ['Durability', 'durability', 1200, 'c'], ['Bonuses (whole set)', 'bonuses', 4438, 'l']]
const MELEE = [['Weapon', 'name', 3200, 'l', true], ['Type', 'type', 1700, 'l'], ['Damage', 'damage', 900, 'c', true], ['Speed', 'speed', 900, 'c'],
  ['DPS', 'dps', 900, 'c'], ['Two-handed', 'two_handed', 1100, 'c'], ['Durability', 'durability', 1200, 'c'], ['Bonuses', 'bonuses', 5238, 'l']]
const RANGED = [['Ranged weapon', 'name', 4200, 'l', true], ['Durability', 'durability', 1500, 'c'], ['Enchantability', 'enchantability', 1600, 'c'],
  ['Bonuses', 'bonuses', 7838, 'l']]
const SHIELDS = [['Shield', 'name', 5000, 'l', true], ['Durability', 'durability', 1500, 'c'], ['Bonuses', 'bonuses', 8638, 'l']]
const BODYCOLS = [['Item', 'name', 4200, 'l', true], ['Mod', 'mod', 3000, 'l'], ['Armour', 'armor', 1100, 'c', true], ['Durability', 'durability', 1300, 'c'],
  ['Bonuses', 'bonuses', 5538, 'l']]
const GLANCE = [['Mod', 'mod', 5138, 'l', true], ['Armour sets', 'sets', 2000, 'c'], ['Armour pieces', 'pieces', 2000, 'c'], ['Melee weapons', 'melee', 2000, 'c'],
  ['Ranged', 'ranged', 2000, 'c'], ['Shields', 'shields', 2000, 'c']]

const total = k => mods.reduce((n, m) => n + m[k].length, 0)
const pieces = mods.reduce((n, m) => n + m.counts.armor_pieces, 0)
const text = (t, o = {}) => new TextRun({ text: t, size: 20, ...o })
const bullet = runs => new Paragraph({ numbering: { reference: 'dots', level: 0 }, spacing: { after: 40 }, children: runs })
const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun(t)] })
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] })
const label = t => p([new TextRun({ text: t, bold: true, size: 19, color: '2E7D4F' })], { spacing: { before: 160, after: 60 }, keepNext: true })
const intro = t => p([text(t, { color: '374151' })], { spacing: { after: 140 } })

const children = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun('Green Lanterns: Armour and Weapons')] }),
  p([text('Every armour set, weapon and shield in the pack, with the stats the game gives them. Updated 9 November 2026.', { color: GREY })], { spacing: { after: 160 } }),
  p([text(`${total('sets')} armour sets and single pieces (${pieces} items), ${total('melee')} melee weapons, ${total('ranged')} ranged weapons, ` +
    `${total('shields')} shields and ${total('body')} mount and pet armours from ${mods.length} mods. The stats were read from the running game, not copied from wikis.`)],
    { spacing: { after: 160 } }),
  h2('How to read the tables'),
  bullet([text('Armour', { bold: true }), text(': armour points per piece and for the whole set. 20 is a full diamond set; one chestplate icon on your HUD is 2 points.')]),
  bullet([text('Toughness', { bold: true }), text(' reduces damage from big hits. '), text('Knockback res.', { bold: true }), text(' is shown like the game shows it: 10 = never knocked back.')]),
  bullet([text('Damage', { bold: true }), text(' is per hit (2 = one heart). '), text('Speed', { bold: true }), text(' is attacks per second at full charge. '),
    text('DPS', { bold: true }), text(' is damage × speed: a rough guide that ignores critical hits, combos and enchantments.')]),
  bullet([text('Type', { bold: true }), text(' and '), text('Two-handed', { bold: true }), text(' come from Better Combat, which gives each weapon type its own swings and combos. Two-handed weapons need your off hand free.')]),
  bullet([text('Bonuses', { bold: true }), text(' are the extra stats a piece gives (spell power, mana, reach, speed…). For armour sets they are added up for the whole set.')]),
  bullet([text('Not included: ', { bold: true }), text('enchantments, Apotheosis affixes and gems (random on looted gear), and set bonuses that a mod adds in its own code. Items hidden from JEI are left out.')]),
  h2('At a glance'),
  table(GLANCE, mods.map(m => ({ mod: m.mod, sets: m.sets.length || '', pieces: m.counts.armor_pieces || '', melee: m.melee.length || '',
    ranged: m.ranged.length || '', shields: m.shields.length || '' }))),
]

children.push(h1('1. Armour'))
children.push(intro('Per mod, from the weakest to the strongest set. Rows with one piece are single items (a helmet design, a crown, a cloak) rather than a 4-piece set. Several numbers in one cell (like 2/3) mean that slot has more than one piece in the set.'))
for (const m of mods) if (m.sets.length) { children.push(h2(m.mod)); children.push(table(ARMOUR, m.sets)) }
const body = mods.flatMap(m => m.body.map(r => ({ ...r, mod: m.mod })))
if (body.length) { children.push(h2('Mount and pet armour')); children.push(table(BODYCOLS, body)) }

children.push(h1('2. Weapons'))
children.push(intro('Per mod, grouped by weapon type and sorted by damage. Ranged weapons follow each mod\'s melee table; their damage depends on the arrow or bolt and how far you draw, so only durability and enchantability are listed.'))
for (const m of mods) {
  if (!m.melee.length && !m.ranged.length) continue
  children.push(h2(m.mod))
  if (m.melee.length) children.push(table(MELEE, m.melee))
  if (m.ranged.length) { children.push(label('Ranged weapons')); children.push(table(RANGED, m.ranged)) }
}

children.push(h1('3. Shields'))
children.push(intro('Shield Expansion gives every shield a parry window and stamina; those numbers live in its own settings, not on the item, so this list shows durability and any extra stats.'))
for (const m of mods) if (m.shields.length) { children.push(h2(m.mod)); children.push(table(SHIELDS, m.shields)) }

const doc = new Document({
  creator: 'Green Lanterns', title: 'Green Lanterns: Armour and Weapons',
  numbering: { config: [{ reference: 'dots', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  styles: {
    default: { document: { run: { font: 'Calibri', size: 20 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal', run: { font: 'Calibri', size: 48, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 80 }, keepNext: true } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 34, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 100 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 25, bold: true, color: '2E7D4F' }, paragraph: { spacing: { before: 260, after: 90 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 850, bottom: 850, left: 850, right: 850 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: 'Green Lanterns: Armour and Weapons  ·  page ', size: 16, color: GREY }),
      new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
    ] })] }) },
    children,
  }],
})

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf)
  console.log(`wrote ${path.relative(ROOT, OUT)}: ${total('sets')} armour rows, ${total('melee')} melee, ${total('ranged')} ranged, ${total('shields')} shields, ${body.length} mount/pet`)
})
