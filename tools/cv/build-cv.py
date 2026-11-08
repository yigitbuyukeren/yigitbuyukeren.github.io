#!/usr/bin/env python3
"""CV içeriğinden dört dosya üretir: /cv/ ve /en/cv/ sayfaları ile bunların PDF'leri.

Kullanım (site kökünden):  python3 tools/cv/build-cv.py
Tek kaynak bu dosyadır; TR ve EN içerik burada yan yana durur ki tutarlı kalsınlar.
PDF için macOS'ta `swift tools/cv/html2pdf.swift` kullanılır (tek sayfa A4, seçilebilir metin).
"""
import html, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = html.escape

CV = {
 "tr": {
  "lang": "tr", "pdf": "Yigit-Eren-Buyukeren-CV-TR.pdf",
  "title": "CV · Yiğit Eren Büyükeren",
  "desc": "Yiğit Eren Büyükeren'in özgeçmişi: Software Developer, Android, mobil ve sunucu sistemleri. RideDeck, Aile Cüzdanı, EXIF Temizleyici.",
  "role": "Software Developer · Android, Mobile & Backend Systems",
  "contact": ["İstanbul, Türkiye", "mail@yigitbuyukeren.com", "yigitbuyukeren.com", "github.com/yigitbuyukeren"],
  "h": {"summary": "Profesyonel özet", "projects": "Projeler", "oss": "Açık kaynak katkısı", "skills": "Teknik yetkinlikler", "edu": "Eğitim ve sertifikalar"},
  "summary": "Android, mobil ve sunucu tarafında uçtan uca uygulama geliştiren yazılımcı. Kotlin ve Jetpack Compose ile açık kaynak bir Android uygulaması (RideDeck), React Native ve PocketBase ile bir mobil uygulama ve sunucusunu (Aile Cüzdanı) geliştirdim. Mantığı platformdan ayırıp test edilebilir tutmaya, kararları belgelemeye ve sahada doğrulanmayanı doğrulanmış diye sunmamaya önem veririm.",
  "projects": [
   {"name": "RideDeck", "meta": "Kotlin, Jetpack Compose, MapLibre · Açık kaynak (Apache 2.0) · github.com/yigitbuyukeren/ridedeck",
    "bullets": [
     "Telefonu motosiklet, araba ve bisiklet için CarPlay tarzı sürüş paneline çeviren Android uygulaması: GPS hız göstergesi, OpenStreetMap ve Valhalla ile sesli navigasyon. Hesap ve kendi sunucusu yok; imzalı v0.5.0 sürümü yayında.",
     "GPS hız verisi için belirsizliğe göre yumuşatma ve aykırı ölçüm doğrulaması, rota eşleme ve yeniden hesaplama mantığını Android’den ayrılmış, birim testli sınıflar olarak yazdım.",
     "JUnit birim testleri; GitHub Actions'ta test, lint ve R8 ile küçültülmüş release derlemesi. Teknik vaka analizi ve bilinen sınırlamalar depoda belgeli.",
    ]},
   {"name": "Aile Cüzdanı", "meta": "React Native, Expo, TypeScript, PocketBase, Python · Geliştirmede, özel kaynak kodu",
    "bullets": [
     "Türk aileleri için ortak bütçe uygulaması: mobil istemci, PocketBase sunucusu (erişim kuralları, rol kontrolü ve hız sınırı sunucuda uygulanır) ve Expo push bildirimleri için Python zamanlayıcısı.",
     "48 eklemeli veritabanı migration’ı kaynak kodda; Caddy ile HTTPS ve yedekleme. Son sunucu değişikliklerinin dağıtımı bekliyor.",
     "4 Kasım 2026 kaydında 764 test; 1 Kasım kaydında 400 HTTP kontrolü. Son sunucu değişikliklerinin HTTP doğrulaması bekliyor; mağaza yayını yok.",
    ]},
   {"name": "EXIF Temizleyici", "meta": "JavaScript, Node.js · Açık kaynak (MIT) · github.com/yigitbuyukeren/exif-temizleyici",
    "bullets": [
     "Fotoğraflardaki GPS, cihaz ve zaman metaverisini JPEG, PNG ve WebP için bayt düzeyinde ayrıştırıp siler; görüntü verisi yeniden sıkıştırılmaz. Bağımlılıksız; sayfa içerik güvenlik politikasıyla ağa kapalı; toplu iş için komut satırı aracı.",
     "38 test ve GitHub Actions.",
    ]},
  ],
  "oss": "Birleştirilen katkılar: cleanyourtv #874 (TV+ yapılandırması), Capso #387 (Türkçe yerelleştirme), macOS uygulaması #113 (Türkçe çeviri), pysad #471 (Python tip ipuçları).",
  "skills": [
   ("Android / mobil", "Kotlin, Jetpack Compose, MapLibre, Gradle, ADB, React Native, Expo, TypeScript"),
   ("Sunucu", "PocketBase, REST API, Python, JavaScript (Node.js)"),
   ("Diğer", "Swift (macOS uygulaması), Shell, HTML, CSS, Vitest, JUnit"),
   ("Araçlar / altyapı", "Git, GitHub Actions, Linux, Caddy, VPS, Tailscale, Cloudflare"),
   ("Ağ", "TCP/IP, alt ağlar, temel yönlendirme"),
  ],
  "edu": [
   ("Açık Öğretim Lisesi", "", "Devam ediyor"),
   ("CCNA: Introduction to Networks (kurs)", "Cisco Networking Academy", "Mart 2026"),
   ("Linux Unhatched", "Cisco Networking Academy", "Şubat 2026"),
   ("Introduction to Cybersecurity", "Cisco Networking Academy", "Şubat 2026"),
   ("Network Fundamentals Training (CCNA ITN)", "Bilişim Academy", "Şubat 2026"),
   ("Ağ Temelleri", "BTK Akademi", "Aralık 2025"),
   ("Bilgisayar Ağları", "BTK Akademi", "Aralık 2025"),
  ],
  "edu_note": "Sertifikalar kurs tamamlama belgeleridir; tam CCNA sertifikası değildir.",
  "web": {"download": "PDF indir", "back": "Ana sayfa", "home": "/", "alt": "/en/cv/", "alt_label": "EN", "alt_lang": "en", "skip": "İçeriğe geç", "pdfpath": "/cv/", "other_pdf": "English PDF"},
 },
 "en": {
  "lang": "en", "pdf": "Yigit-Eren-Buyukeren-CV-EN.pdf",
  "title": "CV · Yiğit Eren Büyükeren",
  "desc": "Résumé of Yiğit Eren Büyükeren: Software Developer, Android, mobile and backend systems. RideDeck, Aile Cüzdanı, EXIF Cleaner.",
  "role": "Software Developer · Android, Mobile & Backend Systems",
  "contact": ["Istanbul, Türkiye", "mail@yigitbuyukeren.com", "yigitbuyukeren.com", "github.com/yigitbuyukeren"],
  "h": {"summary": "Professional summary", "projects": "Projects", "oss": "Open-source contribution", "skills": "Technical skills", "edu": "Education and certificates"},
  "summary": "Software developer building Android, mobile and backend software end to end. I built an open-source Android app with Kotlin and Jetpack Compose (RideDeck) and a mobile app with its server using React Native and PocketBase (Aile Cüzdanı). I keep logic separate from the platform so it can be tested, document decisions, and do not present anything unverified in the field as verified.",
  "projects": [
   {"name": "RideDeck", "meta": "Kotlin, Jetpack Compose, MapLibre · Open source (Apache 2.0) · github.com/yigitbuyukeren/ridedeck",
    "bullets": [
     "Android app that turns a phone into a CarPlay-style riding dashboard for motorcycles, cars and bicycles: GPS speedometer, voice-guided navigation with OpenStreetMap and Valhalla. No account or backend of its own; signed v0.5.0 release published.",
     "Wrote uncertainty-aware GPS speed smoothing with outlier confirmation, route matching and re-routing logic as unit-tested classes separated from Android.",
     "JUnit unit tests; GitHub Actions runs tests, lint and an R8-minified release build. Technical case study and known limitations are documented in the repo.",
    ]},
   {"name": "Aile Cüzdanı", "meta": "React Native, Expo, TypeScript, PocketBase, Python · In development, private source",
    "bullets": [
     "Shared budgeting app for Turkish families: mobile client, PocketBase backend (access rules, role checks and rate limiting enforced on the server) and a Python scheduler for Expo push notifications.",
     "48 append-only migrations in source; single-VPS hosting with Caddy HTTPS and backups. Latest backend deployment is pending.",
     "764 tests recorded on 4 Nov 2026; 400 HTTP checks on 1 Nov. Latest backend HTTP verification is pending; not published in a store.",
    ]},
   {"name": "EXIF Cleaner", "meta": "JavaScript, Node.js · Open source (MIT) · github.com/yigitbuyukeren/exif-temizleyici",
    "bullets": [
     "Parses and strips GPS, device and time metadata from JPEG, PNG and WebP at byte level without re-encoding the image data. Dependency-free; the page is locked off the network by a content security policy; command-line tool for batches.",
     "38 tests and GitHub Actions.",
    ]},
  ],
  "oss": "Merged contributions: cleanyourtv #874 (TV+ configuration), Capso #387 (Turkish localization), macOS app #113 (Turkish translation), pysad #471 (Python type hints).",
  "skills": [
   ("Android / mobile", "Kotlin, Jetpack Compose, MapLibre, Gradle, ADB, React Native, Expo, TypeScript"),
   ("Backend", "PocketBase, REST API, Python, JavaScript (Node.js)"),
   ("Other", "Swift (macOS app), Shell, HTML, CSS, Vitest, JUnit"),
   ("Tools / infrastructure", "Git, GitHub Actions, Linux, Caddy, VPS, Tailscale, Cloudflare"),
   ("Networking", "TCP/IP, subnetting, basic routing"),
  ],
  "edu": [
   ("Open Education High School (Açık Öğretim Lisesi)", "", "In progress"),
   ("CCNA: Introduction to Networks (course)", "Cisco Networking Academy", "March 2026"),
   ("Linux Unhatched", "Cisco Networking Academy", "February 2026"),
   ("Introduction to Cybersecurity", "Cisco Networking Academy", "February 2026"),
   ("Network Fundamentals Training (CCNA ITN)", "Bilişim Academy", "February 2026"),
   ("Network Basics (Ağ Temelleri)", "BTK Akademi", "December 2025"),
   ("Computer Networks (Bilgisayar Ağları)", "BTK Akademi", "December 2025"),
  ],
  "edu_note": "Certificates are course-completion records; not the full CCNA certification.",
  "web": {"download": "Download PDF", "back": "Home", "home": "/en/", "alt": "/cv/", "alt_label": "TR", "alt_lang": "tr", "skip": "Skip to content", "pdfpath": "/en/cv/", "other_pdf": "Türkçe PDF"},
 },
}

