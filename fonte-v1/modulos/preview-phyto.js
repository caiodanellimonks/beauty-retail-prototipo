/* Dados exclusivamente fictícios; entrada independente dos renderizadores. */
(function () {
  'use strict';
  const m=window.BeautyModules;
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
    {label:'Google Ads',spend:12000,clicks:7000},
    {label:'Meta Ads',spend:8000,clicks:5000}
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
  m.pulse(document.getElementById('traffic-pulse'),{periods,series:origins.map(({key,label})=>({key,label}))});
  m.channels(document.getElementById('traffic-channels'),{complete:true,rows:origins.map(({label,sessions})=>({label,value:sessions}))});
  m.media(document.getElementById('media-platforms'),media);
  m.budget(document.getElementById('media-budget'));
  m.outcomes(document.getElementById('outcomes'),{complete:true,rows:origins});
})();
