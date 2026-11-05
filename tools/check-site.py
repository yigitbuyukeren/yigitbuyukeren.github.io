#!/usr/bin/env python3
"""Yerel sayfaların metalarını, görsellerini, iç bağlantılarını ve site haritasını denetler."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HOST = 'yigitbuyukeren.com'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.urls = []
        self.errors = []
        self.figure_depth = 0
        self.source = path.read_text(encoding='utf-8')
        self.feed(self.source)
        if self.figure_depth:
            self.errors.append('kapanmamış figure etiketi')
        for key, count in Counter(self.ids).items():
            if count > 1:
                self.errors.append('tekrarlanan id: ' + key)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.urls.append(attrs[key])
        if tag in ('img', 'source') and attrs.get('srcset'):
            self.urls.extend(item.strip().split()[0] for item in attrs['srcset'].split(',') if item.strip())
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('img alt yok: ' + attrs.get('src', ''))
        if tag == 'figure':
            if self.figure_depth:
                self.errors.append('iç içe figure etiketleri')
            self.figure_depth += 1

    def handle_endtag(self, tag):
        if tag == 'figure':
            if not self.figure_depth:
                self.errors.append('açılmamış figure kapatılıyor')
            else:
                self.figure_depth -= 1


def target_path(source, url):
    path = unquote(url.path)
    if not path:
        return source
    target = ROOT / path.lstrip('/') if path.startswith('/') or url.netloc else source.parent / path
    return target / 'index.html' if target.is_dir() else target


def main():
    pages = {p: Page(p) for p in sorted(ROOT.rglob('*.html'))
             if not any(part in ('tools', '_gh', '.git') for part in p.relative_to(ROOT).parts)
             and p.name != '404.html'}
    errors = []
    for path, page in pages.items():
        issues = list(page.errors)
        for tag in ('<title>', 'name="description"', 'rel="canonical"', 'property="og:title"', 'property="og:image"', '<html lang='):
            if tag not in page.source:
                issues.append('eksik ' + tag)
        if '<h1>' not in page.source and '<h1 ' not in page.source:
            issues.append('h1 yok')
        for raw in page.urls:
            url = urlparse(raw)
            if url.scheme and not (url.scheme in ('http', 'https') and url.netloc == HOST):
                continue
            if url.netloc and url.netloc != HOST:
                continue
            target = target_path(path, url)
            if not target.is_file():
                issues.append('kırık bağlantı veya görsel: ' + raw)
            elif url.fragment and target.suffix == '.html':
                dest = pages.get(target)
                if dest is None:
                    dest = Page(target)
                if unquote(url.fragment) not in dest.ids:
                    issues.append('hedef sayfada bölüm yok: ' + raw)
        errors.extend(f'{path.relative_to(ROOT)}: {issue}' for issue in issues)
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    for loc in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        target = target_path(ROOT / 'index.html', urlparse(loc.text))
        if not target.is_file():
            errors.append('sitemap: yok ' + loc.text)
    for error in errors:
        print(error)
    print('sayfa:', len(pages), 'sorun:', len(errors))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