PRINT_CSS = """
@page{size:595pt 842pt;margin:0}
*{box-sizing:border-box}
html{zoom:.75}
html,body{margin:0;padding:0;background:#fff}
body{width:595pt;height:842pt;padding:30pt 36pt 24pt;font:9.3pt/1.38 Arial,"Helvetica Neue",Helvetica,sans-serif;color:#111;overflow:hidden}
h1{font-size:21pt;line-height:1.1;margin:0 0 2pt;font-weight:700;letter-spacing:-.3pt}
.role{font-size:10pt;margin:0 0 4pt;color:#333;font-weight:600}
.contact{margin:0 0 8pt;font-size:9pt;color:#222}
.contact span+span::before{content:" · "}
h2{font-size:9.6pt;letter-spacing:.6pt;margin:7pt 0 2.5pt;padding-bottom:1.5pt;border-bottom:.7pt solid #111;font-weight:700}
p{margin:0 0 2pt}
.proj{margin:0 0 4pt}
.proj h3{font-size:10pt;margin:0;font-weight:700}
.proj .meta{font-size:8.4pt;color:#444;margin:0 0 1.5pt}
ul{margin:0;padding-left:11pt}
li{margin:0 0 1.2pt}
.sk{display:grid;grid-template-columns:78pt 1fr;gap:1pt 6pt}
.sk b{font-weight:600}
.ed{display:grid;grid-template-columns:1fr auto;gap:0 8pt}
.ed div:nth-child(even){text-align:right;color:#333}
.note{font-size:7.6pt;color:#444;margin-top:2pt}
a{color:inherit;text-decoration:none}
"""

