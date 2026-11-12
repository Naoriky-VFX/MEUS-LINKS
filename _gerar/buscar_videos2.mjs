// Segunda tentativa para quem ficou sem vídeo: busca o nome exato do projeto.
import fs from 'node:fs';
import path from 'node:path';

const RAIZ = 'D:/PROJETOS DE PROGRAMAÇÃO/LINKS-NAORIKY';
const VIDEOS = path.join(RAIZ, '_gerar', 'videos.json');
const IMG_YT = path.join(RAIZ, 'img', 'yt');
const CHAVE = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8';
const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

const videos = JSON.parse(fs.readFileSync(VIDEOS, 'utf8'));

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
    const re = /"videoId":"([\w-]{11})"[^]{0,600}?"title":\{"runs":\[\{"text":"([^"]{3,150})"/g;
    for (const m of txt.matchAll(re)) {
      if (achados.some((a) => a.id === m[1])) continue;
      achados.push({ id: m[1], titulo: m[2] });
      if (achados.length >= 6) break;
    }
    return achados;
  } catch { return []; } finally { clearTimeout(timer); }
};

const normal = (t) => (t || '').toLowerCase().replace(/[-_.]/g, ' ').replace(/\s+/g, ' ');

const faltando = [...repos].filter((r) => !videos[r]).sort();
console.log('sem vídeo:', faltando.length);

let achou = 0;
for (const repo of faltando) {
  const nome = normal(repo.split('/')[1]);
  const dono = repo.split('/')[0];
  let escolhido = null;

  for (const termo of [`"${nome}"`, `${nome} ${dono}`, `${nome} github ia`, `${nome} tutorial`]) {
    const lista = await buscar(termo);
    const bom = lista.find((v) => normal(v.titulo).includes(nome));
    if (bom) { escolhido = bom; break; }
    await dormir(150);
  }

  if (escolhido) {
    videos[repo] = { id: escolhido.id, titulo: escolhido.titulo };
    const destino = path.join(IMG_YT, escolhido.id + '.jpg');
    if (!fs.existsSync(destino)) {
      try {
        const t = await fetch(`https://img.youtube.com/vi/${escolhido.id}/mqdefault.jpg`);
        if (t.ok) fs.writeFileSync(destino, Buffer.from(await t.arrayBuffer()));
      } catch { /* segue */ }
    }
    achou++;
    console.log(`ok   ${repo} → ${escolhido.titulo.slice(0, 60)}`);
  } else {
    console.log(`X    ${repo}`);
  }
  fs.writeFileSync(VIDEOS, JSON.stringify(videos, null, 1));
  await dormir(150);
}

console.log(`\nachados: ${achou}/${faltando.length} | total com vídeo: ${Object.keys(videos).length}`);
