// Baixa o melhor print de cada projeto novo (README primeiro, card do GitHub depois).
// Uso: node baixar_imagens.mjs  (roda na pasta LINKS-NAORIKY)
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const RAIZ = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '..');
const IMG = path.join(RAIZ, 'img');
fs.mkdirSync(IMG, { recursive: true });

const MANIFEST_ARQ = path.join(IMG, 'manifest.json');
let manifest = {};
try { manifest = JSON.parse(fs.readFileSync(MANIFEST_ARQ, 'utf8')); } catch { manifest = {}; }

const repos = new Set();
const andar = (dir) => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === '_gerar' || e.name === 'img') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { andar(p); continue; }
    if (!e.name.endsWith('.html')) continue;
    const html = fs.readFileSync(p, 'utf8');
    for (const m of html.matchAll(/href="(https:\/\/github\.com\/([^/"]+)\/([^/?#"]+))[^"]*"/g)) {
      repos.add(`${m[2]}/${m[3].replace(/\.git$/, '')}`);
    }
  }
};
andar(RAIZ);

const RUIM = /logo|icon|badge|shield|banner|favicon|avatar|screenshot-2020|star|contrib|visitor/i;
const BOM = /screenshot|screen-shot|demo|preview|print|example|interface|usage|terminal|app\.|painel/i;

const baixarBuffer = async (url) => {
  try {
    const r = await fetch(url, { headers: { 'user-agent': 'Mozilla/5.0' }, redirect: 'follow' });
    if (!r.ok) return null;
    if (!/image\//i.test(r.headers.get('content-type') || '')) return null;
    const buf = Buffer.from(await r.arrayBuffer());
    return buf.length < 4000 ? null : buf;
  } catch { return null; }
};

const info = async (buf) => {
  try {
    const m = await sharp(buf).metadata();
    return { w: m.width || 0, h: m.height || 0, formato: m.format || 'png' };
  } catch { return null; }
};

let novos = 0;
for (const repo of [...repos].sort()) {
  if (manifest[repo]) continue;
  const base = repo.replace('/', '__');
  let escolhido = null;

  try {
    const r = await fetch(`https://raw.githubusercontent.com/${repo}/HEAD/README.md`, { headers: { 'user-agent': 'node' } });
    if (r.ok) {
      const texto = await r.text();
      const candidatos = [];
      for (const m of texto.matchAll(/!\[[^\]]*\]\(([^)\s]+)/g)) candidatos.push(m[1]);
      for (const m of texto.matchAll(/<img[^>]+src=["']([^"']+)["']/gi)) candidatos.push(m[1]);

      for (let bruto of candidatos.slice(0, 12)) {
        if (!bruto || bruto.startsWith('data:')) continue;
        let url = bruto;
        if (url.startsWith('//')) url = 'https:' + url;
        else if (url.startsWith('./')) url = url.slice(2);
        if (!/^https?:/i.test(url)) url = `https://raw.githubusercontent.com/${repo}/HEAD/${url.replace(/^\//, '')}`;
        const buf = await baixarBuffer(url);
        if (!buf) continue;
        const meta = await info(buf);
        if (!meta || meta.w < 500 || meta.h < 200) continue;
        const proporcao = meta.w / meta.h;
        const nome = url.toLowerCase();
        let nota = meta.w;
        if (RUIM.test(nome)) nota *= 0.25;
        if (BOM.test(nome)) nota *= 1.6;
        if (proporcao >= 1.15 && proporcao <= 2.6) nota *= 1.5;
        if (!escolhido || nota > escolhido.nota) escolhido = { buf, meta, nota };
        if (escolhido.nota > 1500) break;
      }
    }
  } catch { /* segue */ }

  if (!escolhido) {
    const buf = await baixarBuffer(`https://opengraph.githubassets.com/1/${repo}`);
    if (buf) {
      const meta = await info(buf);
      if (meta) escolhido = { buf, meta, nota: 0 };
    }
  }

  if (escolhido) {
    const ext = escolhido.meta.formato === 'jpeg' ? '.jpg' : '.' + (escolhido.meta.formato || 'png');
    const arquivo = base + ext;
    fs.writeFileSync(path.join(IMG, arquivo), escolhido.buf);
    manifest[repo] = arquivo;
    novos++;
    console.log(`ok   ${repo}  ${escolhido.meta.w}x${escolhido.meta.h}`);
  } else {
    console.log(`X    ${repo}`);
  }
}

fs.writeFileSync(MANIFEST_ARQ, JSON.stringify(manifest, null, 1));
console.log(`\nnovos: ${novos} | total com imagem: ${Object.keys(manifest).length}`);