import re
LINKS = [("cleanyourtv #874", "https://github.com/Gathin23/cleanyourtv/pull/874"), ("Capso #387", "https://github.com/lzhgus/Capso/pull/387"), ("macOS uygulaması #113", "https://github.com/omlahore/RemoveMacAI/pull/113"), ("macOS app #113", "https://github.com/omlahore/RemoveMacAI/pull/113"), ("pysad #471", "https://github.com/selimfirat/pysad/pull/471"), ("mail@yigitbuyukeren.com", "mailto:mail@yigitbuyukeren.com"), ("github.com/yigitbuyukeren/ridedeck", "https://github.com/yigitbuyukeren/ridedeck"),
         ("github.com/yigitbuyukeren/exif-temizleyici", "https://github.com/yigitbuyukeren/exif-temizleyici"), ("github.com/yigitbuyukeren", "https://github.com/yigitbuyukeren"),
         ("github.com/Gathin23/cleanyourtv", "https://github.com/Gathin23/cleanyourtv/pull/874"), ("yigitbuyukeren.com", "https://yigitbuyukeren.com/")]
def linkify(t):
    t = E(t)
    pat = "|".join(re.escape(k) for k, _ in sorted(LINKS, key=lambda x: -len(x[0])))
    d = dict(LINKS)
    return re.sub(pat, lambda m: f'<a href="{d[m.group(0)]}">{m.group(0)}</a>', t)

