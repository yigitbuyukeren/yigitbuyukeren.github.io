#!/usr/bin/env bash
# Paylaşım görsellerini (og-home, og-home-en), README başlıklarını ve (isteğe bağlı) GitHub sosyal önizlemesini üretir.
# Gerekenler: macOS + Xcode komut satırı araçları (swiftc), python3 ve Pillow (pip install pillow).
# Kullanım:   tools/og/render-og.sh [snap ikilisi] [sosyal-önizleme site.jpg yolu]
# İlk argüman verilmezse ../yigitbuyukeren/tools/snap.swift derlenir.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SITE="$(cd "$HERE/../.." && pwd)"
SOCIAL="${2:-}"
TMP="$(mktemp -d)"; SRV=""
cleanup() { [ -n "$SRV" ] && kill "$SRV" 2>/dev/null; rm -rf "$SITE/_gh" "$TMP"; }
trap cleanup EXIT

SNAP="${1:-}"
if [ -z "$SNAP" ]; then
  swiftc -O "$SITE/../yigitbuyukeren/tools/snap.swift" -o "$TMP/snap"; SNAP="$TMP/snap"
fi

mkdir -p "$SITE/_gh"
cp "$HERE/og-home.html" "$HERE/banner-site.html" "$SITE/_gh/"
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$SITE" >/dev/null 2>&1 & SRV=$!
sleep 1
B="http://127.0.0.1:8765/_gh"

# Ana sayfa ekran görüntüleri (açık tema SNAP_JS ile zorlanır)
for t in light dark; do
  SNAP_JS="document.documentElement.setAttribute('data-theme','$t')" "$SNAP" "http://127.0.0.1:8765/" "$SITE/_gh/shot-$t.png" 1440 900 1.5 2
done

"$SNAP" "$B/og-home.html" "$TMP/og.png" 1200 630 2
"$SNAP" "$B/og-home.html?lang=en" "$TMP/og-en.png" 1200 630 2
for t in light dark; do
  "$SNAP" "$B/banner-site.html?theme=$t&shot=shot-$t.png" "$TMP/b-$t.png" 1700 691 1.5
done
[ -n "$SOCIAL" ] && "$SNAP" "$B/banner-site.html?theme=dark&shot=shot-dark.png&h=850&zoom=0.75294" "$TMP/social.png" 1280 640 2

${PYTHON:-python3} - "$TMP" "$SITE" "$SOCIAL" <<'PY'
import sys
from PIL import Image
tmp, site, social = sys.argv[1:4]
def save(src, dst, size, **kw):
    Image.open(f"{tmp}/{src}").convert("RGB").resize(size, Image.LANCZOS).save(dst, **kw)
save("og.png", f"{site}/assets/img/og-home.png", (1200, 630), optimize=True)
save("og-en.png", f"{site}/assets/img/og-home-en.png", (1200, 630), optimize=True)
for t in ("light", "dark"):
    save(f"b-{t}.png", f"{site}/.github/banner-{t}.jpg", (1700, 691), quality=90, optimize=True, progressive=True)
if social:
    save("social.png", social, (1280, 640), quality=90, optimize=True, progressive=True)
PY
