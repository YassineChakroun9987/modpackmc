// Builds docs/Green-Lanterns-Story-and-Classes.docx from tools/classbook.json (python -I tools/classbook_data.py).
//   NODE_PATH=<scratch dir>/node_modules node tools/classbook_doc.js      (needs `npm install docx@9` there)
const fs = require('fs')
const path = require('path')
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, HeadingLevel, Footer, PageNumber, VerticalAlign, TableLayoutType, LevelFormat,
} = require('docx')

const ROOT = path.resolve(__dirname, '..')
const OUT = path.join(ROOT, 'docs', 'Green-Lanterns-Story-and-Classes.docx')
const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'classbook.json'), 'utf8'))

const GREEN = '1E6B3A', LIGHT = 'EEF6F0', GREY = '6B7280', LINE = 'C9D6CD'
const COLOR = { red: 'C0392B', orange: 'D35400', yellow: 'B7950B', green: '1E8449', blue: '2471A3', indigo: '3F3FA8', violet: '7D3C98' }
const WIDTH = 11906 - 2 * 1000
const border = { style: BorderStyle.SINGLE, size: 4, color: LINE }
const borders = { top: border, bottom: border, left: border, right: border }
const pad = { top: 60, bottom: 60, left: 100, right: 100 }

const run = (t, o = {}) => new TextRun({ text: String(t ?? ''), size: 19, ...o })
const para = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [runs], spacing: { before: 0, after: 40 }, ...o })
const body = (t, o = {}) => para([run(t, { size: 20, ...o })], { spacing: { after: 120 } })
const bullet = (runs, size = 20) => new Paragraph({ numbering: { reference: 'dots', level: 0 }, spacing: { after: 30 },
  children: (Array.isArray(runs) ? runs : [run(runs, { size })]) })
const h1 = (t, color, br = true) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: br, children: [new TextRun({ text: t, color })] })
const h2 = (t, color) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, color })] })
const h3 = t => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(t)] })

function cell(children, width, fill, head) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders, margins: pad, verticalAlign: head ? VerticalAlign.CENTER : VerticalAlign.TOP,
    shading: fill ? { fill, type: ShadingType.CLEAR, color: 'auto' } : undefined, children,
  })
}
// cols: [header, width]; rows: arrays of cell-children arrays
function table(cols, rows, headFill = GREEN) {
  const sum = cols.reduce((n, c) => n + c[1], 0)
  if (sum !== WIDTH) throw new Error(`columns sum to ${sum}, not ${WIDTH}`)
  return new Table({
    width: { size: WIDTH, type: WidthType.DXA }, columnWidths: cols.map(c => c[1]), layout: TableLayoutType.FIXED,
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true, children: cols.map(c => cell([para([run(c[0], { bold: true, color: 'FFFFFF', size: 18 })])], c[1], headFill, true)) }),
      ...rows.map((r, i) => new TableRow({ cantSplit: true, children: r.map((ch, j) => cell(ch, cols[j][1], i % 2 ? LIGHT : undefined)) })),
    ],
  })
}
const spacer = () => para([run('')], { spacing: { after: 80 } })

// ---------------------------------------------------------------- quest tables
const QCOLS = [['Quest', 2300], ['Story and what to do', 5000], ['Rewards', 2606]]
function questRows(quests) {
  return quests.map(q => [
    [para([run(q.title, { bold: true })])],
    [para([run(q.desc, { italics: true, color: '374151', size: 18 })]),
      para([run('Do: ', { bold: true, size: 18 }), run(q.tasks, { size: 18 })]),
      ...(q.after ? [para([run('After: ' + q.after, { size: 16, color: GREY })])] : [])],
    [para([run(q.rewards, { size: 18 })])],
  ])
}

// ---------------------------------------------------------------- content
const children = []
children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun('Green Lanterns: Story and Classes')] }))
children.push(body('The main questline, the seven lights (classes) with their quests, skill trees and gear, and how each one levels up. ' +
  'Everything here is read from the actual quest book and skill-tree files, so it is what players will see. Updated 9 November 2026.', { color: GREY }))
children.push(h2('How the story flows'))
const flow = [
  ['Prologue: The Seventh Dawn', 'You wake in a medieval town with 7 days until a pillager Warband attacks. Prepare, find Warlord Vex\'s outpost, win the raid. Killing Vex makes a green star fall: a crashed Green Lantern ship.'],
  ['Act I: Proving Ground', 'The dying Lantern, Kaelen, tells you about the corruption and the seven lights. You gear up, learn magic, explore, and choose one (or more) lights to follow.'],
  ['The class paths', 'Each light has its own chapter. At class level 10 the light whispers, at 25 you dream of it. Then you face that light\'s trial boss and a ring trial: four role-play choices that give you the class ring, or the White or Black ring.'],
  ['The Last Light (finale)', 'The Twilight Forest boss chain, the Chaos Guardian, and finally the Devourer of Gods, a cosmic worm about 335 blocks long.'],
]
flow.forEach(([t, d]) => children.push(bullet([run(t + ': ', { bold: true, size: 20 }), run(d, { size: 20 })])))
children.push(h2('How to read this document'))
;[
  'Quest tables are in the order the quests appear in the book, left to right. "After" lists the quests that unlock it. "(optional)" quests never hold up your path.',
  'Each class chapter is split into phases: Early (before class level 10), Mid (level 10 to 25), Trial and ring, Late (after you have a ring) and Legend (the final quest, after the finale).',
  `Class levels go up to ${D.levels.class_limit}; you can spend at most ${D.levels.class_spent} points per class tree, so you can't take everything. A capstone needs ${D.levels.cap_spent} points spent first.`,
  'Main gear per phase lists the armour, weapons and spellbooks that the phase\'s quests ask for or give, with their base stats.',
].forEach(t => children.push(bullet(t)))

