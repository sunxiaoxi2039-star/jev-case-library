#!/usr/bin/env python3
# 生成 JEV 202 案例精选面板（单文件、暗调、静态渲染全量 + 精选两层）
import json, html
from pathlib import Path

BASE = Path(__file__).resolve().parent

data = json.load(open('/tmp/jev-classified.json'))
cases, CATS = data['cases'], data['cats']
CAT_ORDER = ['intro','router','coding','browser','game','trading','guard','growth','data','maker','robot','hack','eco']
byn = {c['n']: c for c in cases}

def esc(s): return html.escape(s or '')
def fmtv(v):
    return f"{v/10000:.1f}万" if v >= 10000 else str(v)

def card(c):
    badges = ''
    if c['video']: badges += '<span class="badge video">🎬 视频</span>'
    if c['top']: badges += '<span class="badge top">🔥 全网热帖</span>'
    if c['caution']: badges += '<span class="badge caution">⚠️ 冷静剂</span>'
    if c['lang'] == 'zh': badges += '<span class="badge zh">中文</span>'
    why = f'<p class="why">{esc(c["why"])}</p>' if c['why'] else ''
    return f'''<div class="card{' top-card' if c['top'] else ''}">
  <div class="card-head">
    <span class="idx">#{c['n']:03d}</span>
    <a class="author" href="{c['profile']}" target="_blank" rel="noopener">{esc(c['author'])}<small>{esc(c['handle'])}</small></a>
    <span class="metrics">{fmtv(c['vn'])} 浏览 · {fmtv(c['ln'])} 赞 · {esc(c['saves'])} 藏</span>
  </div>
  <p class="text">{esc(c['text'][:260])}{'…' if len(c['text'])>260 else ''}</p>
  {why}
  <div class="card-foot">{badges}<a class="srclink" href="{c['tweet']}" target="_blank" rel="noopener">原帖 ↗</a></div>
</div>'''

def row(c):
    b = '🎬' if c['video'] else ''
    z = '🇨🇳' if c['lang']=='zh' else ''
    return f'''<a class="row" href="{c['tweet']}" target="_blank" rel="noopener"><span class="r-idx">#{c['n']:03d}</span><span class="r-text">{esc((c['text'] or '')[:90])}</span><span class="r-meta">{b}{z} {fmtv(c['vn'])}浏览</span></a>'''

sections = []
for key in CAT_ORDER:
    name, desc, icon = CATS[key]
    cs = [c for c in cases if c['cat'] == key]
    feat = [c for c in cs if c['featured']]
    rest = [c for c in cs if not c['featured']]
    views = sum(c['vn'] for c in cs)
    sections.append(f'''<section class="cat" id="cat-{key}">
  <h2>{icon} {name}<span class="cat-stat">{len(cs)} 条 · 合计 {fmtv(views)} 浏览</span></h2>
  <p class="cat-desc">{desc}</p>
  <div class="cards">{''.join(card(c) for c in feat)}</div>
  {f'<details class="rest"><summary>其余 {len(rest)} 条全部在此（点开逐条看，都可跳原帖）</summary><div class="rows">{"".join(row(c) for c in rest)}</div></details>' if rest else ''}
</section>''')

nav = ''.join(f'<a href="#cat-{k}">{CATS[k][2]} {CATS[k][0]}</a>' for k in CAT_ORDER)

# 翻车专区
caution_cards = ''.join(card(byn[n]) for n in [18, 80, 106, 194, 72])

total_views = sum(c['vn'] for c in cases)
feat_count = sum(1 for c in cases if c['featured'])

