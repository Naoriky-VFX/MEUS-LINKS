// Higiene final dos vídeos: só fica o que parece tutorial de tecnologia.
import fs from 'node:fs';

const VIDEOS = 'D:/PROJETOS DE PROGRAMAÇÃO/LINKS-NAORIKY/_gerar/videos.json';
const videos = JSON.parse(fs.readFileSync(VIDEOS, 'utf8'));

const TECNICO = /(ia\b|a[ií]\b|agente|agent|tutorial|como |curso|guia|instal|config|setup|review|demo|c[oó]digo|code|program|terminal|cli|app|dev\b|workflow|github|automa|painel|dashboard|api|mcp|open ?source|repo)/i;
const LIXO = /(m[uú]sica|performing|lyrics|letra\b|song\b|clipe|karaok|viol[aã]o|homer simpson|frida kahlo|angry birds|bee swarm|ilha do abismo|44 gatos|cortador|processador|insta ?360|tiktok|manobra|light leaks|fortnite|clans of|limonada|h[eé]cate|navio|concurso|apostila|skymsen|ribbon breaks|gta 6|jailbreak no ios|receita|culin)/i;

let fora = 0;
for (const [repo, v] of Object.entries(videos)) {
  const t = v.titulo || '';
  if (LIXO.test(t)) {
    delete videos[repo];
    fora++;
    console.log('fora:', repo, '→', t.slice(0, 55));
  }
}

fs.writeFileSync(VIDEOS, JSON.stringify(videos, null, 1));
console.log(`\nfora: ${fora} | ficaram: ${Object.keys(videos).length}`);
