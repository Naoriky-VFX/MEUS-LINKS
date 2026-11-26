# Regras deste projeto (LINKS-NAORIKY)

Como o dono pede os links e como devemos gravar.

## Adicionar canal

Quando ele mandar um link de vídeo/canal e disser para colocar em **IA → Canais**:

1. **Não tirar** o link da categoria original onde ele já está (software, IA local, ports...).
2. **Adicionar também** um card do canal em `ia/canal/index.html`:
   - print do vídeo em `img/yt/<ID>.jpg` (baixar de `https://i.ytimg.com/vi/<ID>/hqdefault.jpg`);
   - nome do canal, descrição curta e link do canal (`youtube.com/@...`);
   - link do repositório citado no vídeo, como "um a mais".
3. No `dados.json` (e no array `LISTA` do `index.html` da raiz), o item continua na
   categoria original — só ganha o campo `video` com o ID.
4. Onde tem vídeo, a linha da pasta mostra a miniatura + título no lugar de "sem vídeo".

## Contadores e datas

- **Sempre que encontrar contador errado, corrija** (o dono autorizou): cards da home
  (`N links · N pastas`), `N links` das pastas e a data do rodapé.
- Para conferir sem alterar nada: `python _gerar/conferir_contadores.py`.
- A data do rodapé deve ser a do dia em que o site foi mexido.

## Estrutura

- `dados.json` + array `const LISTA` em `index.html` = lista geral (todas as pastas).
- Cada pasta (`ia/agentes`, `software`, `consoles/switch`...) tem o próprio `index.html`
  com tabela e linhas `<tr data-busca="...">`.
- `ia/canal/index.html` é a página de **canais** (cards `.canal`, layout diferente das tabelas).
- `_gerar/` tem os scripts antigos; **não rode `gerar_site.py`** (ele sobrescreve as pastas e
  não conhece as que foram criadas na mão, tipo `ia/local`, `ia/canal` e `servidores/amp`).

## Armadilhas

- Arquivos são **UTF-8**; não regrave com PowerShell (`Set-Content -Encoding UTF8` do PS 5.1
  corrompe acento). Use Node com `fs.writeFileSync(..., "utf8")`.
- Formato do `dados.json` segue o `json.dumps` do Python: `{"chave": "valor", ...}` com `", "` e `": "`.
- Para excluir uma linha da tabela, casar o `<tr data-busca="...">...</tr>` inteiro.
