/* Interactive Canvas map for a completed FORMA demo run. No dependencies. */
window.createNodeGraph = function createNodeGraph(canvas, hooks) {
  const ctx = canvas.getContext('2d');
  const accent='#74c7d5';
  const stageNames = {VI:'FROZEN MEASUREMENTS',SH:'LINE REVIEW',FA:'INDEPENDENT VOTES',ROUTE:'CODE ROUTER',GRAPH:'TYPE GRAPH',HS:'SYNTHESIS'};
  const stageNamesZh = {VI:'冻结测量',SH:'谱线审查',FA:'独立投票',ROUTE:'代码路由',GRAPH:'类型图',HS:'合并与比较'};
  let sample=null, mode='overview', nodes=[], edges=[], scale=1, ox=0, oy=0, cssWidth=0, cssHeight=0;
  let language='zh';
  const tr=value=>window.FORMA_I18N.generated(value,language);
  const brief=value=>{const raw=String(value??'');const match=raw.match(/^(\d+) 项 (.+)$/);return language==='en'&&match?`${match[1]} ${match[2]} items`:window.FORMA_I18N.text(raw,language);};
  let pointer=null, hovered=null;

  const byStage=(stage,hyp)=>sample.nodes.filter(n=>n.stage===stage && (!hyp||n.hyp===hyp));
  const pick=(stage,hyp,part)=>byStage(stage,hyp).find(n=>!part||n.title.includes(part));
  const short=(s,max=25)=>String(s||'').length>max?String(s).slice(0,max-1)+'…':String(s||'');
  function put(list,{x,y,w=218,h=78,label,sub='',badge='',stage,hyp=null,id=null,status='recorded',active=false}){
    const n={x,y,w,h,label,sub,badge,stage,hyp,id,status,active};list.push(n);return n;
  }
  function join(from,to,soft=false){if(from&&to)edges.push({from,to,soft});}
  function overview(){
    nodes=[];edges=[];
    const vi=pick('VI');
    const viBox=put(nodes,{x:55,y:355,w:240,h:92,label:language==='en'?'VI · Frozen measurements':'VI · 冻结测量',sub:'CWT / Gaussian / Redrock',badge:'01',stage:'VI',id:vi?.id,active:!!sample.result.winner_member_hypotheses?.length});
    const survivors=new Set(sample.result.surviving_hypotheses||[]);
    const winners=new Set(sample.result.winner_member_hypotheses||[]);
    const merge=pick('HS',null,'合并'),compare=pick('HS',null,'比较');
    const mergeBox=put(nodes,{x:1375,y:307,w:235,h:84,label:tr('假设合并'),sub:language==='en'?`${sample.result.hs_group_count} final groups`:`${sample.result.hs_group_count} 个最终组`,badge:'HS / MERGE',stage:'HS',id:merge?.id,active:!!winners.size});
    const compareBox=put(nodes,{x:1375,y:440,w:235,h:84,label:tr('跨组比较'),sub:tr(sample.result.winner_type||'弃权'),badge:'HS / COMPARE',stage:'HS',id:compare?.id,active:!!winners.size});
    join(mergeBox,compareBox);
    for(let i=1;i<=6;i++){
      const hyp='H'+i, y=148+(i-1)*100;
      const sh=pick('SH',hyp), route=pick('ROUTE',hyp,'类型入口');
      const graphNodes=byStage('GRAPH',hyp);
      const terminal=graphNodes.find(n=>n.subtitle.includes('analysis_report'))||graphNodes.find(n=>n.subtitle.includes('route_result'))||graphNodes.at(-1);
      const faCount=byStage('FA',hyp).length;
      const graphType=terminal?.graph||route?.output?.selected_initial_graph||'—';
      const active=winners.has(hyp);
      const a=put(nodes,{x:316,y,w:225,label:`${hyp} · SH`,sub:language==='en'?(sh?'Line review complete':'No node artifact'):(sh?'已执行线审':'无节点产物'),badge:'SH',stage:'SH',hyp,id:sh?.id,status:sh?.status,active});
      const b=put(nodes,{x:574,y,w:210,label:`${hyp} · FA`,sub:language==='en'?(faCount?'Independent review':'Shared feature votes'):(faCount?'独立投票与审查':'共享特征投票'),badge:'FA',stage:'FA',hyp,active});
      const c=put(nodes,{x:816,y,w:220,label:language==='en'?`${hyp} · Route`:`${hyp} · 路由`,sub:route?.output?.selected_initial_graph||tr('入口未决'),badge:'ROUTE',stage:'ROUTE',hyp,id:route?.id,status:route?.status,active});
      const d=put(nodes,{x:1065,y,w:250,label:graphNodes.length?(language==='en'?`${hyp} · ${graphType} graph`:`${hyp} · ${graphType} 图`):(language==='en'?`${hyp} · Graph not run`:`${hyp} · 未执行类型图`),sub:graphNodes.length?tr(survivors.has(hyp)?'survive':'not_survived'):(language==='en'?'No positive entry evidence':'无正向入口证据'),badge:'TYPE GRAPH',stage:'GRAPH',hyp,id:terminal?.id,status:graphNodes.length?(survivors.has(hyp)?'survive':'not_survived'):'not_executed',active});
      join(viBox,a);join(a,b);join(b,c);join(c,d,!graphNodes.length);
      if(survivors.has(hyp))join(d,mergeBox);
    }
  }
  function focus(hyp){
    nodes=[];edges=[];
    const path=[];
    const sh=pick('SH',hyp),route=pick('ROUTE',hyp,'类型入口');
    if(sh)path.push({...sh,graphLabel:language==='en'?'SH · Line review':'SH · 谱线审查'});
    const fa=byStage('FA',hyp);
    path.push({stage:'FA',hyp,graphLabel:language==='en'?'FA · Independent votes':'FA · 独立投票',brief:language==='en'?(fa.length?`${fa.length} local checks + shared feature votes`:'Shared feature votes'):(fa.length?`${fa.length} 个局部审查节点 + 共享特征票`:'共享特征投票'),status:'aggregated'});
    if(route)path.push({...route,graphLabel:language==='en'?'Code entry router':'代码入口路由'});
    for(const n of byStage('ROUTE',hyp).filter(n=>n!==route))path.push({...n,graphLabel:tr(n.title.replace(hyp+' · ',''))});
    for(const n of byStage('GRAPH',hyp).sort((a,b)=>a.order-b.order||a.id-b.id))path.push({...n,graphLabel:tr(n.title.replace(hyp+' · ',''))});
    if((sample.result.surviving_hypotheses||[]).includes(hyp)){
      const merge=pick('HS',null,'合并');
      if(merge)path.push({...merge,graphLabel:language==='en'?'Enter HS merge':'进入 HS 合并'});
    }
    path.forEach((item,i)=>{
      const row=Math.floor(i/4),col=i%4;
      const visualCol=row%2?3-col:col;
      const x=80+visualCol*340,y=160+row*140;
      const control=item.stage==='ROUTE'||/队列|出口|queue|exit/i.test(item.graphLabel||'');
      const n=put(nodes,{x:x+(control?25:0),y:y+(control?9:0),w:control?250:300,h:control?82:98,label:item.graphLabel||item.title,
        sub:short(brief(item.brief),36),badge:item.stage+(item.status?' / '+short(tr(item.status),13):''),
        stage:item.stage,hyp,id:item.id,status:item.status,
        active:true});
      if(i)join(nodes[i-1],n);
    });
    if(!nodes.length)put(nodes,{x:100,y:250,w:300,h:85,label:language==='en'?`${hyp} · No displayable nodes`:hyp+' 无可显示节点',stage:'ROUTE',hyp});
  }
  function layout(){mode==='overview'?overview():focus(mode);fit();hooks.onMode?.(mode);}
  function resize(){
    const rect=canvas.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2);
    cssWidth=Math.max(rect.width,1);cssHeight=Math.max(rect.height,1);
    canvas.width=Math.round(cssWidth*dpr);canvas.height=Math.round(cssHeight*dpr);
    ctx.setTransform(dpr,0,0,dpr,0,0);fit();
  }
  function fit(){
    if(!nodes.length||!cssWidth)return;
    const minX=Math.min(...nodes.map(n=>n.x))-35,maxX=Math.max(...nodes.map(n=>n.x+n.w))+35;
    const minY=Math.min(...nodes.map(n=>n.y))-80,maxY=Math.max(...nodes.map(n=>n.y+n.h))+35;
    const availableW=cssWidth-42,availableH=cssHeight-40;
    scale=Math.min(availableW/(maxX-minX),availableH/(maxY-minY),1.15);
    ox=(cssWidth-(maxX-minX)*scale)/2-minX*scale;
    oy=(cssHeight-(maxY-minY)*scale)/2-minY*scale;
    draw();
  }
  function zoom(factor,cx=cssWidth/2,cy=cssHeight/2){
    const next=Math.max(.35,Math.min(2.6,scale*factor)),ratio=next/scale;
    ox=cx-(cx-ox)*ratio;oy=cy-(cy-oy)*ratio;scale=next;draw();
  }
  function rounded(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r);}
  function drawGrid(){
    ctx.clearRect(0,0,cssWidth,cssHeight);
    ctx.fillStyle='#0d0f12';ctx.fillRect(0,0,cssWidth,cssHeight);
    if(mode==='overview'){
      const guides=[0.19,0.35,0.51,0.66,0.82];
      ctx.strokeStyle='#30353b';ctx.lineWidth=1;
      for(const at of guides){const x=cssWidth*at;ctx.beginPath();ctx.moveTo(x,70);ctx.lineTo(x,cssHeight-25);ctx.stroke();}
    }
  }
  function edge(a,b,soft){
    const ax=a.x+a.w,ay=a.y+a.h/2,bx=b.x,by=b.y+b.h/2;
    ctx.beginPath();
    let endX,endY;
    if(Math.abs(a.y-b.y)<5&&bx>ax+20){
      ctx.moveTo(ax,ay);ctx.bezierCurveTo(ax+45,ay,bx-45,by,bx,by);endX=bx;endY=by;
    }else if(Math.abs(a.y-b.y)<5&&b.x<a.x){
      const sx=a.x,tx=b.x+b.w;
      ctx.moveTo(sx,ay);ctx.bezierCurveTo(sx-45,ay,tx+45,by,tx,by);endX=tx;endY=by;
    }else{
      const sx=a.x+a.w/2,sy=a.y+a.h,tx=b.x+b.w/2,ty=b.y;
      ctx.moveTo(sx,sy);ctx.bezierCurveTo(sx,sy+35,tx,ty-35,tx,ty);endX=tx;endY=ty;
    }
    ctx.strokeStyle=soft?'#51575c55':(a.active&&b.active)?'#74c7d5cc':'#747e8566';ctx.lineWidth=(a.active&&b.active)?2:1.3;
    ctx.setLineDash([5,5]);ctx.stroke();ctx.setLineDash([]);
    ctx.fillStyle=soft?'#656a6f':(a.active&&b.active)?accent:'#8b9398';ctx.beginPath();ctx.arc(endX,endY,2.3,0,Math.PI*2);ctx.fill();
  }
  function textFit(value,maxWidth){let s=String(value||'');while(ctx.measureText(s).width>maxWidth&&s.length>2)s=s.slice(0,-2)+'…';return s;}
  function nodeCard(n){
    const hot=hovered===n,active=n.active,missing=n.status==='not_executed';
    rounded(n.x,n.y,n.w,n.h,5);ctx.fillStyle=hot?'#242a2e':active?'#1a2226':'#171a1e';ctx.fill();
    ctx.strokeStyle=active?accent:hot?'#d1d6d9':'#51575c';ctx.lineWidth=active||hot?1.8:1;
    if(missing)ctx.setLineDash([5,5]);ctx.stroke();ctx.setLineDash([]);
    if(active){ctx.fillStyle=accent;ctx.fillRect(n.x,n.y,3,n.h);}
    ctx.fillStyle=active?accent:'#a1a1aa';ctx.font='11px ui-monospace,monospace';ctx.fillText(textFit(n.badge,n.w-28),n.x+17,n.y+19);
    ctx.fillStyle=missing?'#777f84':'#f5f5f4';ctx.font='600 16px Inter,system-ui,sans-serif';ctx.fillText(textFit(n.label,n.w-28),n.x+17,n.y+43);
    if(n.sub){ctx.fillStyle='#b7bbc0';ctx.font='12px Inter,system-ui,sans-serif';ctx.fillText(textFit(n.sub,n.w-28),n.x+17,n.y+61);}
  }
  function draw(){
    if(!cssWidth)return;drawGrid();ctx.save();ctx.translate(ox,oy);ctx.scale(scale,scale);
    if(mode==='overview'){
      const xs=[55,316,574,816,1065,1375];
      for(let i=0;i<xs.length;i++){ctx.fillStyle='#a1a1aa';ctx.font='11px ui-monospace,monospace';ctx.fillText((language==='en'?stageNames:stageNamesZh)[['VI','SH','FA','ROUTE','GRAPH','HS'][i]],xs[i],111);}
    }
    for(const e of edges)edge(e.from,e.to,e.soft);
    for(const n of nodes)nodeCard(n);
    ctx.restore();
  }
  function point(event){const r=canvas.getBoundingClientRect();return{x:event.clientX-r.left,y:event.clientY-r.top};}
  function hit(x,y){const wx=(x-ox)/scale,wy=(y-oy)/scale;return [...nodes].reverse().find(n=>wx>=n.x&&wx<=n.x+n.w&&wy>=n.y&&wy<=n.y+n.h)||null;}
  canvas.addEventListener('pointerdown',e=>{canvas.setPointerCapture(e.pointerId);const p=point(e);pointer={x:p.x,y:p.y,lastX:p.x,lastY:p.y,moved:false};});
  canvas.addEventListener('pointermove',e=>{const p=point(e);
    if(pointer){if(Math.hypot(p.x-pointer.x,p.y-pointer.y)>4)pointer.moved=true;if(pointer.moved){ox+=p.x-pointer.lastX;oy+=p.y-pointer.lastY;draw();canvas.classList.add('dragging');}pointer.lastX=p.x;pointer.lastY=p.y;}
    else{const found=hit(p.x,p.y);if(found!==hovered){hovered=found;draw();}canvas.style.cursor=found?'pointer':'grab';}
  });
  canvas.addEventListener('pointerup',e=>{if(!pointer)return;const p=point(e);if(!pointer.moved){const found=hit(p.x,p.y);if(found)hooks.onNode?.(found);}pointer=null;canvas.classList.remove('dragging');});
  canvas.addEventListener('pointercancel',()=>{pointer=null;canvas.classList.remove('dragging');});
  canvas.addEventListener('wheel',e=>{e.preventDefault();const p=point(e);zoom(e.deltaY<0?1.11:1/1.11,p.x,p.y);},{passive:false});
  new ResizeObserver(resize).observe(canvas);
  return {setSample(value){sample=value;mode='overview';layout();},setMode(value){mode=value;layout();},setLanguage(value){language=value==='en'?'en':'zh';if(sample)layout();},fit,zoom};
};
