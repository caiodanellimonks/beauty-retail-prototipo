# -*- coding: utf-8 -*-
"""Gera a V3 do protótipo de dashboard da Beauty Retail (5 páginas HTML autocontidas).

Uso: py gerar_v3.py   (grava em ./v3)

A V3 é a V2 com identidade visual padronizada (card DN-606): as 5 páginas compartilham a mesma base
(grid, espaçamento, tipografia, cabeçalho, filtros, módulos de indicador, tabelas, notas, estado vazio)
e variam só na camada de marca (cabeçalho, destaque e apoio). As cores por origem de tráfego são fixas.
Conteúdo e números são os da V2. Todos os componentes têm equivalente no Looker Studio: scorecards,
tabelas com métricas nas colunas, gráfico de colunas empilhadas com rótulo de total, campos calculados,
caixa de texto e controles de filtro. Números fictícios, calculados aqui para as páginas baterem entre si.
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v3")
DIAS_FEITOS = 28
DIAS_MES = 31
RITMO = DIAS_FEITOS / DIAS_MES


# ---------------------------------------------------------------- formatação
def fint(n):
    return f"{round(n):,}".replace(",", ".")


def brl(n):
    return "R$ " + fint(n)


def dec(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def pct(x, d=1):
    return dec(x * 100, d) + "%"


def kfmt(v, prefix=""):
    if v >= 1_000_000:
        return f"{prefix}{dec(v / 1_000_000, 1)} mi"
    if v >= 1000:
        s = f"{v / 1000:.1f}".replace(".", ",")
        if s.endswith(",0"):
            s = s[:-2]
        return f"{prefix}{s}k"
    return f"{prefix}{round(v)}"


def split_int(total, weights):
    s = float(sum(weights))
    raw = [total * w / s for w in weights]
    fl = [int(x) for x in raw]
    rest = int(round(total - sum(fl)))
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - fl[i], reverse=True)[:rest]:
        fl[i] += 1
    return fl


def esc(t):
    return t.replace("&", "&amp;")


def ratio(a, b):
    return a / b if b else 0


# ---------------------------------------------------------------- dados
CANAIS = ["Pesquisa paga", "Social pago", "Pesquisa orgânica", "Direto", "Outros"]
W_ENG = [0.95, 0.85, 1.10, 1.10, 0.90]
W_COMPRA = [1.3, 0.7, 1.0, 1.6, 0.6]
W_ATC = [1.3, 0.9, 1.0, 1.4, 0.6]
PLAT_NOME = {"g": "Google Ads", "m": "Meta Ads"}

# Cores fixas por origem de tráfego: iguais nas quatro marcas e no comparativo, em gráfico e tabela.
# Google Ads usa o tom de "Pesquisa paga" e Meta Ads o de "Social pago".
ORIGEM_COR = {
    "Pesquisa paga": "#3f6fa8",
    "Social pago": "#3e9a86",
    "Pesquisa orgânica": "#c79a3b",
    "Direto": "#5d6470",
    "Outros": "#b9b4ab",
}
PLAT_COR = {"g": ORIGEM_COR["Pesquisa paga"], "m": ORIGEM_COR["Social pago"]}
TENDENCIA = [0.10, 0.04, -0.05, 0.06, 0.0]  # inclinação semanal por origem, só para a série ficar realista

MARCAS = {
    "neeche": dict(
        nome="Neeche", arquivo="neeche.html", eyebrow="ALTA PERFUMARIA", ticket=1200,
        plat=dict(
            g=dict(inv=18000, impr=550000, clk=11000, conv=80, val=96000),
            m=dict(inv=12000, impr=700000, clk=7000, conv=40, val=48000),
        ),
        sessoes=20000, eng=0.65, atc=860, compras=300,
        canais=[7000, 4000, 4000, 4000, 1000],
        semanas=[4600, 4900, 5100, 5400],
        yoy=dict(inv=0.10, val=0.18, sessoes=0.12, compras=0.08, receita=0.15, eng_pp=0.012),
        meta=480000, plano=dict(g=20000, m=13000),
        campanhas=[
            ("g", "Search · Marca Neeche", 2, 3, 3.8), ("g", "Search · Perfumaria de nicho", 4, 3, 2.8),
            ("g", "PMax · Gifting", 3, 2, 2.2), ("m", "Prospecção · Gifting", 4, 2, 2.0),
            ("m", "Remarketing · Catálogo", 3, 4, 4.4),
        ],
        bot=True,
    ),
    "lyb": dict(
        nome="LYB", arquivo="lyb.html", eyebrow="LIVE YOUR BEAUTY", ticket=380,
        plat=dict(
            g=dict(inv=22000, impr=750000, clk=15000, conv=150, val=57000),
            m=dict(inv=18000, impr=1150000, clk=15000, conv=120, val=45600),
        ),
        sessoes=35000, eng=0.60, atc=2000, compras=700,
        canais=[12500, 9500, 6500, 5000, 1500],
        semanas=[8000, 8600, 8900, 9500],
        yoy=dict(inv=0.14, val=0.25, sessoes=0.22, compras=0.18, receita=0.21, eng_pp=-0.003),
        meta=300000, plano=dict(g=24000, m=20000),
        campanhas=[
            ("g", "Search · Marca LYB", 2, 3, 3.6), ("g", "Shopping · Maquiagem", 4, 3, 3.0),
            ("g", "PMax · Skincare", 3, 2, 2.4), ("m", "Prospecção · Lançamentos", 4, 2, 1.9),
            ("m", "Remarketing · Catálogo", 3, 4, 4.5), ("m", "Reels · Haircare", 2, 1, 0.9),
        ],
        bot=False,
    ),
    "phyto": dict(
        nome="Phyto Paris", arquivo="phyto.html", eyebrow="CUIDADO CAPILAR", ticket=390,
        plat=dict(
            g=dict(inv=12000, impr=350000, clk=7000, conv=60, val=23400),
            m=dict(inv=8000, impr=600000, clk=5000, conv=55, val=21450),
        ),
        sessoes=15000, eng=0.60, atc=820, compras=300,
        canais=[5500, 4500, 2500, 1700, 800],
        semanas=[3300, 3600, 3900, 4200],
        yoy=dict(inv=-0.05, val=0.08, sessoes=0.06, compras=0.10, receita=0.12, eng_pp=0.005),
        meta=120000, plano=dict(g=13000, m=9000),
        campanhas=[
            ("g", "Search · Marca Phyto", 2, 3, 3.4), ("g", "Search · Tratamento capilar", 5, 3, 3.3),
            ("m", "Prospecção · Coloração", 5, 2, 1.8), ("m", "Remarketing · Assinatura", 3, 4, 4.2),
        ],
        bot=False,
    ),
    "bath": dict(
        nome="Bath & Body Works Brasil", arquivo="bath.html", eyebrow="CORPO · CASA · FRAGRÂNCIAS", ticket=190,
        plat=dict(
            g=dict(inv=15000, impr=750000, clk=15000, conv=130, val=24700),
            m=dict(inv=15000, impr=1150000, clk=15000, conv=110, val=20900),
        ),
        sessoes=30000, eng=0.567, atc=2000, compras=700,
        canais=[10000, 7000, 7500, 4000, 1500],
        semanas=[6600, 7200, 7800, 8400],
        # lançou no Brasil em jul/2026: não existe 2025, então compara com o período anterior
        yoy=dict(ref="prev", inv=-0.12, val=0.06, sessoes=0.09, compras=0.07, receita=0.11, eng_pp=0.004),
        meta=170000, plano=dict(g=16500, m=16500),
        campanhas=[
            ("g", "Search · Marca Bath & Body Works", 2, 3, 3.0), ("g", "PMax · Home fragrance", 4, 3, 3.0),
            ("g", "Shopping · Body care", 3, 2, 2.0), ("m", "Awareness · Coleções", 5, 2, 1.7),
            ("m", "Remarketing · Catálogo", 3, 4, 4.3),
        ],
        bot=False,
    ),
}


def serie_por_origem(sess_c, semanas):
    """Sessões por origem e por semana: cada linha soma o total da origem e cada coluna o total da semana."""
    n_o, n_s = len(sess_c), len(semanas)
    seed = [[s * (1 + t * (w - (n_s - 1) / 2)) for w in range(n_s)] for s, t in zip(sess_c, TENDENCIA)]
    for _ in range(80):
        for i, s in enumerate(sess_c):
            f = s / sum(seed[i])
            seed[i] = [x * f for x in seed[i]]
        for w, tot in enumerate(semanas):
            f = tot / sum(seed[i][w] for i in range(n_o))
            for i in range(n_o):
                seed[i][w] *= f
    cols = [split_int(semanas[w], [seed[i][w] for i in range(n_o)]) for w in range(n_s)]
    m = [[cols[w][i] for w in range(n_s)] for i in range(n_o)]
    for _ in range(2000):  # acerta as linhas mexendo só dentro da mesma coluna
        dif = [sum(m[i]) - sess_c[i] for i in range(n_o)]
        if not any(dif):
            break
        i = max(range(n_o), key=lambda k: dif[k])
        j = min(range(n_o), key=lambda k: dif[k])
        w = max(range(n_s), key=lambda k: m[i][k])
        m[i][w] -= 1
        m[j][w] += 1
    assert all(sum(m[i]) == sess_c[i] for i in range(n_o)) and all(
        sum(m[i][w] for i in range(n_o)) == semanas[w] for w in range(n_s)), "série por origem"
    return m


def construir_marca(chave, c):
    e = dict(chave=chave, nome=c["nome"], arquivo=c["arquivo"], bot=c["bot"], ticket=c["ticket"])
    e["plat"] = {k: dict(v) for k, v in c["plat"].items()}
    e["sessoes"] = c["sessoes"]
    e["engajadas"] = round(c["sessoes"] * c["eng"])
    e["atc"] = c["atc"]
    e["compras"] = c["compras"]
    e["receita"] = c["compras"] * c["ticket"]
    sess_c = c["canais"]
    assert sum(sess_c) == c["sessoes"], (chave, "canais")
    eng_c = split_int(e["engajadas"], [s * w for s, w in zip(sess_c, W_ENG)])
    cmp_c = split_int(e["compras"], [s * w for s, w in zip(sess_c, W_COMPRA)])
    atc_c = split_int(e["atc"], [s * w for s, w in zip(sess_c, W_ATC)])
    e["canais"] = []
    for i, n in enumerate(CANAIS):
        assert eng_c[i] <= sess_c[i] and cmp_c[i] <= atc_c[i], (chave, n)
        e["canais"].append(dict(nome=n, sessoes=sess_c[i], engajadas=eng_c[i], atc=atc_c[i], compras=cmp_c[i]))
    assert sum(c["semanas"]) == c["sessoes"], (chave, "semanas")
    e["semanas"] = list(c["semanas"])
    e["serie"] = serie_por_origem(sess_c, e["semanas"])
    e["yoy"] = c["yoy"]
    e["ref"] = c["yoy"].get("ref", "ano")
    e["meta"] = c["meta"]
    e["plano"] = dict(c["plano"])
    e["campanhas"] = []
    for p in ("g", "m"):
        cs = [x for x in c["campanhas"] if x[0] == p]
        d = e["plat"][p]
        inv = split_int(d["inv"], [x[2] for x in cs])
        imp = split_int(d["impr"], [x[2] for x in cs])
        clk = split_int(d["clk"], [x[3] for x in cs])
        cnv = split_int(d["conv"], [x[3] for x in cs])
        val = split_int(d["val"], [x[3] * x[4] for x in cs])
        for i, x in enumerate(cs):
            e["campanhas"].append(dict(marca=c["nome"], plat=p, nome=x[1], inv=inv[i], impr=imp[i],
                                       clk=clk[i], conv=cnv[i], val=val[i]))
    return e


def completar(e):
    for k in ("inv", "impr", "clk", "conv", "val"):
        e[k] = e["plat"]["g"][k] + e["plat"]["m"][k]
    return e


def anterior(e, chave):
    y = e["yoy"]
    mapa = dict(inv=e["inv"], val=e["val"], sessoes=e["sessoes"], compras=e["compras"], receita=e["receita"])
    return mapa[chave] / (1 + y[chave])


def total_marcas(marcas):
    t = dict(chave="total", nome="Todas as marcas", arquivo="topo-funil.html", bot=any(m["bot"] for m in marcas), ref="ano")
    t["plat"] = {p: {k: sum(m["plat"][p][k] for m in marcas) for k in ("inv", "impr", "clk", "conv", "val")}
                 for p in ("g", "m")}
    for k in ("sessoes", "engajadas", "atc", "compras", "receita", "meta"):
        t[k] = sum(m[k] for m in marcas)
    t["canais"] = [
        {"nome": n, **{k: sum(m["canais"][i][k] for m in marcas) for k in ("sessoes", "engajadas", "atc", "compras")}}
        for i, n in enumerate(CANAIS)
    ]
    t["semanas"] = [sum(m["semanas"][i] for m in marcas) for i in range(4)]
    t["serie"] = [[sum(m["serie"][i][w] for m in marcas) for w in range(4)] for i in range(len(CANAIS))]
    t["plano"] = {p: sum(m["plano"][p] for m in marcas) for p in ("g", "m")}
    t["campanhas"] = [c for m in marcas for c in m["campanhas"]]
    # YoY do total como o Looker calcula: total de 2026 (4 marcas) contra total de 2025 (só as que existiam)
    base = [m for m in marcas if m["ref"] == "ano"]
    ant = {}
    for k in ("inv", "val", "sessoes", "compras", "receita"):
        ant[k] = sum(m[k] for m in marcas) / sum(anterior(m, k) for m in base) - 1
    eng_cur = sum(m["engajadas"] for m in base) / sum(m["sessoes"] for m in base)
    eng_old = sum((m["engajadas"] / m["sessoes"] - m["yoy"]["eng_pp"]) * anterior(m, "sessoes") for m in base) / \
        sum(anterior(m, "sessoes") for m in base)
    ant["eng_pp"] = eng_cur - eng_old
    t["yoy"] = ant
    return t


# ---------------------------------------------------------------- métricas derivadas
def roas(d):
    return ratio(d["val"], d["inv"])


def acos(d):
    return ratio(d["inv"], d["val"])


def refs(e, total=False):
    if e.get("ref") == "prev":
        return dict(suf=" vs período ant.", comp="Comparação: período anterior (03 a 30 de setembro)")
    return dict(suf=" vs 2025", comp="Comparação: mesmo período de 2025")


# ---------------------------------------------------------------- componentes
def delta(g, bom="up", suf="", pp=False):
    seta = "▲" if g >= 0 else "▼"
    txt = f"{seta} {dec(abs(g) * 100, 1)} p.p.{suf}" if pp else f"{seta} {dec(abs(g) * 100, 1)}%{suf}"
    if bom == "neutro":
        cls = "flat"
    else:
        cls = "up" if (g >= 0) == (bom == "up") else "down"
    return f'<span class="delta {cls}">{txt}</span>'


def metrica(rotulo, valor, delta_html, fonte):
    return (f'<div class="metric"><div class="label">{rotulo}</div><div class="value">{valor}</div>'
            f'{delta_html}<div class="source">{fonte}</div></div>')


def modulo(titulo, metricas, span=None):
    """Módulo por domínio: faixa de destaque, título e de 1 a 4 métricas lado a lado (grade de 6 colunas)."""
    n = len(metricas)
    return (f'<section class="module" style="grid-column:span {span or n}"><div class="kicker">{titulo}</div>'
            f'<div class="metrics" style="grid-template-columns:repeat({n},minmax(0,1fr))">{"".join(metricas)}</div></section>')


def modulos(*itens):
    return '<div class="modules">' + "".join(itens) + "</div>"


def plat(p):
    # Looker não coloca selo de cor dentro da célula de tabela: a cor fica só nos gráficos e na legenda
    return PLAT_NOME[p]


def origem(nome):
    return nome


def painel(titulo, desc, corpo, extra=""):
    return f'<div class="panel {extra}"><h3>{titulo}</h3><div class="desc">{desc}</div>{corpo}</div>'


def secao(n, titulo, pergunta):
    return f'<div class="section"><h2>{n}. {titulo}</h2><span>{pergunta}</span></div>'


def tabela(cabecalho, linhas, total=False, extra_cls=""):
    h = "".join(f"<th>{c}</th>" for c in cabecalho)
    corpo = []
    for i, l in enumerate(linhas):
        cls = ' class="total"' if total and i == len(linhas) - 1 else ""
        corpo.append(f"<tr{cls}>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>")
    return f'<div class="scroll"><table class="{extra_cls}"><thead><tr>{h}</tr></thead><tbody>{"".join(corpo)}</tbody></table></div>'


def nice_max(v):
    e = 10 ** math.floor(math.log10(v))
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if v <= m * e:
            return m * e
    return 10 * e


def grafico_empilhado(rotulos, nomes, matriz, aria=""):
    """Colunas empilhadas por origem (cores fixas), com o total de cada intervalo como rótulo."""
    w, h = 650, 205
    esq, dir_, topo, base = 62, 620, 30, 155
    tot = [sum(matriz[i][k] for i in range(len(nomes))) for k in range(len(rotulos))]
    ymax = nice_max(max(tot) * 1.15)
    faixa = (dir_ - esq) / len(rotulos)
    bw = 78
    p = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">']
    for frac in (0, 0.5, 1):
        yy = base - (base - topo) * frac
        p.append(f'<line class="gridline" x1="{esq}" y1="{yy:.1f}" x2="{dir_}" y2="{yy:.1f}"/>')
        p.append(f'<text x="{esq - 8}" y="{yy + 4:.1f}" text-anchor="end">{kfmt(ymax * frac)}</text>')
    for k, r in enumerate(rotulos):
        cx = esq + faixa * (k + 0.5)
        y = base
        for i, n in enumerate(nomes):
            hh = (base - topo) * matriz[i][k] / ymax
            y -= hh
            p.append(f'<rect class="seg" x="{cx - bw / 2:.1f}" y="{y:.1f}" width="{bw}" height="{hh:.1f}" fill="{ORIGEM_COR[n]}"/>')
        p.append(f'<text class="dlabel" x="{cx:.1f}" y="{y - 7:.1f}" text-anchor="middle">{fint(tot[k])}</text>')
        p.append(f'<text x="{cx:.1f}" y="176" text-anchor="middle">{r}</text>')
    p.append("</svg>")
    return "".join(p)


def legenda_origens(canais):
    """Legenda do gráfico (a nativa do Looker): selo de cor e nome da origem."""
    itens = "".join(f'<div class="leg"><i style="background:{ORIGEM_COR[c["nome"]]}"></i><span>{c["nome"]}</span></div>'
                    for c in canais)
    return f'<div class="origin-legend">{itens}</div>'


def grafico_barras(rotulos, grupos, fmt_eixo, fmt_rotulo, aria=""):
    w, h = 650, 205
    esq, dir_, topo, base = 56, 620, 30, 155
    ymax = nice_max(max(v for g in grupos for v in g["v"]) * 1.15)
    n = len(rotulos)
    faixa = (dir_ - esq) / n
    bw = 44
    p = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">']
    for frac in (0, 0.5, 1):
        yy = base - (base - topo) * frac
        p.append(f'<line class="gridline" x1="{esq}" y1="{yy:.1f}" x2="{dir_}" y2="{yy:.1f}"/>')
        p.append(f'<text x="{esq - 8}" y="{yy + 4:.1f}" text-anchor="end">{fmt_eixo(ymax * frac)}</text>')
    ng = len(grupos)
    for i, r in enumerate(rotulos):
        cx = esq + faixa * (i + 0.5)
        for j, g in enumerate(grupos):
            v = g["v"][i]
            hh = (base - topo) * v / ymax
            x = cx - ng * bw / 2 - (ng - 1) * 2 + j * (bw + 4)
            p.append(f'<rect x="{x:.1f}" y="{base - hh:.1f}" width="{bw}" height="{hh:.1f}" fill="{g["cor"]}" rx="2"/>')
            p.append(f'<text class="dlabel" x="{x + bw / 2:.1f}" y="{base - hh - 6:.1f}" text-anchor="middle">{fmt_rotulo(v)}</text>')
        p.append(f'<text x="{cx:.1f}" y="176" text-anchor="middle">{r}</text>')
    p.append("</svg>")
    return "".join(p)


SEMANAS = ["01–07", "08–14", "15–21", "22–28"]


# ---------------------------------------------------------------- seções
def cards_linha1_marca(e):
    return modulos(
        modulo("Mídia", [metrica("Investimento", brl(e["inv"]), "", "Google Ads + Meta Ads"),
                         metrica("Cliques", fint(e["clk"]), "", "Google Ads + Meta Ads")]),
        modulo("Tráfego", [metrica("Sessões", fint(e["sessoes"]), "", "GA4 • todos os canais"),
                           metrica("Taxa de engajamento", pct(ratio(e["engajadas"], e["sessoes"])), "",
                                   "GA4 • sessões engajadas / sessões")]),
        modulo("Conversão", [metrica("Compras GA4", fint(e["compras"]), "", "GA4 • todos os canais"),
                             metrica("Taxa de compra", pct(ratio(e["compras"], e["sessoes"]), 2), "",
                                     "GA4 • sessões com compra / sessões")]),
    )


def cards_linha1_total(t):
    return modulos(
        modulo("Mídia", [metrica("Investimento", brl(t["inv"]), "", "Google Ads + Meta Ads"),
                         metrica("Impressões", fint(t["impr"]), "", "Google Ads + Meta Ads"),
                         metrica("Cliques", fint(t["clk"]), "", "Google Ads + Meta Ads")]),
        modulo("Tráfego", [metrica("Sessões", fint(t["sessoes"]), "", "GA4 • todos os canais"),
                           metrica("Taxa de engajamento", pct(ratio(t["engajadas"], t["sessoes"])), "",
                                   f"GA4 • {fint(t['engajadas'])} sessões engajadas")]),
        modulo("Conversão", [metrica("Compras GA4", fint(t["compras"]), "", "GA4 • todos os canais")]),
    )


def cards_linha2(e, total=False):
    """Pontos 3 e 5: receita, ROAS, ACOS com comparação de período; meta de receita por marca."""
    y = e["yoy"]
    suf = refs(e, total)["suf"]
    ra = roas(e)
    ra_ant = ratio(anterior(e, "val"), anterior(e, "inv"))
    ac = acos(e)
    ac_ant = ratio(anterior(e, "inv"), anterior(e, "val"))
    return modulos(modulo("Receita e retorno", [
        metrica("Receita GA4", brl(e["receita"]), delta(y["receita"], "up", suf), "GA4 • todos os canais"),
        metrica("ROAS", dec(ra) + "x", delta(ra / ra_ant - 1, "up", suf), "Google Ads + Meta Ads"),
        metrica("ACOS", pct(ac), delta(ac / ac_ant - 1, "down", suf), "Google Ads + Meta Ads"),
        metrica("Meta de receita do mês", brl(e["meta"]), "", "soma das metas por marca" if total else "meta da marca"),
    ], span=6))


def tabela_canais(e):
    linhas = [[origem(c["nome"]), fint(c["sessoes"]), pct(ratio(c["engajadas"], c["sessoes"])), fint(c["atc"]), fint(c["compras"]),
               pct(ratio(c["compras"], c["sessoes"]), 2)] for c in e["canais"]]
    linhas.append(["Total", fint(e["sessoes"]), pct(ratio(e["engajadas"], e["sessoes"])), fint(e["atc"]), fint(e["compras"]),
                   pct(ratio(e["compras"], e["sessoes"]), 2)])
    return tabela(["Canal GA4", "Sessões", "Taxa de engajamento", "Adições ao carrinho", "Compras", "Taxa de compra"],
                  linhas, total=True, extra_cls="compact")


def painel_canais(e):
    return painel("Sessões por canal de aquisição", "GA4 • engajamento e conversão por canal", tabela_canais(e), "channel-panel")


def sec_trafego_marca(e):
    ult, prim = e["semanas"][-1], e["semanas"][0]
    graf = grafico_empilhado(["01–07 out", "08–14 out", "15–21 out", "22–28 out"], CANAIS, e["serie"],
                             aria="Sessões por intervalo de sete dias e por origem")
    hero = (
        '<div class="panel pulse-hero"><div class="pulse-summary"><div class="pulse-kicker">Tráfego no site</div>'
        '<div class="pulse-label">Último intervalo</div>'
        f'<div class="pulse-value">{fint(ult)}</div><div class="pulse-caption">sessões · 22–28 out</div>'
        f'<div class="pulse-comparison"><strong>{"+" if ult >= prim else "-"}{dec(abs(ult / prim - 1) * 100, 1)}%</strong>'
        '<span>vs. 1º intervalo<br>01–07 out</span></div></div>'
        '<div class="pulse-chart"><h3>O ritmo do tráfego</h3>'
        f'<div class="desc">Sessões GA4 · intervalos de 7 dias · por origem</div>{graf}{legenda_origens(e["canais"])}</div></div>'
    )
    return f'<div class="grid traffic-grid">{hero}{painel_canais(e)}</div>'


def sec_trafego_total(t):
    graf = grafico_empilhado(SEMANAS, CANAIS, t["serie"], aria="Sessões por semana e por origem")
    esq = painel("Sessões por semana", "GA4 • por origem • revela tendência de tráfego", graf + legenda_origens(t["canais"]))
    return f'<div class="grid traffic-grid">{esq}{painel_canais(t)}</div>'


def tabela_plataformas(e, total=False):
    linhas = []
    for p in ("g", "m"):
        d = e["plat"][p]
        if total:
            linhas.append([plat(p), brl(d["inv"]), fint(d["impr"]), fint(d["clk"]), pct(ratio(d["clk"], d["impr"]), 2),
                           "R$ " + dec(ratio(d["inv"], d["clk"])), dec(roas(d)) + "x", pct(acos(d))])
        else:
            linhas.append([plat(p), brl(d["inv"]), fint(d["clk"]), dec(roas(d)) + "x", pct(acos(d))])
    if total:
        linhas.append(["Total", brl(e["inv"]), fint(e["impr"]), fint(e["clk"]), pct(ratio(e["clk"], e["impr"]), 2),
                       "R$ " + dec(ratio(e["inv"], e["clk"])), dec(roas(e)) + "x", pct(acos(e))])
        return tabela(["Plataforma", "Investimento", "Impressões", "Cliques", "CTR", "CPC", "ROAS", "ACOS"],
                      linhas, total=True)
    linhas.append(["Total", brl(e["inv"]), fint(e["clk"]), dec(roas(e)) + "x", pct(acos(e))])
    return tabela(["Plataforma", "Investimento", "Cliques", "ROAS", "ACOS"], linhas, total=True)


def tabela_orcamento_marca(e):
    linhas = []
    tp = tr = 0
    for p in ("g", "m"):
        plan, real = e["plano"][p], e["plat"][p]["inv"]
        tp += plan
        tr += real
        linhas.append([plat(p), brl(plan), brl(real)])
    linhas.append(["Total", brl(tp), brl(tr)])
    return tabela(["Canal", "Orçamento mensal aprovado", "Consumo do orçamento"], linhas, total=True)


def tabela_orcamento_total(marcas, t):
    linhas = []
    for m in marcas:
        for p in ("g", "m"):
            plan, real = m["plano"][p], m["plat"][p]["inv"]
            linhas.append([m["nome"], plat(p), brl(plan), brl(real)])
    tp = sum(t["plano"].values())
    tr = t["inv"]
    linhas.append(["Todas as marcas", "Todos", brl(tp), brl(tr)])
    return tabela(["Marca (site)", "Canal", "Orçamento mensal aprovado", "Consumo do orçamento"], linhas, total=True, extra_cls="left2")


def tabela_campanhas(e, total=False, limite=None):
    camp = sorted(e["campanhas"], key=lambda c: -c["inv"])
    if limite:
        camp = camp[:limite]
    linhas = []
    for c in camp:
        if total:
            base = [plat(c["plat"]), c["nome"], brl(c["inv"]), fint(c["impr"]), fint(c["clk"]),
                    pct(ratio(c["clk"], c["impr"]), 2), "R$ " + dec(ratio(c["inv"], c["clk"])),
                    dec(ratio(c["val"], c["inv"])) + "x", pct(ratio(c["inv"], c["val"]))]
            linhas.append([c["marca"]] + base)
        else:
            linhas.append([plat(c["plat"]), c["nome"], brl(c["inv"]), fint(c["clk"]),
                           dec(ratio(c["val"], c["inv"])) + "x", pct(ratio(c["inv"], c["val"]))])
    if total:
        cab = ["Marca", "Plataforma", "Campanha", "Investimento", "Impressões", "Cliques", "CTR", "CPC", "ROAS", "ACOS"]
    else:
        cab = ["Plataforma", "Campanha", "Investimento", "Cliques", "ROAS", "ACOS"]
    return tabela(cab, linhas, extra_cls="camp camp-total" if total else "camp")


def painel_campanhas(e, total=False):
    desc = ("Maiores campanhas por investimento" if total else "Nível de campanha")
    return painel("Campanhas", desc, tabela_campanhas(e, total, 10 if total else None))


NOTA_ROAS = "ROAS = valor de conversão ÷ investimento. ACOS = investimento ÷ valor de conversão. O valor de conversão vem das plataformas e não é a receita do GA4."


def sec_midia_marca(e):
    p1 = painel("Desempenho por plataforma", "Métricas de mídia • distribuição de verba, cliques e retorno",
                tabela_plataformas(e) +
                '<p class="note">Campanhas e grupos de anúncio podem complementar a leitura quando o detalhamento estiver disponível. '
                'A comparação de cliques depende de definições compatíveis.</p>')
    p2 = painel("Orçamento e retorno", "Orçamento mensal aprovado e consumo por canal", tabela_orcamento_marca(e))
    return f'<div class="grid">{p1}{p2}</div><div style="height:12px"></div>{painel_campanhas(e)}'


def sec_midia_total(marcas, t):
    g = split_int(t["plat"]["g"]["inv"], [0.22, 0.25, 0.28, 0.25])
    m = split_int(t["plat"]["m"]["inv"], [0.24, 0.26, 0.25, 0.25])
    graf = grafico_barras(SEMANAS, [dict(v=g, cor=PLAT_COR["g"]), dict(v=m, cor=PLAT_COR["m"])], lambda v: kfmt(v, "R$ "),
                          lambda v: kfmt(v, "R$ "), aria="Investimento semanal por plataforma")
    esq = painel("Investimento por semana e plataforma", "R$ mil por semana • ajuda a identificar mudanças na distribuição da verba",
                 graf + f'<div class="legend"><span class="key" style="background:{PLAT_COR["g"]}"></span>Google Ads '
                        f'<span class="key" style="background:{PLAT_COR["m"]}"></span>Meta Ads</div>')
    dir_ = painel("Desempenho de mídia por plataforma", "Compara volume, eficiência de clique e retorno • métricas das plataformas",
                  tabela_plataformas(t, total=True) +
                  '<p class="note">CTR = cliques ÷ impressões; CPC = investimento ÷ cliques. '
                  'Os tipos de clique devem ser alinhados entre plataformas antes da comparação.</p>')
    orc = painel("Orçamento por site e canal", "Orçamento mensal aprovado e consumo em cada marca e canal",
                 tabela_orcamento_total(marcas, t))
    return (f'<div class="grid mid-grid">{esq}{dir_}</div><div style="height:12px"></div>{orc}'
            f'<div style="height:12px"></div>{painel_campanhas(t, True)}')


def sec_eventos(e):
    linhas = [["Adições ao carrinho", fint(e["atc"]), "Indício de interesse nos produtos"],
              ["Compras", fint(e["compras"]), "Resultado de conversão no site"]]
    return painel("Eventos de interesse no site", "GA4 • contagem ilustrativa de eventos no período",
                  tabela(["Evento", "Quantidade", "Finalidade"], linhas) +
                  '<p class="note">Contagens de eventos não formam um funil de usuários: podem incluir ações repetidas. '
                  'A cobertura e as definições do tracking devem ser validadas em cada marca.</p>')


def sec_projecao(e):
    pj = lambda v: v / RITMO
    itens = [
        ("Sessões", fint(pj(e["sessoes"]))),
        ("Sessões engajadas", fint(pj(e["engajadas"]))),
        ("Adições ao carrinho", fint(pj(e["atc"]))),
        ("Compras", fint(pj(e["compras"]))),
    ]
    fonte = "GA4 • ritmo de 01 a 28 out levado até o dia 31"
    ms = [metrica(f"{n} · projeção do mês", v, "", fonte) for n, v in itens]
    return modulos(modulo("Tráfego", ms[:2], span=3), modulo("Conversão", ms[2:], span=3))


def tabela_marcas(marcas, t):
    linhas = []
    for m in marcas + [t]:
        linhas.append([m["nome"], brl(m["inv"]), fint(m["clk"]), fint(m["sessoes"]), pct(ratio(m["engajadas"], m["sessoes"])),
                       fint(m["compras"]), pct(ratio(m["compras"], m["sessoes"]), 2), brl(m["receita"]),
                       dec(roas(m)) + "x", pct(acos(m)), brl(m["meta"])])
    return tabela(["Marca", "Investimento · mídia", "Cliques · mídia", "Sessões · GA4", "Engajamento · GA4", "Compras · GA4",
                   "Taxa de compra · GA4", "Receita · GA4", "ROAS", "ACOS", "Meta de receita"],
                  linhas, total=True, extra_cls="compact")


# ---------------------------------------------------------------- tema e CSS
# Base comum: neutros, tipografia, espaçamento, componentes. Igual nas 5 páginas.
BASE = dict(canvas="#e8e8e8", paper="#f5f4f2", ink="#161616", muted="#676767", line="#e4e1dd")

# Camada de marca: só estes campos mudam de uma página para outra.
#   header / header_ink = faixa do cabeçalho; accent = destaque; tint = apoio (fundos claros); img = imagem do cabeçalho
MARCA_TOKENS = {
    "total": dict(header="#2d3137", header_ink="#ffffff", accent="#5b6773", tint="#eceff1", img=None),
    "neeche": dict(header="#191919", header_ink="#ffffff", accent="#242424", tint="#f5f1ed",
                   img=("https://neeche.vteximg.com.br/arquivos/ids/167648/MIND%20GAMES%20DESK.jpg?v=639238018304700000", "180% auto", "right 72%", ".36")),
    "lyb": dict(header="#efe3d3", header_ink="#171717", accent="#282420", tint="#efe3d3",
                img=("https://beautyglam.vteximg.com.br/arquivos/ids/169924/PRIMAVERA.png?v=639259459186470000", "240% auto", "right 52%", ".29")),
    "phyto": dict(header="#142d4b", header_ink="#ffffff", accent="#3c789c", tint="#e3eef4", img=None),
    "bath": dict(header="#1a242e", header_ink="#ffffff", accent="#bb562e", tint="#f8eee7",
                 img=("https://bathandbodyworks.vtexassets.com/assets/vtex.file-manager-graphql/images/93e4c806-da0e-4b6e-963b-9ebe8e3c512e___94832c88d631af1a50b1e055ee6b4db9.png", "180% auto", "right 58%", ".35")),
}
TEMAS = {k: {**BASE, **v} for k, v in MARCA_TOKENS.items()}

CSS = """
:root{--serif:Georgia,"Times New Roman",serif;--sans:Arial,sans-serif;--gap:12px;--radius:8px;--up:#188038;--down:#c5221f}
*{box-sizing:border-box}
body{margin:0;background:var(--canvas);color:var(--ink);font:14px var(--sans)}
.page{max-width:1440px;margin:24px auto;background:var(--paper);padding:0 40px 36px;box-shadow:0 1px 5px #00000018;border-radius:var(--radius);overflow:hidden}
.header{position:relative;overflow:hidden;isolation:isolate;margin:0 -40px;padding:29px 40px;background:var(--header);color:var(--header-ink);min-height:150px;display:flex;justify-content:space-between;align-items:center;gap:24px;border-bottom:4px solid var(--accent)}
.header::before{content:"";position:absolute;z-index:0;top:0;right:0;bottom:0;width:62%;background-repeat:no-repeat;pointer-events:none}
.header-main,.brand-lockup{position:relative;z-index:1}
.eyebrow{display:block;font:600 10px var(--sans);letter-spacing:1.7px;opacity:.76;text-transform:uppercase}
.header h1{font:400 27px/1.2 var(--serif);margin:5px 0 6px;letter-spacing:-.2px}
.subhead{opacity:.75;font-size:12px}
.brand-name{font:400 21px var(--serif);letter-spacing:1px;text-align:right;white-space:nowrap}
.brand-caption{font-size:10px;letter-spacing:1.1px;text-transform:uppercase;opacity:.72;margin-top:7px;text-align:right}
.brand-nav{display:flex;margin:0 -40px;padding:0 40px;background:#fff;border-bottom:1px solid var(--line);overflow:auto;white-space:nowrap}
.brand-nav a{padding:14px 17px 12px;color:var(--muted);text-decoration:none;font-size:12px;border-bottom:2px solid transparent}
.brand-nav a.active{color:var(--ink);border-bottom-color:var(--accent);font-weight:bold}
.notice{margin:22px 0 14px;padding:10px 14px;background:var(--tint);border-left:3px solid var(--accent);font-size:11px;border-radius:4px}
.alert{margin:0 0 14px;padding:11px 14px;background:#fdecea;border-left:3px solid var(--down);color:#6b1311;font-size:12px;border-radius:4px;line-height:1.5}
.filters{display:flex;gap:9px;flex-wrap:wrap;margin:0 0 24px}
.filter{background:#fff;border:1px solid var(--line);padding:10px 14px;min-width:170px;font-size:12px;border-radius:5px}
.filter b{font-size:10px;text-transform:uppercase;letter-spacing:.45px;color:var(--muted);font-weight:600}
.filter small{display:block;font-size:10px;color:var(--muted);margin-top:2px}
.filter i{float:right;font-style:normal;color:var(--muted)}
.section{margin:32px 0 12px;display:flex;align-items:baseline;gap:13px}
.section h2{font:400 20px var(--serif);margin:0}
.section span{font-size:12px;color:var(--muted)}
/* módulo por domínio: faixa de destaque + título + 1 a 4 métricas */
.modules{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:var(--gap)}
.modules+.modules{margin-top:var(--gap)}
.module,.panel{background:#fff;border-radius:var(--radius);border:1px solid var(--line);min-width:0}
.module{border-top:3px solid var(--accent);padding:16px 18px 15px}
.kicker{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--accent)}
.metrics{display:grid;margin-top:12px}
.metric{padding:0 16px;min-width:0}
.metric:first-child{padding-left:0}.metric:last-child{padding-right:0}
.metric+.metric{border-left:1px solid var(--line)}
.label{font-size:11px;font-weight:600;color:var(--muted)}
.value{font-size:24px;font-weight:500;margin:10px 0 4px}
.source{font-size:10px;color:var(--muted);line-height:1.4;margin-top:4px}
.delta{display:block;font-size:11px;font-weight:600}
.delta.up{color:var(--up)}.delta.down{color:var(--down)}.delta.flat{color:var(--muted)}
/* estado vazio: campo sem valor */
.vazio{color:var(--muted);font-weight:400}
.vazio-pill{display:inline-block;background:var(--tint);color:var(--muted);border-radius:3px;font-size:10px;font-weight:700;padding:3px 6px;margin-left:6px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap)}
.mid-grid{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr)}
.panel{padding:20px}
.panel h3{font:400 16px var(--serif);margin:0 0 3px}
.panel .desc{font-size:11px;color:var(--muted);margin-bottom:16px}
.scroll{overflow:auto}
table{border-collapse:collapse;width:100%;font-size:12px;text-align:right}
th{background:var(--tint);font-weight:600;color:var(--ink)}
td,th{padding:10px 9px;white-space:nowrap}
table.compact td,table.compact th{padding:10px 7px}
table.compact th{white-space:normal;vertical-align:bottom}
thead th{border-bottom:1px solid var(--line)}
td:first-child,th:first-child{text-align:left}
table.camp td:nth-child(2),table.camp th:nth-child(2),table.left2 td:nth-child(2),table.left2 th:nth-child(2){text-align:left}
table.camp-total td:nth-child(3),table.camp-total th:nth-child(3){text-align:left}
tbody tr.total{font-weight:600}
tbody tr.total td{border-top:1px solid var(--line)}
.note{color:var(--muted);font-size:11px;line-height:1.55;margin:14px 0 0}
.chart{width:100%;height:auto;display:block;overflow:visible}
.chart text{font:11px var(--sans);fill:var(--muted)}
.chart .dlabel{font-weight:600;fill:var(--ink)}
.chart .gridline{stroke:var(--line);stroke-width:1}
.chart .seg{stroke:#fff;stroke-width:.8}
.legend{font-size:11px;color:var(--muted);margin-top:6px}
.key{display:inline-block;width:14px;height:3px;vertical-align:middle;margin:0 5px 0 12px}
.key:first-child{margin-left:0}
/* legenda por origem: mesmas cores fixas em gráfico e tabela */
.origin-legend{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:12px}
.leg{display:flex;align-items:center;gap:7px;font-size:11px;color:var(--muted)}
.leg i{width:9px;height:9px;border-radius:2px;flex:none}
.traffic-grid{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);align-items:stretch}
.pulse-hero{padding:0;display:grid;grid-template-columns:174px minmax(0,1fr);overflow:hidden;min-height:300px}
.pulse-summary{background:var(--accent);color:#fff;padding:23px 19px;display:flex;flex-direction:column}
.pulse-kicker{font-size:10px;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;line-height:1.5}
.pulse-label{font-size:11px;margin-top:25px}
.pulse-value{font:400 36px/1.1 var(--serif);letter-spacing:-.6px;margin-top:5px}
.pulse-caption{font-size:11px;line-height:1.5;margin-top:4px}
.pulse-comparison{margin-top:auto;padding-top:20px}
.pulse-comparison strong{font-size:19px;display:block}
.pulse-comparison span{display:block;font-size:10px;line-height:1.45;margin-top:3px}
.pulse-chart{min-width:0;padding:22px 20px 15px;display:flex;flex-direction:column}
.pulse-chart h3{font:400 17px var(--serif);margin:0 0 4px}
.pulse-chart .desc{margin:0 0 10px}
.bottom{font-size:11px;color:var(--muted);border-top:1px solid var(--line);padding-top:15px;margin-top:28px;line-height:1.6}
@media(max-width:1100px){.traffic-grid,.mid-grid{grid-template-columns:minmax(0,1fr)}.module{grid-column:1/-1!important}}
@media(max-width:900px){.grid{grid-template-columns:minmax(0,1fr)}.page{margin:0;padding:0 16px 25px;border-radius:0}.header,.brand-nav{margin-left:-16px;margin-right:-16px;padding-left:16px;padding-right:16px}}
@media(max-width:700px){.metrics{grid-template-columns:1fr!important}.metric,.metric:first-child,.metric:last-child{padding:10px 0}.metric+.metric{border-left:0;border-top:1px solid var(--line)}}
@media(max-width:500px){.value{font-size:20px}.brand-lockup{display:none}.pulse-hero{grid-template-columns:1fr}.section{flex-direction:column;gap:4px}}
"""

MARCAS_E = {}


def navegacao(ativa):
    itens = [("Comparativo", "topo-funil.html", "total")] + [(m["nome"], m["arquivo"], k) for k, m in MARCAS_E.items()]
    return '<nav class="brand-nav" aria-label="Páginas do protótipo">' + "".join(
        f'<a href="{href}"{" class=active aria-current=page" if k == ativa else ""}>{esc(nome)}</a>' for nome, href, k in itens) + "</nav>"


def filtros(marca_txt, comp_txt=None):
    itens = []
    for a, b in (("Período", "01 a 28 de outubro de 2026"), ("Marca", marca_txt), ("Plataforma de mídia", "Todas"), ("Canal GA4", "Todos")):
        itens.append(f'<div class="filter"><b>{a}</b><br>{esc(b)} <i>▾</i></div>')
    return '<div class="filters">' + "".join(itens) + "</div>"


ALERTA_BOT = '<div class="alert"><b>Neeche possui bot atuando nos tráfegos.</b></div>'


def pagina(chave, titulo_h1, eyebrow, nome_marca, caption, corpo, marca_filtro, e):
    t = TEMAS[chave]
    vars_ = (f":root{{--canvas:{t['canvas']};--paper:{t['paper']};--ink:{t['ink']};--muted:{t['muted']};--line:{t['line']};"
             f"--accent:{t['accent']};--tint:{t['tint']};--header:{t['header']};--header-ink:{t['header_ink']}}}")
    img = ""
    if t["img"]:
        u, size, pos, op = t["img"]
        img = f'.header::before{{background-image:url("{u}");background-size:{size};background-position:{pos};opacity:{op}}}'
    eyebrow_html = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    cap = f'<div class="brand-caption">{caption}</div>' if caption else ""
    return f"""<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(nome_marca)} | Protótipo topo de funil</title>
<style>{vars_}{CSS}{img}</style></head><body><main class="page">
<header class="header"><div class="header-main">{eyebrow_html}<h1>{titulo_h1}</h1>
<span class="subhead">Topo de funil &nbsp;|&nbsp; acompanhamento semanal</span></div>
<div class="brand-lockup"><div class="brand-name">{esc(nome_marca)}</div>{cap}</div></header>
{navegacao(chave)}
<div class="notice"><b>PROTÓTIPO VISUAL</b> — valores inteiramente ilustrativos. Filtros e gráficos são representações estáticas; não há conexão com as fontes.</div>
{filtros(marca_filtro, refs(e, chave == "total")["comp"])}
{corpo}
</main></body></html>"""


BOTTOM_BACKFILL = " A comparação com o ano anterior depende de histórico carregado (backfill) em todas as fontes."


def corpo_marca(e):
    partes = []
    if e["bot"]:
        partes.append(ALERTA_BOT)
    partes += [
        secao(1, "Visão geral", "Investimento, captação e resposta do site"),
        cards_linha1_marca(e) + cards_linha2(e),
        secao(2, "Tráfego e interação", "Como o tráfego evolui e de onde vem?"),
        sec_trafego_marca(e),
        secao(3, "Mídia", "Onde investimos e o que gerou cliques?"),
        sec_midia_marca(e),
        secao(4, "Interação e conversão", "O tráfego avança para ações relevantes?"),
        sec_eventos(e),
        secao(5, "Projeção do mês", "Onde o mês deve fechar se o ritmo continuar?"),
        sec_projecao(e),
        ('<div class="bottom">Este recorte usa dados fictícios coerentes com o comparativo. A página representa uma navegação que pode ser '
         'montada no Looker Studio; disponibilidade de dados, fontes e filtros ainda precisa de validação.' +
         BOTTOM_BACKFILL + '</div>'),
    ]
    return "".join(partes)


def corpo_total(marcas, t):
    partes = []
    nota = ('<p class="note" style="margin:8px 0 0">Bath &amp; Body Works Brasil começou em jul/2026 e não tinha 2025: '
            'a variação do total compara as 4 marcas de 2026 com as 3 que existiam em 2025. '
            'Na página da Bath a comparação é com o período anterior.</p>')
    partes += [
        secao(1, "Visão geral", "Quanto investimos e que volume de visitas e interação tivemos?"),
        cards_linha1_total(t) + cards_linha2(t, total=True) + nota,
        secao(2, "Tráfego e interação", "De onde chegam as sessões e como elas evoluem?"),
        sec_trafego_total(t),
        secao(3, "Mídia", "Onde está a verba e como evoluem os sinais de captação?"),
        sec_midia_total(marcas, t),
        secao(4, "Marcas e conversão", "Quais marcas merecem investigação e como variam os resultados?"),
        painel("Comparativo por marca", "Mídia e GA4 lado a lado • números de GA4 incluem todos os canais",
               tabela_marcas(marcas, t) +
               '<p class="note">Taxa de compra ilustrativa = sessões com compra ÷ sessões. No exemplo, cada compra ocorre em uma sessão distinta; '
               'a implementação depende da medição de sessões com compra. Não interprete cliques, sessões e compras como etapas de um mesmo grupo de pessoas.</p>'),
        secao(5, "Projeção do mês", "Onde o mês deve fechar se o ritmo continuar?"),
        sec_projecao(t),
        ('<div class="bottom">Fontes previstas: Google Ads, Meta Ads e GA4. Orçamento mensal, receita e retorno '
         'ficam sujeitos a definição e disponibilidade das fontes. O comparativo de marcas não pressupõe público unificado. Um filtro de '
         'plataforma de mídia deve afetar apenas componentes de mídia, salvo quando houver mapeamento validado com o GA4.' + BOTTOM_BACKFILL + '</div>'),
    ]
    return "".join(partes)


def main():
    os.makedirs(OUT, exist_ok=True)
    marcas = []
    for k, c in MARCAS.items():
        e = completar(construir_marca(k, c))
        MARCAS_E[k] = e
        marcas.append(e)
    t = completar(total_marcas(marcas))
    assert sum(c["sessoes"] for c in t["canais"]) == t["sessoes"]
    assert sum(c["compras"] for c in t["canais"]) == t["compras"]
    for m in marcas + [t]:
        assert sum(c["inv"] for c in m["campanhas"]) == m["inv"], m["nome"]
        assert sum(c["val"] for c in m["campanhas"]) == m["val"], m["nome"]
        assert sum(c["clk"] for c in m["campanhas"]) == m["clk"], m["nome"]
    for m in marcas:
        pg = pagina(m["chave"], "Aquisição e performance", MARCAS[m["chave"]]["eyebrow"], m["nome"], "Beauty Retail",
                    corpo_marca(m), m["nome"], m)
        open(os.path.join(OUT, m["arquivo"]), "w", encoding="utf-8").write(pg)
    pg = pagina("total", "Visão de aquisição e performance", "TODAS AS MARCAS", "BEAUTY RETAIL", "Comparativo",
                corpo_total(marcas, t), "Todas as marcas", t)
    open(os.path.join(OUT, "topo-funil.html"), "w", encoding="utf-8").write(pg)
    print("ok", [m["nome"] + f" ROAS {roas(m):.2f}" for m in marcas + [t]])


if __name__ == "__main__":
    main()
