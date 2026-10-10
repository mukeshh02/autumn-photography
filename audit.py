"""Check copied pages and CSS for missing local resources and navigation."""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit
from mirror import destination, normalize, ROOT

missing = Counter()
checked = set()
class Links(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ('href', 'src', 'poster'):
            if name in attrs and tag in ('a', 'img', 'script', 'link', 'source', 'video'):
                check(attrs[name], self.base)

def check(value, base):
    if not value or value.startswith(('#', 'data:', 'mailto:', 'tel:', 'javascript:')):
        return
    full = urljoin(base, value)
    if urlsplit(full).netloc not in ('avala.bold-themes.com', 'localhost:3000'):
        return
    if urlsplit(full).path.startswith(('/fonts/', '/local-demo.js')):
        file = ROOT / urlsplit(full).path.lstrip('/')
    else:
        url = normalize(full, base)
        if not url:
            return
        file = destination(url)
    checked.add(str(file))
    if not file.exists():
        missing[urlsplit(full).path] += 1

pages = list(ROOT.rglob('*.html'))
for file in pages:
    relative = file.relative_to(ROOT).as_posix()
    base = 'https://avala.bold-themes.com/' + relative.removesuffix('index.html')
    Links(base).feed(file.read_text(encoding='utf-8'))
for file in ROOT.rglob('*.css'):
    base = 'https://avala.bold-themes.com/' + file.relative_to(ROOT).as_posix()
    for value in re.findall(r'''url\(\s*["']?([^\s\)"']+)''', file.read_text(encoding='utf-8', errors='replace')):
        check(value, base)
report = {'html_files': len(pages), 'checked_local_paths': len(checked), 'missing': dict(missing.most_common())}
Path('audit-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
