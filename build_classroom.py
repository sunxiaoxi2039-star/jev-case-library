#!/usr/bin/env python3
# JEV 课堂面板：13 节课 · 缩略图墙 · 学习进度 · 练手作业
import json, html
from pathlib import Path

BASE = Path(__file__).resolve().parent

D = json.load(open('/tmp/jev-classified.json'))
cases, CATS = D['cases'], D['cats']
by = {c['n']: c for c in cases}
CAT_ORDER = ['intro','router','coding','browser','game','trading','guard','growth','data','maker','robot','hack','eco']

# 每节课的主打案例（谁发片率高、内容最能讲清这一类）
FEATURE = {
 'intro':   (108, 156, '先搞清它到底是个啥：看创始人自己怎么定义它，再看两条 45 秒科普。'),
 'router':  (199, 93,  '它最常见的活：当调度员。看 Slack agent 怎么被它提速一倍，再看 90 个 skill 怎么自动选对。'),
 'coding':   (74, 69,  '程序员的活：PR 评审便宜 200 倍、给代码质量打分——Jev 评审 MCP 就是这类。'),
 'browser': (186, 26,  '亲手点：「Jev Use」对比视频（就是它把 Codex 变快）+ 7 秒找航班。这是最容易亲眼看到效果的一类。'),
 'game':    (67, 71,  '上手门槛最低：看中文博主杀戮尖塔代打，再看一小时重建特斯拉 FSD。'),
 'trading': (104, 14,  '真金实银：看 104 万人围观的买卖机器人，再看中文解读「为啥交易只需要判断」。'),
 'guard':   (3, 15,   '防骗工具：给 X 帖子自动标注「诱导/挑拨/推销」，自动跳过 YouTube 广告。'),
 'growth':  (170, 128,'营销增长线的活：40 秒拆 724 条广告 + 19 秒分类完竞品 1891 条广告，只要 12 美分。'),
 'data':    (66, 11,  '批量打标签：1018 篇论文 8 美分、3000 款零食 28 秒。信源打分、商品打标这类活就这么干。'),
 'maker':   (197, 94, '办公搭档：预测式表格、演讲自动翻页——「谁都能当乔布斯」。'),
 'robot':   (201, 62, '硬件世界：机械臂自己想到用钩子够方块；一句话下目标的机器人任务。'),
 'hack':    (195, 80, '边界测试：它真的不会写字？让它画画、玩电车难题，看极限在哪。'),
 'eco':     (158, 159,'退路：不等审批怎么玩（OpenRouter beta）、开源复刻版现在就能调。'),
}
def feat_pair(key):
    a, b = FEATURE[key][0], FEATURE[key][1]
    return by[a], by[b]

def esc(s): return html.escape(s or '')
def fmtv(v): return f"{v/10000:.1f}万" if v >= 10000 else str(v)

# 进度存 localStorage；卡片=缩略图网格
def thumb_cell(c):
    return f'''<div class="cell" onclick="mark({c['n']})" id="cell{c['n']}">
<a class="poster" href="videos/{c['n']:03d}.mp4" target="_blank"><img src="thumbs/{c['n']:03d}.jpg" loading="lazy" alt=""><span class="play">▶</span></a>
<a class="meta" href="{c['tweet']}" target="_blank" rel="noopener">
  <b>{esc(c['author'])}</b><small>{esc(c['handle'])} · {fmtv(c['vn'])}人看过</small>
  <p>{esc(c['text'][:92])}{'…' if len(c['text'])>92 else ''}</p>
</a>
<span class="done" id="done{c['n']}" title="点击标记已学">✓</span>
</div>'''

sections = []
for key in CAT_ORDER:
    name, desc, icon = CATS[key]
    a, b = feat_pair(key)
    lesson, why = FEATURE[key][2], FEATURE[key][3] if len(FEATURE[key])>3 else ''
    cs = [c for c in cases if c['cat'] == key]
    views = sum(c['vn'] for c in cs)
    sections.append(f'''<section class="lesson" id="L-{key}">
<header class="l-head" onclick="toggle('{key}')">
  <span class="l-no">{CAT_ORDER.index(key)+1:02d}</span>
  <h2>{icon} {name}</h2>
  <span class="l-stat">{len(cs)} 案例 · {fmtv(views)} 浏览</span>
  <span class="l-arrow" id="ar-{key}">▾</span>
</header>
<p class="l-desc">{desc}——{lesson}</p>
<div class="l-body" id="bd-{key}">
  <div class="duo">
    <div class="pick"><a href="videos/{a['n']:03d}.mp4" target="_blank"><img src="thumbs/{a['n']:03d}.jpg"><span class="play big">▶ 先看这条</span></a><b>{esc(a['author'])}</b><small>{esc(a['handle'])} · {fmtv(a['vn'])}人看过</small><p>{esc(a['text'][:110])}</p></div>
    <div class="pick"><a href="videos/{b['n']:03d}.mp4" target="_blank"><img src="thumbs/{b['n']:03d}.jpg"><span class="play big">▶ 再看这条</span></a><b>{esc(b['author'])}</b><small>{esc(b['handle'])} · {fmtv(b['vn'])}人看过</small><p>{esc(b['text'][:110])}</p></div>
  </div>
  <details class="more"><summary>本类还有 {len(cs)-2} 条（点开墙）</summary><div class="grid">{''.join(thumb_cell(c) for c in cs)}</div></details>
</div>
</section>''')

