/* Dados exclusivamente fictícios; entrada independente dos renderizadores. */
(function () {
  'use strict';
  const m=window.BeautyModules;
  const D=window.PHYTO_V2;
  const origins=[
    {key:'google',label:'Google Ads',weekly:[950,1150,1350,1550],engagedSessions:3000,addToCart:320,purchases:110,purchaseSessions:110},
    {key:'meta',label:'Meta Ads',weekly:[800,900,1100,1200],engagedSessions:2100,addToCart:250,purchases:70,purchaseSessions:70},
    {key:'organico',label:'Orgânico',weekly:[1050,1050,950,950],engagedSessions:2800,addToCart:190,purchases:95,purchaseSessions:95},
    {key:'outros',label:'Outros',weekly:[500,500,500,500],engagedSessions:1100,addToCart:60,purchases:25,purchaseSessions:25}
  ];
  const sum=(rows,key)=>rows.reduce((total,row)=>total+row[key],0);
  // Distribuição sintética diária preserva os totais já exibidos por origem e semana.
  const offsets=[[-10,-7,-4,0,4,7,10],[-6,3,-5,6,1,-2,3],[-5,2,5,-2,3,-4,1],[-3,3,-2,2,0,-2,2]];
  origins.forEach((o,i)=>{
    o.daily=o.weekly.flatMap(week=>Array.from({length:7},(_,day)=>Math.floor(week/7)+offsets[i][day]+(day<week%7?1:0)));
    o.sessions=o.daily.reduce((total,value)=>total+value,0);
  });
  const periods=Array.from({length:28},(_,i)=>({label:`${String(i+1).padStart(2,'0')} out`,values:Object.fromEntries(origins.map(o=>[o.key,o.daily[i]]))}));
  const media={complete:true,rows:[
    {label:'Google Ads',spend:12000,clicks:7000,roas:D.plat.g.roas,acos:D.plat.g.acos},
    {label:'Meta Ads',spend:8000,clicks:5000,roas:D.plat.m.roas,acos:D.plat.m.acos}
  ]};
  const sessions=sum(origins,'sessions');
  const rate=(numerator,denominator)=>denominator>0?100*numerator/denominator:null;
  m.overview(document.getElementById('kpi-media'), {label:'Mídia',metrics:[
    {label:'Investimento',value:sum(media.rows,'spend'),kind:'money',caption:'Google Ads + Meta Ads'},
    {label:'Cliques',value:sum(media.rows,'clicks'),caption:'Google Ads + Meta Ads'}
  ]});
  m.overview(document.getElementById('kpi-traffic'), {label:'Tráfego',metrics:[
    {label:'Sessões',value:sessions,caption:'GA4 · todos os canais'},
    {label:'Engajamento',value:rate(sum(origins,'engagedSessions'),sessions),kind:'percentage',caption:'Sessões engajadas / sessões'}
  ]});
  m.overview(document.getElementById('kpi-conversion'), {label:'Conversão',metrics:[
    {label:'Compras',value:sum(origins,'purchases'),caption:'GA4 · eventos'},
    {label:'Taxa de compra',value:rate(sum(origins,'purchaseSessions'),sessions),kind:'percentage',decimals:2,caption:'Sessões com compra / sessões'}
  ]});
  m.pulse(document.getElementById('traffic-pulse'),{periods,labels:true,series:origins.map(({key,label})=>({key,label}))});
  m.channels(document.getElementById('traffic-channels'),{complete:true,rows:origins.map(({label,sessions})=>({label,value:sessions}))});
  m.media(document.getElementById('media-platforms'),media);
  m.budget(document.getElementById('media-budget'),{rows:D.budget});
  m.campaigns(document.getElementById('media-campaigns'),{rows:D.campaigns});
  m.outcomes(document.getElementById('outcomes'),{complete:true,rows:origins});
  // Receita, ROAS, ACOS com comparação de período e meta de receita.
  const arrow=g=>(g>=0?'▲ ':'▼ ')+Math.abs(g*100).toFixed(1).replace('.',',')+'% vs 2025';
  const tone=(g,good)=>(g>=0)===(good==='up')?'up':'down';
  m.overview(document.getElementById('kpi-revenue'), {label:'Receita',metrics:[
    {label:'Receita GA4',value:D.revenue,kind:'money',delta:arrow(D.yoy.receita),tone:tone(D.yoy.receita,'up'),caption:'GA4 · todos os canais'},
    {label:'Meta de receita do mês',value:D.meta,kind:'money',caption:'meta da marca'}
  ]});
  m.overview(document.getElementById('kpi-return'), {label:'Retorno em mídia',metrics:[
    {label:'ROAS',value:D.roas,kind:'ratio',delta:arrow(D.yoy.roas),tone:tone(D.yoy.roas,'up'),caption:'Google Ads + Meta Ads'},
    {label:'ACOS',value:D.acos,kind:'percentage',delta:arrow(D.yoy.acos),tone:tone(D.yoy.acos,'down'),caption:'Google Ads + Meta Ads'}
  ]});
  // Projeção mensal das métricas do funil: ritmo de 01 a 28 out levado até o dia 31.
  const project=v=>Math.round(v*31/28);
  const note='GA4 · ritmo de 01 a 28 out até o dia 31';
  m.overview(document.getElementById('proj-traffic'), {label:'Tráfego · projeção do mês',metrics:[
    {label:'Sessões',value:project(sessions),caption:note},
    {label:'Sessões engajadas',value:project(sum(origins,'engagedSessions')),caption:note}
  ]});
  m.overview(document.getElementById('proj-conversion'), {label:'Conversão · projeção do mês',metrics:[
    {label:'Adições ao carrinho',value:project(sum(origins,'addToCart')),caption:note},
    {label:'Compras',value:project(sum(origins,'purchases')),caption:note}
  ]});
})();