// Part 1: main story
children.push(h1('1. The main story'))
for (const ch of D.main) {
  children.push(h2(ch.title))
  if (ch.subtitle) children.push(body(ch.subtitle, { italics: true, color: GREY }))
  children.push(table(QCOLS, questRows(ch.quests)))
}

// Part 2: the seven lights
children.push(h1('2. The seven lights'))
children.push(body('Every class is a Lantern Corps. Join one from Act I with its chapter\'s first quest; you can join more than one, but each levels by playing its own style.'))
children.push(table([['Light', 1300], ['Class', 2300], ['Theme', 3700], ['Trial boss', 2606]],
  D.classes.map(c => [
    [para([run(c.id[0].toUpperCase() + c.id.slice(1), { bold: true, color: COLOR[c.id] })])],
    [para([run(c.name, { bold: true })]), para([run(c.corps, { size: 16, color: GREY })])],
    [para([run(c.tree.desc, { size: 18 })])],
    [para([run(c.boss, { size: 18 })])],
  ])))

for (const c of D.classes) {
  const col = COLOR[c.id]
  children.push(h1(`${c.id[0].toUpperCase() + c.id.slice(1)}: ${c.name}`, col))
  children.push(body(`"${c.motto}"`, { italics: true, color: col }))
  children.push(body(c.tree.desc))
  children.push(table([['Class facts', 2300], ['', 7606]], [
    [[para([run('Corps', { bold: true })])], [para([run(c.corps)])]],
    [[para([run('Ring', { bold: true })])], [para([run(c.ring)])]],
    [[para([run('Trial boss', { bold: true })])], [para([run(c.boss)])]],
    [[para([run('Nemeses (big class XP)', { bold: true })])], [para([run(c.nemeses.join(', '))])]],
    [[para([run('Earns class XP from', { bold: true })])], c.xp.map(x => bullet(x, 18))],
  ], col))

  children.push(h2('Skill tree', col))
  children.push(body(`Starts with ${c.tree.root.node} (${c.tree.root.effect}). Three branches of 11 nodes each; a branch's capstone needs ${D.levels.cap_spent} points spent in the tree.`))
  for (const b of c.tree.branches) {
    children.push(h3(b.name))
    children.push(table([['Node', 3000], ['Cost', 900], ['Effect', 6006]], b.nodes.map(n => [
      [para([run(n.node, { bold: !!n.kind }), ...(n.kind ? [run('  ' + n.kind, { size: 16, color: col })] : [])])],
      [para([run(n.cost)], { alignment: AlignmentType.CENTER })],
      [para([run(n.effect, { size: 18 })])],
    ]), col))
  }

  children.push(h2('Main gear by phase', col))
  children.push(table([['Phase', 1800], ['Gear the quests ask for or give (base stats)', 8106]],
    c.gear.filter(g => g.gear.length).map(g => [[para([run(g.phase, { bold: true })])], g.gear.map(x => bullet(x, 17))]), col))

  children.push(h2('Quests', col))
  for (const ph of ['Early', 'Mid', 'Trial and ring', 'Late', 'Legend']) {
    const qs = c.chapter.quests.filter(q => q.phase === ph)
    if (!qs.length) continue
    children.push(h3(`${ph} (${qs.length} quest${qs.length === 1 ? '' : 's'})`))
    children.push(table(QCOLS, questRows(qs), col))
  }
}

// Part 3: Adventurer
children.push(h1('3. The Adventurer tree (everyone)'))
children.push(body(D.adventurer.tree.desc))
children.push(h3('Earns XP from'))
D.adventurer.xp.forEach(x => children.push(bullet(x)))
for (const b of D.adventurer.tree.branches) {
  children.push(h3(b.name))
  children.push(table([['Node', 3000], ['Cost', 900], ['Effect', 6006]], b.nodes.map(n => [
    [para([run(n.node, { bold: !!n.kind }), ...(n.kind ? [run('  ' + n.kind, { size: 16, color: GREEN })] : [])])],
    [para([run(n.cost)], { alignment: AlignmentType.CENTER })], [para([run(n.effect, { size: 18 })])]])))
}

// Appendix: guides
children.push(h1('4. Mod guides (for reference)'))
children.push(body('Short chapters that teach each big mod. They unlock as you go and are not part of the story.'))
children.push(table([['Chapter', 3300], ['About', 5506], ['Quests', 1100]], D.guides.map(g => [
  [para([run(g.title, { bold: true })])], [para([run(g.subtitle, { size: 18 })])], [para([run(g.quests)], { alignment: AlignmentType.CENTER })]])))

const doc = new Document({
  creator: 'Green Lanterns', title: 'Green Lanterns: Story and Classes',
  numbering: { config: [{ reference: 'dots', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 300, hanging: 200 } } } }] }] },
  styles: {
    default: { document: { run: { font: 'Calibri', size: 20 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal', run: { font: 'Calibri', size: 48, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 80 }, keepNext: true } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 34, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 100 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 26, bold: true, color: '2E7D4F' }, paragraph: { spacing: { before: 280, after: 100 }, keepNext: true, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 22, bold: true, color: '374151' }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 1000, right: 1000 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: 'Green Lanterns: Story and Classes  ·  page ', size: 16, color: GREY }),
      new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY })] })] }) },
    children,
  }],
})
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log('wrote ' + path.relative(ROOT, OUT)) })
