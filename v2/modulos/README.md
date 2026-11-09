# Prévia modular — Beauty Retail

Prévia local para validação visual, não uma Community Visualization publicada. `beauty-modules.js` contém renderizadores independentes, `beauty-modules.css` fornece o estilo comum e `preview-phyto.js` contém somente dados fictícios e composição. As cores vêm de variáveis definidas pela página da marca.

| Módulo visual | Entrada necessária | Finalidade e cuidado |
|---|---|---|
| Indicadores por domínio | Métricas no grão do período | Separar mídia, tráfego e conversão; não somar taxas entre linhas. |
| Tráfego por origem | Dia, origem da sessão e sessões por combinação | Empilhar as origens exclusivas: a altura total é o total diário. O destaque é seleção local, não filtro nativo. |
| Canais | Canal e sessões | Percentuais exigem categorias mutuamente exclusivas e cobertura completa do total exibido. |
| Plataformas de mídia | Plataforma, investimento e cliques | A participação é sobre as plataformas exibidas; Google e Meta precisam de fonte consolidada ou combinação validada. |
| Planejamento e retorno | Orçamento e retorno ainda não definidos | Ausências são `—`; atribuição e receita precisam ser definidas. |
| Interação e conversão por origem | Origem da sessão, sessões, sessões engajadas, eventos de carrinho e compra e sessões com compra | Calcular taxas com numerador e denominador corretos; eventos não são pessoas nem etapas de funil. Os totais exigem cobertura completa e categorias exclusivas. |

A implementação final exigirá contratos e fontes por módulo, adaptação para `dscc`, configuração/manifesto e validação no relatório. Controles de período e filtros do relatório devem ser nativos; o destaque local da tendência não promete cross-filter. A imagem do cabeçalho é pública e remota na prévia; dependências externas não são base confiável dentro do iframe.

Na prévia, Google Ads e Meta Ads representam tráfego pago; Orgânico e Outros completam os grupos. O mapeamento real de origem/mídia/campanha, tráfego não identificado e configurações de atribuição devem ser validados na fonte. Os eventos são agrupados pela origem da sessão em que ocorreram, não pelo modelo de atribuição de eventos nem por causalidade.