def tr_upper(t):
    return t.replace("i", "İ").replace("ı", "I").upper()

def H(c, k):
    t = c['h'][k]
    return tr_upper(t) if c['lang'] == 'tr' else t.upper()

def print_html(c):
    projs = "".join(
        f'<div class="proj"><h3>{E(p["name"])}</h3><p class="meta">{linkify(p["meta"])}</p><ul>' +
        "".join(f"<li>{E(b)}</li>" for b in p["bullets"]) + "</ul></div>" for p in c["projects"])
    sk = "".join(f"<b>{E(k)}</b><span>{E(v)}</span>" for k, v in c["skills"])
    ed = "".join(f"<div>{E(a)}{', ' + E(b) if b else ''}</div><div>{E(d)}</div>" for a, b, d in c["edu"])
    contact = "".join(f"<span>{linkify(x)}</span>" for x in c["contact"])
    return f"""<!doctype html><html lang="{c['lang']}"><head><meta charset="utf-8"><title>{E(c['title'])}</title><style>{PRINT_CSS}</style></head><body>
<h1>Yiğit Eren Büyükeren</h1><p class="role">{E(c['role'])}</p><p class="contact">{contact}</p>
<h2>{E(H(c,'summary'))}</h2><p>{E(c['summary'])}</p>
<h2>{E(H(c,'projects'))}</h2>{projs}
<h2>{E(H(c,'oss'))}</h2><p>{linkify(c['oss'])}</p>
<h2>{E(H(c,'skills'))}</h2><div class="sk">{sk}</div>
<h2>{E(H(c,'edu'))}</h2><div class="ed">{ed}</div><p class="note">{E(c['edu_note'])}</p>
</body></html>"""

WEB_CSS = """
.cv{max-width:calc(880px + 2*var(--gutter));padding-block:clamp(28px,5vw,72px) 112px}
.cv h1{font-size:clamp(48px,7vw + 8px,96px);letter-spacing:-.055em;line-height:.94;margin-bottom:16px}
.cv .role{font:500 13px/1.5 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 24px}
.cv ul.contact{display:flex;flex-wrap:wrap;gap:0 24px;list-style:none;margin:0 0 24px;padding:0;color:var(--ink-2)}
.cv ul.contact li{display:flex;align-items:center;min-height:44px}
.cv h2{font:500 12.5px/1.4 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:64px 0 24px;padding-top:16px;border-top:1px solid var(--rule-strong)}
.cv .proj{margin:0 0 36px}
.cv .proj h3{font-size:var(--fs-h4);letter-spacing:-.035em;margin-bottom:6px}
.cv .proj .meta{font:500 13px/1.5 var(--f-mono);color:var(--muted);margin:0 0 12px}
.cv ul.b{margin:0;padding-left:20px;color:var(--ink-2)}
.cv ul.b li{margin:0 0 8px}
.cv ul.b li::marker{color:var(--accent)}
.cv h2 + p{color:var(--ink-2)}
.cv dl{display:grid;grid-template-columns:200px 1fr;gap:12px 24px;margin:0}
.cv dt{font-weight:600}
.cv dd{margin:0;color:var(--ink-2)}
.cv table{width:100%;border-collapse:collapse}
.cv td{padding:14px 0;border-top:1px solid var(--rule);vertical-align:top}
.cv td:last-child{text-align:right;white-space:nowrap;font-family:var(--f-mono);font-size:13px;color:var(--muted)}
.cv .note{color:var(--muted);font-size:var(--fs-sm);margin-top:12px}
@media (max-width:640px){.cv dl{grid-template-columns:1fr;gap:2px}.cv dd{margin-bottom:12px}.cv td:last-child{white-space:normal}}
"""

