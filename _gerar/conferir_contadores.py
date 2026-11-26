# -*- coding: utf-8 -*-
"""Confere os contadores do site (somente leitura).

Uso:  python _gerar/conferir_contadores.py

Compara:
- os cards da home (links e pastas por categoria) com o dados.json;
- o "N links" de cada pagina de pasta com o numero de linhas da tabela.

Nao altera nada: so avisa o que esta errado.
"""

import io
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GRUPOS = {
    "consoles/index.html": ("Consoles", True),
    "servidores/index.html": ("Servidores de jogos online", True),
    "design/index.html": ("Tutos-Design-Produto-Padrõe-Code", True),
    "ia/index.html": ("IA", True),
    "ports/index.html": ("Ports & mods de jogos", False),
    "software/index.html": ("Windows & software", False),
    "estudos/index.html": ("Estudos & livros", False),
}


def esperado(dados, prefixo, tem_pastas):
    itens = [i for i in dados if str(i.get("cat", "")).startswith(prefixo)]
    total = len(itens)
    texto = f"{total} {'link' if total == 1 else 'links'}"
    if tem_pastas:
        pastas = len({i.get("cat") for i in itens})
        if prefixo == "IA":
            pastas += 1  # ia/canal
        texto += f" · {pastas} {'pasta' if pastas == 1 else 'pastas'}"
    return texto


def conferir():
    problemas = []
    dados = json.load(io.open(os.path.join(BASE, "dados.json"), encoding="utf-8"))

    home = io.open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
    for href, (prefixo, tem_pastas) in GRUPOS.items():
        padrao = re.compile(
            r'<a class="categoria" href="' + re.escape(href) + r'">.*?<div class="num">([^<]*)</div>',
            re.DOTALL,
        )
        achado = padrao.search(home)
        if not achado:
            problemas.append(f"home: card {href} nao encontrado")
            continue
        atual = achado.group(1).strip()
        certo = esperado(dados, prefixo, tem_pastas)
        if atual != certo:
            problemas.append(f"home {href}: esta '{atual}', deveria ser '{certo}'")

    for pasta, _subs, arquivos in os.walk(BASE):
        if ".git" in pasta:
            continue
        for nome in arquivos:
            if not nome.endswith(".html"):
                continue
            caminho = os.path.join(pasta, nome)
            t = io.open(caminho, encoding="utf-8").read()
            achado = re.search(r'id="contagem"[^>]*>([^<]*)<', t)
            if not achado:
                continue
            linhas = len(re.findall(r"<tr data-busca=", t))
            if linhas == 0:
                continue
            certo = f"{linhas} {'link' if linhas == 1 else 'links'}"
            atual = achado.group(1).strip()
            if atual != certo:
                problemas.append(
                    f"{os.path.relpath(caminho, BASE)}: esta '{atual}', deveria ser '{certo}'"
                )
    return problemas


if __name__ == "__main__":
    falhas = conferir()
    if not falhas:
        print("contadores ok")
        sys.exit(0)
    print(f"{len(falhas)} problema(s):")
    for item in falhas:
        print(" -", item)
    sys.exit(1)
