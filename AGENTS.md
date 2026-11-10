# Kişisel Site
- Build/framework yok: düz HTML/CSS/JS. Harici font, CDN veya analitik ekleme; gizlilik ve tema davranışını koru.
- Sayfa eklerken TR/EN eşini, `sitemap.xml`, `hreflang`, canonical ve 404 bağlantılarını güncelle.
- Kontrol: `python3 tools/check-site.py`; değişiklikte yerel bağlantı, meta ve mobil görünüm.
- `main` push'u yalnız kaynak repoyu günceller; GitHub Pages aynası kapalıdır. Canlı site VPS'tedir, `DEPLOY_HOST` ile ayrı dağıtım ister.
