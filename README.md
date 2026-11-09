# Beauty Retail: protótipo da dashboard (V2)

Protótipo em HTML da dashboard do Beauty Retail, com as 8 alterações que o cliente pediu em cima da V1. Todos os valores são fictícios.

## Onde está cada coisa

- `v2/`: as 5 páginas (`topo-funil`, `neeche`, `lyb`, `phyto`, `bath`), a pasta `modulos/` da Phyto e o `NOTAS-V2.md`, que tem a tabela "ponto do cliente, onde está, como montar no Looker".
- `gerar_v2.py`: gera as páginas de `v2/` (`py gerar_v2.py`). Os números são calculados lá, pra as páginas baterem entre si.
- `modulos-v2/`: módulos da Phyto com os ajustes da V2. O gerador copia pra `v2/modulos/`.
- `fonte-v1/`: página e módulos originais da Phyto, sem alteração.

## Pra mexer

Mudança de número, texto ou estrutura: edita o `gerar_v2.py` (ou `modulos-v2/` no caso da Phyto) e roda de novo. Se editar o HTML de `v2/` direto, o gerador sobrescreve na próxima rodada.

## O que mudou da V1

1. Canal com engajamento e conversão
2. Rótulos nos gráficos de série
3. ROAS, ACOS e receita com comparação YoY
4. Granularidade de campanha
5. Metas por marca e investimento por canal e site
6. Backfill (só um aviso no rodapé)
7. Projeção mensal das métricas do funil
8. Aviso do bot na Neeche
