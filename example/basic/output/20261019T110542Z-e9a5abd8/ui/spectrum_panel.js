/* Read-only spectrum view. Coordinates come only from frozen measurement IDs
 * or explicit center wavelengths in the selected node artifact. */
window.createSpectrumPanel = function createSpectrumPanel(canvas, caption) {
  const ctx = canvas.getContext('2d');
  let sample = null, node = null, scaleMode = 'full', language = 'zh';
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  function markers() {
    if (!node) return [];
    const output = node.output || {};
    const positions = sample?.spectrum_data?.feature_positions || {};
    const found = [];
    function add(id, wavelength) {
      const x = finite(wavelength) ? wavelength : positions[id];
      if (finite(x) && !found.some(item => item.id === id && Math.abs(item.x - x) < 0.01)) {
        found.push({id: id || 'center', x});
      }
    }
    if (output['feature ID']) add(output['feature ID'], output['中心波长 Å']);
    for (const pair of output['采纳或待定的线对'] || []) {
      if (pair.feature) add(pair.feature);
    }
    // A measured feature ID has an observed coordinate. A predicted wavelength
    // alone is deliberately not shown as a measured signal.
    function visit(value, depth) {
      if (!value || typeof value !== 'object' || depth > 3 || found.length >= 16) return;
      if (value.measurement_id && positions[value.measurement_id]) add(value.measurement_id);
      for (const child of Object.values(value)) if (child && typeof child === 'object') visit(child, depth + 1);
    }
    if (node.stage === 'GRAPH') visit(output, 0);
    return found.slice(0, 16);
  }
  function draw() {
    const rect = canvas.getBoundingClientRect(), dpr = Math.min(devicePixelRatio || 1, 2);
    if (!rect.width || !rect.height) return;
    canvas.width = Math.round(rect.width * dpr); canvas.height = Math.round(rect.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = rect.width, h = rect.height;
    ctx.fillStyle = '#111317'; ctx.fillRect(0, 0, w, h);
    const spec = sample?.spectrum_data || {}, x = spec.wavelength || [], y = spec.flux || [];
    if (!x.length || x.length !== y.length) {caption.textContent = language==='en'?'No spectrum arrays are available for this sample.':'该样本没有可绘制的光谱数组。'; return;}
    const marks = markers();
    let lo = x[0], hi = x[x.length - 1];
    if (marks.length === 1) {lo = Math.max(lo, marks[0].x - 150); hi = Math.min(hi, marks[0].x + 150);}
    else if (marks.length > 1 && Math.max(...marks.map(m => m.x)) - Math.min(...marks.map(m => m.x)) < 850) {
      lo = Math.max(lo, Math.min(...marks.map(m => m.x)) - 80);
      hi = Math.min(hi, Math.max(...marks.map(m => m.x)) + 80);
    }
    const left = 61, right = 11, top = 15, bottom = 31, pw = w - left - right, ph = h - top - bottom;
    const xx = value => left + (value - lo) / (hi - lo) * pw;
    const indices = [];
    for (let i = 0; i < x.length; i++) if (x[i] >= lo && x[i] <= hi && finite(y[i]) && spec.valid?.[i] !== false) indices.push(i);
    if (!indices.length) {caption.textContent = language==='en'?'No valid samples in this wavelength range.':'所选波段没有有效采样。'; return;}
    const visible = indices.map(i => y[i]);
    const continuum = spec.continuum || [];
    if (scaleMode === 'full' && continuum.length === x.length) {
      for (const i of indices) if (finite(continuum[i])) visible.push(continuum[i]);
    }
    let low, high;
    if (scaleMode === 'detail') {
      const ordered = visible.sort((a,b) => a-b);
      low = ordered[Math.floor((ordered.length-1)*.02)];
      high = ordered[Math.floor((ordered.length-1)*.98)];
    } else {
      low = Math.min(...visible); high = Math.max(...visible);
    }
    const span = Math.max(high-low, .2), margin = span*.07;
    const ymin = low-margin, ymax=high+margin;
    const yy = value => top + ph - (value-ymin)/(ymax-ymin)*ph;
    ctx.strokeStyle = '#343a40'; ctx.lineWidth = 1; ctx.beginPath();
    for (let j=0;j<=3;j++){const py=top+j*ph/3;ctx.moveTo(left,py);ctx.lineTo(w-right,py);}
    ctx.stroke();
    ctx.font='10px ui-monospace,monospace';ctx.fillStyle='#a1a1aa';
    const tick = value => Math.abs(value)>=10?value.toFixed(1):value.toFixed(2);
    ctx.fillText(tick(ymax),4,top+8);ctx.fillText(tick(ymin),4,top+ph);
    ctx.fillText(lo.toFixed(0)+' Å',left,h-7);ctx.textAlign='right';ctx.fillText(hi.toFixed(0)+' Å',w-right,h-7);ctx.textAlign='left';
    function trace(values,color,width) {
      if (!values || values.length !== x.length) return;
      ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();let started=false;
      for(let i=0;i<x.length;i++){const v=values[i];
        if(x[i]<lo||x[i]>hi||spec.valid?.[i]===false||!finite(v)){started=false;continue;}
        if(!started){ctx.moveTo(xx(x[i]),yy(v));started=true;}else ctx.lineTo(xx(x[i]),yy(v));
      }ctx.stroke();
    }
    ctx.save();ctx.beginPath();ctx.rect(left,top,pw,ph);ctx.clip();
    trace(y,'#d1d6d9',1.05);
    trace(spec.continuum,'#8b9ca3',1);
    ctx.restore();
    marks.forEach((m,i)=>{if(m.x<lo||m.x>hi)return;const px=xx(m.x);
      ctx.strokeStyle='#74c7d5';ctx.setLineDash([4,4]);ctx.beginPath();ctx.moveTo(px,top);ctx.lineTo(px,top+ph);ctx.stroke();ctx.setLineDash([]);
      ctx.fillStyle='#74c7d5';ctx.font='10px ui-monospace,monospace';
      ctx.fillText(m.id.length>18?m.id.slice(0,16)+'…':m.id,Math.min(px+4,w-130),top+11+(i%3)*12);
    });
    const scaleNote = language==='en'
      ? (scaleMode === 'full' ? 'Y axis includes all valid samples in view' : 'Detail view uses the 2–98% range; extremes may be clipped')
      : (scaleMode === 'full' ? '纵轴覆盖当前波段全部有效采样' : '细节对比采用 2–98% 范围，极值可能裁切');
    caption.textContent = language==='en'
      ? (marks.length ? `${marks.length} recorded measurement positions · white: observed flux · gray: VI continuum · ${scaleNote}` : `Full spectrum · selected node has no locatable measurement ID · ${scaleNote}`)
      : (marks.length ? `${marks.length} 个已记录测量位置 · 实线为观测通量，灰线为 VI continuum · ${scaleNote}` : `全谱观察 · 当前节点未提供可定位的观测测量 ID · ${scaleNote}`);
  }
  new ResizeObserver(draw).observe(canvas);
  return {setSample(value){sample=value;node=null;draw();},setNode(value){node=value;draw();},setScale(value){scaleMode=value==='detail'?'detail':'full';draw();},setLanguage(value){language=value==='en'?'en':'zh';draw();}};
};
