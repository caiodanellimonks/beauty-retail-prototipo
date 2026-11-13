# Beauty Retail: protótipo da dashboard (V2)

Protótipo em HTML da dashboard do Beauty Retail, com as 8 alterações que o cliente pediu em cima da V1. Todos os valores são fictícios.

## Onde está cada coisa

- `v2/`: as 5 páginas (`topo-funil`, `neeche`, `lyb`, `phyto`, `bath`), a pasta `modulos/` da Phyto e o `NOTAS-V2.md`, que tem a tabela "ponto do cliente, onde está, como montar no Looker".
- `v3/`: as mesmas 5 páginas com a identidade visual padronizada (card DN-606). A Phyto usa o mesmo molde das outras, sem a pasta `modulos/`. O `GUIA-VISUAL.md` tem os tokens de cor, as cores por origem de tráfego e como montar cada componente no Looker.
- `gerar_v2.py`: gera as páginas de `v2/` (`py gerar_v2.py`). Os números são calculados lá, pra as páginas baterem entre si.
- `gerar_v3.py`: gera as páginas de `v3/` (`py gerar_v3.py`). Mesmos números da V2.
- `modulos-v2/`: módulos da Phyto com os ajustes da V2. O gerador copia pra `v2/modulos/`.
- `fonte-v1/`: página e módulos originais da Phyto, sem alteração.

## Pra mexer

Mudança de número, texto ou estrutura: edita o `gerar_v2.py` (ou `modulos-v2/` no caso da Phyto) ou o `gerar_v3.py` e roda de novo. Se editar o HTML direto, o gerador sobrescreve na próxima rodada.

## O que mudou da V1

1. Canal com engajamento e conversão
2. Rótulos nos gráficos de série
3. ROAS, ACOS e receita com comparação YoY
4. Granularidade de campanha
5. Metas por marca e investimento por canal e site
6. Backfill (só um aviso no rodapé)
7. Projeção mensal das métricas do funil
8. Aviso do bot na Neeche