html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JEV 202 条案例 · 分类精选库</title>
<style>
:root{{--bg:#0b0b10;--bg2:#12121a;--card:#16161f;--line:#262633;--txt:#e8e4da;--dim:#9a94a8;--gold:#d4a94e;--gold2:#f0c96e;--red:#e0604e;--green:#5fb878;}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--txt);font-family:-apple-system,"PingFang SC","Hiragino Sans GB",sans-serif;line-height:1.7}}
.wrap{{max-width:1060px;margin:0 auto;padding:0 22px}}
header{{padding:90px 0 50px;text-align:center;background:radial-gradient(ellipse 80% 60% at 50% -10%,#2a2140 0%,transparent 70%)}}
h1{{font-family:Georgia,"Songti SC",serif;font-size:44px;font-weight:700;letter-spacing:2px;background:linear-gradient(135deg,#f5e3b3,#d4a94e 60%,#a37c2e);-webkit-background-clip:text;background-clip:text;color:transparent}}
.sub{{color:var(--dim);margin-top:14px;font-size:15px}}
.stats{{display:flex;justify-content:center;gap:36px;margin-top:34px;flex-wrap:wrap}}
.stat b{{font-size:30px;color:var(--gold2);font-family:Georgia,serif}}
.stat span{{display:block;color:var(--dim);font-size:12px;margin-top:2px}}
.answer{{background:linear-gradient(180deg,#171322,#12121a);border:1px solid #33284d;border-radius:16px;padding:34px 38px;margin:46px 0}}
.answer h2{{font-family:Georgia,"Songti SC",serif;color:var(--gold2);font-size:24px;margin-bottom:14px}}
.answer p{{color:#cfc9bd;font-size:15.5px;margin:10px 0}}
.answer p b{{color:var(--gold2)}}
.answer .three{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:18px}}
.answer .cell{{background:#0e0d16;border:1px solid var(--line);border-radius:12px;padding:16px 18px;font-size:14px;color:#bdb6ab}}
.answer .cell b{{display:block;color:var(--txt);margin-bottom:6px;font-size:15px}}
nav{{position:sticky;top:0;z-index:9;background:rgba(11,11,16,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding:12px 0;margin:20px 0 0}}
nav .wrap{{display:flex;gap:6px;flex-wrap:wrap}}
nav a{{color:var(--dim);text-decoration:none;font-size:12.5px;padding:5px 11px;border-radius:20px;border:1px solid transparent;white-space:nowrap}}
nav a:hover{{color:var(--gold2);border-color:#3d3452}}
section.cat{{padding:44px 0 10px;border-top:1px solid var(--line)}}
h2{{font-family:Georgia,"Songti SC",serif;font-size:26px;color:var(--txt);letter-spacing:1px}}
.cat-stat{{font-size:13px;color:var(--dim);font-family:-apple-system,sans-serif;margin-left:14px;font-weight:400}}
.cat-desc{{color:var(--dim);font-size:14px;margin:6px 0 22px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;display:flex;flex-direction:column;transition:border-color .2s}}
.card:hover{{border-color:#4a3f66}}
.top-card{{border-color:#5a4a2a;background:linear-gradient(180deg,#1c1812,#16161f)}}
.card-head{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}}
.idx{{color:var(--gold);font-family:Georgia,serif;font-size:13px}}
.author{{color:var(--txt);text-decoration:none;font-weight:600;font-size:14.5px}}
.author small{{color:var(--dim);font-weight:400;margin-left:6px}}
.author:hover{{color:var(--gold2)}}
.metrics{{margin-left:auto;color:var(--dim);font-size:12px}}
.text{{color:#c8c2b6;font-size:13.5px;margin:10px 0 0;flex:1}}
.why{{color:var(--gold2);font-size:13px;margin-top:10px;padding:8px 12px;background:rgba(212,169,78,.07);border-left:2px solid var(--gold);border-radius:0 8px 8px 0}}
.card-foot{{display:flex;align-items:center;gap:8px;margin-top:12px;flex-wrap:wrap}}
.badge{{font-size:11px;padding:2px 9px;border-radius:12px;background:#232233;color:#b9b3c6}}
.badge.video{{background:#1e2b22;color:#7fce9a}}
.badge.top{{background:#3a2a16;color:#f0b56e}}
.badge.caution{{background:#3a1e1a;color:#f0937f}}
.badge.zh{{background:#1a2a3a;color:#7fb8f0}}
.srclink{{margin-left:auto;color:var(--gold);font-size:12.5px;text-decoration:none}}
.srclink:hover{{color:var(--gold2);text-decoration:underline}}
details.rest{{margin-top:14px}}
details.rest summary{{cursor:pointer;color:var(--dim);font-size:13.5px;padding:10px 4px;list-style:none}}
details.rest summary::before{{content:"▸ ";color:var(--gold)}}
details.rest[open] summary::before{{content:"▾ "}}
.rows{{border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.row{{display:flex;gap:12px;padding:9px 16px;color:#b5af a3;text-decoration:none;font-size:13px;border-bottom:1px solid #1c1c26;align-items:baseline}}
.row{{color:#b5afa3}}
.row:last-child{{border-bottom:none}}
.row:hover{{background:#1a1a26}}
.r-idx{{color:var(--gold);font-family:Georgia,serif;font-size:11.5px;flex-shrink:0}}
.r-text{{flex:1;color:#b5afa3}}
.r-meta{{color:var(--dim);font-size:11.5px;flex-shrink:0}}
.caution-sec{{background:linear-gradient(180deg,#1d1210,#12121a);border:1px solid #4a2620;border-radius:16px;padding:30px 34px;margin:46px 0}}
.caution-sec h2{{color:#f0937f}}
.caution-sec .tip{{color:#c9a89f;font-size:14px;margin:8px 0 20px}}
.homework{{background:linear-gradient(180deg,#101d16,#12121a);border:1px solid #204a30;border-radius:16px;padding:30px 34px;margin:46px 0}}
.homework h2{{color:#7fce9a}}
.hw{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin-top:18px}}
.hw .cell{{background:#0d1510;border:1px solid #1e3325;border-radius:12px;padding:16px 18px;font-size:13.5px;color:#b3c4b6}}
.hw .cell b{{display:block;color:#a8e0ba;margin-bottom:6px;font-size:14.5px}}
.hw .cell a{{color:var(--gold)}}
footer{{text-align:center;color:var(--dim);font-size:12.5px;padding:50px 0 60px;border-top:1px solid var(--line);margin-top:40px}}
footer a{{color:var(--gold)}}
@media(max-width:640px){{h1{{font-size:30px}}.stats{{gap:20px}}}}
</style></head><body>
<header><div class="wrap">
<h1>JEV 正在被用来做什么</h1>
<p class="sub">X 平台 202 条真实案例 · 全量分类 + {feat_count} 条精选点评 · 数据来自向明的开源案例库（2026-09-21 抓取）</p>
<div class="stats">
<div class="stat"><b>202</b><span>实操案例</span></div>
<div class="stat"><b>13</b><span>分类</span></div>
<div class="stat"><b>{feat_count}</b><span>精选带点评</span></div>
<div class="stat"><b>{fmtv(total_views)}</b><span>案例合计浏览</span></div>
<div class="stat"><b>9</b><span>语言（中文 9 条）</span></div>
</div></div></header>

<div class="wrap"><div class="answer">
<h2>先答你的问题：有了钥匙，为啥一定要通过 Claude Code？——不必须。</h2>
<p>Jev 本身就是一个 <b>HTTP API</b>：发一个请求、它回一个判断。谁都能直接调，curl 一行命令就行，跟 Claude Code 没有绑定关系。这 202 条案例里<b>几乎没有一条是通过 Claude Code 用的</b>——全是直接调 API 做自己的东西。</p>
<p>很多人第一个接的是 Claude Code：现成的 fast-jev-compaction 插件不用自己写代码、/compact 是天天在用的真功能、出了问题一键回滚。这是最小赌注的入门路径，不是唯一的门。</p>
<div class="three">
<div class="cell"><b>① 拿到钥匙后</b>命令行、Python 脚本、自动化流程……想插哪插哪，API 不挑家。</div>
<div class="cell"><b>② 等不及审批</b>OpenRouter 已上线 Jev beta（案例 #158），还有三个开源复刻版（#159/#17/#34）现在就能玩。</div>
<div class="cell"><b>③ 连账号都不想注册</b>Easy-Jev、Ask Jev anything 等公开 demo 网页（#168/#56/#142），点开就摸。</div>
</div></div></div>

<nav><div class="wrap">{nav}</div></nav>

<main class="wrap">
{''.join(sections)}

<div class="caution-sec" id="caution">
<h2>⚠️ 冷静剂专区：不全是捷报</h2>
<p class="tip">发布才几天，案例库九成是兴奋期演示。这几条是稀缺的反面信息，比 100 条炫技更有决策价值。</p>
<div class="cards">{caution_cards}</div>
</div>

<div class="homework" id="homework">
<h2>🎯 你可以马上抄的作业（按业务场景配对）</h2>
<div class="hw">
<div class="cell"><b>资讯聚合/雷达 → 信源打分/事件聚类</b>抄 #66（1018 篇论文分类 8 美分）和 #8（428 条新闻 28 秒给 15 个品牌配热点）。Jev 天生干「海量条目快速打标签」。</div>
<div class="cell"><b>多 agent / skill 体系 → 调度员</b>抄 #93（90 个 skill 自动选）和 #164（Claude Code/Codex/opencode 之间路由任务）——和「模型路由」同一个思路，Jev 可以当那个「判断层」。</div>
<div class="cell"><b>内容生产 → 爆款拆解流水线</b>抄 #170（40 秒拆 724 条广告的钩子/CTA）和 #101（每条帖子 61 问 1 秒打完）。竞品拆解的体力活全可外包给它。</div>
<div class="cell"><b>钥匙还没下来 → 先摸手感</b>OpenRouter beta（#158）或用开源复刻（#159），不花审批时间。</div>
</div></div>
</main>

<footer><div class="wrap">
数据来源：<a href="https://render.qmuse.pub/p/muse/8079593307628562/index.html" target="_blank" rel="noopener">向明 · JEV 案例库</a>（非官方，与 TypeSafe 无隶属）· 源码 <a href="https://github.com/Hiwoniu/Jev-Case" target="_blank" rel="noopener">GitHub Hiwoniu/Jev-Case</a><br>
整理：社区整理版 · 2026-09-21 · 案例浏览数合计 {fmtv(total_views)}（原页标称 1 亿+ 含外链引用流量，统计有滞后）· 每条「原帖」直链 X 原帖
</div></footer>
</body></html>'''

(BASE / 'JEV-202案例精选.html').write_text(html_doc)
# 原始数据留档
json.dump(cases, open(BASE / 'jev-202-案例数据.json','w'), ensure_ascii=False, indent=1)
print('written', len(html_doc)//1024, 'KB')
