// Pruebas de persistencia de la app web, con una "cuenta" simulada. Uso:
//   (cd web && python3 -m http.server 8765 &)  y luego  node tests/web_persistencia.js <estado_real.json>
const { chromium } = require('playwright'); const fs = require('fs');
const real = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); const REAL = real.data ? real.data.estado : real.estado;
const PATH = 'data/users/u_test/progreso';
let ok = 0, mal = 0; const check = (c, m) => { (c ? ok++ : mal++); console.log((c ? '  ✓ ' : '  ✗ ') + m); };
async function nuevaPagina(browser, store, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const writes = []; let gets = 0;
  await ctx.exposeFunction('__dbGet', p => { gets++; if (opts.fallarGets && gets <= opts.fallarGets) throw new Error('red'); return store[p] === undefined ? null : store[p]; });
  await ctx.exposeFunction('__dbSet', (p, d) => { writes.push(p); store[p] = d; });
  await ctx.exposeFunction('__dbList', pre => Object.keys(store).filter(k => k.startsWith(pre)).map(k => ({ id: k.slice(pre.length), d: store[k] })));
  await ctx.addInitScript(([local]) => {
    if (local && !localStorage.getItem('paesm2-estado-v1')) localStorage.setItem('paesm2-estado-v1', local);
    const mk = path => ({ get: async () => { const v = await window.__dbGet(path); return { exists: v !== null, data: () => v, metadata: { fromCache: false, hasPendingWrites: false } }; },
      set: async d => { await window.__dbSet(path, JSON.parse(JSON.stringify(d))); }, onSnapshot: () => () => {},
      collection: n => ({ doc: i => mk(path + '/' + n + '/' + i), get: async () => ({ docs: (await window.__dbList(path + '/' + n + '/')).map(x => ({ id: x.id, data: () => x.d })) }) }) });
    window.claude = { use: async n => n === 'user' ? { id: async () => 'u_test' } : n === 'db' ? { doc: mk } : null };
  }, [opts.local || null]);
  const p = await ctx.newPage(); await p.route('**/fonts.googleapis.com/**', r => r.abort());
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index.html'); await p.waitForSelector('.hero, #main .card', { timeout: 15000 });
  return { p, ctx, writes, errs };
}
(async () => {
  const b = await chromium.launch();
  const ric = e => e.hist.length + Object.keys(e.oficiales).length;
  console.log('Escenario 1: teléfono SIN datos + cuenta con datos reales (el fallo que ocurrió)');
  { const store = { [PATH]: { estado: REAL, ts: REAL.ts } };
    const { p, errs } = await nuevaPagina(b, store);
    await p.waitForTimeout(1500);
    const e = await p.evaluate(() => window.__paes.estado());
    check(e.hist.length >= REAL.hist.length && Object.keys(e.oficiales).length >= Object.keys(REAL.oficiales).length, `la página recuperó tu progreso (${e.hist.length} respuestas, ${Object.keys(e.oficiales).length} oficiales)`);
    await p.click('#tabs [data-v=guias]'); await p.click('[data-act=lec][data-g="01_funcion_cuadratica"]'); await p.click('[data-act=lec-next]');
    await p.waitForTimeout(2500);
    const c = store[PATH].estado;
    check(c.hist.length >= REAL.hist.length, `la nube conserva el historial (${c.hist.length} ≥ ${REAL.hist.length})`);
    check(Object.keys(c.oficiales).length >= Object.keys(REAL.oficiales).length, 'la nube conserva las preguntas oficiales');
    check(Object.values(c.errores).reduce((t, x) => t + x.intentos, 0) >= Object.values(REAL.errores).reduce((t, x) => t + x.intentos, 0), 'la nube conserva los intentos de tus errores');
    check(!!c.guias['01_funcion_cuadratica'], 'y registró el avance nuevo de la lección');
    check(Object.keys(store).some(k => k.includes('/respaldos/')), 'se creó un respaldo diario en la cuenta');
    check(errs.length === 0, 'sin errores de JavaScript'); }
  console.log('Escenario 2: la nube no responde al abrir (no debe escribir nada hasta leerla)');
  { const store = { [PATH]: { estado: REAL, ts: REAL.ts } };
    const { p, writes } = await nuevaPagina(b, store, { fallarGets: 2 });
    await p.click('#tabs [data-v=guias]'); await p.click('[data-act=fc-ini]'); await p.click('[data-act=fc-flip]'); await p.click('[data-act=fc-ok]');
    await p.waitForTimeout(1500);
    check(writes.length === 0, `no escribió en la nube mientras no pudo leerla (escrituras: ${writes.length})`);
    await p.waitForTimeout(9000);
    const c = store[PATH].estado;
    check(c.hist.length >= REAL.hist.length && Object.keys(c.formulas).length >= 1, 'al recuperar la conexión combinó: conserva lo real y suma lo nuevo');
    check(await p.evaluate(() => window.__paes.sync()) === 'ok', 'el indicador pasó a "guardado"'); }
  console.log('Escenario 3: dispositivo desactualizado con fecha "más nueva"');
  { const store = { [PATH]: { estado: REAL, ts: REAL.ts } };
    const stale = JSON.parse(JSON.stringify(REAL)); stale.hist = []; stale.oficiales = {}; stale.ensayos = []; Object.values(stale.errores).forEach(x => { x.intentos = 0; x.racha = 0; }); stale.ts = Date.now() + 1e8;
    const { p } = await nuevaPagina(b, store, { local: JSON.stringify(stale) });
    await p.waitForTimeout(1500); await p.click('#tabs [data-v=guias]'); await p.click('[data-act=fc-ini]'); await p.click('[data-act=fc-flip]'); await p.click('[data-act=fc-ok]'); await p.waitForTimeout(2500);
    const c = store[PATH].estado;
    check(c.hist.length >= REAL.hist.length && c.ensayos.length >= REAL.ensayos.length, 'un dispositivo vacío pero "más nuevo" no borra la nube'); }
  console.log('Escenario 4: reglas de combinación');
  { const { p } = await nuevaPagina(b, {});
    const r = await p.evaluate(() => { const M = window.__paes.merge;
      const A = { errores: { x: { intentos: 3, racha: 2, proximo: '2026-11-28' }, y: { intentos: 0, racha: 0 } }, hist: [['d1', 't', 's', 0, 1, -1, -1, 'aa1'], ['d1', 't', 's', 0, 1, -1, -1, 'aa2']], dias: { d1: [5, 4] }, guias: { g: { h: false, max: 2, p: 2, v: 5 } }, oficiales: { q: { ok: true, f: '2026-11-22' } }, ensayos: [] };
      const B = { errores: { x: { intentos: 1, racha: 0 }, y: { intentos: 2, racha: 1 } }, hist: [['d1', 't', 's', 0, 1, -1, -1, 'aa2'], ['d2', 't', 's', 0, 0, -1, -1, 'bb1']], dias: { d1: [2, 1], d2: [1, 0] }, guias: { g: { h: true, max: 6, p: 6, v: 9 } }, oficiales: { q: { ok: false, f: '2026-11-21' } }, ensayos: [] };
      const m = M(A, B); return { ex: m.errores.x.intentos, ey: m.errores.y.intentos, h: m.hist.map(e => e[7]), d1: m.dias.d1[0], gh: m.guias.g.h, gmax: m.guias.g.max, oq: m.oficiales.q.ok }; });
    check(r.ex === 3 && r.ey === 2, 'cada error conserva la versión con más intentos');
    check(JSON.stringify(r.h) === JSON.stringify(['aa1', 'aa2', 'bb1']), 'el historial se une sin duplicar');
    check(r.d1 === 5 && r.gh === true && r.gmax === 6 && r.oq === true, 'días, lecciones y oficiales se combinan bien'); }
  console.log(`\n${ok} correctas, ${mal} fallidas`); await b.close(); process.exit(mal ? 1 : 0);
})();
