const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, 'public');
const types = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.avif':'image/avif','.webp':'image/webp','.svg':'image/svg+xml','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf','.mp4':'video/mp4','.ico':'image/x-icon'};
http.createServer((req,res) => {
  let file;
  try { file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://localhost').pathname)); }
  catch { res.writeHead(400); return res.end('Invalid URL'); }
  if (file !== root && !file.startsWith(root + path.sep)) { res.writeHead(403); return res.end('Forbidden'); }
  try {
    const url = new URL(req.url, 'http://localhost');
    const query = [...url.searchParams].filter(([key]) => ['blog_list_view','pf_list_view','bt_sidebar','orderby','paged','product-page'].includes(key)).sort(([a],[b]) => a.localeCompare(b));
    if (query.length) {
      const key = crypto.createHash('sha1').update(new URLSearchParams(query).toString()).digest('hex').slice(0,12);
      const view = path.join(file, '__views', key + '.html');
      if (fs.existsSync(view)) file = view;
    }
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    res.writeHead(200, {'Content-Type':types[path.extname(file)] || 'application/octet-stream'});
    fs.createReadStream(file).pipe(res);
  } catch { res.writeHead(404); res.end('Page or asset not found'); }
}).listen(process.env.PORT || 3000, '127.0.0.1', () => console.log('Autumn website: http://localhost:' + (process.env.PORT || 3000)));
