# Beauty Retail, guia visual (DN-606)

As 5 páginas (Comparativo, Neeche, LYB, Phyto Paris e Bath) agora usam a mesma base e mudam só a camada de marca. A página de referência é a Neeche. Conteúdo e números são os da V2. Páginas geradas por `../gerar_v3.py`.

## O que mudou em relação à V2

- Base comum nas 5 páginas: neutros, tipografia, espaçamento, cabeçalho, filtros, módulos de indicador, tabelas, notas e estado vazio.
- Visão geral por domínio, como na Phyto: Mídia, Tráfego, Conversão e Receita e retorno.
- Tráfego lido por origem: colunas empilhadas por origem, total da semana no topo, legenda com as cores fixas.
- Cabeçalho, título serifado e leitura sóbria da Neeche em todas as páginas.
- A Phyto deixou de ter página própria com módulos customizados e usa o mesmo molde das outras. Saem o controle deslizante de dia e o painel de seleção.
- O Comparativo segue a ordem das marcas: 1 Visão geral, 2 Tráfego e interação, 3 Mídia, 4 Marcas e conversão, 5 Projeção do mês. Na V2 a Mídia vinha antes do Tráfego.
- Cabeçalho do Comparativo ganhou o mesmo formato das marcas (linha pequena acima do título e legenda abaixo do nome).

## Base comum

| Item | Valor |
|---|---|
| Fonte | Títulos, nome da marca e número de destaque em Georgia. Resto em Arial |
| Fundo da tela / da página | `#e8e8e8` / `#f5f4f2` |
| Texto / texto secundário | `#161616` / `#676767` |
| Linhas e bordas | `#e4e1dd` |
| Espaçamento | 12 px entre módulos, 20 px dentro dos painéis, cantos de 8 px, 40 px de margem lateral |
| Cabeçalho | 150 px de altura, linha pequena em maiúsculas, título serifado de 27 px, nome da marca à direita, faixa de 4 px na cor de destaque, menu de páginas logo abaixo |
| Filtros | Período, Marca, Plataforma de mídia e Canal GA4, nessa ordem, iguais em todas as páginas |
| Variação | Alta `#188038`, queda `#c5221f`. Em ACOS e custo a lógica é invertida |
| Alerta | Fundo `#fdecea`, faixa `#c5221f` |
| Nota de método | Texto de 11 px em cinza abaixo do componente (`note`), aviso de protótipo no topo, rodapé com ressalvas |
| Estado vazio | Traço (-) em cinza no lugar do valor, com a etiqueta "Sem dado" ao lado (estilos `vazio` e `vazio-pill`). Nenhum campo está vazio hoje, o estilo fica definido para quando faltar valor |

## Camada de marca

Só estes campos mudam de uma página para outra.

| Página | Cabeçalho | Texto do cabeçalho | Destaque | Apoio | Imagem |
|---|---|---|---|---|---|
| Comparativo (Beauty Retail) | `#2d3137` | `#ffffff` | `#5b6773` | `#eceff1` | sem |
| Neeche | `#191919` | `#ffffff` | `#242424` | `#f5f1ed` | foto da campanha |
| LYB | `#efe3d3` | `#171717` | `#282420` | `#efe3d3` | arte da campanha |
| Phyto Paris | `#142d4b` | `#ffffff` | `#3c789c` | `#e3eef4` | sem |
| Bath & Body Works | `#1a242e` | `#ffffff` | `#bb562e` | `#f8eee7` | arte da campanha |

Onde cada cor entra:
- Destaque: borda superior e título de cada módulo, painel de resumo do tráfego, aba ativa do menu, faixa do cabeçalho, borda do aviso.
- Apoio: fundo do cabeçalho das tabelas e do aviso de protótipo.

## Cores fixas por origem de tráfego

Iguais nas quatro marcas e no Comparativo.

| Origem | Cor | Observação |
|---|---|---|
| Pesquisa paga | `#3f6fa8` | Google Ads usa o mesmo tom |
| Social pago | `#3e9a86` | Meta Ads usa o mesmo tom |
| Pesquisa orgânica | `#c79a3b` | |
| Direto | `#5d6470` | |
| Outros | `#b9b4ab` | |

## Componentes e como fazer no Looker Studio

| Componente | Como fazer |
|---|---|
| Módulo por domínio | Retângulo com borda superior na cor de destaque, caixa de texto com o título e de 1 a 4 scorecards dentro |
| Resumo do tráfego (painel escuro) | Retângulo na cor de destaque com scorecards de texto branco: último intervalo e variação contra o 1º intervalo (campo calculado) |
| Colunas empilhadas por origem | Gráfico de colunas empilhadas, dimensão "Grupo de canais padrão", métrica sessões, cor de cada série definida à mão. O total no topo precisa de uma série "Total" em gráfico combinado, só com rótulos (faz com ajuste) |
| Legenda | A legenda nativa do gráfico |
| Tabelas | Métricas nas colunas, cabeçalho na cor de apoio, linha de total |
| Filtros | Controles de lista e de período, na mesma ordem em todas as páginas |
| Aviso e alerta | Caixa de texto com fundo e borda |
| Fonte | Georgia e Arial constam na lista de fontes do Looker Studio (confirmar ao montar o tema) |

Não entra no Looker, por isso ficou de fora: selo de cor dentro da célula da tabela e legenda com o total de cada origem. A cor aparece no gráfico e na legenda, e os totais estão na tabela ao lado.

## Onde estão os 8 pontos do cliente

| # | Ponto | Marcas (Neeche, LYB, Phyto, Bath) | Comparativo |
|---|---|---|---|
| 1 | Canal com engajamento e conversão | Seção 2, tabela "Sessões por canal de aquisição" | Seção 2, mesma tabela |
| 2 | Label nos gráficos | Seção 2, "O ritmo do tráfego" | Seção 2 "Sessões por semana" e seção 3 "Investimento por semana" |
| 3 | ROAS, ACOS e receita com YoY | Seção 1, módulo "Receita e retorno"; colunas na tabela de plataformas (seção 3) | Seção 1, mesmo módulo; colunas na tabela "Marcas e conversão" (seção 4) |
| 4 | Campanha | Seção 3, painel "Campanhas" | Seção 3, mesmo painel (10 maiores) |
| 5 | Metas e investimento por canal e site | Seção 1, cartão "Meta de receita do mês"; seção 3, "Orçamento e retorno" | Seção 3, "Orçamento por site e canal"; coluna de meta na tabela da seção 4 |
| 6 | Backfill | Frase no rodapé | Frase no rodapé |
| 7 | Projeção mensal | Seção 5 | Seção 5 |
| 8 | Bot da Neeche | Faixa vermelha no topo da página da Neeche | |

## A confirmar

- ACOS: usei investimento ÷ valor de conversão. Falta o cliente confirmar a definição.
- Cores de destaque e apoio das marcas saíram da V2 e da identidade das campanhas. Se o cliente tiver manual de marca, trocar pelos valores oficiais.
- Neeche teve melhor recepção do stakeholder e por isso é a referência. Aprovada a página, as outras 4 já estão no mesmo molde.
- Números continuam fictícios.
