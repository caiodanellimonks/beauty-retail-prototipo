/* Renderizadores independentes para a prévia. Não são um pacote dscc publicado. */
(function (global) {
  'use strict';
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const valid = n => typeof n === 'number' && Number.isFinite(n);
  const number = n => valid(n) ? new Intl.NumberFormat('pt-BR').format(n) : '—';
  const money = n => valid(n) ? 'R$ ' + number(n) : '—';
  const pct = (n, digits = 1) => valid(n) ? new Intl.NumberFormat('pt-BR',{minimumFractionDigits:digits,maximumFractionDigits:digits}).format(n) + '%' : '—';
  const signedPct = n => valid(n) ? (n > 0 ? '+' : '') + pct(n) : '—';
  const ratio = (n, d) => valid(n) && valid(d) && d > 0 && n >= 0 && n <= d ? n / d * 100 : null;
  const colors = ['var(--ink)','var(--blue)','var(--source-organic, #397657)','var(--source-other, #806681)'];
  const format = item => item.kind === 'money' ? money(item.value) : item.kind === 'percentage' ? pct(item.value,item.decimals ?? 1) : number(item.value);
  const heading = (title, subtitle, tag) => `<div class="module-heading"><div><h3>${escape(title)}</h3><p>${escape(subtitle)}</p></div>${tag ? `<span class="module-tag">${escape(tag)}</span>` : ''}</div>`;

  function overview(root, data) {
    root.classList.add('module','overview');
    root.innerHTML = `<span class="module-kicker">${escape(data.label)}</span><div class="overview-values">${data.metrics.map(m => `<div><span class="metric-label">${escape(m.label)}</span><strong class="metric-value">${escape(format(m))}</strong><span class="metric-caption">${escape(m.caption)}</span></div>`).join('')}</div>`;
  }

  function pulse(root, data) {
    root.classList.add('module','pulse');
    const periods=data.periods, series=data.series;
    const complete=periods.length>0 && series.length>0 && periods.every(p=>series.every(s=>valid(p.values?.[s.key]) && p.values[s.key]>=0));
    if (!complete) { root.innerHTML=`<div class="pulse-body">${heading('Evolução das sessões','GA4 · origem da sessão','GA4')}<p class="module-note">Dados indisponíveis para um ou mais dias e origens.</p></div>`; return; }
    const total=p=>series.reduce((sum,s)=>sum+p.values[s.key],0);
    const maxTotal=Math.max(...periods.map(total));
    const unit=maxTotal>0?10**Math.floor(Math.log10(maxTotal)):1;
    const axis=maxTotal>0?Math.ceil(maxTotal/unit)*unit:1;
    const left=55,right=610,top=20,bottom=151;
    const xs=periods.map((_,i)=>periods.length===1?(left+right)/2:left+i*(right-left)/(periods.length-1));
    const y=value=>bottom-value/axis*(bottom-top);
    const grid=[axis,axis/2,0].map((n,i)=>{const gy=top+i*(bottom-top)/2;return `<line class="gridline" x1="${left}" y1="${gy}" x2="${right}" y2="${gy}"/><text class="axis-label" x="45" y="${gy+4}" text-anchor="end">${number(n)}</text>`;}).join('');
    let floor=periods.map(()=>0);
    const areas=series.map((s,j)=>{
      const lower=[...floor];
      floor=periods.map((p,i)=>lower[i]+p.values[s.key]);
      const upperPoints=periods.map((p,i)=>`${xs[i].toFixed(1)},${y(floor[i]).toFixed(1)}`);
      const lowerPoints=periods.map((p,i)=>`${xs[i].toFixed(1)},${y(lower[i]).toFixed(1)}`).reverse();
      return `<path class="stacked-area" data-series="${escape(s.key)}" style="fill:${colors[j%colors.length]}" d="M ${upperPoints.join(' L ')} L ${lowerPoints.join(' L ')} Z"/>`;
    }).join('');
    const ticks=[...new Set([0,Math.round((periods.length-1)/4),Math.round((periods.length-1)/2),Math.round(3*(periods.length-1)/4),periods.length-1])];
    const labels=ticks.map(i=>`<text class="day-label" x="${xs[i].toFixed(1)}" y="174" text-anchor="middle">${escape(periods[i].label)}</text>`).join('');
    const legend=series.map((s,i)=>`<div class="series-item"><i class="series-swatch" style="background:${colors[i%colors.length]}"></i><span>${escape(s.label)}</span><strong class="series-number">—</strong></div>`).join('');
    root.innerHTML=`<div class="pulse-feature" aria-live="polite"><span class="module-kicker">Tráfego no site</span><span class="feature-label"></span><strong class="feature-value"></strong><span class="feature-period"></span><div class="feature-change"></div></div><div class="pulse-body">${heading('Evolução das sessões por origem','Origem da sessão · sessões por dia','GA4')}<div class="series-caption"></div><div class="series-legend" aria-label="Sessões por origem no dia selecionado">${legend}</div><div class="pulse-chart-wrap"><svg class="pulse-svg" viewBox="0 0 650 185" role="img">${grid}${areas}<line class="selection-line" y1="${top}" y2="${bottom}"/><circle class="selection-dot" r="5"/>${labels}</svg><input class="day-slider" type="range" min="0" max="${periods.length-1}" value="${periods.length-1}" step="1" aria-label="Selecionar dia"/><div class="pulse-hint">Arraste para selecionar um dia</div></div></div>`;
    const slider=root.querySelector('.day-slider');
    const featureLabel=root.querySelector('.feature-label');
    const featureValue=root.querySelector('.feature-value');
    const featurePeriod=root.querySelector('.feature-period');
    const featureChange=root.querySelector('.feature-change');
    const caption=root.querySelector('.series-caption');
    const numbers=root.querySelectorAll('.series-number');
    const indicator=root.querySelector('.selection-line');
    const point=root.querySelector('.selection-dot');
    const chart=root.querySelector('.pulse-svg');
    function select(index) {
      const p=periods[index], baseline=total(periods[0]), amount=total(p);
      const change=index>0 && baseline>0?(amount-baseline)/baseline*100:null;
      featureLabel.textContent=index===periods.length-1?'Último dia':'Dia selecionado';
      featureValue.textContent=number(amount);
      featurePeriod.innerHTML=`sessões · ${escape(p.label)}<br>todas as origens`;
      featureChange.innerHTML=index===0?'<strong>Referência</strong><span>primeiro dia</span>':`<strong>${signedPct(change)}</strong><span>vs. primeiro dia<br>${escape(periods[0].label)}</span>`;
      caption.textContent=`Sessões em ${p.label}`;
      series.forEach((s,i)=>{numbers[i].textContent=number(p.values[s.key]);});
      indicator.setAttribute('x1',xs[index]);indicator.setAttribute('x2',xs[index]);
      point.setAttribute('cx',xs[index]);point.setAttribute('cy',y(amount));
      slider.setAttribute('aria-valuetext',`${p.label}: ${number(amount)} sessões`);
      chart.setAttribute('aria-label',`Sessões diárias por origem, de ${periods[0].label} a ${periods[periods.length-1].label}. Em ${p.label}, ${number(amount)} sessões: `+series.map(s=>`${s.label} ${number(p.values[s.key])}`).join(', ')+'.');
    }
    slider.addEventListener('input',()=>select(Number(slider.value)));
    select(periods.length-1);
  }

  function channels(root, data) {
    root.classList.add('module','channels');
    const rows=data.rows;
    const allValid=rows.every(r=>valid(r.value)&&r.value>=0);
    const total=allValid?rows.reduce((sum,r)=>sum+r.value,0):null;
    const complete=data.complete === true && allValid && total>0;
    root.innerHTML = `${heading('De onde vem o tráfego','Distribuição por origem da sessão','GA4')}<div class="channels-total"><strong>${complete?number(total):'—'}</strong><span>${complete?'sessões no período':'total indisponível'}</span></div><div class="segmented" aria-hidden="true">${complete ? rows.map((r,i)=>`<span style="width:${r.value/total*100}%;background:${colors[i%colors.length]}"></span>`).join('') : ''}</div><div class="channel-list">${rows.map((r,i)=>`<div class="channel-row"><span class="channel-name"><i style="background:${colors[i%colors.length]}"></i>${escape(r.label)}</span><span class="channel-number">${number(r.value)}</span><span class="channel-share">${complete?pct(r.value/total*100):'—'}</span></div>`).join('')}</div>${complete?'':'<p class="module-note">Participação indisponível enquanto a cobertura dos canais não for confirmada.</p>'}`;
  }

  function media(root, data) {
    root.classList.add('module','media-module');
    const rows=data.rows;
    const allValid=rows.every(r=>valid(r.spend)&&r.spend>=0);
    const total=allValid?rows.reduce((sum,r)=>sum+r.spend,0):null;
    const complete=data.complete===true && allValid && total>0;
    root.innerHTML = `${heading('Distribuição do investimento','Google Ads + Meta Ads','Mídia')}<div class="media-top"><div class="media-total"><strong>${complete?money(total):'—'}</strong><span>investimento considerado</span></div><span class="media-share-label">Participação entre<br>as plataformas exibidas</span></div><div class="segmented" aria-hidden="true">${complete?rows.map((r,i)=>`<span style="width:${r.spend/total*100}%;background:${colors[i%colors.length]}"></span>`).join(''):''}</div><div class="platforms">${rows.map((r,i)=>`<div class="platform"><div class="platform-head">${escape(r.label)} <span>${complete?pct(r.spend/total*100,0):'—'}</span></div><strong>${money(r.spend)}</strong><small>${number(r.clicks)} cliques</small></div>`).join('')}</div><p class="module-note">Cliques e investimento são métricas das plataformas de mídia.</p>`;
  }

  function budget(root) {
    root.classList.add('module','budget-module');
    root.innerHTML = `${heading('Planejamento e retorno','Indicadores aguardando definição das fontes','')}<div style="margin-top:15px"><span class="pending-pill">A definir</span></div><div class="pending-values"><div class="pending"><small>Orçamento aprovado</small><strong>—</strong></div><div class="pending"><small>Consumo do orçamento</small><strong>—</strong></div><div class="pending"><small>Retorno em mídia</small><strong>—</strong></div></div><p class="module-note">Receita, orçamento e modelo de atribuição precisam ser validados.</p>`;
  }

  function engagement(root, data) {
    root.classList.add('module','engagement-module');
    const rate=ratio(data.engagedSessions,data.sessions);
    root.innerHTML = `${heading('Qualidade da visita','Sessões com engajamento','GA4')}<div class="engagement-line"><strong>${pct(rate)}</strong><span>taxa de engajamento</span></div><div class="engagement-meter" role="img" aria-label="Taxa de engajamento: ${pct(rate)}">${rate === null ? '' : `<i style="width:${rate}%"></i>`}</div><div class="engagement-detail">${number(data.engagedSessions)} sessões engajadas em ${number(data.sessions)} sessões</div>`;
  }

  function events(root, data) {
    root.classList.add('module','events-module');
    root.innerHTML = `${heading('Interesse e conversão','Eventos registrados no site','GA4')}<div class="event-values">${data.map(e=>`<div class="event"><span>${escape(e.label)}</span><strong>${number(e.value)}</strong><small>eventos no período</small></div>`).join('')}</div><p class="module-note">Eventos podem se repetir na mesma sessão; os números não representam etapas de um funil de usuários.</p>`;
  }

  function outcomes(root, data) {
    root.classList.add('module','outcomes');
    const rows=data.rows;
    const fields=['sessions','engagedSessions','addToCart','purchases','purchaseSessions'];
    const complete=data.complete===true && rows.length>0 && rows.every(r=>fields.every(k=>valid(r[k])&&r[k]>=0) && r.engagedSessions<=r.sessions && r.purchaseSessions<=r.sessions);
    const total={};
    fields.forEach(k=>total[k]=complete?rows.reduce((sum,r)=>sum+r[k],0):null);
    const cells=r=>`<td>${number(r.sessions)}</td><td><span class="rate-value">${pct(ratio(r.engagedSessions,r.sessions))}</span></td><td>${number(r.addToCart)}</td><td>${number(r.purchases)}</td><td><span class="rate-value">${pct(ratio(r.purchaseSessions,r.sessions),2)}</span></td>`;
    const tableRows=rows.map((r,i)=>`<tr><th scope="row"><span class="outcome-origin"><i style="background:${colors[i%colors.length]}"></i>${escape(r.label)}</span></th>${cells(r)}</tr>`).join('');
    root.innerHTML=`${heading('Interação e conversão por origem','Origem da sessão em que as ações ocorreram','GA4')}<div class="outcomes-scroll" role="region" tabindex="0" aria-label="Comparação de interação e conversão por origem"><table class="outcomes-table"><thead><tr><th scope="col">Origem da sessão</th><th scope="col">Sessões</th><th scope="col">Engajamento</th><th scope="col">Adições ao carrinho</th><th scope="col">Compras</th><th scope="col">Taxa de compra</th></tr></thead><tbody>${tableRows}</tbody><tfoot><tr><th scope="row">Total</th>${cells(total)}</tr></tfoot></table></div><p class="scroll-hint">Deslize para ver todas as métricas →</p><p class="module-note">Engajamento = sessões engajadas / sessões; taxa de compra = sessões com compra / sessões. Adições e compras são eventos e podem se repetir.</p><p class="module-note outcome-note">Google Ads e Meta Ads representam mídia paga; orgânico e outros completam a classificação ilustrativa. As regras de origem precisam ser validadas no GA4; a associação não mede efeito causal.</p>`;
  }

  global.BeautyModules = Object.freeze({overview,pulse,channels,media,budget,engagement,events,outcomes});
})(window);
