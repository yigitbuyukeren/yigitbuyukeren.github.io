/* "Kil" ana sayfa: hero arkasında yavaşça akan sıcak leke animasyonu.
   Bağımlılık yok; sekme gizlenince ve hero görünmezken durur,
   hareket azaltma tercihinde tek kare çizer. */
(function () {
  'use strict';
  var c = document.getElementById('clay');
  if (!c || !c.getContext) return;
  var ctx = c.getContext('2d');
  var reduce = matchMedia('(prefers-reduced-motion: reduce)');
  var w = 0, h = 0, dpr = 1, t = Math.random() * 40;
  var raf = 0, last = 0, visible = true;

  var blobs = [
    { x: .60, y: .26, r: .52, dx: .035, dy: .030, p: 0.0 },
    { x: .93, y: .54, r: .46, dx: .028, dy: -.038, p: 1.4 },
    { x: .74, y: .88, r: .50, dx: -.030, dy: .028, p: 2.6 },
    { x: .28, y: 1.02, r: .38, dx: .022, dy: -.020, p: 3.4 }
  ];
  var alpha = [.30, .22, .10];

  function dark() {
    var th = document.documentElement.dataset.theme;
    if (th === 'dark') return true;
    if (th === 'light') return false;
    return matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function palette() {
    return dark()
      ? ['226,131,95', '176,64,42', '240,161,132']
      : ['176,64,42', '201,138,75', '94,82,69'];
  }

  function resize() {
    var r = c.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    w = Math.max(1, Math.round(r.width));
    h = Math.max(1, Math.round(r.height));
    c.width = Math.round(w * dpr);
    c.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function draw() {
    if (!w || !h) return;
    var p = palette(), d = dark();
    ctx.clearRect(0, 0, w, h);
    ctx.globalCompositeOperation = d ? 'screen' : 'multiply';
    for (var i = 0; i < blobs.length; i++) {
      var b = blobs[i], ph = t + b.p;
      var x = (b.x + Math.sin(ph * .6) * b.dx) * w;
      var y = (b.y + Math.cos(ph * .45) * b.dy) * h;
      var rad = b.r * Math.max(w, h) * (0.92 + Math.sin(ph * .3) * .08);
      var col = p[i % p.length], a = alpha[i];
      var g = ctx.createRadialGradient(x, y, 0, x, y, rad);
      g.addColorStop(0, 'rgba(' + col + ',' + a + ')');
      g.addColorStop(.55, 'rgba(' + col + ',' + (a * .42) + ')');
      g.addColorStop(1, 'rgba(' + col + ',0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(x, y, rad, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';
  }

  function loop(ts) {
    raf = requestAnimationFrame(loop);
    if (!visible || ts - last < 33) return;
    last = ts;
    t += 0.018;
    draw();
  }
  function start() { if (!raf && !reduce.matches) raf = requestAnimationFrame(loop); }
  function stop() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }

  resize();
  draw();

  if (reduce.matches) {
    addEventListener('resize', function () { resize(); draw(); }, { passive: true });
    var tb = document.getElementById('theme');
    if (tb) tb.addEventListener('click', function () { setTimeout(draw, 30); });
    return;
  }

  addEventListener('resize', function () { resize(); draw(); }, { passive: true });
  if ('ResizeObserver' in window) {
    new ResizeObserver(function () { resize(); draw(); }).observe(c);
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible) start(); else stop();
    }).observe(c);
  }
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop(); else if (visible) start();
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', draw);
  var themeBtn = document.getElementById('theme');
  if (themeBtn) themeBtn.addEventListener('click', function () { setTimeout(draw, 30); });
  start();
})();
