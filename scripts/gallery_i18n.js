/* Interface translations only. Scientific records, IDs, and source artifacts
 * retain their original language and wording. */
window.FORMA_I18N = (() => {
  const en = {
    'Scientific verification · demo run':'Scientific verification · demo run',
    'RA 前暂定结果':'Provisional result · RA pending',
    '调查流程 / Investigation graph':'Investigation graph',
    '拖动平移 · 滚轮缩放 · 点击节点查看证据':'Drag to pan · scroll to zoom · click a node for evidence',
    '全局图':'Overview','聚焦假设':'Focus on hypothesis','放大':'Zoom in','缩小':'Zoom out',
    '适配':'Fit','全屏':'Fullscreen','退出全屏':'Exit fullscreen',
    '虚线＝调查顺序，不表示严格数据依赖；具体来源见节点产物。青色＝全局图中的 HS 暂定胜出路径，或聚焦图中的当前假设路径；结果待 RA 审查。':'Dashed lines show investigation order, not exact data provenance. Cyan marks the provisional HS winner in overview, or the focused hypothesis path. RA review is pending.',
    '显示路径':'Displayed path','其他节点':'Other nodes',
    '纵轴：完整范围':'Y axis: full range','纵轴：细节对比':'Y axis: detail view',
    '光谱纵轴范围':'Spectrum Y axis range','所选节点对应的观测光谱':'Observed spectrum for the selected node',
    '观测证据和所选节点':'Observed evidence and selected node','交互式推理图':'Interactive investigation graph',
    '03 / 节点输出':'03 / Node outputs','图中节点与下方卡片均可打开结构化输出':'Select a graph node or card to inspect its output',
    '搜索节点、feature ID、谱线或判定…':'Search nodes, feature IDs, lines, or decisions…',
    '搜索节点':'Search nodes','假设筛选':'Hypothesis filter','全部假设':'All hypotheses',
    '显示更多节点':'Show more nodes','节点详情':'Node details',
    '冻结测量':'Frozen measurements','SH 线审':'SH line review','FA 独立投票':'FA independent voting',
    '代码路由':'Code routing','类型图':'Type graph','HS 合并与比较':'HS merge and comparison',
    '全部节点':'All nodes','显式弃权':'Explicit abstention','弃权':'Abstained',
    '无存活组':'No surviving group','无胜出组':'No winner group',
    '锚红移 z':'Anchor redshift z','专家 VI':'Expert VI','存活假设':'Surviving hypotheses',
    '本次运行没有给出比较理由。':'No comparison reason was recorded in this run.',
    '查看 VI 特征图 ↗':'View VI feature plot ↗',
    'FA 同一 feature 的独立票合为一张卡；每张卡仍可打开原始票据。':'Independent FA votes for the same feature appear on one card; each original ballot remains accessible.',
    '卡片展示本次运行的记录，不代表最终分类或准确率估计。':'Cards show this run’s records, not final classification or an accuracy estimate.',
    '个节点 · 已显示':'nodes · showing','展开 ↗':'Inspect ↗',
    '没有匹配的节点。试试清除搜索或筛选。':'No matching nodes. Clear the search or filters.',
    '选择图中的节点':'Select a node in the graph',
    '这里显示节点判断、观测位置与原始证据入口。':'The node decision, observed location, and source artifacts will appear here.',
    '查看证据与完整字段 ↗':'Inspect evidence and full fields ↗',
    '该测量位置有连贯信号':'Coherent signal at this measured position',
    '候选特征未通过真实性投票':'Candidate feature did not pass the reality vote',
    '双线获得支持':'Doublet supported','双线未获支持':'Doublet not supported',
    '调查入口：':'Investigation entry: ','入口未决':'Entry unresolved',
    '已记录类型图检查':'Type graph check recorded','已记录比较结果':'Comparison result recorded',
    '已记录':'Recorded','比较依据':'Comparison basis',
    '独立投票':'Independent votes','票支持信号存在':'votes support signal presence',
    '赞成':'Yes','反对':'No','条谱线审查':'predicted lines reviewed',
    '票支持':'votes support','候选 feature':'candidate feature',
    '本次证据 / 原始产物':'Evidence / source artifacts',
    '完整结构化字段 · 展开':'Full structured fields · expand','节点输出':'Node output',
    '字段来自本次运行产物；长篇会话和摘要校验请查看原始记录。':'Fields come from this run. See source artifacts for full sessions and checksums.',
    '查看节点产物':'Inspect node artifact','展开查看该节点的观测与判断':'Inspect this node’s observations and decision','另有':'More: ',
    '项，见原始产物':'items; see source artifact',
    '此节点没有排队项或冲突项。':'No queued items or conflicts in this node.',
    '节点产物':'Node artifact','全谱图':'Full spectrum plot','特征图':'Feature plot',
    '谱线表':'Line table','线审判读':'Line review judgments','采纳谱线图':'Adopted lines plot',
    '报告':'Report','分析报告':'Analysis report',
    '冻结光谱测量':'Frozen spectrum measurements','谱线审查':'Line review',
    '特征真实性':'Feature reality','双线审查':'Doublet review','Lyα forest 审查':'Lyα forest review',
    '类型入口':'Type entry','类型图起点':'Type graph entry','谱线对齐':'Line alignment',
    '类型分析报告':'Type analysis report','清洗后的谱线':'Cleaned lines',
    '类型图出口':'Type graph exit','宽线清单':'Broad-line inventory',
    '缺线复核队列':'Missing-line review queue','Type 1 形式门':'Type 1 formal gate',
    '假设合并':'Hypothesis merge','跨组比较':'Cross-group comparison',
    '固定红移下的 ID 绑定线表':'ID-bound line table at fixed redshift',
    '独立投票 · 同一测量合并展示':'Independent votes · grouped by measurement',
    '代码依次检查诊断证据':'Code checks diagnostic evidence in order',
    '初始入口及固定假设红移':'Initial entry and fixed hypothesis redshift',
    '同一假设内部处理线对冲突':'Resolve line-pair conflicts within one hypothesis',
    '同类型组合并':'Merge groups of the same type','候选组间证据横评':'Compare evidence across candidate groups',
    '假设红移':'Hypothesis redshift','审查谱线':'Reviewed lines','状态分布':'Status counts',
    '采纳或待定的线对':'Adopted or pending line pairs','中心波长 Å':'Center wavelength Å',
    '信号类型':'Signal kind','独立票数':'Independent votes','票决':'Vote result',
    '单票':'Individual ballots',
    'complete':'Complete','recorded':'Recorded','signal_present':'Signal present',
    'signal_absent':'Signal absent','not_executed':'Not executed','not_survived':'Not survived',
    'survive':'Survived','undecided':'Undecided','provisional_selection':'Provisional selection',
    'true':'Yes','false':'No',
  };
  const zh = {'complete':'已完成','recorded':'已记录','signal_present':'信号存在',
    'signal_absent':'信号不存在','not_executed':'未执行','not_survived':'未存活',
    'survive':'存活','undecided':'未决','provisional_selection':'暂定胜出'};
  const titleParts = Object.keys(en).filter(key => /[\u3400-\u9fff]/.test(key)).sort((a,b)=>b.length-a.length);
  function text(value, lang) {const raw=String(value??'—');return (lang==='en'?en:zh)[raw]||raw;}
  function generated(value, lang) {
    const raw=String(value??'—');if(lang!=='en')return text(raw,lang);
    if(en[raw])return en[raw];
    // Only generated presentation labels are passed here, never model prose.
    let out=raw;
    for(const part of titleParts)if(out.includes(part))out=out.replaceAll(part,en[part]);
    return out;
  }
  function link(value, lang) {
    const raw=String(value);
    const ballot=raw.match(/^第 (\d+) 票$/);
    return lang==='en'&&ballot?`Ballot ${ballot[1]}`:text(raw,lang);
  }
  return {text,generated,link};
})();
