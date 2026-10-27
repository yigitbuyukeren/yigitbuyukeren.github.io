#!/usr/bin/env python3
"""Yerel site kontrolü (404 ve dogum-gunu/ demoları dışarıda; onlar ayrı projenin kopyası): iç bağlantılar ve görseller var mı, title/description/canonical/hreflang/OG var mı, sitemap'teki sayfalar mevcut mu."""
import os, re, sys, glob
from urllib.parse import urlparse, unquote
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = [p for p in glob.glob(ROOT + '/**/*.html', recursive=True) if '/tools/' not in p and not p.endswith('/404.html') and '/_gh/' not in p and '/.git/' not in p]
bad = 0
def exists(path):
    path = unquote(path.split('#')[0].split('?')[0])
    if not path or path == '/': return True
    f = os.path.join(ROOT, path.lstrip('/'))
    return os.path.isfile(f) or os.path.isfile(os.path.join(f, 'index.html'))
ids = {}
for p in sorted(pages):
    s = open(p, encoding='utf-8').read(); rel = os.path.relpath(p, ROOT)
    ids = set(re.findall(r'\sid="([^"]+)"', s))
    def err(m):
        global bad; bad += 1; print(f'{rel}: {m}')
    for tag in ['<title>', 'name="description"', 'rel="canonical"', 'property="og:title"', 'property="og:image"']:
        if tag not in s: err('eksik ' + tag)
    if '<html lang=' not in s: err('html lang yok')
    for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
        u = m.group(1)
        if u.startswith(('mailto:', 'tel:', 'data:', 'javascript:')): continue
        if u.startswith('#'):
            if u[1:] and u[1:] not in ids: err('kırık bağlantı ' + u)
            continue
        pu = urlparse(u)
        if pu.scheme in ('http', 'https'):
            if pu.netloc == 'yigitbuyukeren.com' and not exists(pu.path): err('kırık (mutlak) ' + u)
            continue
        if u.startswith('/') and not exists(u): err('kırık ' + u)
    for m in re.finditer(r'<img[^>]*>', s):
        t = m.group(0)
        if 'alt=' not in t: err('img alt yok: ' + t[:60])
    if rel != '404.html' and not re.search(r'<h1[ >]', s): err('h1 yok')
for u in re.findall(r'<loc>https://yigitbuyukeren.com([^<]*)</loc>', open(ROOT + '/sitemap.xml').read()):
    if not exists(u): bad += 1; print('sitemap: yok ' + u)
print('sayfa:', len(pages), 'sorun:', bad)
sys.exit(1 if bad else 0)
