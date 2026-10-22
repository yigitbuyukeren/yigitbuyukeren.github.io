/* Tema düğmesi, üst bar çizgisi, görünür olunca belirme, İstanbul saati ve GitHub'dan canlı bilgiler. */
(function () {
  var d = document, root = d.documentElement, EN = root.lang === 'en';

  /* Tema: ilk değer <head> içindeki satırda uygulanır, burada yalnızca düğme. */
  var tb = d.getElementById('theme');
  if (tb) tb.addEventListener('click', function () {
    var dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    var next = dark ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  var head = d.querySelector('.site-head');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', scrollY > 8); };
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }

  var r = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    r.forEach(function (e) { io.observe(e); });
  } else r.forEach(function (e) { e.classList.add('in'); });

  /* İstanbul saati */
  var clock = d.getElementById('clock');
  if (clock) {
    var fmt = new Intl.DateTimeFormat(EN ? 'en-GB' : 'tr-TR', { timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit' });
    var tick = function () { clock.textContent = (EN ? 'Istanbul ' : 'İstanbul ') + fmt.format(new Date()); };
    tick(); setInterval(tick, 20000);
  }

  var y = d.getElementById('y');
  if (y) y.textContent = new Date().getFullYear();

  /* GitHub: son gönderilen depo ve cleanyourtv PR durumu. Hata olursa sayfadaki sabit metin kalır. */
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

  var pr = d.getElementById('gh-pr');
  if (pr) get('https://api.github.com/repos/Gathin23/cleanyourtv/pulls/874').then(function (p) {
    var t = p.merged_at ? (EN ? 'merged' : 'birleştirildi') : p.state === 'open' ? (EN ? 'in review' : 'incelemede') : (EN ? 'closed' : 'kapandı');
    pr.textContent = t;
    d.querySelectorAll('[data-pr-state]').forEach(function (n) { n.textContent = t; });
  }).catch(function () {});
})();
