/* Tema düğmesi, mobil menü, görünür olunca belirme ve etkin bölüm işareti.
   Dış istek yok; saat, imleç önizlemesi ve GitHub çağrısı kaldırıldı. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var EN = root.lang === 'en' || /^\/en(\/|$)/.test(location.pathname);
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Tema: ilk değer <head> içindeki satırda uygulanır; burada yalnızca düğme. */
  var tb = d.getElementById('theme');
  if (tb) tb.addEventListener('click', function () {
    var dark = root.dataset.theme
      ? root.dataset.theme === 'dark'
      : !matchMedia('(prefers-color-scheme: light)').matches;
    var next = dark ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  /* Yapışkan başlık: kaydırınca ince alt çizgi. */
  var head = d.querySelector('.site-head');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', scrollY > 8); };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Mobil menü: tam ekran katman. aria-expanded, Esc, odak tuzağı,
     açıkken arka planın inert olması ve 861px üstünde kendiliğinden kapanma. */
  var btn = d.querySelector('.menu-btn'), menu = d.getElementById('menu');
  if (btn && menu) {
    var inertEls = d.querySelectorAll('main, .site-foot');
    var setOpen = function (open, restore) {
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.hidden = !open;
      d.body.classList.toggle('menu-open', open);
      inertEls.forEach(function (el) {
        if (open) el.setAttribute('inert', '');
        else el.removeAttribute('inert');
      });
      if (open) {
        var first = menu.querySelector('a');
        if (first) first.focus();
      } else if (restore) btn.focus();
    };
    btn.addEventListener('click', function () {
      setOpen(btn.getAttribute('aria-expanded') !== 'true', true);
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false, false);
    });
    d.addEventListener('keydown', function (e) {
      if (menu.hidden) return;
      if (e.key === 'Escape') { e.preventDefault(); setOpen(false, true); return; }
      if (e.key !== 'Tab') return;
      /* Odak yalnızca düğme ile menü bağlantıları arasında döner. */
      var items = [btn].concat([].slice.call(menu.querySelectorAll('a')));
      var i = items.indexOf(d.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
      else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
    });
    matchMedia('(min-width: 861px)').addEventListener('change', function (m) {
      if (m.matches && !menu.hidden) setOpen(false, false);
    });
  }

  /* Görünür olunca belirme. Hareket azaltmada doğrudan görünür. */
  var r = d.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    r.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    r.forEach(function (e) { io.observe(e); });
  }

  /* Üst çubukta ve menüde görünen bölümün bağlantısını işaretle. */
  var links = d.querySelectorAll('.site-nav a[href^="#"], .menu a[href^="#"], .toc a[href^="#"]');
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      (map[id] = map[id] || []).push(a);
    });
    var setCurrent = function (id) {
      links.forEach(function (a) { a.removeAttribute('aria-current'); });
      (map[id] || []).forEach(function (a) { a.setAttribute('aria-current', 'true'); });
    };
    var spy = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        if (e.target.classList.contains('hero')) setCurrent('');
        else if (map[e.target.id]) setCurrent(e.target.id);
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) {
      var s = d.getElementById(id);
      if (s) spy.observe(s);
    });
    var hero = d.querySelector('.hero');
    if (hero) spy.observe(hero);
  }

  /* Brief formu: veriyi hiçbir yere göndermeden mailto taslağı üretir.
     JS yoksa formun action="mailto:" özniteliği devreye girer. */
  var brief = d.getElementById('brief');
  if (brief) brief.addEventListener('submit', function (e) {
    e.preventDefault();
    var val = function (id) { var el = d.getElementById(id); return el ? el.value.trim() : ''; };
    var name = val('b-name'), mail = val('b-mail'), type = val('b-type'), when = val('b-time'), msg = val('b-msg');
    var L = EN
      ? { name: 'Name: ', mail: 'Email: ', type: 'Scope: ', when: 'Timing: ', proj: 'Project:', subj: 'Project: ' }
      : { name: 'Ad: ', mail: 'E-posta: ', type: 'Kapsam: ', when: 'Zamanlama: ', proj: 'Proje:', subj: 'Proje: ' };
    var subject = L.subj + type + (name ? ' — ' + name : '');
    var body = [
      L.name + name,
      L.mail + mail,
      L.type + type,
      L.when + when,
      '',
      L.proj,
      msg
    ].join('\n');
    location.href = 'mailto:mail@yigitbuyukeren.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });

  /* Alt bilgideki yıl. */
  var y = d.getElementById('y');
  if (y) y.textContent = new Date().getFullYear();
})();
