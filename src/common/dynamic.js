/* Dynamic character map shared by the Iliad, Aeneid and Journey pages: an overview laid out by the book, and a focus
   mode where the clicked person moves to the center with their relationships in a ring around them.
   Book-specific settings come in DATA (title, R1, R2, face `f` per node, camp and cat labels). */
(() => {
  const app = document.getElementById('app');
  const svg = document.getElementById('map');
  const scroller = document.getElementById('mapscroll');
  const panel = document.getElementById('panel');
  const btnOv = document.getElementById('btn-ov');
  const N = DATA.nodes, E = DATA.edges, IDS = DATA.order;
  const CX = DATA.CX, CY = DATA.CY, K_OV = DATA.R_OV / 40;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const TORDER = { kin: 0, mas: 1, aid: 2, tie: 3, foe: 4 };

  const nodeEl = {}, ptEl = {}, flipEl = {}, nmEl = {}, sbEl = {};
  svg.querySelectorAll('.node').forEach(g => {
    const id = g.dataset.id;
    nodeEl[id] = g; ptEl[id] = g.querySelector('.pt'); flipEl[id] = g.querySelector('.flip');
    nmEl[id] = g.querySelector('.nm'); sbEl[id] = g.querySelector('.sb');
  });
  const edgeEl = [], labEl = [];
  svg.querySelectorAll('.edge').forEach(p => edgeEl[+p.dataset.e] = p);
  svg.querySelectorAll('.elab').forEach(g => labEl[+g.dataset.e] = g);
  const adj = {};
  IDS.forEach(id => adj[id] = []);
  E.forEach((e, i) => { adj[e.s].push(i); adj[e.t].push(i); });

  const hidden = new Set();
  let lang = 'zh', mode = 'ov', center = null, view = { kind: 'intro' }, trail = [];

  // ------------------------------------------------------------ text helpers
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const L = (o, k) => lang === 'zh' ? o[k] : o[k + '_en'];
  const nm = id => lang === 'zh' ? N[id].zh : N[id].en;
  const T = {
    zh: { close: '关闭', portrait: '小像', src: '出处：', rels: n => `${n}的关系`, bk: b => `（${b}）`, back: n => `← 回到${n}`,
          dies: b => `死于${b}`, trail: '足迹', title: DATA.title.zh, aria: (n, c, s) => `${n}，${c}，${s}`,
          edgeAria: (a, b, l) => `${a}与${b}：${l}` },
    en: { close: 'Close', portrait: 'Portrait', src: 'Source: ', rels: n => `Relationships of ${n}`, bk: b => `(${b})`,
          back: n => `← Back to ${n}`, dies: b => `Dies in ${b}`, trail: 'Trail', title: DATA.title.en,
          aria: (n, c, s) => `${n}, ${c}, ${s}`, edgeAria: (a, b, l) => `${a} and ${b}: ${l}` },
  };
  // half-and-half rings: demi = god + mortal, demimon = god + demon
  const ring = (cat, r, sw) => (cat === 'demi' || cat === 'demimon')
    ? `<path class="ring ring-g" d="M${-r},0 A${r},${r} 0 0 1 ${r},0" stroke-width="${sw}"/><path class="ring ${cat === 'demi' ? 'ring-m' : 'ring-x'}" d="M${r},0 A${r},${r} 0 0 1 ${-r},0" stroke-width="${sw}"/>`
    : `<circle class="ring" r="${r}" stroke-width="${sw}"/>` + (cat === 'god' ? `<circle class="halo" r="${r + 5.5}"/>` : '');
  const mini = (id, size) => {
    const n = N[id], sw = size < 50 ? 7 : 5;
    const dead = n.dies ? '<g class="dead" transform="translate(36 36)"><circle r="12"/><path d="M-5,-5 L5,5 M5,-5 L-5,5"/></g>' : '';
    return `<svg class="mini cat-${n.cat}" viewBox="-56 -56 112 112" width="${size}" height="${size}" aria-hidden="true">` +
      `<use xlink:href="#pt-${id}" href="#pt-${id}" x="-50" y="-50" width="100" height="100"/>${ring(n.cat, 50, sw)}${dead}</svg>`;
  };

  // ------------------------------------------------------------ geometry
  const ovFace = id => N[id].f || (N[id].ox < CX ? 1 : -1);   // which way the portrait faces in the overview
  const R1MIN = (DATA.R1 || [240, 320])[0], R1MAX = (DATA.R1 || [240, 320])[1], R2 = DATA.R2 || 455;
  const cur = {};
  const kOv = id => N[id].ok || K_OV;   // a book may draw its hub larger in the overview
  IDS.forEach(id => { cur[id] = { x: N[id].ox, y: N[id].oy, k: kOv(id), f: ovFace(id), role: 'ov', a: 0 }; });

  function ovTargets() {
    const t = {};
    IDS.forEach(id => { t[id] = { x: N[id].ox, y: N[id].oy, k: kOv(id), f: ovFace(id), role: 'ov', a: 0 }; });
    return t;
  }
  function neighbors(c) {
    const m = new Map();
    adj[c].forEach(i => {
      const e = E[i];
      if (hidden.has(e.type)) return;
      const o = e.s === c ? e.t : e.s;
      if (!m.has(o)) m.set(o, []);
      m.get(o).push(i);
    });
    return m;
  }
  function spread(ids, desired) {
    const n = ids.length, out = {};
    if (!n) return out;
    const order = ids.slice().sort((a, b) => desired[a] - desired[b]);
    const step = 2 * Math.PI / n;
    let best = null;
    for (let s = 0; s < 360; s += 2) {
      const off = s * Math.PI / 180;
      let cost = 0;
      order.forEach((id, i) => {
        const d = Math.abs(((off + i * step - desired[id]) % (2 * Math.PI) + 3 * Math.PI) % (2 * Math.PI) - Math.PI);
        cost += d * d;
      });
      if (!best || cost < best.c) best = { c: cost, off };
    }
    order.forEach((id, i) => out[id] = best.off + i * step);
    return out;
  }
  function fcTargets(c) {
    const nb = neighbors(c), ring1 = [...nb.keys()];
    const desired = {};
    IDS.forEach(id => { desired[id] = Math.atan2(N[id].oy - N[c].oy, N[id].ox - N[c].ox); });
    const R1 = Math.max(R1MIN, Math.min(R1MAX, ring1.length * 128 / (2 * Math.PI)));
    // a crowded ring (a hub with dozens of relationships) gets smaller portraits so they do not overlap
    const kRing = Math.min(36, Math.max(22, 2 * Math.PI * R1 / Math.max(1, ring1.length) * 0.42)) / 40;
    const a1 = spread(ring1, desired);
    const others = IDS.filter(id => id !== c && !nb.has(id));
    const a2 = spread(others, desired);
    const t = {};
    t[c] = { x: CX, y: CY, k: 60 / 40, f: 1, role: 'center', a: 0 };
    const crowd = kRing < 0.8;
    ring1.slice().sort((p, q) => a1[p] - a1[q]).forEach((id, ri) => {
      const a = a1[id], x = CX + R1 * Math.cos(a), y = CY + R1 * Math.sin(a);
      t[id] = { x, y, k: kRing, f: x > CX + 1 ? -1 : 1, role: 'ring', a, ri, crowd };
    });
    others.forEach(id => {
      const a = a2[id], x = CX + R2 * Math.cos(a), y = CY + R2 * Math.sin(a);
      t[id] = { x, y, k: 17 / 40, f: x > CX + 1 ? -1 : 1, role: 'outer', a };
    });
    return { t, nb, R1 };
  }

  // ------------------------------------------------------------ rendering
  function applyNode(id, s) {
    nodeEl[id].setAttribute('transform', `translate(${s.x.toFixed(1)} ${s.y.toFixed(1)})`);
    ptEl[id].setAttribute('transform', `scale(${s.k.toFixed(3)})`);
    flipEl[id].setAttribute('transform', `scale(${s.f.toFixed(3)} 1)`);
  }
  function updateEdges() {
    E.forEach((e, i) => {
      const a = cur[e.s], b = cur[e.t];
      edgeEl[i].setAttribute('d', `M${a.x.toFixed(1)},${a.y.toFixed(1)} L${b.x.toFixed(1)},${b.y.toFixed(1)}`);
    });
  }
  function setNodeLabel(id) {
    const s = cur[id], role = s.role, n1 = nmEl[id], n2 = sbEl[id], r = 40 * s.k;
    n1.textContent = nm(id);
    n2.textContent = L(N[id], 'sub');
    // overview names: English runs longer than Chinese, so it is set a size smaller
    let fs1 = lang === 'en' ? 12.5 : 14, fs2 = 12, show2 = false, anchor = 'middle', x = 0, y1 = r + 17, y2 = 0;
    if (role === 'center') { fs1 = 22; fs2 = 13.5; show2 = true; y1 = r + 26; y2 = y1 + 18; }
    else if (role === 'ring' || role === 'outer') {
      const small = role === 'outer', crowd = role === 'ring' && s.crowd;
      // crowded ring: names only, a little smaller, every other one pushed further out so neighbors do not collide
      fs1 = small ? 11.5 : crowd ? 13.5 : 16; show2 = !small && !crowd;
      const st = crowd && s.ri % 2 ? 15 : 0;
      const sn = Math.sin(s.a), cs = Math.cos(s.a);
      if (crowd) {   // names point straight out from the ring, so they never sit on the next portrait
        const d = r + 6;
        x = cs * d;
        if (Math.abs(cs) > 0.38) { anchor = cs > 0 ? 'start' : 'end'; y1 = sn * d + fs1 * 0.35; }
        else y1 = sn < 0 ? sn * d - 2 - st : sn * d + fs1 + st;
      } else if (sn < -0.42) { y2 = -(r + 8); y1 = show2 ? y2 - fs2 - 3 : -(r + 6 + st); }
      else if (sn > 0.42) { y1 = r + fs1 + 2 + st; y2 = y1 + fs2 + 3; }
      else { anchor = cs > 0 ? 'start' : 'end'; x = (cs > 0 ? 1 : -1) * (r + 8); y1 = show2 ? -2 : 4; y2 = y1 + fs2 + 3; }
    }
    const put = () => [[n1, y1, fs1], [n2, y2, fs2]].forEach(([el, y, fs]) => {
      el.setAttribute('x', x.toFixed(1)); el.setAttribute('y', y.toFixed(1));
      el.setAttribute('font-size', fs); el.setAttribute('text-anchor', anchor);
    });
    put();
    // a side label that would run off the edge of the map goes under the portrait instead
    if (anchor !== 'middle') {
      let w = 0;
      try { w = n1.getComputedTextLength(); } catch (e) { /* not rendered yet */ }
      const gx = s.x + x;
      if ((anchor === 'end' && gx - w < 4) || (anchor === 'start' && gx + w > DATA.W - 4)) {
        anchor = 'middle'; x = 0; y1 = r + fs1 + 2; y2 = y1 + fs2 + 3; put();
      }
    }
    n2.style.display = show2 ? '' : 'none';
    const g = nodeEl[id];
    g.setAttribute('aria-label', T[lang].aria(nm(id), DATA.cat[lang][N[id].cat], L(N[id], 'sub')));
  }
  // overview: where two neighbors' names would touch, the later one drops half a line
  function staggerOv() {
    if (mode !== 'ov') return;
    const placed = [];
    const hit = b => placed.some(o => b[0] < o[2] + 3 && b[2] > o[0] - 3 && b[1] < o[3] && b[3] > o[1]);
    IDS.slice().sort((a, b) => cur[a].x - cur[b].x).forEach(id => {
      const t = nmEl[id], s = cur[id];
      let bb;
      try { bb = t.getBBox(); } catch (e) { return; }
      let box = [s.x + bb.x, s.y + bb.y, s.x + bb.x + bb.width, s.y + bb.y + bb.height];
      if (bb.width && hit(box)) {
        t.setAttribute('y', (+t.getAttribute('y') + 13).toFixed(1));
        box = [box[0], box[1] + 13, box[2], box[3] + 13];
      }
      placed.push(box);
    });
  }
  function relabel() { IDS.forEach(setNodeLabel); staggerOv(); }
  function setRoles() {
    IDS.forEach(id => {
      const g = nodeEl[id];
      g.classList.remove('r-ov', 'r-center', 'r-ring', 'r-outer');
      g.classList.add('r-' + cur[id].role);
    });
  }

  let raf = null;
  function animateTo(targets, done) {
    if (raf) cancelAnimationFrame(raf);
    const from = {};
    IDS.forEach(id => {
      from[id] = { ...cur[id] };
      cur[id].role = targets[id].role; cur[id].a = targets[id].a; cur[id].ri = targets[id].ri || 0; cur[id].crowd = !!targets[id].crowd;
    });
    setRoles();
    const dur = reduce ? 0 : 720, t0 = performance.now();
    svg.classList.add('moving');
    const step = now => {
      const p = dur ? Math.min(1, (now - t0) / dur) : 1;
      const e = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
      IDS.forEach(id => {
        const a = from[id], b = targets[id];
        const s = { x: a.x + (b.x - a.x) * e, y: a.y + (b.y - a.y) * e, k: a.k + (b.k - a.k) * e, f: a.f + (b.f - a.f) * e };
        Object.assign(cur[id], s);
        applyNode(id, s);
      });
      updateEdges();
      if (p < 1) raf = requestAnimationFrame(step);
      else { raf = null; svg.classList.remove('moving'); relabel(); done && done(); }
    };
    raf = requestAnimationFrame(step);
  }

  // edge labels (focus mode)
  function overlapSum(b, list) {
    let s = 0;
    for (const o of list) {
      const ox = Math.min(b[2] + 2, o[2]) - Math.max(b[0] - 2, o[0]);
      const oy = Math.min(b[3] + 2, o[3]) - Math.max(b[1] - 2, o[1]);
      if (ox > 0 && oy > 0) s += ox * oy;
    }
    return s;
  }
  function hideLabels() { labEl.forEach(g => { g.classList.remove('vis', 'on'); g.setAttribute('tabindex', '-1'); }); }
  function placeLabels() {
    hideLabels();
    if (mode !== 'fc') return;
    const boxes = [];
    IDS.forEach(id => {
      const s = cur[id], r = 40 * s.k + 3;
      boxes.push([s.x - r, s.y - r, s.x + r, s.y + r]);
      if (s.role === 'ring' || s.role === 'center') {
        [nmEl[id], sbEl[id]].forEach(t => {
          if (t.style.display === 'none' || !t.textContent) return;
          try { const bb = t.getBBox(); boxes.push([s.x + bb.x, s.y + bb.y, s.x + bb.x + bb.width, s.y + bb.y + bb.height]); } catch (e) { /* not rendered */ }
        });
      }
    });
    const list = adj[center].filter(i => !hidden.has(E[i].type))
      .sort((a, b) => cur[E[a].s === center ? E[a].t : E[a].s].a - cur[E[b].s === center ? E[b].t : E[b].s].a);
    list.forEach(i => {
      const g = labEl[i], t = g.querySelector('text'), rc = g.querySelector('rect');
      const e = E[i];
      t.textContent = L(e, 'label');
      let w = 60;
      try { w = t.getComputedTextLength() + 16; } catch (err) { /* keep estimate */ }
      const h = 21;
      const other = e.s === center ? e.t : e.s, a = cur[center], b = cur[other];
      const len = Math.hypot(b.x - a.x, b.y - a.y), ux = (b.x - a.x) / len, uy = (b.y - a.y) / len;
      const ra = 40 * a.k + 8, rb = 40 * b.k + 8;
      let best = null;
      for (const tt of [0.5, 0.38, 0.62, 0.28, 0.72, 0.2, 0.8]) {
        const d = ra + (len - ra - rb) * tt, x = a.x + ux * d, y = a.y + uy * d;
        const bx = [x - w / 2, y - h / 2, x + w / 2, y + h / 2];
        const ov = overlapSum(bx, boxes) + Math.abs(tt - 0.5) * 30;
        if (!best || ov < best.ov) best = { ov, x, y, bx };
        if (ov < 20) break;
      }
      boxes.push(best.bx);
      rc.setAttribute('x', (best.x - w / 2).toFixed(1)); rc.setAttribute('y', (best.y - h / 2).toFixed(1));
      rc.setAttribute('width', w.toFixed(1)); rc.setAttribute('height', h);
      t.setAttribute('x', best.x.toFixed(1)); t.setAttribute('y', (best.y + 4.6).toFixed(1));
      g.setAttribute('aria-label', T[lang].edgeAria(nm(e.s), nm(e.t), L(e, 'label')));
      g.setAttribute('tabindex', '0');
      g.classList.add('vis');
    });
  }
  function setEdgeVisibility(nb) {
    E.forEach((e, i) => {
      edgeEl[i].classList.toggle('off', hidden.has(e.type));
      edgeEl[i].classList.toggle('vis', mode === 'fc' && (e.s === center || e.t === center) && !hidden.has(e.type));
    });
  }

  // ------------------------------------------------------------ modes
  function focusOn(id, opts = {}) {
    if (!N[id]) return;
    center = id; mode = 'fc';
    svg.classList.remove('mode-ov', 'hov'); svg.classList.add('mode-fc');
    clearHover();
    hideLabels();
    const { t } = fcTargets(id);
    setEdgeVisibility();
    animateTo(t, () => { placeLabels(); centerScroll(); });
    trail = trail.filter(x => x !== id); trail.push(id); if (trail.length > 7) trail.shift();
    btnOv.disabled = false;
    if (!opts.keepPanel) showNode(id);
  }
  function toOverview() {
    mode = 'ov'; center = null;
    svg.classList.remove('mode-fc', 'hov'); svg.classList.add('mode-ov');
    clearHover();
    hideLabels();
    setEdgeVisibility();
    animateTo(ovTargets());
    btnOv.disabled = true;
    showIntro();
  }
  function relayout() {
    if (mode === 'fc') {
      hideLabels(); setEdgeVisibility();
      const { t } = fcTargets(center);
      animateTo(t, () => placeLabels());
    } else setEdgeVisibility();
  }
  function centerScroll() {
    if (scroller.scrollWidth <= scroller.clientWidth + 2 && scroller.scrollHeight <= scroller.clientHeight + 2) return;
    const k = scroller.scrollWidth / DATA.W;
    scroller.scrollTo({ left: CX * k - scroller.clientWidth / 2, top: CY * (scroller.scrollHeight / DATA.H) - scroller.clientHeight / 2, behavior: reduce ? 'auto' : 'smooth' });
  }

  // ------------------------------------------------------------ hover
  function clearHover() {
    svg.classList.remove('hov');
    Object.values(nodeEl).forEach(g => g.classList.remove('on'));
    edgeEl.forEach(p => p.classList.remove('on', 'on2'));
    labEl.forEach(g => g.classList.remove('on'));
  }
  function hoverNode(id) {
    clearHover();
    if (mode === 'ov') {
      svg.classList.add('hov');
      nodeEl[id].classList.add('on');
      adj[id].forEach(i => {
        if (hidden.has(E[i].type)) return;
        edgeEl[i].classList.add('on'); nodeEl[E[i].s].classList.add('on'); nodeEl[E[i].t].classList.add('on');
      });
    } else if (id !== center) {
      adj[id].forEach(i => {
        const e = E[i];
        if (hidden.has(e.type)) return;
        if (e.s === center || e.t === center) { edgeEl[i].classList.add('on'); labEl[i].classList.add('on'); }
        else edgeEl[i].classList.add('on2');
      });
    }
  }
  function hoverEdge(i) {
    clearHover();
    edgeEl[i].classList.add('on'); labEl[i].classList.add('on');
  }

  // ------------------------------------------------------------ panel
  function pills(id) {
    const n = N[id];
    let s = `<span class="pill cat-${n.cat}">${DATA.cat[lang][n.cat]}</span>`;
    if (DATA.camp[n.camp]) s += `<span class="pill camp">${esc(DATA.camp[n.camp][lang])}</span>`;
    if (n.dies) s += `<span class="pill dead">✕ ${esc(T[lang].dies(lang === 'zh' ? n.dies : n.dies_en))}</span>`;
    return s;
  }
  function trailHtml() {
    if (trail.length < 2) return '';
    const items = trail.map((id, i) => i === trail.length - 1
      ? `<span class="cur">${esc(nm(id))}</span>`
      : `<button type="button" data-go="${id}">${esc(nm(id))}</button>`).join('<span class="sep">›</span>');
    return `<nav class="trail" aria-label="${T[lang].trail}">${items}</nav>`;
  }
  // the English name under the Chinese one, unless it only repeats the original-language name (Aeneas / AENEAS, Sun Wukong / Sūn Wùkōng);
  // English pages show no Chinese
  const plain = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z]/gi, '').toLowerCase();
  function altName(id) {
    const n = N[id];
    return lang === 'en' || plain(n.en) === plain(n.gr) ? '' : `<span class="cen">${esc(n.en)}</span>`;
  }
  function crossHtml(id) {
    return window.dpCross((DATA.cross || {})[id], lang);
  }
  function showIntro() {
    view = { kind: 'intro' };
    panel.innerHTML = INTRO_HTML;
  }
  function showNode(id) {
    view = { kind: 'node', id };
    const n = N[id], t = T[lang];
    const rels = adj[id].slice().sort((a, b) => TORDER[E[a].type] - TORDER[E[b].type]);
    const items = rels.map(i => {
      const e = E[i], other = e.s === id ? e.t : e.s;
      return `<li><button type="button" data-go="${other}">${mini(other, 30)}` +
        `<span class="who">${esc(nm(other))}<span class="pill t-${e.type}">${esc(L(e, 'label'))}</span></span>` +
        `<span class="rt">${esc(L(e, 'text'))} <span class="bk">${esc(t.bk(L(e, 'bk')))}</span></span></button></li>`;
    }).join('');
    panel.innerHTML = `${trailHtml()}
      <div class="ch"><span class="big">${mini(id, 84)}</span><div>
        <h2 class="cname">${esc(nm(id))}</h2>
        <div class="cgr">${esc(n.gr)}${altName(id)}</div>
        <div class="cmeta">${pills(id)}</div></div></div>
      <p class="cmeta" style="margin-top:8px">${esc(L(n, 'sub'))}</p>
      <p class="cbio">${esc(L(n, 'bio'))}</p>
      <p class="cicon"><b>${t.portrait}</b>${esc(L(n, 'icon'))}</p>
      ${crossHtml(id)}
      <ul class="rels" aria-label="${esc(t.rels(nm(id)))}">${items}</ul>`;
    panel.scrollTop = 0;
  }
  function showEdge(i) {
    view = { kind: 'edge', id: i };
    const e = E[i], ty = DATA.types[e.type], t = T[lang];
    labEl.forEach(g => g.classList.remove('on')); labEl[i].classList.add('on');
    panel.innerHTML = `${trailHtml()}
      <div class="pair">
        <button class="who2" type="button" data-go="${e.s}">${mini(e.s, 58)}<span class="nmx">${esc(nm(e.s))}</span></button>
        <span class="bar t-${e.type}" style="color:var(--${e.type})"></span>
        <button class="who2" type="button" data-go="${e.t}">${mini(e.t, 58)}<span class="nmx">${esc(nm(e.t))}</span></button>
      </div>
      <p class="elabel" style="color:var(--${e.type})">${esc(L(e, 'label'))}</p>
      <div class="cmeta"><span class="pill t-${e.type}">${lang === 'zh' ? ty.zh : ty.en}</span>${esc(lang === 'zh' ? ty.desc : ty.desc_en)}</div>
      <p class="etext">${esc(L(e, 'text'))}</p>
      <p class="src">${t.src}${esc(L(e, 'bk'))}</p>
      ${center ? `<button type="button" class="backlink" data-show="${center}">${esc(t.back(nm(center)))}</button>` : ''}`;
    panel.scrollTop = 0;
    if (matchMedia('(max-width: 1100px)').matches) panel.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'nearest' });
  }
  function rerenderPanel() {
    if (view.kind === 'node') showNode(view.id);
    else if (view.kind === 'edge') showEdge(view.id);
    else showIntro();
  }

  // ------------------------------------------------------------ events
  let dragMoved = false;
  svg.addEventListener('click', ev => {
    if (dragMoved) return;
    const nd = ev.target.closest('.node');
    const lb = ev.target.closest('.elab.vis, .edge.vis');
    if (nd) {
      const id = nd.dataset.id;
      if (mode === 'fc' && id === center) showNode(id);
      else focusOn(id);
    } else if (lb) showEdge(+lb.dataset.e);
    else if (mode === 'fc') toOverview();   // a click on empty space returns to the overview
  });
  svg.addEventListener('keydown', ev => {
    if (ev.key !== 'Enter' && ev.key !== ' ') return;
    const nd = ev.target.closest('.node'), lb = ev.target.closest('.elab');
    if (nd) { ev.preventDefault(); nd.dataset.id === center ? showNode(center) : focusOn(nd.dataset.id); }
    else if (lb) { ev.preventDefault(); showEdge(+lb.dataset.e); }
  });
  svg.addEventListener('pointerover', ev => {
    if (ev.pointerType === 'touch' || raf) return;
    const nd = ev.target.closest('.node'), lb = ev.target.closest('.elab.vis, .edge.vis');
    if (nd) hoverNode(nd.dataset.id);
    else if (lb) hoverEdge(+lb.dataset.e);
  });
  svg.addEventListener('pointerout', ev => {
    if (ev.pointerType === 'touch') return;
    const to = ev.relatedTarget && ev.relatedTarget.closest && ev.relatedTarget.closest('.node, .elab.vis, .edge.vis');
    if (!to) {
      clearHover();
      if (view.kind === 'edge') labEl[view.id].classList.add('on');
    }
  });
  panel.addEventListener('click', ev => {
    const go = ev.target.closest('[data-go]');
    if (go) { focusOn(go.dataset.go); return; }
    const sh = ev.target.closest('[data-show]');
    if (sh) showNode(sh.dataset.show);
  });
  btnOv.addEventListener('click', toOverview);
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && mode === 'fc') toOverview(); });

  document.querySelectorAll('.tog').forEach(b => b.addEventListener('click', () => {
    const t = b.dataset.type, on = b.getAttribute('aria-pressed') === 'true';
    b.setAttribute('aria-pressed', on ? 'false' : 'true');
    on ? hidden.add(t) : hidden.delete(t);
    relayout();
  }));

  // zoom & pan
  const LV = [1, 1.35, 1.8, 2.4];
  let z = 0;
  const updatePannable = () => scroller.classList.toggle('pannable', scroller.scrollWidth > scroller.clientWidth + 2 || scroller.scrollHeight > scroller.clientHeight + 2);
  function setZoom(nz) {
    nz = Math.max(0, Math.min(LV.length - 1, nz));
    const cxr = (scroller.scrollLeft + scroller.clientWidth / 2) / scroller.scrollWidth;
    const cyr = (scroller.scrollTop + scroller.clientHeight / 2) / scroller.scrollHeight;
    z = nz;
    svg.style.width = (LV[z] * 100) + '%';
    requestAnimationFrame(() => {
      scroller.scrollLeft = cxr * scroller.scrollWidth - scroller.clientWidth / 2;
      scroller.scrollTop = cyr * scroller.scrollHeight - scroller.clientHeight / 2;
      updatePannable();
    });
  }
  document.querySelectorAll('.toolbar [data-z]').forEach(b => b.addEventListener('click', () => {
    const d = +b.dataset.z; setZoom(d === 0 ? 0 : z + d);
  }));
  let drag = null;
  scroller.addEventListener('pointerdown', ev => {
    if (ev.pointerType !== 'mouse' || ev.button !== 0 || !scroller.classList.contains('pannable')) return;
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
    drag = null; scroller.classList.remove('dragging');
    setTimeout(() => { dragMoved = false; }, 0);
  });
  window.addEventListener('resize', updatePannable);

  // roster
  document.querySelectorAll('.rcard').forEach(b => b.addEventListener('click', () => {
    focusOn(b.dataset.id);
    document.querySelector('.stage').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }));

  // ------------------------------------------------------------ language
  function setLang(l, save) {
    lang = l === 'en' ? 'en' : 'zh';
    app.dataset.lang = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    document.title = T[lang].title;
    document.querySelectorAll('[data-setlang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setlang === lang)));
    document.querySelectorAll('.tog').forEach(b => { const ty = DATA.types[b.dataset.type]; b.title = lang === 'zh' ? ty.desc : ty.desc_en; });
    svg.querySelectorAll('text[data-zh]').forEach(t => { t.textContent = t.dataset[lang]; });
    relabel();
    if (mode === 'fc' && !raf) placeLabels();
    rerenderPanel();
    window.dpLinks(lang);
    if (save) window.dpSaveLang(lang);
  }
  document.querySelectorAll('[data-setlang]').forEach(b => b.addEventListener('click', () => setLang(b.dataset.setlang, true)));

  // ------------------------------------------------------------ init
  const tokens = window.dpHash();
  let initLang = tokens.find(x => x === 'en' || x === 'zh');
  if (!initLang) initLang = window.dpStoredLang();
  if (!initLang) {
    const nav = (navigator.languages && navigator.languages[0]) || navigator.language || 'zh';
    initLang = /^zh/i.test(nav) ? 'zh' : 'en';
  }
  setLang(initLang, false);
  IDS.forEach(id => applyNode(id, cur[id]));
  setRoles();
  updateEdges();
  requestAnimationFrame(() => {
    updatePannable();
    if (scroller.scrollWidth > scroller.clientWidth + 2) scroller.scrollLeft = (scroller.scrollWidth - scroller.clientWidth) / 2;
    const who = tokens.find(x => N[x]);
    if (who) { focusOn(who); document.querySelector('.stage').scrollIntoView({ block: 'start' }); }
  });
})();