def web_html(c, base):
    w = c["web"]
    other = "/en/cv/" if c["lang"] == "tr" else "/cv/"
    canon = f"https://yigitbuyukeren.com{w['pdfpath']}"
    tr_url, en_url = "https://yigitbuyukeren.com/cv/", "https://yigitbuyukeren.com/en/cv/"
    pdf = f"{w['pdfpath']}{c['pdf']}"
    projs = "".join(
        f'<div class="proj"><h3>{E(p["name"])}</h3><p class="meta">{E(p["meta"])}</p><ul class="b">' +
        "".join(f"<li>{E(b)}</li>" for b in p["bullets"]) + "</ul></div>" for p in c["projects"])
    sk = "".join(f"<dt>{E(k)}</dt><dd>{E(v)}</dd>" for k, v in c["skills"])
    ed = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(d)}</td></tr>" for a, b, d in c["edu"])
    contact = ('<li>' + E(c["contact"][0]) + '</li><li><a class="link" href="mailto:mail@yigitbuyukeren.com">mail@yigitbuyukeren.com</a></li>'
               '<li><a class="link" href="/">yigitbuyukeren.com</a></li><li><a class="link" href="https://github.com/yigitbuyukeren" rel="me">github.com/yigitbuyukeren</a></li>')
    en = c["lang"] == "en"
    home_label = "Yiğit Eren Büyükeren, " + ("home" if en else "ana sayfa")
    theme_label = "Light or dark theme" if en else "Açık ya da koyu tema"
    head = base["head"].replace("{{LANG}}", c["lang"]).replace("{{TITLE}}", E(c["title"])).replace("{{DESC}}", E(c["desc"])) \
        .replace("{{CANON}}", canon).replace("{{TR}}", tr_url).replace("{{EN}}", en_url).replace("{{LOCALE}}", "en_US" if en else "tr_TR") \
        .replace("{{CSS}}", WEB_CSS)
    header = base["header"].replace("{{HOME}}", w["home"]).replace("{{HOMELABEL}}", home_label).replace("{{THEME}}", theme_label) \
        .replace("{{ALT}}", w["alt"]).replace("{{ALTLANG}}", w["alt_lang"]).replace("{{ALTLABEL}}", w["alt_label"]).replace("{{ALTNAME}}", "English" if c["lang"] == "tr" else "Türkçe")
    return f"""{head}
<body>
<a class="skip" href="#main">{w['skip']}</a>
{header}
<main id="main"><article class="cv wrap">
<p class="crumbs"><a href="{w['home']}">{w['back']}</a><span aria-hidden="true">/</span><span>CV</span></p>
<h1>Yiğit Eren Büyükeren</h1><p class="role"{'' if en else ' lang="en"'}>{E(c['role'])}</p>
<ul class="contact">{contact}</ul>
<div class="actions"><a class="btn primary" href="{pdf}" download>{w['download']} <span class="arr" aria-hidden="true">↓</span></a><a class="btn" href="{other_pdf_href(c)}" download>{w['other_pdf']} <span class="arr" aria-hidden="true">↓</span></a></div>
<h2>{E(tr_upper(c['h']['summary']) if c['lang']=='tr' else c['h']['summary'].upper())}</h2><p>{E(c['summary'])}</p>
<h2>{E(c['h']['projects'])}</h2>{projs}
<h2>{E(c['h']['oss'])}</h2><p>{E(c['oss'])}</p>
<h2>{E(c['h']['skills'])}</h2><dl>{sk}</dl>
<h2>{E(c['h']['edu'])}</h2><table><thead><tr><th scope="col" class="vh">{"Education or certificate" if en else "Eğitim veya sertifika"}</th><th scope="col" class="vh">{"Issuer" if en else "Veren"}</th><th scope="col" class="vh">{"Date" if en else "Tarih"}</th></tr></thead>{ed}</table><p class="note">{E(c['edu_note'])}</p>
</article></main>
<footer class="site-foot"><div class="wrap"><span>© <span id="y">2026</span> Yiğit Eren Büyükeren</span><nav aria-label="{'Footer links' if en else 'Alt bağlantılar'}"><a href="{w['home']}">{w['back']}</a><a href="https://github.com/yigitbuyukeren">GitHub</a></nav></div></footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""

def other_pdf_href(c):
    return ("/en/cv/" + CV["en"]["pdf"]) if c["lang"] == "tr" else ("/cv/" + CV["tr"]["pdf"])

def main():
    # Site sayfalarının ortak üst ve alt kısmı ana sayfadan alınır (aynı simge ve tema düğmesi).
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    moon = src[src.index('<button class="icon-btn" id="theme"'):src.index('</button>', src.index('<button class="icon-btn" id="theme"')) + 9]
    header = ('<header class="site-head"><div class="wrap">'
              '<a class="mark" href="{{HOME}}"><span class="mark-badge" aria-hidden="true">yb<i>.</i></span><span>Yiğit <span class="mark-name-long">Eren </span>Büyükeren</span></a>'
              '<div class="head-tools" style="margin-left:auto">' + moon.replace('aria-label="Açık ya da koyu tema"', 'aria-label="{{THEME}}"') +
              '<a class="icon-btn" href="{{ALT}}" hreflang="{{ALTLANG}}" lang="{{ALTLANG}}" aria-label="{{ALTLABEL}}, {{ALTNAME}}">{{ALTLABEL}}</a></div></div></header>')
    head = ('<!doctype html>\n<html lang="{{LANG}}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>{{TITLE}}</title>\n<meta name="description" content="{{DESC}}">\n<meta name="author" content="Yiğit Eren Büyükeren">\n'
            '<link rel="canonical" href="{{CANON}}">\n<link rel="alternate" hreflang="tr" href="{{TR}}">\n<link rel="alternate" hreflang="en" href="{{EN}}">\n<link rel="alternate" hreflang="x-default" href="{{TR}}">\n'
            '<meta property="og:type" content="profile">\n<meta property="og:site_name" content="Yiğit Eren Büyükeren">\n<meta property="og:title" content="{{TITLE}}">\n<meta property="og:description" content="{{DESC}}">\n'
            '<meta property="og:url" content="{{CANON}}">\n<meta property="og:image" content="https://yigitbuyukeren.com/assets/img/og-home.png">\n<meta property="og:locale" content="{{LOCALE}}">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="theme-color" content="#F3F0E8" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#121110" media="(prefers-color-scheme: dark)">\n'
            '<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">\n<link rel="icon" href="/assets/img/favicon-yb.png" type="image/png">\n<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">\n'
            '<link rel="preload" href="/assets/fonts/bricolage-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
            "<script>try{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}catch(e){}document.documentElement.classList.add('js')</script>\n"
            '<link rel="stylesheet" href="/assets/site.css?v=20261109">\n<style>{{CSS}}</style>\n</head>')
    base = {"head": head, "header": header}
    do_pdf = "--no-pdf" not in sys.argv
    for key, c in CV.items():
        outdir = os.path.join(ROOT, "cv" if key == "tr" else "en/cv")
        os.makedirs(outdir, exist_ok=True)
        open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(web_html(c, base))
        if do_pdf:
            with tempfile.TemporaryDirectory() as d:
                p = os.path.join(d, "cv.html")
                open(p, "w", encoding="utf-8").write(print_html(c))
                r = subprocess.run(["swift", os.path.join(ROOT, "tools/cv/html2pdf.swift"), p, os.path.join(outdir, c["pdf"])], capture_output=True, text=True)
                print(r.stdout.strip(), r.stderr.strip())
                if r.returncode: sys.exit(r.returncode)

if __name__ == "__main__":
    main()
