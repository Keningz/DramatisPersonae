/* The timeline engine, shared by the Three Kingdoms and the Red Chamber pages: the "click anyone to bring them to the
   center" map, plus a chapter slider that decides who has appeared, who has died, which side or household each person
   belongs to (the colour of the portrait's border) and which relationships exist and in what form.

   Optional, driven by DATA:
     DATA.cut     the last chapter of the original text (80 for the Red Chamber). A switch then hides everything after
                  it — later chapters, deaths, changes of household, relationship phases and the `late` biographies.
     DATA.uniform the slider gives every chapter the same width (otherwise acts carry their own f0/f1 fractions,
                  matching the overview's time axis and its "now" line)
     node.verses  poems shown in the person's card; node.born the birth family; camp entries may carry a label
     DATA.seasons a TV series: chapters are episodes, numbered through the seasons (lengths given here) and shown as
                  S3E9 / 第3季第9集; "(S3E9)" in running text becomes a chip
     DATA.spoil   nothing after the slider's episode is shown in the panel (later life events, phases, sides, deaths)
     DATA.remember the slider position is kept in the browser
     node.subs    captions that change over time [[ep, zh, en]]; node.bios biography entries shown from their episode
     node.full    full names; node.pre dead before the story begins (node.seen: first seen in a vision);
     node.down    [[from, to, zh, en, zh back, en back]] dead for a while, then brought back; node.ini a seal letter
     node.em      seal emblems over time [[ep, key]] drawn from <symbol id="em-key">; node.emHome the whole-series one
     [data-from] / [data-until] elements of the map appear only between those chapters */
