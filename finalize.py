"""Remove demo tracking, correct script order, and store Google fonts locally."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
from pathlib import Path
import re
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent / 'public'
FONT_DIR = ROOT / 'fonts'
FONT_DIR.mkdir(exist_ok=True)

def local_font(url):
    ext = Path(urllib.parse.urlsplit(url).path).suffix
    if ext not in ('.woff2', '.woff', '.ttf'):
        ext = '.css'
    name = hashlib.sha1(url.encode()).hexdigest()[:16] + ext
    file = FONT_DIR / name
    if not file.exists():
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=40) as response:
            data = response.read()
        if ext == '.css':
            css = data.decode()
            for child in set(re.findall(r'url\((https://fonts.gstatic.com/[^)]+)\)', css)):
                css = css.replace(child, local_font(child))
            data = css.encode()
        file.write_bytes(data)
    return '/fonts/' + name

files = list(ROOT.rglob('*.html'))
font_urls = set()
for file in files:
    text = file.read_text(encoding='utf-8')
    font_urls.update(html.unescape(u) for u in re.findall(r'''href=["'](https://fonts.googleapis.com/[^"']+)["']''', text))
fonts = {}
def download_font(url):
    try:
        return url, local_font(url)
    except Exception as exc:
        print('Font download failed:', str(exc), flush=True)
        return url, url
with ThreadPoolExecutor(max_workers=4) as pool:
    fonts.update(pool.map(download_font, sorted(font_urls)))
for file in files:
    text = file.read_text(encoding='utf-8')
    # The copy should not report visits to the original demo's analytics.
    text = re.sub(r'<script\b[^>]*>.*?</script>', lambda m: '' if any(x in m.group(0) for x in ('googletagmanager', 'google-analytics', 'wp_recaptchaLoadCallback')) else m.group(0), text, flags=re.S | re.I)
    text = re.sub(r'<noscript>\s*<iframe[^>]*googletagmanager.*?</noscript>', '', text, flags=re.S)
    core = re.search(r'<script\b[^>]*\bid="jquery-core-js"[^>]*></script>', text)
    migrate = re.search(r'<script\b[^>]*\bid="jquery-migrate-js"[^>]*></script>', text)
    if core and migrate and core.start() > migrate.start():
        tag = re.sub(r'\sdefer(?=[\s>])', '', core.group(0))
        text = text.replace(core.group(0), '')
        text = text.replace(migrate.group(0), tag + '\n' + migrate.group(0))
    for remote, local in fonts.items():
        text = text.replace(remote, local).replace(remote.replace('&', '&#038;'), local).replace(remote.replace('&', '&amp;'), local)
    file.write_text(text, encoding='utf-8')
for file in ROOT.rglob('*.css'):
    text = file.read_text(encoding='utf-8', errors='replace')
    # The demo references retired font formats; use its available font files.
    for font in ('FontAwesome5Regular', 'FontAwesome5Solid'):
        text = text.replace(font + '.woff2', font + '.ttf')
    text = re.sub(r'(FontAwesome5(?:Regular|Solid)\.ttf[\"\']?\))\s*format\([\"\']woff2[\"\']\)', r'\1 format("truetype")', text)
    for font in ('WooCommerce', 'star'):
        text = text.replace(font + '.eot', font + '.woff')
    # Old payment-method icons are absent on the live demo too. They are unused
    # by this static checkout, so remove their unavailable background images.
    text = re.sub(r'''url\(["']?[^)"']*/credit-cards/[^)"']+\.png["']?\)''', 'none', text)
    file.write_text(text, encoding='utf-8')
print(f'Finalized {len(files)} HTML files and {len(fonts)} font stylesheets.')
