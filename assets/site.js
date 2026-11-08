/* Tema düğmesi, mobil menü, etkin bölüm işareti, görünür olunca belirme, proje önizlemesi, İstanbul saati ve GitHub'dan canlı bilgiler. */
(function () {
  var d = document, root = d.documentElement, EN = root.lang === 'en';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Tema: varsayılan koyu. İlk değer <head> içindeki satırda uygulanır, burada yalnızca düğme. */
  var tb = d.getElementById('theme');
  if (tb) tb.addEventListener('click', function () {
    var dark = root.dataset.theme ? root.dataset.theme === 'dark' : !matchMedia('(prefers-color-scheme: light)').matches;
    var next = dark ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  var head = d.querySelector('.site-head');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', scrollY > 8); };
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }

  /* Mobil menü: tam ekran katman. aria-expanded, Esc ile kapanır, odak katmana gider ve düğmeye döner. */
  var btn = d.querySelector('.menu-btn'), menu = d.getElementById('menu');
  if (btn && menu) {
    var inertEls = d.querySelectorAll('main, .site-foot');
    var setOpen = function (open, restore) {
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.hidden = !open;
      root.classList.toggle('menu-open', open);
      inertEls.forEach(function (el) { if (open) el.setAttribute('inert', ''); else el.removeAttribute('inert'); });
      if (open) { var first = menu.querySelector('a'); if (first) first.focus(); }
      else if (restore) btn.focus();
    };
    btn.addEventListener('click', function () { setOpen(btn.getAttribute('aria-expanded') !== 'true', true); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false, false); });
    d.addEventListener('keydown', function (e) {
      if (menu.hidden) return;
      if (e.key === 'Escape') { e.preventDefault(); setOpen(false, true); return; }
      if (e.key !== 'Tab') return;
      /* Odak yalnızca düğme ile menü bağlantıları arasında döner */
      var items = [btn].concat([].slice.call(menu.querySelectorAll('a')));
      var i = items.indexOf(d.activeElement);
      if (e.shiftKey && (i <= 0)) { e.preventDefault(); items[items.length - 1].focus(); }
      else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
    });
    matchMedia('(min-width: 861px)').addEventListener('change', function (m) { if (m.matches && !menu.hidden) setOpen(false, false); });
  }

  var r = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    r.forEach(function (e) { io.observe(e); });
  } else r.forEach(function (e) { e.classList.add('in'); });

  /* Üst çubukta ve menüde görünen bölümün bağlantısını işaretle */
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
    Object.keys(map).forEach(function (id) { var s = d.getElementById(id); if (s) spy.observe(s); });
    var hero = d.querySelector('.hero'); if (hero) spy.observe(hero);
  }

  /* İndeks listesi: fare ile satırın üzerine gelince küçük resim imleci izler (yalnızca ince imleç) */
  var rows = d.querySelectorAll('.index-list .work');
  if (rows.length && matchMedia('(min-width: 900px) and (hover: hover) and (pointer: fine)').matches) {
    var peek = d.createElement('div'), inner = d.createElement('div'), pimg = d.createElement('img');
    peek.className = 'peek'; peek.setAttribute('aria-hidden', 'true'); inner.className = 'peek-in'; pimg.alt = ''; pimg.decoding = 'async';
    inner.appendChild(pimg); peek.appendChild(inner); d.body.appendChild(peek);
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = 0, shown = false;
    var place = function () {
      var w = peek.offsetWidth, h = peek.offsetHeight;
      var x = Math.min(tx + 28, innerWidth - w - 16), y = Math.min(ty + 20, innerHeight - h - 16);
      if (reduce) { cx = x; cy = y; } else { cx += (x - cx) * 0.2; cy += (y - cy) * 0.2; }
      peek.style.transform = 'translate3d(' + Math.round(cx) + 'px,' + Math.round(cy) + 'px,0)';
      raf = (!reduce && (Math.abs(x - cx) > 0.5 || Math.abs(y - cy) > 0.5)) ? requestAnimationFrame(place) : 0;
    };
    var move = function (e) { tx = e.clientX; ty = e.clientY; if (!shown) { cx = tx + 28; cy = ty + 20; shown = true; } if (!raf) raf = requestAnimationFrame(place); };
    rows.forEach(function (row) {
      var img = row.querySelector('.work-thumb img');
      if (!img) return;
      row.addEventListener('pointerenter', function (e) {
        pimg.src = img.currentSrc || img.src; tx = e.clientX; ty = e.clientY; cx = tx + 28; cy = ty + 20; place();
        peek.classList.add('on');
      });
      row.addEventListener('pointermove', move);
      row.addEventListener('pointerleave', function () { peek.classList.remove('on'); shown = false; });
    });
    addEventListener('scroll', function () { peek.classList.remove('on'); shown = false; }, { passive: true });
  }

  /* İstanbul saati */
  var clock = d.getElementById('clock');
  if (clock) {
    var fmt = new Intl.DateTimeFormat(EN ? 'en-GB' : 'tr-TR', { timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit' });
    var tick = function () { clock.textContent = (EN ? 'Istanbul ' : 'İstanbul ') + fmt.format(new Date()); };
    tick(); setInterval(tick, 20000);
  }

  var y = d.getElementById('y');
  if (y) y.textContent = new Date().getFullYear();

  /* GitHub: son gönderilen depo. Hata olursa sayfadaki sabit metin kalır. */
  var ago = function (iso) {
    var days = Math.floor((Date.now() - new Date(iso)) / 864e5);
    if (EN) return days < 1 ? 'today' : days === 1 ? 'yesterday' : days < 30 ? days + ' days ago' : new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
    return days < 1 ? 'bugün' : days === 1 ? 'dün' : days < 30 ? days + ' gün önce' : new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
  };
  var get = function (url) { return fetch(url, { headers: { Accept: 'application/vnd.github+json' } }).then(function (res) { return res.ok ? res.json() : Promise.reject(res.status); }); };

  var last = d.getElementById('gh-last');
  if (last) get('https://api.github.com/users/yigitbuyukeren/repos?per_page=20&sort=pushed').then(function (list) {
    var skip = { 'yigitbuyukeren': 1, 'yigitbuyukeren.github.io': 1 };
    var repo = list.filter(function (x) { return !x.fork && !skip[x.name]; })[0];
    if (!repo) return;
    var a = d.createElement('a'); a.href = repo.html_url; a.textContent = repo.name;
    var s = d.createElement('small'); s.textContent = ago(repo.pushed_at);
    last.replaceChildren(a, s);
  }).catch(function () {});
})();
