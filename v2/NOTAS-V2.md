# Beauty Retail, protótipo V2

Partiu da V1 (mesma estrutura, textos e identidade de cada marca) e acrescenta só os 8 pontos do cliente. Abrir `topo-funil.html` (Comparativo); as outras páginas são a navegação por marca. HTML estático com dados fictícios, gerado por `../gerar_v2.py`.

Só usa componentes que existem no Looker Studio: scorecard com comparação de período, tabela com métricas nas colunas, gráfico de série temporal e de colunas com rótulos, campo calculado, caixa de texto.

| # | Feedback do cliente | Onde está na V2 | Como fazer no Looker |
|---|---|---|---|
| 1 | Canal com métricas de engajamento e conversão | O painel "Sessões por canal de aquisição" virou tabela: sessões, taxa de engajamento, adições ao carrinho, compras, taxa de compra | Tabela com "Grupo de canais padrão" do GA4 e as métricas do GA4; taxas em campos calculados |
| 2 | Label no gráfico de séries | Rótulos de dados nos gráficos de linha e de colunas | "Mostrar rótulos de dados" |
| 3 | ROAS, ACOS e receita com YoY | Cartões Receita GA4, ROAS e ACOS com variação contra 2025; colunas ROAS e ACOS nas tabelas de mídia e de marcas; coluna Receita na tabela de marcas | Scorecard com comparação de período; ROAS e ACOS em campos calculados |
| 4 | Granularidade de campanha | Painel "Campanhas" na seção Mídia | Tabela com a dimensão campanha |
| 5 | Metas por marca e investimento por canal e site | Cartão "Meta de receita do mês"; coluna "Meta de receita" na tabela de marcas; "Orçamento e retorno" por canal (brand) e "Orçamento por site e canal" (Comparativo), com Orçamento mensal aprovado e Consumo do orçamento | Planilha Google Sheets com metas e orçamento por marca e canal, em blend com Ads e GA4 |
| 6 | Backfill | Frase no rodapé de cada página. Não é componente visual | Carregar histórico (pelo menos 2025) de Google Ads, Meta Ads e GA4 no BigQuery |
| 7 | Projeção mensal das métricas do funil | Seção "Projeção do mês": cartões de sessões, sessões engajadas, adições ao carrinho e compras | Campo calculado: realizado ÷ dias decorridos × dias do mês |
| 8 | Neeche com bot no tráfego | Faixa de alerta na página da Neeche | Caixa de texto fixa |

## A confirmar

- **ACOS** não apareceu nos docs; usei investimento ÷ valor de conversão. ROAS é valor de conversão ÷ investimento.
- **Bath & Body Works Brasil** lançou em jul/2026, então não existe 2025: a página dela compara com o período anterior. No Comparativo o cartão compara o total de 2026 (4 marcas) com o total de 2025 (3 marcas), que é o que o Looker faz; a nota na tela explica.
- **Phyto:** usa a página original da V1 (`phyto.html` + pasta `modulos/`, que chegou depois). Os 8 pontos foram aplicados nos módulos dela. O ponto 1 já existia: a tabela "Interação e conversão por origem" tem engajamento e conversão por origem da sessão, então não mudou. O ponto 2 entrou como rótulo do total em cada dia do gráfico de áreas (no Looker: gráfico combinado com uma série "Total" em linha, só com rótulos). O controle deslizante e o painel de seleção são da V1 e continuam sendo visualização customizada, como o README original já dizia. Os arquivos novos são `modulos/dados-v2-phyto.js` e os ajustes em `beauty-modules.js`, `beauty-modules.css` e `preview-phyto.js`; os originais estão em `fonte-v1/`.
- Metas, orçamento e todos os números são fictícios.
