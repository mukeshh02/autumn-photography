"""Download the public Autumn demo as a static, locally navigable website."""
import concurrent.futures as futures
import html
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.parse as parse
import urllib.request as request

ORIGIN = 'https://avala.bold-themes.com'
START = ORIGIN + '/autumn/home/home-02/'
ROOT = Path(__file__).resolve().parent / 'public'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36'}
if os.getenv('REFERENCE_COOKIE'):
    HEADERS['Cookie'] = os.environ['REFERENCE_COOKIE']
seen = set()
failures = []
pages = []

def normalize(value, base):
    value = html.unescape(value).replace('\\/', '/').strip('\"\'')
    u = parse.urlsplit(parse.urljoin(base, value))
    if u.netloc != 'avala.bold-themes.com':
        return None
    if any(x in u.path for x in ['/wp-json', '/feed/', '/wp-admin', '/xmlrpc', '/wp-login', '/.well-known']):
        return None
    if not u.path.startswith(('/autumn/', '/wp-content/', '/wp-includes/')):
        return None
    if u.query and any(x in u.query for x in ['add-to-cart', 'replytocom', 'wc-ajax', 'rest_route']):
        return None
    query = parse.parse_qsl(u.query)
    allowed = {'blog_list_view', 'pf_list_view', 'bt_sidebar', 'orderby', 'paged', 'product-page'}
    query = sorted((k, v) for k, v in query if k in allowed)
    return ORIGIN + u.path + ('?' + parse.urlencode(query) if query else '')

def destination(url):
    p = parse.unquote(parse.urlsplit(url).path).lstrip('/')
    if parse.urlsplit(url).query:
        key = hashlib.sha1(parse.urlsplit(url).query.encode()).hexdigest()[:12]
        p = p.rstrip('/') + '/__views/' + key + '.html'
    if not Path(p).suffix:
        p = p.rstrip('/') + '/index.html'
    target = (ROOT / p).resolve()
    if not target.is_relative_to(ROOT.resolve()):
        raise ValueError('Unsafe asset path')
    return target

def fetch(url):
    try:
        target = destination(url)
        cached = target.exists()
        if cached:
            data = target.read_bytes()
            kind = {'.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript'}.get(target.suffix, '')
        else:
            with request.urlopen(request.Request(url, headers=HEADERS), timeout=45) as response:
                data = response.read()
                kind = response.headers.get('Content-Type', '')
                if response.status != 200 or b'sgcaptcha' in data[:1000]:
                    raise ValueError('Reference server challenge: ' + str(response.status))
        children = set()
        if 'text/html' in kind or 'text/css' in kind or 'javascript' in kind:
            text = data.decode('utf-8', errors='replace')
            if 'text/html' in kind:
                pages.append(url)
                candidates = re.findall(r'''(?:href|src|data-src|data-background|data-image)\s*=\s*["']([^"']+)["']''', text, re.I)
                candidates += re.findall(r'''https?:(?:\\/|/){2}avala\.bold-themes\.com[^\s"'<>\\)]+''', text)
                for srcset in re.findall(r'''srcset\s*=\s*["']([^"']+)["']''', text):
                    candidates += [v.strip().split(' ')[0] for v in srcset.split(',')]
                # Avoid sending demo forms or analytics to the original website.
                text = re.sub(r'<script[^>]+src=["\'][^"\']*(?:googletagmanager|google-analytics)[^>]*>.*?</script>', '', text, flags=re.S)
                if '/local-demo.js' not in text:
                    text = text.replace('</body>', '<script src="/local-demo.js"></script></body>')
            else:
                candidates = []
            candidates += re.findall(r'''url\(\s*["']?([^\s\)"']+)''', text)
            for value in candidates:
                child = normalize(value, url)
                if child:
                    children.add(child)
            text = text.replace(ORIGIN + '/', '/').replace('http://avala.bold-themes.com/', '/').replace('//avala.bold-themes.com/', '/')
            text = text.replace('https:\\/\\/avala.bold-themes.com\\/', '\\/')
            data = text.encode('utf-8')
        target = destination(url)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return children
    except Exception as exc:
        failures.append({'url': url, 'error': str(exc)})
        return set()

def main():
    ROOT.mkdir(exist_ok=True)
    queue = {START}
    with futures.ThreadPoolExecutor(max_workers=8) as pool:
        while queue:
            current = sorted(queue - seen)
            if not current:
                break
            seen.update(current)
            queue = set()
            for children in pool.map(fetch, current):
                queue.update(children - seen)
            print(f'Downloaded {len(seen)} URLs; {len(pages)} pages; {len(queue)} queued; {len(failures)} failures', flush=True)
    home = destination(START)
    if home.exists():
        (ROOT / 'index.html').write_bytes(home.read_bytes())
    (ROOT / 'local-demo.js').write_text("document.addEventListener('submit', function(e) { e.preventDefault(); alert('Local preview: this form is not connected to a live service.'); }, true);", encoding='utf-8')
    Path('mirror-report.json').write_text(json.dumps({'pages': sorted(pages), 'downloaded': len(seen)-len(failures), 'failures': failures}, indent=2), encoding='utf-8')
    print('Mirror complete.', flush=True)

if __name__ == '__main__':
    main()
