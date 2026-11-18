# HISTÓRICO — LINKS-NAORIKY

Diário do site de links (uma seção por dia). O "como fazer" está no `AGENTS.md`.

---

## 17/11/2026 — dia inteiro de curadoria

### O que mudou

- **Canais (`ia/canal`)** virou página padronizada: cada canal é um card com print, nome,
  descrição, links e uma **grade de vídeos** embaixo (dá pra acrescentar vídeos novos sem
  criar card repetido). Todos os cards ficaram dentro do mesmo container (antes dois estavam
  fora, ocupando a largura toda).
- **Canais cadastrados:** Kauã Miguel (Kc1t), You Ensina, João Ernani, Willian IA,
  Gustavo Honorato e Felipe Borges - Fala IA! (4 vídeos).
- **Links novos (com print):**
  - IA · Agentes: rerun-build/rerun, HelixDB/helix-foundry, koshimazaki/genobi, shorts-kit,
    cinetic, NousResearch/hermes-agent, kerpopule/hermes-jev-skills,
    multica-ai/andrej-karpathy-skills, czlonkowski/n8n-skills
  - IA · IA local: jtydhr88/ComfyArt, rhymeas/Creativefield, nomadoor/ComfyUI-Panorama-Stickers
  - IA · Voz & áudio: SaarthurR/atticus-mac
  - Windows & software: net-merge, vscode-theme (dinbtechit), OpenSelena/omniget,
    medhachim/CapRocket, flecha-browser, rewindvm, MultiPath, Pulsar, zigzag, kinoklip,
    nanoui, Lemon-Studio, dioramas, textfold, florilegium
  - Consoles: seedds/nxnative (Switch), elripalda/RecompStore (PS5)
  - Ports: Lothrik/diablo4-build-calc, DarkDBx/DiabloIV.Helper, MagicBeanDev/Longshot (Zelda OoT)
  - Estudos: magosheimus/hotmart-course-downloader
  - Servidores: nova pasta **Painel de servidores (AMP)** (CubeCoders/AMPTemplates)
- **Contadores** de links e pastas recalculados em todas as páginas (estavam defasados).

### Regras que ficaram

- Canal **não tira** o link da categoria original — ele continua lá e o canal entra como extra.
- Todo link novo entra **com print**; vídeo é sempre que existir um **tutorial** de verdade
  (não vale vídeo homônimo).
- Formato do `dados.json` segue o `json.dumps` do Python (`", "` e `": "`).

### Pendências

- ~21 links antigos ainda sem vídeo (não existe tutorial no YouTube).
- 14 ferramentas do ranking (Flecha, RewindVM, MultiPath, Pulsar, Zigzag, Kinoklip, shorts-kit,
  Atticus, nanoui, Lemon Studio, Dioramas, TextFold, cinetic, florilegium) entraram sem vídeo.
- Pasta `servidores/amp` foi criada a partir do modelo de `servidores/palworld` — revisar texto
  se quiser detalhes do AMP.
- Não rodar `_gerar/gerar_site.py`: ele não conhece as pastas criadas na mão (`ia/local`,
  `ia/canal`, `servidores/amp`, `ia/api-painel`).

### Commits do dia

`e537a98` 15 repos · `6fbf6de` CapRocket no canal · `4e00bbe` canais padronizados ·
`0625222` contadores · `cc0176c` Felipe Borges · `b8ff168` 14 ferramentas do ranking ·
`dbd121b` vídeo certo do karpathy-skills