(() => {
  const app = document.getElementById('app');
  const svg = document.getElementById('map');
  const scroller = document.getElementById('mapscroll');
  const panel = document.getElementById('panel');
  const btnOv = document.getElementById('btn-ov');
  const N = DATA.nodes, E = DATA.edges, IDS = DATA.order, ACTS = DATA.acts, CH = DATA.chapters;
  const CX = DATA.CX, CY = DATA.CY, K_OV = DATA.R_OV / 40, ALL = 9999, FULL = DATA.last || 120, CUT = DATA.cut || 0;
  const CAMPKEYS = Object.keys(DATA.camp);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const LATEKEY = 'dp-late-' + (DATA.page || 'x'), TKEY = 'dp-t-' + (DATA.page || 'x');
  const SEAS = DATA.seasons || null, SPOIL = !!DATA.spoil;
  const se = c => { let s = 1, n = c; for (const len of SEAS) { if (n <= len) return [s, n]; n -= len; s++; } return [s, n]; };
  const seIdx = (s, e) => SEAS.slice(0, s - 1).reduce((a, b) => a + b, 0) + e;
  const epCode = c => { const [s, e] = se(c); return `S${s}E${e}`; };

  const nodeEl = {}, ptEl = {}, nmEl = {}, sbEl = {}, embEl = {};
  svg.querySelectorAll('.node').forEach(g => {
    const id = g.dataset.id;
    nodeEl[id] = g; ptEl[id] = g.querySelector('.pt'); embEl[id] = g.querySelector('.emb');
    nmEl[id] = g.querySelector('.nm'); sbEl[id] = g.querySelector('.sb');
  });
  const edgeEl = [], labEl = [];
  const timed = [...svg.querySelectorAll('[data-from], [data-until]')];
  svg.querySelectorAll('.edge').forEach(p => edgeEl[+p.dataset.e] = p);
  svg.querySelectorAll('.elab').forEach(g => labEl[+g.dataset.e] = g);
  const adj = {};
  IDS.forEach(id => adj[id] = []);
  E.forEach((e, i) => { adj[e.s].push(i); adj[e.t].push(i); });

  const hidden = new Set();
  let lang = 'zh', mode = 'ov', center = null, view = { kind: 'intro' }, trail = [];
  let t = ALL;
  let late = !CUT;                          // with no cut, the whole book is always shown

  // ------------------------------------------------------------ time helpers
  const lastCh = () => late ? FULL : CUT;   // the last chapter on the slider
  const isAll = () => t === ALL;
  const now = () => isAll() ? lastCh() : t; // the chapter the map shows ("whole book" = the last chapter shown)
  const inBook = c => c <= lastCh();
  const isLate = c => CUT && c > CUT;
  const debuted = id => N[id].debut <= now();
  const downAt = id => !isAll() && !!N[id].down && N[id].down.some(d => t >= d[0] && t < d[1]);   // dead for a while
  const gone = id => !isAll() && (!!N[id].pre || (N[id].dies && N[id].dies <= t) || downAt(id));  // dead by the end of chapter t
  const violent = id => !!N[id].violent;                                  // only a violent death gets the ✕
  const diedInBook = id => !!N[id].pre || (N[id].dies && inBook(N[id].dies));
  const deathShown = id => !!N[id].pre || (diedInBook(id) && (!SPOIL || isAll() || N[id].dies <= t));
  const marked = id => (violent(id) && diedInBook(id) && (isAll() || gone(id))) || downAt(id);
  const spoilHide = c => SPOIL && !isAll() && c > t;                     // not yet seen at the slider's episode
  const campAt = id => {
    const n = N[id];
    if (isAll()) return late || !n.home80 ? n.home : n.home80;
    let c = n.camps[0][1];
    n.camps.forEach(([ch, cp]) => { if (ch <= t) c = cp; });
    return c;
  };
  const emAt = id => {                     // the seal emblem in force at the slider's episode
    const n = N[id];
    if (!n.em) return null;
    if (isAll()) return n.emHome;
    let k = n.em[0][1];
    n.em.forEach(([ch, g]) => { if (ch <= t) k = g; });
    return k;
  };
  const XL = 'http://www.w3.org/1999/xlink';
  const phaseIdx = (e, tt = now()) => {    // index of the phase in force at chapter tt, -1 before the first
    let k = -1;
    e.phases.forEach((p, j) => { if (p.ch <= tt) k = j; });
    return k;
  };
  const ph = i => E[i].phases[Math.max(0, phaseIdx(E[i]))];
  const active = i => phaseIdx(E[i]) >= 0;
  const typeOf = i => ph(i).type;
  const shown = i => active(i) && !hidden.has(typeOf(i));

  // ------------------------------------------------------------ text helpers
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const L = (o, k) => lang === 'zh' ? o[k] : o[k + '_en'];
  const nm = id => lang === 'zh' ? N[id].zh : N[id].en;
  const DIG = '零一二三四五六七八九';
  const cnum = n => n < 10 ? DIG[n] : n < 20 ? '十' + (n % 10 ? DIG[n % 10] : '') : n < 100 ? DIG[Math.floor(n / 10)] + '十' + (n % 10 ? DIG[n % 10] : '')
    : n === 100 ? '一百' : n < 110 ? '一百零' + DIG[n - 100] : '一百' + (n < 120 ? '一十' + (n % 10 ? DIG[n % 10] : '') : '二十');
  const chName = c => SEAS ? (([s, e]) => lang === 'zh' ? `第${s}季第${e}集` : `Season ${s}, Episode ${e}`)(se(c))
    : lang === 'zh' ? `第${cnum(c)}回` : `Chapter ${c}`;
  const chShort = c => SEAS ? epCode(c) : lang === 'zh' ? `第${c}回` : `Ch. ${c}`;
  const campName = c => DATA.camp[c][lang];
  const deathText = id => N[id].pre ? (lang === 'zh' ? `剧前已故：${N[id].death}` : `Dead before the story: ${N[id].death_en}`)
    : SEAS ? (lang === 'zh' ? `${epCode(N[id].dies)} ${N[id].death}` : `${N[id].death_en}, ${epCode(N[id].dies)}`)
    : lang === 'zh' ? `第${N[id].dies}回${N[id].death}` : `${N[id].death_en}, ch. ${N[id].dies}`;
  const subOf = id => {                    // the caption in force at the slider's chapter
    const n = N[id];
    if (!n.subs || !n.subs.length || isAll()) return L(n, 'sub');
    let s = null;
    n.subs.forEach(x => { if (x[0] <= t) s = x; });
    return s ? (lang === 'zh' ? s[1] : s[2]) : L(n, 'sub');
  };
  const T = {
    zh: { portrait: '小像', src: '出处：', back: n => `← 回到${n}`, trail: '足迹', title: DATA.title.zh,
          debut: c => `第${c}回登场`, died: '已去世', notyet: c => `第${c}回才登场`,
          aria: (n, c, s) => `${n}，${c}，${s}`, edgeAria: (a, b, l) => `${a}与${b}：${l}`,
          life: '经历', history: '这段关系的变化', camps: DATA.campsLabel ? DATA.campsLabel.zh : '所属', all: '全书',
          allTitle: () => late ? `全书${cnum(FULL)}回` : `前${cnum(CUT)}回`,
          allHint: '拖动上面的滑块，或按 ▶ 从第一回播放', play: '播放', pause: '暂停',
          newp: '登场', newr: '关系', died2: '去世', none: '本回没有图中人物的大事', stat: (p, r) => `共 ${p} 人、${r} 段关系`,
          campTo: c => `归${c}`, joined: '登场', born: b => `娘家：${b}家`, lateTag: '续', lateTitle: '后四十回（程高本续书）',
          lateBio: '后四十回', verses: '判词与曲' },
    en: { portrait: 'Portrait', src: 'Source: ', back: n => `← Back to ${n}`, trail: 'Trail', title: DATA.title.en,
          debut: c => `Appears in ch. ${c}`, died: 'Dead', notyet: c => `Appears in chapter ${c}`,
          aria: (n, c, s) => `${n}, ${c}, ${s}`, edgeAria: (a, b, l) => `${a} and ${b}: ${l}`,
          life: 'Life in the story', history: 'How this relationship changed', camps: DATA.campsLabel ? DATA.campsLabel.en : 'Sides',
          all: 'Whole book', allTitle: () => late ? `All ${FULL} chapters` : `The first ${CUT} chapters`,
          allHint: 'Drag the slider above, or press ▶ to play from chapter 1',
          play: 'Play', pause: 'Pause', newp: 'Enter', newr: 'Ties', died2: 'Die', none: 'Nothing happens to anyone on the map in this chapter',
          stat: (p, r) => `${p} people and ${r} relationships`, campTo: c => `joins ${c}`, joined: 'Enters the story',
          born: b => `née ${b}`, lateTag: 'late', lateTitle: 'Chapters 81–120 (the Cheng–Gao continuation)',
          lateBio: 'Chapters 81–120', verses: 'Verses' },
  };
  if (DATA.allHint) { T.zh.allHint = DATA.allHint.zh; T.en.allHint = DATA.allHint.en; }
  if (SEAS) {
    Object.assign(T.zh, { debut: c => `${epCode(c)} 登场`, notyet: c => `${epCode(c)} 才登场`, all: '全剧',
      mention: c => `${epCode(c)} 首次提到`, seen: c => `${epCode(c)} 在幻象中出现`, none: '本集没有图中人物的大事',
      later: n => `往后还有 ${n} 段经历，时间轴拖到后面的集数才显示。`, laterLife: n => `往后还有 ${n} 件事，拖到后面的集数才显示。` });
    Object.assign(T.en, { debut: c => `Appears in ${epCode(c)}`, notyet: c => `Appears in ${epCode(c)}`, all: 'Whole series',
      mention: c => `First mentioned in ${epCode(c)}`, seen: c => `Seen in a vision, ${epCode(c)}`,
      none: 'Nothing happens to anyone on the map in this episode',
      later: n => `${n} more passage${n > 1 ? 's' : ''} of this story appear further along the timeline.`,
      laterLife: n => `${n} more event${n > 1 ? 's' : ''} appear further along the timeline.` });
    if (DATA.allTitle) { T.zh.allTitle = () => DATA.allTitle.zh; T.en.allTitle = () => DATA.allTitle.en; }
  }
  const lateTag = c => isLate(c) ? `<span class="xu" title="${esc(T[lang].lateTitle)}">${T[lang].lateTag}</span>` : '';
  // a chapter chip in running text: "(第25回)" / "(ch. 25)" become buttons that move the timeline there
  function linkChapters(s) {
    s = esc(s);
    if (SEAS) {
      return s.replace(/\(S(\d)E(\d+)(?:[—–]S(\d)E(\d+))?\)/g, (m, s1, e1, s2, e2) =>
        `<button type="button" class="chref" data-ch="${seIdx(+s1, +e1)}">S${s1}E${e1}${s2 ? '–S' + s2 + 'E' + e2 : ''}</button>`);
    }
    if (lang === 'zh') {
      return s.replace(/\(第([0-9、至—,，]+)回\)/g, (m, g) => {
        const c = parseInt(g, 10);
        return `<button type="button" class="chref" data-ch="${c}">第${g}回</button>`;
      });
    }
    return s.replace(/\((?:ch|chs)\. ([0-9–, ]+)\)/g, (m, g) => {
      const c = parseInt(g, 10);
      return `<button type="button" class="chref" data-ch="${c}">ch. ${g}</button>`;
    });
  }
  const mini = (id, size) => {
    const sw = size < 50 ? 7 : 5, dead = marked(id);
    const mark = dead ? '<g class="dead" transform="translate(36 36)"><circle r="12"/><path d="M-5,-5 L5,5 M5,-5 L-5,5"/></g>' : '';
    const n = N[id], em = emAt(id);
    const ini = !n.ini ? '' : em
      ? `<use xlink:href="#em-${em}" href="#em-${em}" x="-36" y="-47" width="72" height="72" color="${n.ink}"/>` +
        `<text class="ini" y="31" dy=".36em" text-anchor="middle" font-size="${lang === 'zh' ? 20 : 21}" fill="${n.ink}">${esc(lang === 'zh' ? n.ini : n.ini_en)}</text>`
      : `<text class="ini" y="0" dy=".36em" text-anchor="middle" font-size="${lang === 'zh' ? 50 : 58}" fill="${n.ink}">${esc(lang === 'zh' ? n.ini : n.ini_en)}</text>`;
    return `<svg class="mini camp-${campAt(id)}${gone(id) ? ' gone' : ''}" viewBox="-56 -56 112 112" width="${size}" height="${size}" aria-hidden="true">` +
      `<use xlink:href="#pt-${id}" href="#pt-${id}" x="-50" y="-50" width="100" height="100"/>${ini}<circle class="ring" r="50" stroke-width="${sw}"/>${mark}</svg>`;
  };

  // ------------------------------------------------------------ geometry
  const R1MIN = DATA.R1[0], R1MAX = DATA.R1[1], R2 = DATA.R2;
  const cur = {};
  IDS.forEach(id => { cur[id] = { x: N[id].ox, y: N[id].oy, k: K_OV, f: 1, role: 'ov', a: 0 }; });
  function ovTargets() {
    const tg = {};
    IDS.forEach(id => { tg[id] = { x: N[id].ox, y: N[id].oy, k: K_OV, f: 1, role: 'ov', a: 0 }; });
    return tg;
  }
  function neighbors(c) {
    const m = new Map();
    adj[c].forEach(i => {
      if (!shown(i)) return;
      const e = E[i], o = e.s === c ? e.t : e.s;
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
    const kRing = Math.min(36, Math.max(22, 2 * Math.PI * R1 / Math.max(1, ring1.length) * 0.42)) / 40;
    const a1 = spread(ring1, desired);
    // people not yet in the story are parked on the outer ring too, but invisible
    const others = IDS.filter(id => id !== c && !nb.has(id));
    const a2 = spread(others, desired);
    const tg = {};
    tg[c] = { x: CX, y: CY, k: 60 / 40, f: 1, role: 'center', a: 0 };
    const crowd = kRing < 0.86 || ring1.length > 20;
    ring1.slice().sort((p, q) => a1[p] - a1[q]).forEach((id, ri) => {
      const a = a1[id];
      tg[id] = { x: CX + R1 * Math.cos(a), y: CY + R1 * Math.sin(a), k: kRing, f: 1, role: 'ring', a, ri, crowd };
    });
    others.forEach(id => {
      const a = a2[id];
      tg[id] = { x: CX + R2 * Math.cos(a), y: CY + R2 * Math.sin(a), k: 17 / 40, f: 1, role: 'outer', a };
    });
    return { t: tg, nb, R1 };
  }

  // ------------------------------------------------------------ rendering
  function applyNode(id, s) {
    nodeEl[id].setAttribute('transform', `translate(${s.x.toFixed(1)} ${s.y.toFixed(1)})`);
    ptEl[id].setAttribute('transform', `scale(${s.k.toFixed(3)})`);
  }
  function updateEdges() {
    E.forEach((e, i) => {
      const a = cur[e.s], b = cur[e.t];
      edgeEl[i].setAttribute('d', `M${a.x.toFixed(1)},${a.y.toFixed(1)} L${b.x.toFixed(1)},${b.y.toFixed(1)}`);
    });
  }
  function nodeStatus(id) {
    if (!debuted(id)) return T[lang].notyet(N[id].debut);
    return campName(campAt(id)) + (gone(id) ? (lang === 'zh' ? '，' : ', ') + T[lang].died : '');
  }
  function setNodeLabel(id) {
    const s = cur[id], role = s.role, n1 = nmEl[id], n2 = sbEl[id], r = 40 * s.k;
    n1.textContent = nm(id);
    n2.textContent = subOf(id);
    let fs1 = lang === 'en' ? 12 : 13.5, fs2 = 12, show2 = false, anchor = 'middle', x = 0, y1 = r + 16, y2 = 0;
    if (role === 'center') { fs1 = 22; fs2 = 13.5; show2 = true; y1 = r + 26; y2 = y1 + 18; }
    else if (role === 'ring' || role === 'outer') {
      const small = role === 'outer', crowd = role === 'ring' && s.crowd;
      fs1 = small ? 11.5 : crowd ? 13.5 : 16; show2 = !small && !crowd;
      const st = crowd && s.ri % 2 ? 15 : 0;
      const sn = Math.sin(s.a), cs = Math.cos(s.a);
      if (crowd) {
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
    if (anchor !== 'middle') {
      let w = 0;
      try { w = n1.getComputedTextLength(); } catch (e) { /* not rendered yet */ }
      const gx = s.x + x;
      if ((anchor === 'end' && gx - w < 4) || (anchor === 'start' && gx + w > DATA.W - 4)) {
        anchor = 'middle'; x = 0; y1 = r + fs1 + 2; y2 = y1 + fs2 + 3; put();
      }
    }
    n2.style.display = show2 ? '' : 'none';
    nodeEl[id].setAttribute('aria-label', T[lang].aria(nm(id), nodeStatus(id), subOf(id)));
  }
  function staggerOv() {
    if (mode !== 'ov') return;
    // portraits count as taken space too, so a dropped name does not land on the face below
    const placed = IDS.filter(debuted).map(id => { const s = cur[id], r = 40 * s.k * 0.92; return [s.x - r, s.y - r, s.x + r, s.y + r]; });
    const hit = b => placed.some(o => b[0] < o[2] + 3 && b[2] > o[0] - 3 && b[1] < o[3] && b[3] > o[1]);
    IDS.filter(debuted).sort((a, b) => cur[a].x - cur[b].x).forEach(id => {
      const tx = nmEl[id], s = cur[id];
      let bb;
      try { bb = tx.getBBox(); } catch (e) { return; }
      const box0 = [s.x + bb.x, s.y + bb.y, s.x + bb.x + bb.width, s.y + bb.y + bb.height];
      // where two names would touch, the later one drops a line, or two
      let dy = 0;
      if (bb.width) {
        const area = d => { const b = [box0[0], box0[1] + d, box0[2], box0[3] + d]; return overlapSum(b, placed); };
        const tries = [0, 12, 24].map(d => [d, hit([box0[0], box0[1] + d, box0[2], box0[3] + d]) ? area(d) + 1 : 0]);
        const free = tries.find(([, a]) => a === 0);
        dy = free ? free[0] : tries.sort((p, q) => p[1] - q[1])[0][0];
      }
      if (dy) tx.setAttribute('y', (+tx.getAttribute('y') + dy).toFixed(1));
      placed.push([box0[0], box0[1] + dy, box0[2], box0[3] + dy]);
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
  function animateTo(targets, done, dur0) {
    if (raf) cancelAnimationFrame(raf);
    const from = {};
    IDS.forEach(id => {
      from[id] = { ...cur[id] };
      cur[id].role = targets[id].role; cur[id].a = targets[id].a; cur[id].ri = targets[id].ri || 0; cur[id].crowd = !!targets[id].crowd;
    });
    setRoles();
    const dur = reduce ? 0 : (dur0 === undefined ? 720 : dur0), t0 = performance.now();
    svg.classList.add('moving');
    const step = tnow => {
      const p = dur ? Math.min(1, (tnow - t0) / dur) : 1;
      const k = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
      IDS.forEach(id => {
        const a = from[id], b = targets[id];
        const s = { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, k: a.k + (b.k - a.k) * k, f: 1 };
        Object.assign(cur[id], s);
        applyNode(id, s);
      });
      updateEdges();
      if (p < 1) raf = requestAnimationFrame(step);
      else { raf = null; svg.classList.remove('moving'); relabel(); done && done(); }
    };
    raf = requestAnimationFrame(step);
  }

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
      if (!debuted(id)) return;
      const s = cur[id], r = 40 * s.k + 3;
      boxes.push([s.x - r, s.y - r, s.x + r, s.y + r]);
      if (s.role === 'ring' || s.role === 'center') {
        [nmEl[id], sbEl[id]].forEach(tx => {
          if (tx.style.display === 'none' || !tx.textContent) return;
          try { const bb = tx.getBBox(); boxes.push([s.x + bb.x, s.y + bb.y, s.x + bb.x + bb.width, s.y + bb.y + bb.height]); } catch (e) { /* not rendered */ }
        });
      }
    });
    const other = i => E[i].s === center ? E[i].t : E[i].s;
    const list = adj[center].filter(shown).sort((a, b) => cur[other(a)].a - cur[other(b)].a);
    list.forEach(i => {
      const g = labEl[i], tx = g.querySelector('text'), rc = g.querySelector('rect');
      const e = E[i], p = ph(i);
      tx.textContent = L(p, 'label');
      g.setAttribute('class', `elab t-${p.type}${p.ch === t ? ' fresh' : ''}`);
      let w = 60;
      try { w = tx.getComputedTextLength() + 16; } catch (err) { /* keep estimate */ }
      const h = 21;
      const a = cur[center], b = cur[other(i)];
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
      tx.setAttribute('x', best.x.toFixed(1)); tx.setAttribute('y', (best.y + 4.6).toFixed(1));
      g.setAttribute('aria-label', T[lang].edgeAria(nm(e.s), nm(e.t), L(p, 'label')));
      g.setAttribute('tabindex', '0');
      g.classList.add('vis');
    });
  }
  function setEdgeVisibility() {
    E.forEach((e, i) => {
      const k = phaseIdx(e), p = e.phases[Math.max(0, k)];
      const el = edgeEl[i];
      el.setAttribute('class', `edge t-${p.type}`);
      el.classList.toggle('off', k < 0 || hidden.has(p.type));
      el.classList.toggle('past', k >= 0 && (gone(e.s) || gone(e.t)));
      el.classList.toggle('fresh', !isAll() && k >= 0 && p.ch === t);
      el.classList.toggle('vis', mode === 'fc' && (e.s === center || e.t === center) && shown(i));
    });
  }
  function setNodeStates() {
    IDS.forEach(id => {
      const g = nodeEl[id], n = N[id];
      CAMPKEYS.forEach(c => g.classList.remove('camp-' + c));
      g.classList.add('camp-' + campAt(id));
      g.classList.toggle('fut', !debuted(id));
      g.classList.toggle('gone', !!gone(id));
      g.classList.toggle('isdead', marked(id));
      g.classList.toggle('fresh', !isAll() && n.debut === t);
      g.classList.toggle('dying', !isAll() && ((violent(id) && n.dies === t) || (!!n.down && n.down.some(d => d[0] === t))));
      const k = emAt(id), u = embEl[id];
      if (k && u && u.dataset.k !== k) {
        u.setAttribute('href', '#em-' + k); u.setAttributeNS(XL, 'xlink:href', '#em-' + k); u.dataset.k = k;
      }
    });
    const nc = now();
    timed.forEach(el => {
      const f = +(el.dataset.from || 0), u = +(el.dataset.until || 1e9);
      el.style.display = nc >= f && nc < u ? '' : 'none';
    });
  }

  // ------------------------------------------------------------ modes
  function focusOn(id, opts = {}) {
    if (!N[id]) return;
    if (!debuted(id)) setTime(N[id].debut, { quiet: true });   // a person not yet in the story: jump to their entrance
    center = id; mode = 'fc';
    svg.classList.remove('mode-ov', 'hov'); svg.classList.add('mode-fc');
    clearHover();
    hideLabels();
    const { t: tg } = fcTargets(id);
    setEdgeVisibility();
    animateTo(tg, () => { placeLabels(); centerScroll(); });
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
  function relayout(dur) {
    if (mode === 'fc') {
      hideLabels(); setEdgeVisibility();
      const { t: tg } = fcTargets(center);
      animateTo(tg, () => placeLabels(), dur);
    } else { setEdgeVisibility(); relabel(); }
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
    if (!debuted(id)) return;
    if (mode === 'ov') {
      svg.classList.add('hov');
      nodeEl[id].classList.add('on');
      adj[id].forEach(i => {
        if (!shown(i)) return;
        edgeEl[i].classList.add('on'); nodeEl[E[i].s].classList.add('on'); nodeEl[E[i].t].classList.add('on');
      });
    } else if (id !== center) {
      adj[id].forEach(i => {
        const e = E[i];
        if (!shown(i)) return;
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
    const n = N[id], tt = T[lang];
    let s = `<span class="pill campp camp-${campAt(id)}">${esc(campName(campAt(id)))}</span>`;
    s += `<span class="pill chp">${esc(n.pre && tt.mention ? tt.mention(n.debut) : tt.debut(n.debut))}</span>`;
    if (n.pre && n.seen && tt.seen && !spoilHide(n.seen)) s += `<span class="pill chp">${esc(tt.seen(n.seen))}</span>`;
    if (deathShown(id)) s += (violent(id) ? `<span class="pill dead">✕ ${esc(deathText(id))}</span>` : `<span class="pill nat">${esc(deathText(id))}</span>`) + lateTag(n.dies);
    else if (downAt(id)) { const d = n.down.find(x => t >= x[0] && t < x[1]); s += `<span class="pill dead">✕ ${esc(epCode(d[0]) + ' ' + (lang === 'zh' ? d[2] : d[3]))}</span>`; }
    if (n.born) s += `<span class="pill chp">${esc(tt.born(lang === 'zh' ? n.born : n.born_en))}</span>`;
    return s;
  }
  function trailHtml() {
    if (trail.length < 2) return '';
    const items = trail.map((id, i) => i === trail.length - 1
      ? `<span class="cur">${esc(nm(id))}</span>`
      : `<button type="button" data-go="${id}">${esc(nm(id))}</button>`).join('<span class="sep">›</span>');
    return `<nav class="trail" aria-label="${T[lang].trail}">${items}</nav>`;
  }
  const plain = s => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z]/gi, '').toLowerCase();
  function altName(id) {
    const n = N[id], other = lang === 'zh' ? n.en : n.zh;
    return lang === 'zh' && plain(other) === plain(n.gr) ? '' : `<span class="cen">${esc(other)}</span>`;
  }
  const when = c => isAll() ? '' : c > t ? ' later' : c === t ? ' nowc' : '';
  const chipBtn = c => `<button type="button" class="chref" data-ch="${c}">${esc(chShort(c))}</button>`;
  const campLabel = c => c.length > 2 ? `<span class="clab">${esc(lang === 'zh' ? c[2] : c[3])}</span>` : '';
  function campLine(id) {
    const cs = N[id].camps.filter(c => inBook(c[0]) && !spoilHide(c[0]));
    if (cs.length < 2) return '';
    return `<p class="camps"><b>${T[lang].camps}</b>` + cs.map(c =>
      `<span class="cstep${when(c[0])}">${chipBtn(c[0])}<span class="pill campp camp-${c[1]}">${esc(campName(c[1]))}</span>${campLabel(c)}</span>`).join('<span class="arr">→</span>') + '</p>';
  }
  function showIntro() {
    view = { kind: 'intro' };
    panel.innerHTML = INTRO_HTML;
  }
  // a person's life, in story order: entrance, change of side, every phase of every relationship, death
  function lifeItems(id) {
    const n = N[id], tt = T[lang], items = [];
    items.push({ c: n.debut, o: 0, html: `<span class="ev ev-in">${esc(tt.joined)}</span>` });
    n.camps.slice(1).forEach(c => items.push({ c: c[0], o: 1, html: c.length > 2
      ? `<span class="ev">${esc(lang === 'zh' ? c[2] : c[3])}</span><span class="pill campp camp-${c[1]}">${esc(campName(c[1]))}</span>`
      : `<span class="ev">${esc(tt.campTo(campName(c[1])))}</span><span class="pill campp camp-${c[1]}">${esc(campName(c[1]))}</span>` }));
    adj[id].forEach(i => {
      const e = E[i], other = e.s === id ? e.t : e.s;
      e.phases.forEach(p => {
        if (hidden.has(p.type)) return;
        items.push({ c: p.ch, o: 2, html:
          `<button type="button" class="lwho" data-go="${other}">${mini(other, 26)}<span>${esc(nm(other))}</span></button>` +
          `<button type="button" class="pill t-${p.type}" data-edge="${i}">${esc(L(p, 'label'))}</button>` +
          `<span class="ltext">${esc(L(p, 'text'))}</span>` });
      });
    });
    if (n.dies) items.push({ c: n.dies, o: 3, html: violent(id) ? `<span class="ev ev-out">✕ ${esc(L(n, 'death'))}</span>` : `<span class="ev ev-nat">${esc(L(n, 'death'))}</span>` });
    (n.down || []).forEach(d => {
      items.push({ c: d[0], o: 3, html: `<span class="ev ev-out">✕ ${esc(lang === 'zh' ? d[2] : d[3])}</span>` });
      items.push({ c: d[1], o: 0, html: `<span class="ev ev-in">${esc(lang === 'zh' ? d[4] : d[5])}</span>` });
    });
    items.sort((a, b) => a.c - b.c || a.o - b.o);
    return items.filter(it => inBook(it.c));
  }
  function verseHtml(id) {
    const vs = N[id].verses;
    if (!vs || !vs.length) return '';
    const tt = T[lang];
    return `<h3 class="lifeh">${tt.verses}</h3>` + vs.map(v => {
      const title = lang === 'zh' ? v.t[0] : v.t[1];
      const pic = v.pic ? `<p class="vpic">${esc(lang === 'zh' ? v.pic[0] : v.pic[1])}</p>` : '';
      const lines = (lang === 'zh' ? v.zh : v.en).map(l => `<span class="vl">${esc(l)}</span>`).join('');
      const orig = lang === 'zh' ? '' : `<p class="vorig" lang="zh-CN">${v.zh.map(l => `<span class="vl">${esc(l)}</span>`).join('')}</p>`;
      const note = v.note ? `<p class="vnote">${esc(lang === 'zh' ? v.note[0] : v.note[1])}</p>` : '';
      return `<figure class="verse v-${v.k}"><figcaption>${esc(title)}</figcaption>${pic}<p class="vtext">${lines}</p>${orig}${note}</figure>`;
    }).join('');
  }
  function showNode(id) {
    view = { kind: 'node', id };
    const n = N[id], tt = T[lang];
    let lastC = 0;
    const all = lifeItems(id), items = all.filter(it => !spoilHide(it.c)), hiddenN = all.length - items.length;
    const life = items.map(it => {
      const head = it.c !== lastC ? chipBtn(it.c) + lateTag(it.c) : '<span class="chref ghost"></span>';
      lastC = it.c;
      return `<li class="litem${when(it.c)}${isLate(it.c) ? ' lt' : ''}">${head}<div class="lbody">${it.html}</div></li>`;
    }).join('');
    const lateBio = late && n.late ? `<p class="cbio cbio-late"><span class="latehd">${esc(tt.lateBio)}</span>${linkChapters(L(n, 'late'))}</p>` : '';
    let bio;
    if (n.bios) {                 // entries shown from their episode on
      const vis = n.bios.filter(b => !spoilHide(b[0])), rest = n.bios.length - vis.length;
      bio = vis.map(b => `<p class="cbio">${linkChapters(lang === 'zh' ? b[1] : b[2])}</p>`).join('') +
        (rest ? `<p class="cbio spoil">${esc(tt.later(rest))}</p>` : '');
    } else bio = `<p class="cbio">${linkChapters(L(n, 'bio'))}</p>`;
    const nameLine = n.full ? `${esc(L(n, 'full'))}<span class="cen">${esc(lang === 'zh' ? n.full_en : n.full)}</span>` : esc(n.gr) + altName(id);
    panel.innerHTML = `${trailHtml()}
      <div class="ch"><span class="big">${mini(id, 84)}</span><div>
        <h2 class="cname">${esc(nm(id))}</h2>
        <div class="cgr">${nameLine}</div>
        <div class="cmeta">${pills(id)}</div></div></div>
      <p class="cmeta" style="margin-top:8px">${esc(subOf(id))}</p>
      ${campLine(id)}
      ${bio}
      ${lateBio}
      ${n.icon ? `<p class="cicon"><b>${tt.portrait}</b>${linkChapters(L(n, 'icon'))}</p>` : ''}
      ${verseHtml(id)}
      <h3 class="lifeh">${tt.life}</h3>
      <ol class="life">${life}</ol>${hiddenN && tt.laterLife ? `<p class="cbio spoil">${esc(tt.laterLife(hiddenN))}</p>` : ''}`;
    panel.scrollTop = 0;
  }
  function showEdge(i) {
    view = { kind: 'edge', id: i };
    const e = E[i], tt = T[lang], k = phaseIdx(e), p = e.phases[Math.max(0, k)], ty = DATA.types[p.type];
    labEl.forEach(g => g.classList.remove('on')); if (labEl[i]) labEl[i].classList.add('on');
    const phs = e.phases.filter(q => inBook(q.ch) && !spoilHide(q.ch));
    const hist = phs.map((q, j) =>
      `<li class="hitem${j === k ? ' nowp' : ''}${!isAll() && q.ch > t ? ' later' : ''}${isLate(q.ch) ? ' lt' : ''}">${chipBtn(q.ch)}${lateTag(q.ch)}<div class="lbody">` +
      `<span class="pill t-${q.type}">${esc(lang === 'zh' ? DATA.types[q.type].zh : DATA.types[q.type].en)}</span>` +
      `<b class="hl">${esc(L(q, 'label'))}</b><span class="ltext">${esc(L(q, 'text'))}</span>` +
      ((q.alt !== undefined ? q.alt : q.bk_en !== `Chapter ${q.ch}`) ? `<span class="src">${tt.src}${esc(L(q, 'bk'))}</span>` : '') + '</div></li>').join('');
    panel.innerHTML = `${trailHtml()}
      <div class="pair">
        <button class="who2" type="button" data-go="${e.s}">${mini(e.s, 58)}<span class="nmx">${esc(nm(e.s))}</span></button>
        <span class="bar t-${p.type}" style="color:var(--${p.type})"></span>
        <button class="who2" type="button" data-go="${e.t}">${mini(e.t, 58)}<span class="nmx">${esc(nm(e.t))}</span></button>
      </div>
      <p class="elabel" style="color:var(--${p.type})">${esc(L(p, 'label'))}</p>
      <div class="cmeta"><span class="pill t-${p.type}">${lang === 'zh' ? ty.zh : ty.en}</span>${esc(lang === 'zh' ? ty.desc : ty.desc_en)}</div>
      <p class="etext">${esc(L(p, 'text'))}</p>
      <p class="src">${tt.src}${esc(L(p, 'bk'))}${lateTag(p.ch)}</p>
      ${phs.length > 1 ? `<h3 class="lifeh">${tt.history}</h3><ol class="life hist">${hist}</ol>` : ''}
      ${center ? `<button type="button" class="backlink" data-show="${center}">${esc(tt.back(nm(center)))}</button>` : ''}`;
    panel.scrollTop = 0;
    if (matchMedia('(max-width: 1100px)').matches) panel.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'nearest' });
  }
  function rerenderPanel() {
    if (view.kind === 'node') showNode(view.id);
    else if (view.kind === 'edge') showEdge(view.id);
    else showIntro();
  }

  // ------------------------------------------------------------ timeline
  const track = document.getElementById('tl-track'), handle = document.getElementById('tl-handle');
  const fill = document.getElementById('tl-fill'), playBtn = document.getElementById('tl-play');
  const allBtn = document.getElementById('tl-all'), chEl = document.getElementById('tl-ch');
  const titleEl = document.getElementById('tl-title'), statEl = document.getElementById('tl-stat');
  const lateBtn = document.getElementById('tl-late');
  const actEls = [...document.querySelectorAll('.tlact')];
  const nowLine = svg.querySelector('.nowline'), nowTxt = nowLine && svg.querySelector('.nowline text');
  const FR = DATA.trackFrac;       // the acts take this share of the track; "whole book" takes the rest
  // each act's share of the act part of the track: fixed (matching the map's time axis) or by chapter count
  let actF = [];
  function layoutActs() {
    const lc = lastCh();
    actF = ACTS.map(a => DATA.uniform ? { f0: (a.a - 1) / lc, f1: Math.min(a.b, lc) / lc } : { f0: a.f0, f1: a.f1 });
    actEls.forEach((el, j) => {
      const on = ACTS[j].a <= lc;
      el.hidden = !on;
      el.style.flex = on ? `${(actF[j].f1 - actF[j].f0).toFixed(5)} 1 0` : '';
      el.classList.toggle('lateact', isLate(ACTS[j].a));
    });
    track.setAttribute('aria-valuemax', String(lc + 1));
  }
  function frac(c) {
    for (let j = 0; j < ACTS.length; j++) {
      const a = ACTS[j], f = actF[j];
      if (c <= a.b) return f.f0 + (f.f1 - f.f0) * ((c - a.a + 0.5) / (a.b - a.a + 1));
    }
    return 1;
  }
  function chapterAt(f) {
    if (f > FR) return ALL;
    const g = f / FR, lc = lastCh();
    for (let j = 0; j < ACTS.length; j++) {
      const a = ACTS[j], af = actF[j];
      if (a.a > lc) break;
      if (g <= af.f1) return Math.max(a.a, Math.min(a.b, lc, a.a + Math.floor((g - af.f0) / (af.f1 - af.f0) * (a.b - a.a + 1))));
    }
    return lc;
  }
  function renderTimeline() {
    const tt = T[lang];
    const pos = isAll() ? (FR + 1) / 2 : frac(t) * FR;
    handle.style.left = (pos * 100) + '%';
    fill.style.width = (pos * 100) + '%';
    track.classList.toggle('all', isAll());
    track.classList.toggle('inlate', !isAll() && isLate(t));
    track.setAttribute('aria-valuenow', String(isAll() ? lastCh() + 1 : t));
    track.setAttribute('aria-valuetext', isAll() ? tt.allTitle() : `${chName(t)} ${CH[t - 1][lang]}`);
    allBtn.setAttribute('aria-pressed', String(isAll()));
    chEl.innerHTML = isAll() ? esc(tt.allTitle()) : esc(chName(t)) + lateTag(t);
    titleEl.textContent = isAll() ? tt.allHint : CH[t - 1][lang];
    actEls.forEach((el, j) => el.classList.toggle('cur', !isAll() && t >= ACTS[j].a && t <= ACTS[j].b));
    // what happens in this chapter
    if (isAll()) {
      const np = IDS.filter(id => inBook(N[id].debut)).length, nr = E.filter(e => inBook(e.phases[0].ch)).length;
      statEl.innerHTML = esc(tt.stat(np, nr));
    } else {
      const nu = IDS.filter(id => N[id].debut === t && !N[id].pre),
        de = IDS.filter(id => N[id].dies === t || (N[id].down && N[id].down.some(d => d[0] === t)));
      const nr = E.filter(e => e.phases.some(p => p.ch === t)).length;
      const who = ids => ids.map(id => `<button type="button" data-go="${id}">${esc(nm(id))}</button>`).join(lang === 'zh' ? '、' : ', ');
      const parts = [];
      if (nu.length) parts.push(`<span class="st st-in">${tt.newp}</span>${who(nu)}`);
      if (nr) parts.push(`<span class="st st-r">${tt.newr}</span>${nr}`);
      if (de.length) parts.push(`<span class="st st-out">${tt.died2}</span>${who(de)}`);
      statEl.innerHTML = parts.length ? parts.join('<span class="sep">·</span>') : `<span class="none">${tt.none}</span>`;
    }
    // the "now" line on the map
    if (nowLine) {
      if (isAll()) nowLine.style.display = 'none';
      else {
        nowLine.style.display = '';
        const x = DATA.X0 + (DATA.X1 - DATA.X0) * frac(t);
        nowLine.setAttribute('transform', `translate(${x.toFixed(1)} 0)`);
        nowTxt.textContent = String(t);
        // on a narrow screen the map scrolls sideways: keep the "now" line in view
        if (mode === 'ov' && scroller.scrollWidth > scroller.clientWidth + 2) {
          const px = x / DATA.W * scroller.scrollWidth;
          if (px < scroller.scrollLeft + 40 || px > scroller.scrollLeft + scroller.clientWidth - 40) {
            scroller.scrollLeft = Math.max(0, px - scroller.clientWidth * 0.6);
          }
        }
      }
    }
    // the line-type toggles count what is on the map now
    document.querySelectorAll('.tog').forEach(b => {
      const ty = b.dataset.type;
      b.querySelector('.tc').textContent = String(E.filter((e, i) => active(i) && typeOf(i) === ty).length);
    });
  }
  function setTime(nt, opts = {}) {
    nt = nt === ALL ? ALL : Math.max(1, Math.min(lastCh(), nt));
    if (nt === t && !opts.force) return;
    t = nt;
    if (DATA.remember) { try { localStorage.setItem(TKEY, String(t)); } catch (e) { /* storage unavailable */ } }
    setNodeStates();
    renderTimeline();
    if (opts.quiet) { setEdgeVisibility(); relabel(); return; }
    if (mode === 'fc') {
      clearHover();
      relayout(opts.fast ? 260 : 480);
    } else { setEdgeVisibility(); relabel(); }
    if (view.kind === 'node' || view.kind === 'edge') rerenderPanel();
  }
  // the switch for the last forty chapters
  function setLate(on, save) {
    if (!CUT) return;
    late = !!on;
    if (lateBtn) lateBtn.setAttribute('aria-pressed', String(late));
    app.classList.toggle('late-on', late);
    if (save) { try { localStorage.setItem(LATEKEY, late ? '1' : '0'); } catch (e) { /* storage unavailable */ } }
    layoutActs();
    if (!isAll() && t > lastCh()) t = lastCh();
    setTime(t, { force: true });
  }
  if (lateBtn) lateBtn.addEventListener('click', () => { stopPlay(); setLate(!late, true); });
  let playing = null;
  function stopPlay() {
    if (!playing) return;
    clearInterval(playing); playing = null;
    playBtn.classList.remove('on'); playBtn.setAttribute('aria-label', T[lang].play);
    playBtn.querySelector('.ic').textContent = '▶';
  }
  function startPlay() {
    if (isAll() || t >= lastCh()) setTime(1, { fast: true });
    playBtn.classList.add('on'); playBtn.setAttribute('aria-label', T[lang].pause);
    playBtn.querySelector('.ic').textContent = '❚❚';
    playing = setInterval(() => {
      if (t >= lastCh()) { stopPlay(); return; }
      setTime(t + 1, { fast: true });
    }, reduce ? 900 : 650);
  }
  playBtn.addEventListener('click', () => playing ? stopPlay() : startPlay());
  allBtn.addEventListener('click', () => { stopPlay(); setTime(isAll() ? lastCh() : ALL); });
  let tdrag = false;
  const fromPointer = ev => {
    const r = track.getBoundingClientRect();
    return chapterAt(Math.max(0, Math.min(1, (ev.clientX - r.left) / r.width)));
  };
  track.addEventListener('pointerdown', ev => {
    if (ev.button !== undefined && ev.button !== 0) return;
    stopPlay(); tdrag = true;
    track.setPointerCapture(ev.pointerId);
    track.classList.add('drag');
    setTime(fromPointer(ev), { fast: true });
    ev.preventDefault();
  });
  track.addEventListener('pointermove', ev => { if (tdrag) setTime(fromPointer(ev), { fast: true }); });
  const endDrag = () => { if (!tdrag) return; tdrag = false; track.classList.remove('drag'); };
  track.addEventListener('pointerup', endDrag);
  track.addEventListener('pointercancel', endDrag);
  track.addEventListener('keydown', ev => {
    const k = ev.key, lc = lastCh();
    let nt = null;
    if (k === 'ArrowRight' || k === 'ArrowUp') nt = isAll() ? ALL : t >= lc ? ALL : t + 1;
    else if (k === 'ArrowLeft' || k === 'ArrowDown') nt = isAll() ? lc : t - 1;
    else if (k === 'PageUp') nt = isAll() ? ALL : Math.min(lc, t + 10);
    else if (k === 'PageDown') nt = Math.max(1, (isAll() ? lc : t) - 10);
    else if (k === 'Home') nt = 1;
    else if (k === 'End') nt = ALL;
    if (nt !== null) { ev.preventDefault(); stopPlay(); setTime(nt); }
  });
  statEl.addEventListener('click', ev => { const go = ev.target.closest('[data-go]'); if (go) { stopPlay(); focusOn(go.dataset.go); } });

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
    else if (mode === 'fc') toOverview();
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
      if (view.kind === 'edge' && labEl[view.id]) labEl[view.id].classList.add('on');
    }
  });
  panel.addEventListener('click', ev => {
    const chb = ev.target.closest('[data-ch]');
    if (chb) {
      stopPlay();
      const c = +chb.dataset.ch;
      if (CUT && c > CUT && !late) setLate(true, true);
      setTime(c); return;
    }
    const ed = ev.target.closest('[data-edge]');
    if (ed) { showEdge(+ed.dataset.edge); return; }
    const go = ev.target.closest('[data-go]');
    if (go) { focusOn(go.dataset.go); return; }
    const sh = ev.target.closest('[data-show]');
    if (sh) showNode(sh.dataset.show);
  });
  btnOv.addEventListener('click', toOverview);
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && mode === 'fc') toOverview(); });

  document.querySelectorAll('.tog').forEach(b => b.addEventListener('click', () => {
    const ty = b.dataset.type, on = b.getAttribute('aria-pressed') === 'true';
    b.setAttribute('aria-pressed', on ? 'false' : 'true');
    on ? hidden.add(ty) : hidden.delete(ty);
    relayout();
    if (view.kind === 'node') showNode(view.id);
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

  document.querySelectorAll('.rcard').forEach(b => b.addEventListener('click', () => {
    focusOn(b.dataset.id);
    document.querySelector('.stage').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }));
  // the intro's chapter buttons ([data-ch]) are handled by the panel's click handler above

  // ------------------------------------------------------------ language
  function setLang(l, save) {
    lang = l === 'en' ? 'en' : 'zh';
    app.dataset.lang = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    document.title = T[lang].title;
    document.querySelectorAll('[data-setlang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setlang === lang)));
    document.querySelectorAll('.tog').forEach(b => { const ty = DATA.types[b.dataset.type]; b.title = lang === 'zh' ? ty.desc : ty.desc_en; });
    svg.querySelectorAll('text[data-zh]').forEach(tx => { tx.textContent = tx.dataset[lang]; });
    playBtn.setAttribute('aria-label', playing ? T[lang].pause : T[lang].play);
    renderTimeline();
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
  if (CUT) {
    let stored = null;
    try { stored = localStorage.getItem(LATEKEY); } catch (e) { /* storage unavailable */ }
    late = stored === '1';
    if (tokens.includes('full')) late = true;
    if (tokens.includes('cut')) late = false;
    if (lateBtn) lateBtn.setAttribute('aria-pressed', String(late));
    app.classList.toggle('late-on', late);
  }
  let chTok = tokens.map(x => /^c(\d{1,3})$/.exec(x)).find(Boolean);
  if (SEAS && !chTok) {
    const m = tokens.map(x => /^s(\d)e(\d{1,2})$/.exec(x)).find(Boolean);
    if (m) chTok = [m[0], String(seIdx(+m[1], +m[2]))];
  }
  if (!chTok && DATA.remember && !tokens.includes('all')) {
    let st = null;
    try { st = localStorage.getItem(TKEY); } catch (e) { /* storage unavailable */ }
    if (st && /^\d{1,3}$/.test(st) && +st !== ALL) chTok = ['', st];
  }
  if (chTok) {
    if (CUT && +chTok[1] > CUT) { late = true; if (lateBtn) lateBtn.setAttribute('aria-pressed', 'true'); app.classList.add('late-on'); }
    t = Math.max(1, Math.min(lastCh(), +chTok[1]));
  }
  layoutActs();
  setNodeStates();
  setEdgeVisibility();
  setLang(initLang, false);
  IDS.forEach(id => applyNode(id, cur[id]));
  setRoles();
  updateEdges();
  requestAnimationFrame(() => {
    updatePannable();
    relabel();
    if (scroller.scrollWidth > scroller.clientWidth + 2) scroller.scrollLeft = (scroller.scrollWidth - scroller.clientWidth) / 2;
    if (!isAll()) renderTimeline();
    const who = tokens.find(x => N[x]);
    if (who) { focusOn(who); document.querySelector('.stage').scrollIntoView({ block: 'start' }); }
  });
})();
