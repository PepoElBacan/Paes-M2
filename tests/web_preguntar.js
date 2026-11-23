// Prueba de "Preguntarle a Claude": simula window.claude.use('sample') y el gesto de deslizar hacia arriba.
// Uso: cd web && python3 -m http.server 8765  →  node tests/web_preguntar.js [estado.json]
const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const ruta = process.argv[2] || 'progreso/respaldo_web_restaurado_2026-11-22.json';
const est = JSON.parse(fs.readFileSync(ruta, 'utf8')).estado;
let fallos = 0;
const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fallos++; };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true });
  await ctx.addInitScript((e) => {
    if (!localStorage.getItem('paesm2-estado-v1')) localStorage.setItem('paesm2-estado-v1', JSON.stringify(e));
    window.__llamadas = [];
    const sample = async (input, opts) => {
      window.__llamadas.push({ input: JSON.parse(JSON.stringify(input)), opts: Object.keys(opts || {}) });
      const txt = window.__fallar ? null : 'Piensa en el **vértice**: $x_v=-\\dfrac{b}{2a}$. Cuesta \\$100.';
      if (window.__fallar) throw { code: 'rate_limited', message: 'x' };
      if (opts && opts.onText) { await new Promise(r => setTimeout(r, 50)); opts.onText({ text: txt.slice(0, 20), delta: txt.slice(0, 20) }); await new Promise(r => setTimeout(r, 50)); opts.onText({ text: txt, delta: txt.slice(20) }); }
      return { text: txt, truncated: false, modelTierApplied: 'default' };
    };
    sample.limits = async () => ({ maxPromptBytes: 262144, images: { maxCount: 1, maxInputBytes: 1e7, mediaTypes: ['image/png'] } });
    window.claude = { use: async (n) => (n === 'sample' ? sample : null) };
  }, est);
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  await p.route('**/fonts.googleapis.com/**', r => r.abort());
  await p.route(/cdnjs|jsdelivr|unpkg/, r => r.abort());
  await p.route('**/index.html', async r => { const resp = await r.fetch(); r.fulfill({ response: resp, headers: { ...resp.headers(), 'content-type': 'text/html; charset=utf-8' } }); });
  const txt = async (s) => (await p.textContent(s)).replace(/\s+/g, ' ');
  await p.goto('http://127.0.0.1:8765/index.html');
  await p.waitForSelector('[data-act=repaso-ini],[data-act=repaso-cont]');
  await p.evaluate(() => { try { localStorage.removeItem('paesm2-repaso-v1'); } catch (e) {} });
  await p.click('[data-act=repaso-ini],[data-act=repaso-cont]');
  await p.waitForSelector('.sesion-top');
  await p.waitForSelector('[data-act=ask]');
  ok(true, 'aparece el botón "Preguntar" en la pregunta');
  // deslizar hacia arriba desde la barra inferior
  const swipe = (sel, dy) => p.evaluate(({ sel, dy }) => {
    const el = document.querySelector(sel), r = el.getBoundingClientRect();
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    const mk = (type, yy) => new TouchEvent(type, { bubbles: true, cancelable: true, changedTouches: [new Touch({ identifier: 1, target: el, clientX: x, clientY: yy })], touches: type === 'touchend' ? [] : [new Touch({ identifier: 1, target: el, clientX: x, clientY: yy })] });
    el.dispatchEvent(mk('touchstart', y)); el.dispatchEvent(mk('touchend', y + dy));
  }, { sel, dy });
  await swipe('#tabs button[data-v=hoy]', -90);
  ok(await p.isVisible('#ask-msgs'), 'deslizar hacia arriba desde la barra de abajo abre el panel');
  await p.click('.ask-head [data-act=ask-x]');
  ok(!(await p.isVisible('#ask-msgs')), 'se cierra con "Cerrar"');
  await swipe('#tabs button[data-v=hoy]', -10);
  ok(!(await p.isVisible('#ask-msgs')), 'un toque corto no abre el panel');
  await p.click('[data-act=ask]');
  ok(await p.isVisible('#ask-msgs'), 'el botón "Preguntar" también abre el panel');
  await p.click('#ask-sug button >> nth=0');
  await p.waitForFunction(() => document.querySelectorAll('.am-a').length >= 1 && !document.querySelector('.ask-hint'));
  await p.waitForTimeout(300);
  const ll = await p.evaluate(() => window.__llamadas);
  ok(ll.length === 1, 'se hizo una llamada a Claude');
  const ctxTxt = ll[0].input[0].content;
  ok(ctxTxt.includes('CONTEXTO DE LA PREGUNTA') && ctxTxt.includes('AÚN NO responde'), 'el contexto indica que aún no respondes');
  ok(!/clave oficial es la|La correcta es la/.test(ctxTxt), 'no le entrega la respuesta correcta antes de responder');
  ok(ll[0].opts.includes('cache') && ll[0].opts.includes('signal'), 'llamada sin caché y cancelable');
  ok(ll[0].input.at(-1).role === 'user' && ll[0].input.at(-1).content === 'Dame una pista', 'termina con el mensaje del estudiante');
  const resp = await p.innerHTML('#ask-msgs');
  ok(resp.includes('<strong>vértice</strong>') && (resp.includes('mxp') || resp.includes('katex')), 'la respuesta muestra negrita y matemática');
  ok(resp.includes('$100'), 'el signo de pesos literal se ve como $');
  // escribir un mensaje propio
  await p.fill('#ask-txt', 'No entiendo el paso 2');
  await p.click('#ask-send');
  await p.waitForFunction(() => window.__llamadas.length === 2);
  await p.waitForTimeout(400);
  const ll2 = await p.evaluate(() => window.__llamadas[1].input);
  ok(ll2.length >= 4 && ll2.at(-1).content === 'No entiendo el paso 2', 'la conversación conserva el historial');
  // error
  await p.evaluate(() => { window.__fallar = true; });
  await p.fill('#ask-txt', 'otra duda');
  await p.click('#ask-send');
  await p.waitForSelector('.am-e');
  ok((await txt('.am-e')).includes('límite'), 'muestra un mensaje claro si falla (rate_limited)');
  await p.evaluate(() => { window.__fallar = false; });
  await p.click('.ask-head [data-act=ask-x]');
  // responder la pregunta y volver a preguntar: ahora el contexto incluye la respuesta
  if (await p.$('[data-act=resp]')) await p.click('[data-act=resp]'); else await p.click('[data-act=resp-of][data-l=A]');
  if (await p.$('[data-act=conf][data-c="1"]')) await p.click('[data-act=conf][data-c="1"]');
  await p.click('[data-act=ask]');
  const sugs = await txt('#ask-sug');
  ok(/equivoqué|trampa/.test(sugs) || (await p.innerHTML('#ask-msgs')).length > 0, 'tras responder, las sugerencias cambian o se conserva la charla');
  await p.fill('#ask-txt', 'explica');
  await p.click('#ask-send');
  await p.waitForFunction(() => window.__llamadas.length >= 3);
  const c3 = (await p.evaluate(() => window.__llamadas.at(-1).input[0].content));
  ok(/marcó la|El estudiante marcó/.test(c3), 'tras responder, el contexto incluye lo que marcaste');
  await p.waitForTimeout(400);
  await p.screenshot({ path: os.tmpdir() + '/ask.png' });
  await p.click('.ask-head [data-act=ask-x]');
  ok(errs.length === 0, 'sin errores de JavaScript ' + JSON.stringify(errs));
  await b.close();
  console.log(fallos ? fallos + ' fallidas' : 'todo bien');
  process.exit(fallos ? 1 : 0);
})();