html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JEV 课堂 · 13 节课学会裁判</title>
<style>
:root{{--bg:#0b0b10;--card:#16161f;--line:#262633;--txt:#e8e4da;--dim:#9a94a8;--gold:#d4a94e;--gold2:#f0c96e;--green:#5fb878;--red:#e0604e;}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--txt);font-family:-apple-system,"PingFang SC",sans-serif;line-height:1.7;background:radial-gradient(ellipse 90% 55% at 50% -15%,rgba(46,36,74,.55) 0%,transparent 70%),var(--bg)}}
.wrap{{max-width:1150px;margin:0 auto;padding:56px 22px 90px}}
h1{{font-family:Georgia,"Songti SC",serif;font-size:40px;letter-spacing:2px;text-align:center;background:linear-gradient(135deg,#f5e3b3,#d4a94e 60%,#a37c2e);-webkit-background-clip:text;background-clip:text;color:transparent}}
.sub{{text-align:center;color:var(--dim);font-size:14px;margin-top:10px}}
.howto{{background:linear-gradient(180deg,#171322,#12121a);border:1px solid #33284d;border-radius:16px;padding:26px 30px;margin:38px 0}}
.howto b{{color:var(--gold2)}}
.howto p{{color:#cfc9bd;font-size:14.5px;margin:8px 0}}
.progress{{position:sticky;top:0;z-index:8;background:rgba(11,11,16,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:12px 0;margin:26px 0}}
.p-in{{display:flex;align-items:center;gap:14px}}
.p-bar{{flex:1;height:10px;background:#232233;border-radius:5px;overflow:hidden}}
.p-bar i{{display:block;height:100%;width:0;background:linear-gradient(90deg,#5fb878,#d4a94e);transition:width .4s}}
.p-text{{color:var(--dim);font-size:13px;white-space:nowrap}}
.lesson{{border:1px solid var(--line);border-radius:16px;background:var(--card);margin-bottom:18px;overflow:hidden}}
.l-head{{display:flex;align-items:center;gap:14px;padding:20px 24px;cursor:pointer;user-select:none}}
.l-no{{font-family:Georgia,serif;color:var(--gold);font-size:15px;border:1px solid #3a3050;border-radius:8px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.l-head h2{{font-family:Georgia,"Songti SC",serif;font-size:21px;letter-spacing:1px}}
.l-stat{{margin-left:auto;color:var(--dim);font-size:12.5px}}
.l-arrow{{color:var(--gold);transition:transform .2s}}
.l-arrow.closed{{transform:rotate(-90deg)}}
.l-desc{{padding:0 24px 16px;color:var(--dim);font-size:13.5px;border-bottom:1px dashed #232233}}
.l-body{{padding:20px 24px}}
.duo{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
.pick{{background:#0e0d16;border:1px solid var(--line);border-radius:12px;padding:14px;position:relative}}
.pick img{{width:100%;border-radius:8px;display:block;aspect-ratio:16/9;object-fit:cover}}
.pick b{{display:block;margin-top:10px;font-size:14.5px}}
.pick small{{color:var(--dim)}}
.pick p{{color:#bdb6ab;font-size:13px;margin-top:6px}}
a.poster{{position:relative;display:block}}
.play{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;background:rgba(0,0,0,.25);opacity:0;transition:.2s;border-radius:8px}}
.play.big{{font-size:15px;background:rgba(0,0,0,.45);opacity:1;font-weight:600;letter-spacing:1px}}
a:hover .play{{opacity:1}}
details.more summary{{cursor:pointer;color:var(--dim);font-size:13.5px;padding:10px 2px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:14px;margin-top:12px}}
.cell{{background:#0e0d16;border:1px solid var(--line);border-radius:10px;overflow:hidden;position:relative;cursor:pointer;transition:border-color .2s}}
.cell:hover{{border-color:#4a3f66}}
.cell img{{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}}
.cell .meta{{display:block;padding:10px 12px;text-decoration:none;color:var(--txt)}}
.cell b{{font-size:13px}}
.cell small{{color:var(--dim);display:block;font-size:11.5px;margin-top:2px}}
.cell p{{color:#b5afa3;font-size:12px;margin-top:6px;line-height:1.5}}
.done{{position:absolute;top:8px;right:8px;width:26px;height:26px;border-radius:50%;background:rgba(0,0,0,.5);border:1px solid #4a3f66;color:#4a3f66;font-size:14px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.2s}}
.done.on{{background:var(--green);border-color:var(--green);color:#0b0b10}}
footer{{text-align:center;color:var(--dim);font-size:12.5px;margin-top:44px;padding-top:26px;border-top:1px solid var(--line)}}
@media(max-width:720px){{.duo{{grid-template-columns:1fr}}h1{{font-size:28px}}}}
.quickstart{{margin:14px 0;padding:12px 16px;border:1px solid #2a2f42;border-left:3px solid #c9a86a;border-radius:8px;background:#141824;font-size:13.5px;line-height:1.9}}
.quickstart code{{background:rgba(255,255,255,.07);padding:1px 6px;border-radius:4px;font-size:12px}}
.quickstart a{{color:#c9a86a}}
</style></head><body><div class="wrap">
<h1>JEV 课堂</h1>
<p class="sub">13 节课，一节课一类用法 · 每条案例本地视频+缩略图 · 点开即看，看完点 ✓ 记进度</p>
<div class="howto">
<p><b>怎么用这个课堂：</b>从上往下，一节课一节课来。每节课先看「▶ 先看这条」视频（本地视频直接放，不用登录），再扫一眼「▶ 再看这条」，然后去「<b>Jev 裁判台</b>」网页把那一招亲手玩一遍。</p>
<p><b>练手作业（每节课后做）：</b>第 1 课→在 AI 对话里喊「让裁判看看 X」；第 2 课→丢给 AI 两个模型让它用裁判选；第 3 课→让 Codex 也接上裁判试一次；第 4 课→拿裁判台判「周末去哪玩」；第 5 课→让裁判给你的某个想法打分；第 6 课→让裁判判 3 条资讯好不好；第 7 课→拿裁判台试「这 3 个标题哪个好」；第 8 课→让 AI 批量判 5 件事。</p>
</div>
<div class="quickstart">
<p><b>🚀 十分钟跑通（新手从这里开始）：</b>① typesafe.ai 注册领 Key（新账号自带 $5 额度）→ ② 设环境变量 <code>TYPESAFE_API_KEY</code> → ③ <code>npx skills add typesafe-ai/skills --skill typesafe-ai</code> 装官方 Skill → ④ 让 Codex 调一次最小测试，拿到真实返回才算接通 → ⑤ 丢一篇文章实战：Codex 出 16 个候选标题，Jev 按吸引力/原文贴合度/表达自然度打 0-4 档分，程序加权出前 6。完整图文步骤见仓库 <a href="USAGE.md">USAGE.md</a> · 实操案例出自<a href="https://mp.weixin.qq.com/s/kn1nSF2eFKZTL5CERaDwfw" target="_blank" rel="noopener">李岳 · 公众号「丶平凡世界」</a>（2026-09-22，本指南为浓缩版，细节与版权归原作者）</p>
</div>
<div class="progress"><div class="p-in"><span class="p-text" id="ptext">进度 0 / 202</span><div class="p-bar"><i id="pbar"></i></div><span class="p-text">顶部进度条 · 点卡片右上角 ✓ 记「已学」</span></div></div>
{''.join(sections)}
<footer>视频与数据来自向明的 JEV 案例库（非官方）· 面板：社区整理 · 2026-09-21 · 202 条案例 · 每节课点开还能看同类全部视频</footer>
</div>
<script>
const KEY='jev-learn-v1';
function load(){{try{{return JSON.parse(localStorage.getItem(KEY))||{{}}}}catch(e){{return {{}}}}
let done=load();
function save(){{localStorage.setItem(KEY,JSON.stringify(done));upd()}}
function upd(){{
  let n=Object.keys(done).length;
  document.getElementById('pbar').style.width=(n/202*100)+'%';
  document.getElementById('ptext').textContent='进度 '+n+' / 202';
  Object.keys(done).forEach(id=>{{let el=document.getElementById('done'+id);if(el)el.classList.add('on')}});
}}
function mark(id){{ if(done[id])delete done[id];else done[id]=1; save(); }}
function toggle(k){{let b=document.getElementById('bd-'+k),a=document.getElementById('ar-'+k);if(b.style.display==='none'){{b.style.display='';a.classList.remove('closed')}}else{{b.style.display='none';a.classList.add('closed')}}}}
// 默认只展开第一节
document.querySelectorAll('.l-body').forEach((b,i)=>{{if(i>0){{b.style.display='none';document.getElementById('ar-'+b.id.slice(3)).classList.add('closed')}}}});
upd();
</script>
</body></html>'''

(BASE / 'JEV课堂.html').write_text(html_doc)
print('课堂面板已生成，大小', len(html_doc)//1024, 'KB')
