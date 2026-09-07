/* かいごしごと 共通スクリプト
 *
 * 方針
 * - 数値は必ず先に確定値をDOMに入れてからアニメーションする。
 *   requestAnimationFrame が動かない環境（バックグラウンドタブ・省電力・
 *   描画停止中）でも、0や古い値のまま残らないようにするため。
 * - localStorage は例外を投げうる（プライベートモード、サイトデータ拒否）ため
 *   すべて try/catch で包み、失敗しても機能が落ちるだけで画面は壊さない。
 * - 対象要素が無いページでも安全に何もしないこと。
 * - prefers-reduced-motion を尊重し、その場合は動かさず結果だけ出す。
 */
(function () {
  'use strict';

  var reduce = false;
  try {
    reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) {}

  // ---------------------------------------------------------- localStorage
  var K_YAKIN = 'kaigo.yakin';
  var K_HIST = 'kaigo.recent';

  function load(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function save(key, val) {
    try { localStorage.setItem(key, val); } catch (e) {}
  }
  function loadJSON(key) {
    var raw = load(key);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  }
  function num(n) {
    return Number(n || 0).toLocaleString('ja-JP');
  }

  // ------------------------------------------------------------- 数値の増減
  function animateNumber(el, from, to, dur) {
    el.textContent = num(to);              // 先に確定値
    if (reduce || from === to) return;
    var t0 = null;
    var token = (el._tk = (el._tk || 0) + 1);
    function step(t) {
      if (el._tk !== token) return;        // 新しい指示が来ていれば降りる
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = num(Math.round(from + (to - from) * e));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // 画面に入ったら一度だけ実行する
  var seen = [];
  function onView(el, fn) {
    if (!el) return;
    if (!('IntersectionObserver' in window)) { fn(); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting || seen.indexOf(en.target) !== -1) return;
        seen.push(en.target);
        fn();
        io.unobserve(en.target);
      });
    }, { threshold: 0.25 });
    io.observe(el);
  }

  // ------------------------------------------- 01 ヒーロー統計のカウントアップ
  function initCounters() {
    var els = document.querySelectorAll('[data-count]');
    if (!els.length) return;
    // JSやrAFが動かなくても正しい件数が見えている状態にしておく
    Array.prototype.forEach.call(els, function (el) {
      el.textContent = num(+el.getAttribute('data-count'));
    });
    if (reduce) return;
    var host = els[0].closest('.h-meta, .h-stat, .yakinhero, .searchhero, .thero-copy') || els[0];
    onView(host, function () {
      Array.prototype.forEach.call(els, function (el) {
        animateNumber(el, 0, +el.getAttribute('data-count'), 800);
      });
    });
  }

  // ------------------------------------------- 02 掲載情報の充実度バーが伸びる
  function initBars() {
    var bars = document.querySelectorAll('.cov-bar i[data-w]');
    if (!bars.length) return;
    var host = document.querySelector('.coverage');

    function finish(stagger) {
      Array.prototype.forEach.call(bars, function (b, i) {
        var go = function () { b.style.width = b.getAttribute('data-w') + '%'; };
        if (stagger) setTimeout(go, i * 70); else go();
      });
    }
    if (reduce || !host || !('IntersectionObserver' in window)) { finish(false); return; }

    Array.prototype.forEach.call(bars, function (b) { b.style.width = '0%'; });
    var done = false;
    function run(stagger) {
      if (done) return;
      done = true;
      finish(stagger);
    }
    onView(host, function () { run(true); });
    // 保険：IntersectionObserver が発火しない環境（描画停止・省電力など）でも
    // バーが0%のまま残らないよう、一定時間後に必ず最終値にする
    setTimeout(function () { run(false); }, 2500);
  }

  // ------------------------------------------------ 03 選んだ夜勤条件を覚える
  function rememberYakin(key, label, count) {
    if (!key || !label) return;
    save(K_YAKIN, JSON.stringify({ k: key, l: label, c: count || 0 }));
  }

  function initYakinMemory() {
    // A の夜勤ピッカー
    Array.prototype.forEach.call(document.querySelectorAll('.ypick[data-yk]'), function (a) {
      a.addEventListener('click', function () {
        rememberYakin(a.getAttribute('data-yk'), a.getAttribute('data-yk-label'),
          +a.getAttribute('data-yk-count'));
      });
    });
  }

  // 「前回の続きから」の帯を出す
  function initResume() {
    var mount = document.getElementById('resumeMount');
    if (!mount) return;
    var v = loadJSON(K_YAKIN);
    if (!v || !v.l) return;
    var el = document.createElement('div');
    el.className = 'resume';
    el.innerHTML =
      '<div class="wrap resume-in">' +
        '<p class="resume-t">前回の続きから：<b>' + esc(v.l) + '</b>' +
          (v.c ? ' <span class="resume-c">' + num(v.c) + '件</span>' : '') + '</p>' +
        '<a class="resume-go" href="list.html">この条件で見る →</a>' +
        '<button type="button" class="resume-x" aria-label="この記憶を消す">×</button>' +
      '</div>';
    mount.appendChild(el);
    el.querySelector('.resume-x').addEventListener('click', function () {
      try { localStorage.removeItem(K_YAKIN); } catch (e) {}
      el.remove();
    });
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }

  // ------------------------------------------------------ 04 最近見た求人
  function recordJobView() {
    var b = document.body;
    if (b.getAttribute('data-page') !== 'job') return;
    var t = b.getAttribute('data-job-title');
    var f = b.getAttribute('data-job-facility');
    var u = b.getAttribute('data-job-url');
    if (!t || !u) return;
    var list = loadJSON(K_HIST);
    if (!Array.isArray(list)) list = [];
    list = [{ t: t, f: f || '', u: u }].concat(
      list.filter(function (x) { return x && x.u !== u; })
    ).slice(0, 6);
    save(K_HIST, JSON.stringify(list));
  }

  function initRecent() {
    var mount = document.getElementById('recentMount');
    if (!mount) return;
    var list = loadJSON(K_HIST);
    if (!Array.isArray(list) || !list.length) return;
    var items = list.slice(0, 4).map(function (x) {
      return '<li><a href="' + esc(x.u) + '">' +
        '<span class="rc-t">' + esc(x.t) + '</span>' +
        (x.f ? '<span class="rc-f">' + esc(x.f) + '</span>' : '') +
        '</a></li>';
    }).join('');
    var el = document.createElement('section');
    el.className = 'band recent-band';
    el.innerHTML =
      '<div class="wrap">' +
        '<div class="recent-head"><h2>最近見た求人</h2>' +
          '<button type="button" class="recent-x">履歴を消す</button></div>' +
        '<ul class="recent-list">' + items + '</ul>' +
      '</div>';
    mount.appendChild(el);
    el.querySelector('.recent-x').addEventListener('click', function () {
      try { localStorage.removeItem(K_HIST); } catch (e) {}
      el.remove();
    });
  }

  // ------------------------------------------------ 05 3つの質問で絞り込む
  function initDiagnosis() {
    var box = document.getElementById('shindan');
    if (!box) return;
    var out = box.querySelector('.dx-n');
    var lbl = box.querySelector('.dx-l');
    var link = box.querySelector('.dx-go');
    if (!out) return;
    var base = +out.getAttribute('data-base') || 0;
    var sel = {};   // group -> {v, n?, r?, label}

    function calc() {
      var n = base;
      if (sel.yakin) n = sel.yakin.n;
      if (sel.shoku) n = Math.round(n * sel.shoku.r);
      if (sel.area) n = Math.round(n * sel.area.r);
      return Math.max(n, 1);
    }
    function paint() {
      var from = parseInt(String(out.textContent).replace(/[^0-9]/g, ''), 10) || 0;
      animateNumber(out, from, calc(), 420);
      var picked = ['yakin', 'shoku', 'area']
        .filter(function (k) { return sel[k]; })
        .map(function (k) { return sel[k].label; });
      if (lbl) {
        lbl.textContent = picked.length
          ? '件　' + picked.join('・') + ' の求人'
          : '件（3つ選ぶと、あなたに合う求人の数になります）';
      }
      if (link) link.hidden = picked.length < 1;
    }

    Array.prototype.forEach.call(box.querySelectorAll('.dx-opts'), function (g) {
      var key = g.getAttribute('data-g');
      g.addEventListener('click', function (ev) {
        var b = ev.target.closest ? ev.target.closest('button') : null;
        if (!b || !g.contains(b)) return;
        var v = b.getAttribute('data-v');
        if (sel[key] && sel[key].v === v) {
          delete sel[key];
        } else {
          sel[key] = {
            v: v,
            n: +b.getAttribute('data-n') || 0,
            r: parseFloat(b.getAttribute('data-r')) || 1,
            label: b.getAttribute('data-label') || b.textContent.trim()
          };
          if (key === 'yakin') {
            rememberYakin(v, sel[key].label, sel[key].n);
          }
        }
        Array.prototype.forEach.call(g.querySelectorAll('button'), function (x) {
          x.setAttribute('aria-pressed', String(!!sel[key] && sel[key].v === x.getAttribute('data-v')));
        });
        paint();
      });
    });

    // 前回覚えた夜勤条件があれば最初から選んでおく
    var prev = loadJSON(K_YAKIN);
    if (prev && prev.k) {
      var b = box.querySelector('.dx-opts[data-g="yakin"] button[data-v="' + prev.k + '"]');
      if (b) b.click();
    }
    paint();
  }

  // ------------------------------------------------------------------ 起動
  function boot() {
    recordJobView();
    initCounters();
    initBars();
    initYakinMemory();
    initResume();
    initRecent();
    initDiagnosis();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
