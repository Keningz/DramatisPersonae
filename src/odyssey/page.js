(() => {
  const app = document.getElementById('app');
  const svg = document.getElementById('map');
  const scroller = document.getElementById('mapscroll');
  const card = document.getElementById('card');
  const hint = document.getElementById('hint');
  const N = DATA.nodes, E = DATA.edges;
  const nodeEls = {}, edgeEls = [], labEls = [];
  svg.querySelectorAll('.node').forEach(g => nodeEls[g.dataset.id] = g);
  svg.querySelectorAll('.edge').forEach(g => edgeEls[+g.dataset.e] = g);
  svg.querySelectorAll('.elab').forEach(g => (labEls[+g.dataset.e] = labEls[+g.dataset.e] || []).push(g));
  const adj = {};
  Object.keys(N).forEach(id => adj[id] = []);
  E.forEach((e, i) => { adj[e.s].push(i); adj[e.t].push(i); });
  const hidden = new Set();
  const TORDER = { kin: 0, aid: 1, tie: 2, foe: 3 };
  let sel = null; // {kind:'node'|'edge', id}
  let lang = 'zh';
  const T = {
    zh: { close: '关闭', portrait: '小像', src: '出处：', rels: n => `${n}的关系`, bk: b => `（${b}）`, title: '奥德赛人物谱',
          aria: (n, c, s) => `${n}，${c}，${s}` },
    en: { close: 'Close', portrait: 'Portrait', src: 'Source: ', rels: n => `Relationships of ${n}`, bk: b => `(${b})`,
          title: 'Who’s Who in the Odyssey', aria: (n, c, s) => `${n}, ${c}, ${s}` },
  };
  const nm = id => lang === 'zh' ? N[id].zh : N[id].en;
  const f = (o, k) => lang === 'zh' ? o[k] : o[k + '_en'];

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const mini = (id, size) => {
    const n = N[id];
    const halo = n.cat === 'god' ? '<circle class="halo" cx="50" cy="50" r="55.5"/>' : '';
    return `<svg class="mini cat-${n.cat}" viewBox="-6 -6 112 112" width="${size}" height="${size}" aria-hidden="true">` +
      `<use xlink:href="#pt-${id}" href="#pt-${id}" width="100" height="100"/><circle class="ring" cx="50" cy="50" r="50" stroke-width="${size < 50 ? 7 : 5}"/>${halo}</svg>`;
  };

  function crossHtml(id) {
    return window.dpCross((DATA.cross || {})[id], lang);
  }

  function applyFocus(f) {
    Object.values(nodeEls).forEach(g => g.classList.remove('on'));
    edgeEls.forEach(g => g.classList.remove('on', 'sel'));
    labEls.forEach(a => a.forEach(g => g.classList.remove('on')));
    if (!f) { svg.classList.remove('focus'); return; }
    svg.classList.add('focus');
    if (f.kind === 'node') {
      nodeEls[f.id].classList.add('on');
      adj[f.id].forEach(i => {
        if (hidden.has(E[i].type)) return;
        edgeEls[i].classList.add('on'); labEls[i].forEach(g => g.classList.add('on'));
        nodeEls[E[i].s].classList.add('on'); nodeEls[E[i].t].classList.add('on');
      });
    } else {
      const e = E[f.id];
      edgeEls[f.id].classList.add('on', 'sel'); labEls[f.id].forEach(g => g.classList.add('on'));
      nodeEls[e.s].classList.add('on'); nodeEls[e.t].classList.add('on');
    }
  }

  function placeCard() { /* the panel sits beside the map */ }

  function showNode(id) {
    const n = N[id], t = T[lang];
    const rels = adj[id].slice().sort((a, b) => TORDER[E[a].type] - TORDER[E[b].type]);
    const items = rels.map(i => {
      const e = E[i], other = e.s === id ? e.t : e.s;
      return `<li><button type="button" data-edge="${i}">${mini(other, 30)}` +
        `<span class="who">${esc(nm(other))}<span class="pill t-${e.type}">${esc(f(e, 'label'))}</span></span>` +
        `<span class="rt">${esc(f(e, 'text'))} <span class="bk">${esc(t.bk(f(e, 'bk')))}</span></span></button></li>`;
    }).join('');
    card.innerHTML = `<button class="x" type="button" aria-label="${t.close}">×</button>
      <div class="ch"><span class="big">${mini(id, 84)}</span><div>
        <h2 class="cname">${esc(nm(id))}</h2>
        <div class="cgr">${esc(n.gr)}<span class="cen">${esc(lang === 'zh' ? n.en : n.zh)}</span></div>
        <div class="cmeta"><span class="pill cat-${n.cat}">${DATA.cat[lang][n.cat]}</span>${esc(f(n, 'sub'))}</div></div></div>
      <p class="cbio">${esc(f(n, 'bio'))}</p>
      <p class="cicon"><b>${t.portrait}</b>${esc(f(n, 'icon'))}</p>
      ${crossHtml(id)}
      <ul class="rels" aria-label="${esc(t.rels(nm(id)))}">${items}</ul>`;
    card.hidden = false;
    placeCard(n.x);
  }

  function showEdge(i) {
    const e = E[i], s = N[e.s], t = N[e.t], ty = DATA.types[e.type], tx = T[lang];
    card.innerHTML = `<button class="x" type="button" aria-label="${tx.close}">×</button>
      <div class="pair">
        <button class="who2" type="button" data-go="${e.s}">${mini(e.s, 58)}<span class="nmx">${esc(nm(e.s))}</span></button>
        <span class="bar t-${e.type}" style="color:var(--${e.type})"></span>
        <button class="who2" type="button" data-go="${e.t}">${mini(e.t, 58)}<span class="nmx">${esc(nm(e.t))}</span></button>
      </div>
      <p class="elabel" style="color:var(--${e.type})">${esc(f(e, 'label'))}</p>
      <div class="cmeta"><span class="pill t-${e.type}">${lang === 'zh' ? ty.zh : ty.en}</span>${esc(lang === 'zh' ? ty.desc : ty.desc_en)}</div>
      <p class="etext">${esc(f(e, 'text'))}</p>
      <p class="src">${tx.src}${esc(f(e, 'bk'))}</p>`;
    card.hidden = false;
    placeCard((s.x + t.x) / 2);
  }

  function select(kind, id) {
    sel = { kind, id };
    applyFocus(sel);
    kind === 'node' ? showNode(id) : showEdge(id);
    if (hint) hint.hidden = true;
    card.scrollTop = 0;
    if (matchMedia('(max-width: 1100px)').matches) {
      card.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'nearest' });
    }
  }
  function clearSel() { sel = null; applyFocus(null); card.innerHTML = INTRO_HTML; card.scrollTop = 0; }

  // ---- map events
  let dragMoved = false;
  svg.addEventListener('click', ev => {
    if (dragMoved) return;
    const nd = ev.target.closest('.node');
    const lb = ev.target.closest('.elab, .edge');
    if (nd) select('node', nd.dataset.id);
    else if (lb) select('edge', +lb.dataset.e);
    else clearSel();
  });
  svg.addEventListener('keydown', ev => {
    if (ev.key !== 'Enter' && ev.key !== ' ') return;
    const nd = ev.target.closest('.node'), lb = ev.target.closest('.elab');
    if (nd) { ev.preventDefault(); select('node', nd.dataset.id); }
    else if (lb) { ev.preventDefault(); select('edge', +lb.dataset.e); }
  });
  svg.addEventListener('pointerover', ev => {
    if (ev.pointerType === 'touch') return;
    const nd = ev.target.closest('.node');
    const lb = ev.target.closest('.elab, .edge');
    if (nd) applyFocus({ kind: 'node', id: nd.dataset.id });
    else if (lb) applyFocus({ kind: 'edge', id: +lb.dataset.e });
  });
  svg.addEventListener('pointerout', ev => {
    if (ev.pointerType === 'touch') return;
    const to = ev.relatedTarget && ev.relatedTarget.closest && ev.relatedTarget.closest('.node, .elab, .edge');
    if (!to) applyFocus(sel);
  });
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape') clearSel(); });

  card.addEventListener('click', ev => {
    if (ev.target.closest('.x')) { clearSel(); return; }
    const eb = ev.target.closest('[data-edge]');
    if (eb) { select('edge', +eb.dataset.edge); return; }
    const go = ev.target.closest('[data-go]');
    if (go) select('node', go.dataset.go);
  });

  // ---- type toggles
  document.querySelectorAll('.tog').forEach(b => b.addEventListener('click', () => {
    const t = b.dataset.type;
    const on = b.getAttribute('aria-pressed') === 'true';
    b.setAttribute('aria-pressed', on ? 'false' : 'true');
    on ? hidden.add(t) : hidden.delete(t);
    E.forEach((e, i) => {
      const off = hidden.has(e.type);
      edgeEls[i].classList.toggle('off', off);
      labEls[i].forEach(g => g.classList.toggle('off', off));
    });
    applyFocus(sel);
  }));

  // ---- zoom & pan
  const LV = [1, 1.4, 1.9, 2.6];
  let z = 0;
  function setZoom(nz) {
    nz = Math.max(0, Math.min(LV.length - 1, nz));
    const cxr = (scroller.scrollLeft + scroller.clientWidth / 2) / scroller.scrollWidth;
    const cyr = (scroller.scrollTop + scroller.clientHeight / 2) / scroller.scrollHeight;
    z = nz;
    svg.style.width = (LV[z] * 100) + '%';
    requestAnimationFrame(() => {
      scroller.scrollLeft = cxr * scroller.scrollWidth - scroller.clientWidth / 2;
      scroller.scrollTop = cyr * scroller.scrollHeight - scroller.clientHeight / 2;
      scroller.classList.toggle('pannable', scroller.scrollWidth > scroller.clientWidth + 2 || scroller.scrollHeight > scroller.clientHeight + 2);
    });
  }
  document.querySelectorAll('.zoom button').forEach(b => b.addEventListener('click', () => {
    const d = +b.dataset.z;
    setZoom(d === 0 ? 0 : z + d);
  }));
  let drag = null;
  scroller.addEventListener('pointerdown', ev => {
    if (ev.pointerType !== 'mouse' || ev.button !== 0) return;
    if (!scroller.classList.contains('pannable')) return;
    drag = { x: ev.clientX, y: ev.clientY, l: scroller.scrollLeft, t: scroller.scrollTop };
    dragMoved = false;
  });
  window.addEventListener('pointermove', ev => {
    if (!drag) return;
    const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
    if (!dragMoved && Math.hypot(dx, dy) > 5) { dragMoved = true; scroller.classList.add('dragging'); }
    if (dragMoved) { scroller.scrollLeft = drag.l - dx; scroller.scrollTop = drag.t - dy; }
  });
  window.addEventListener('pointerup', () => {
    if (!drag) return;
    drag = null;
    scroller.classList.remove('dragging');
    setTimeout(() => { dragMoved = false; }, 0);
  });
  const updatePannable = () => scroller.classList.toggle('pannable', scroller.scrollWidth > scroller.clientWidth + 2 || scroller.scrollHeight > scroller.clientHeight + 2);
  window.addEventListener('resize', updatePannable);
  requestAnimationFrame(() => {
    updatePannable();
    if (scroller.scrollWidth > scroller.clientWidth + 2) {
      scroller.scrollLeft = (scroller.scrollWidth - scroller.clientWidth) / 2;
    }
  });

  // ---- language
  function setLang(l, save) {
    lang = l === 'en' ? 'en' : 'zh';
    app.dataset.lang = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    document.title = T[lang].title;
    document.querySelectorAll('[data-setlang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setlang === lang)));
    document.querySelectorAll('.tog').forEach(b => {
      const ty = DATA.types[b.dataset.type];
      b.title = lang === 'zh' ? ty.desc : ty.desc_en;
    });
    Object.entries(nodeEls).forEach(([id, g]) => {
      const n = N[id];
      g.setAttribute('aria-label', T[lang].aria(nm(id), DATA.cat[lang][n.cat], f(n, 'sub')));
    });
    if (sel) (sel.kind === 'node' ? showNode(sel.id) : showEdge(sel.id));
    window.dpLinks(lang);
    if (save) window.dpSaveLang(lang);
  }
  document.querySelectorAll('[data-setlang]').forEach(b => b.addEventListener('click', () => setLang(b.dataset.setlang, true)));
  const tokens = window.dpHash();
  (() => {
    const h = tokens.find(x => x === 'en' || x === 'zh');
    if (h) return setLang(h, false);
    const stored = window.dpStoredLang();
    if (stored) return setLang(stored, false);
    const nav = (navigator.languages && navigator.languages[0]) || navigator.language || 'zh';
    setLang(/^zh/i.test(nav) ? 'zh' : 'en', false);
  })();

  // ---- roster
  document.querySelectorAll('.rcard').forEach(b => b.addEventListener('click', () => {
    const id = b.dataset.id;
    select('node', id);
    document.getElementById('stage').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    const n = N[id];
    if (scroller.scrollWidth > scroller.clientWidth + 2) {
      const k = scroller.scrollWidth / DATA.w;
      scroller.scrollLeft = n.x * k - scroller.clientWidth / 2;
    }
  }));

  // ---- arriving from another book: open that person
  const who = tokens.find(x => N[x]);
  if (who) requestAnimationFrame(() => {
    select('node', who);
    document.getElementById('stage').scrollIntoView({ block: 'start' });
    if (scroller.scrollWidth > scroller.clientWidth + 2) {
      scroller.scrollLeft = N[who].x * (scroller.scrollWidth / DATA.w) - scroller.clientWidth / 2;
    }
  });
})();
