// Loads tiered_chest_loot.js with LootJS/KubeJS stubs, runs both events, prints JSON.
// usage: node harness.js <script.js> <loot_tables.json> <out.json>
'use strict';
const fs = require('fs');
const vm = require('vm');
const [script, ltPath, outPath] = process.argv.slice(2);
const ids = JSON.parse(fs.readFileSync(ltPath, 'utf8')).loot_tables;

const calls = [];
const logs = [];
function mkEntry(kind, data) {
  const e = { kind, data, conds: [] };
  e.when = function (fn) {
    const c = {
      matchDimension(d) { if (arguments.length !== 1 || typeof d !== 'string') throw new Error('matchDimension arg'); e.conds.push({ dim: d }); return c; },
      matchCustomCondition(j) { e.conds.push({ json: JSON.parse(JSON.stringify(j)) }); return c; },
    };
    fn(c);
    return e;
  };
  return e;
}
const LootEntry = {
  reference(id) { if (arguments.length !== 1 || typeof id !== 'string') throw new Error('reference arg'); return mkEntry('ref', id); },
  alternative(...xs) { if (xs.length !== 2) throw new Error('alternative expects 2 children here, got ' + xs.length); return mkEntry('alt', xs); },
};
const created = {};
const lootTablesEvent = {
  getLootTableIds() {
    const all = ids.concat(Object.keys(created));
    let i = 0;
    return { iterator() { return { hasNext() { return i < all.length; }, next() { return { toString() { return all[i++]; } }; } }; } };
  },
  hasLootTable(id) { return ids.includes(id) || id in created; },
  create(id) {
    if (this.hasLootTable(id)) throw new Error('create existing ' + id);
    const t = { pools: [] };
    created[id] = t;
    return { createPool(fn) { const p = { entries: [] }; fn({ addEntry(e) { p.entries.push(e); return this; } }); t.pools.push(p); return this; } };
  },
};
const modifiers = [];
const modifiersEvent = {
  addTableModifier(rx) {
    if (Object.prototype.toString.call(rx) !== '[object RegExp]') throw new Error('filter not regex');
    const m = { rx, pools: [] };
    modifiers.push(m);
    return {
      pool(fn) {
        const p = { entries: [], name: null, rolls: null };
        fn({ name(n) { p.name = n; return this; }, rolls(r) { p.rolls = r; return this; }, addEntry(e) { p.entries.push(e); return this; } });
        m.pools.push(p);
        return this;
      },
    };
  },
};
let tablesCb = null, modsCb = null;
const ctx = {
  LootJS: { lootTables(cb) { tablesCb = cb; }, modifiers(cb) { modsCb = cb; } },
  LootEntry,
  console: { info: (s) => logs.push(['info', String(s)]), error: (s) => logs.push(['error', String(s)]), warn: (s) => logs.push(['warn', String(s)]) },
  String,
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(script, 'utf8'), ctx, { filename: script });
if (!tablesCb || !modsCb) throw new Error('events not registered');
tablesCb(lootTablesEvent);
modsCb(modifiersEvent);

function ser(e) { return { kind: e.kind, data: e.kind === 'alt' ? e.data.map(ser) : e.data, conds: e.conds }; }
const allIds = ids.concat(Object.keys(created));
const tierOf = {};
for (const m of modifiers) {
  const mm = /^greenlanterns_tier_([1-5])_[0-9]+$/.exec(m.pools[0].name); if (!mm) throw new Error('bad pool name ' + m.pools[0].name); const tier = Number(mm[1]);
  for (const id of allIds) {
    if (m.rx.test(id)) {
      if (tierOf[id]) throw new Error('table matched twice: ' + id);
      tierOf[id] = tier;
    }
  }
}
const out = {
  tierOf,
  created: Object.fromEntries(Object.entries(created).map(([k, v]) => [k, v.pools.map(p => p.entries.map(ser))])),
  modifiers: modifiers.map(m => ({ len: m.rx.source.length, pools: m.pools.map(p => ({ name: p.name, rolls: p.rolls, entries: p.entries.map(ser) })) })),
  logs,
  data: {
    dims: ctx.GL_LOOT_DIMENSION_MIN_TIER, structs: ctx.GL_LOOT_STRUCTURE_MIN_TIER, missing: ctx.GL_LOOT_MISSING_TABLES,
    inject: ctx.GL_LOOT_INJECT,
  },
};
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log('harness ok: modifiers=' + modifiers.length + ' classified=' + Object.keys(tierOf).length + ' created=' + Object.keys(created).length);
