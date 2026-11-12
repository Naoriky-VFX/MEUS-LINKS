// Vídeo tutorial (PT-BR primeiro) para cada projeto, via busca interna do YouTube.
import fs from 'node:fs';
import path from 'node:path';

const RAIZ = 'D:/PROJETOS DE PROGRAMAÇÃO/LINKS-NAORIKY';
const IMG_YT = path.join(RAIZ, 'img', 'yt');
const SAIDA = path.join(RAIZ, '_gerar', 'videos.json');
fs.mkdirSync(IMG_YT, { recursive: true });
fs.mkdirSync(path.dirname(SAIDA), { recursive: true });

const CHAVE = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8';
const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

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

let videos = {};
try { videos = JSON.parse(fs.readFileSync(SAIDA, 'utf8')); } catch { videos = {}; }

const buscar = async (termo) => {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 12000);
  try {
    const r = await fetch(`https://www.youtube.com/youtubei/v1/search?key=${CHAVE}&prettyPrint=false`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0' },
      body: JSON.stringify({
        context: { client: { clientName: 'WEB', clientVersion: '2.20241101.01.00', hl: 'pt', gl: 'BR' } },
        query: termo,
        params: 'EgIQAQ%3D%3D',
      }),
      signal: ctrl.signal,
    });
    const txt = await r.text();
    const achados = [];
    const re = /"videoId":"([\w-]{11})"[^]{0,600}?"title":\{"runs":\[\{"text":"([^"]{3,140})"/g;
    for (const m of txt.matchAll(re)) {
      if (achados.some((a) => a.id === m[1])) continue;
      achados.push({ id: m[1], titulo: m[2] });
      if (achados.length >= 4) break;
    }
    return achados;
  } catch {
    return [];
  } finally {
    clearTimeout(timer);
  }
};

let novos = 0;
const fila = [...repos].sort().filter((r) => !videos[r]);
console.log('faltando:', fila.length, '| já com vídeo:', Object.keys(videos).length);

for (const repo of fila) {
  const nome = repo.split('/')[1].replace(/[-_]/g, ' ');
  let achado = null;

  for (const termo of [`${nome} tutorial português`, `${nome} tutorial`, `${nome} como usar`]) {
    const lista = await buscar(termo);
    if (lista.length) { achado = lista[0]; break; }
    await dormir(150);
  }

  if (achado) {
    videos[repo] = { id: achado.id, titulo: achado.titulo };
    const destino = path.join(IMG_YT, achado.id + '.jpg');
    if (!fs.existsSync(destino)) {
      try {
        const t = await fetch(`https://img.youtube.com/vi/${achado.id}/mqdefault.jpg`);
        if (t.ok) fs.writeFileSync(destino, Buffer.from(await t.arrayBuffer()));
      } catch { /* segue */ }
    }
    novos++;
    console.log(`ok   ${repo} → ${achado.titulo.slice(0, 55)}`);
  } else {
    console.log(`X    ${repo}`);
  }

  fs.writeFileSync(SAIDA, JSON.stringify(videos, null, 1));
  await dormir(120);
}

console.log(`\nvídeos: ${Object.keys(videos).length}/${repos.size} (novos: ${novos})`);
