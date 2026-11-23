const { chromium } = require('playwright');
const fs = require('fs');
const SC = require('os').tmpdir();
const est = JSON.parse(fs.readFileSync('' + (process.argv[2] || 'progreso/respaldo_web_restaurado_2026-11-22.json') + '', 'utf8')).estado;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  await ctx.addInitScript((e) => { if (!localStorage.getItem('paesm2-estado-v1')) localStorage.setItem('paesm2-estado-v1', JSON.stringify(e)); }, est);
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  await p.route('**/fonts.googleapis.com/**', r => r.abort());
  await p.route('**/cdnjs.cloudflare.com/**', r => r.abort());
  await p.route('**/cdn.jsdelivr.net/**', r => r.abort());
  await p.route('**/unpkg.com/**', r => r.abort());
  const ok = (c, m) => console.log((c ? '  ✓ ' : '  ✗ ') + m);
  const txt = async () => (await p.textContent('#main')).replace(/\s+/g, ' ');
  await p.goto('http://127.0.0.1:8765/index.html');
  await p.waitForSelector('[data-act=repaso-ini]');
  await p.click('[data-act=repaso-ini]');
  const n0 = await p.textContent('.sesion-top .mono');
  const total = +n0.split('/')[1];
  console.log('total', total);
  const responde = async () => {
    // pregunta generada: opción A ; oficial: letra A
    if (await p.$('[data-act=resp]')) await p.click('[data-act=resp]');
    else await p.click('[data-act=resp-of][data-l=A]');
    for (const c of ['[data-act=conf][data-c="1"]']) { if (await p.$(c)) await p.click(c); }
    await p.click('[data-act=sig]');
  };
  const t1 = await txt();
  await responde(); await responde(); await responde();
  const q3 = await txt();
  // salir
  await p.click('[data-act=salir]');
  ok((await txt()).includes('Continuar repaso') && (await txt()).includes('3/' + total), 'tras salir: "Continuar repaso · 3/' + total + '"');
  // recargar la página
  await p.reload();
  await p.waitForSelector('[data-act=repaso-cont]');
  ok((await txt()).includes('Continuar repaso') && (await txt()).includes('3/' + total), 'tras recargar sigue "Continuar repaso · 3/' + total + '"');
  await p.click('[data-act=repaso-cont]');
  ok((await p.textContent('.sesion-top .mono')).trim() === `4/${total}`, 'retoma en la pregunta 4');
  // misma pregunta 4 que antes de salir? (compara texto de la 4ª pregunta guardada)
  const pend = await p.evaluate(() => JSON.parse(localStorage.getItem('paesm2-repaso-v1')).items.length);
  ok(pend === total, 'los ' + total + ' elementos del repaso se conservaron');
  // pestaña Repaso también muestra continuar
  await p.click('[data-act=salir]');
  await p.click('#tabs [data-v=repaso]');
  ok((await txt()).includes('Continuar repaso'), 'la pestaña Repaso ofrece continuar');
  await p.click('[data-act=repaso-cont]');
  // terminar
  for (let i = 3; i < total; i++) await responde();
  const fin = await txt();
  ok(fin.includes('Siguiente repaso') && fin.includes('Repaso completado'), 'al terminar ofrece "Siguiente repaso"');
  ok(await p.evaluate(() => localStorage.getItem('paesm2-repaso-v1') === null), 'el repaso guardado se borra al terminar');
  await p.screenshot({ path: SC + '/rep_fin.png' });
  await p.click('[data-act=repaso-ini]');
  ok((await p.textContent('.sesion-top .mono')).trim().startsWith('1/'), 'el siguiente repaso arranca en 1');
  const hist = await p.evaluate(() => window.__paes.estado().hist.length);
  console.log('hist', hist, 'errs', JSON.stringify(errs));
  await b.close();
})();
