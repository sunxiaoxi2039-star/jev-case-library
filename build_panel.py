#!/usr/bin/env python3
# JEV 202 案例：分类映射 + 精选点评 → 单文件暗调面板
import json, re, html

cases = json.load(open('/tmp/jev-cases.json'))

# ---------- 13 类定义 ----------
CATS = {
 'intro':   ('一句话看懂 Jev', '官宣、科普、45 秒讲清它是啥', '📣'),
 'router':  ('给 Agent 当调度员', '判断任务该派给谁：路由模型、挑技能、分工', '🧭'),
 'coding':  ('编码工具链', 'Claude Code / PR 评审 / 自动化测试里的加速器', '🛠'),
 'browser': ('浏览器与电脑遥控', 'Browser Use、Computer Use、语音操作 Mac', '🖱'),
 'game':    ('游戏与自动驾驶', '马里奥、火箭、特斯拉 FSD——炫技主战场', '🎮'),
 'trading': ('真金白银交易', '有人赚钱，有人真钱止损——含翻车实录', '💹'),
 'guard':   ('内容审核与防骗', '意图标注、广告跳过、辩论测谎', '🛡'),
 'growth':  ('营销广告与增长', '广告拆解、线索打分、竞品监测——营销团队的主战场', '📈'),
 'data':    ('数据分类与文档处理', '论文、邮件、税务单、人民日报——批量打标签', '🗂'),
 'maker':   ('办公·界面·语音', '表格、幻灯片、Figma、文件夹管家', '🗄'),
 'robot':   ('机器人与硬件', '机械臂、无人机、MuJoCo 仿真', '🦾'),
 'hack':    ('整活与边界测试', '逼它画画写字、电车难题——看极限在哪', '🃏'),
 'eco':     ('开源替代与生态', '不等审批：OpenRouter、开源复刻、本地版', '🌱'),
}

# ---------- 202 条分类映射 ----------
M = {
 1:'game',2:'maker',3:'guard',4:'maker',5:'game',6:'guard',7:'hack',8:'growth',9:'game',10:'maker',
 11:'data',12:'game',13:'browser',14:'trading',15:'guard',16:'game',17:'eco',18:'trading',19:'intro',20:'router',
 21:'trading',22:'router',23:'robot',24:'browser',25:'hack',26:'browser',27:'coding',28:'intro',29:'intro',30:'game',
 31:'data',32:'hack',33:'data',34:'eco',35:'growth',36:'browser',37:'hack',38:'intro',39:'intro',40:'intro',
 41:'intro',42:'data',43:'data',44:'intro',45:'router',46:'hack',47:'router',48:'guard',49:'router',50:'coding',
 51:'game',52:'intro',53:'game',54:'browser',55:'data',56:'hack',57:'growth',58:'game',59:'coding',60:'browser',
 61:'intro',62:'robot',63:'growth',64:'growth',65:'growth',66:'data',67:'game',68:'browser',69:'coding',70:'eco',
 71:'game',72:'game',73:'game',74:'coding',75:'intro',76:'coding',77:'maker',78:'hack',79:'game',80:'hack',
 81:'maker',82:'hack',83:'router',84:'intro',85:'game',86:'router',87:'intro',88:'intro',89:'router',90:'robot',
 91:'router',92:'intro',93:'router',94:'maker',95:'hack',96:'guard',97:'game',98:'maker',99:'game',100:'router',
 101:'growth',102:'intro',103:'coding',104:'trading',105:'guard',106:'game',107:'growth',108:'intro',109:'eco',110:'maker',
 111:'intro',112:'router',113:'intro',114:'eco',115:'coding',116:'browser',117:'guard',118:'intro',119:'maker',120:'intro',
 121:'intro',122:'guard',123:'coding',124:'intro',125:'router',126:'game',127:'game',128:'growth',129:'game',130:'game',
 131:'coding',132:'game',133:'intro',134:'eco',135:'game',136:'intro',137:'intro',138:'hack',139:'maker',140:'hack',
 141:'hack',142:'hack',143:'growth',144:'game',145:'browser',146:'browser',147:'data',148:'intro',149:'maker',150:'game',
 151:'maker',152:'intro',153:'browser',154:'hack',155:'browser',156:'intro',157:'game',158:'eco',159:'eco',160:'robot',
 161:'maker',162:'data',163:'game',164:'router',165:'game',166:'intro',167:'maker',168:'hack',169:'browser',170:'growth',
 171:'guard',172:'intro',173:'router',174:'game',175:'coding',176:'data',177:'data',178:'browser',179:'hack',180:'router',
 181:'browser',182:'browser',183:'router',184:'intro',185:'router',186:'browser',187:'browser',188:'maker',189:'data',190:'intro',
 191:'growth',192:'trading',193:'coding',194:'trading',195:'hack',196:'hack',197:'maker',198:'hack',199:'router',200:'router',
 201:'robot',202:'intro',
}

# ---------- 精选点评（一句话人话） ----------
WHY = {
 108:'创始人亲自官宣：ChatGPT 联合发明人讲为什么聊天模型≠AGI，3460 万浏览的第一手原点',
 156:'45 秒 TL;DR，140 万人看过的最短入门',
 118:'中文 50 秒科普视频，把底层架构讲透（梭哈.AI 出品）',
 52:'创始人原话：「下一个时代不是 Claude Code 时代」——正好回答你的疑问',
 59:'即时 compaction，265 万浏览——就是 compaction 这个高频场景',
 74:'PR 评审比 Claude 便宜约 200 倍、半秒出结果，6 个真实 PR 演示',
 50:'一个现成插件就能接进 Claude Code，修它最大的痛点',
 123:'并行浏览器对抗测试，17.8 万浏览',
 69:'jev-review：本地优先的 MCP 评审插件，给编码 agent 打分',
 26:'Browser Use + Jev：找航班 7 秒、0.0039 美元，248 万浏览的出圈帖',
 153:'自研 computer use：比 Opus 5 便宜 155 倍、快约 20 倍',
 186:'中文实测：Codex+Jev 组成「Jev Use」，加日历全程无停顿',
 182:'中文教程：Jev 当判官指导 Codex 操作电脑，附申请视频',
 169:'语音实时遥控浏览器，25.8 万浏览',
 71:'一小时重建特斯拉 FSD，55.6 万浏览',
 67:'中文实测：杀戮尖塔 2 代打，0.7 秒一步，「画面都没看清就操作完了」',
 126:'国际象棋三方对战：Jev vs Fable 5.1 vs GPT-6 Astra',
 157:'Jev 对 GLM 5.3 下棋：GLM 29 步将死获胜，但 Jev 每步 0.3 秒不到万分之一步价',
 104:'交易机器人：只做 Buy/Sell+置信度，104 万浏览的现象级帖',
 14:'中文解读：Monad 工程师做链上自动交易，63.5 万浏览',
 18:'冷静剂：真钱 ₹10 万 5 倍杠杆日内交易，当天触及止损——不全是大捷',
 194:'直播实验：拿 1 万美元纸交易，结果连载中',
 122:'特朗普 vs 贺锦丽辩论实时测谎仪，每句 5 个是非题',
 3:'中文 Chrome 插件：给 X 帖子实时标注意图（诱导/挑拨/推销/机生）',
 15:'YouTube 赞助广告自动跳过，每个视频约 0.005 美元，开源',
 171:'坐在 GPT 和你之间，不合规矩的草稿直接杀掉',
 170:'40 秒拆完 37 个品牌 724 条在投广告：钩子/格式/CTA 全标出',
 128:'竞品广告监测：1891 条广告 19 秒分类完，成本 12 美分',
 8:'中文实测：428 条实时新闻为 15 个品牌匹配借势热点，28 秒完成',
 101:'每条帖子 61 个问题 1 秒打完，0.0004 美元——爆款预测流水线',
 143:'150 个虚拟人格做产品意向调研，5 秒、1.8 日元',
 65:'700 条高意向线索 40 秒配好个性化外联话术',
 33:'中文硬核实测：人民日报 2.4 万条历史数据回测分类准确率',
 66:'1018 篇 AI 论文分类，总成本 0.08 美元、中位延迟 256ms',
 42:'100 封邮件欺诈检测 1.42 秒，拿不准的再路由给 Kimi K3',
 31:'400 家公司 × 1 份简历，12 秒预测该投谁',
 11:'3000 款儿童零食多标准打分，28 秒 0.11 美元',
 197:'预测式电子表格：敲「紧急度」三个字，每行 100ms 内自动评级',
 94:'演讲时幻灯片自动翻页：说什么就显示哪页，「谁都能当乔布斯」',
 161:'盯着 Downloads 文件夹自动整理，7.8 万浏览',
 139:'随时待命的语音助手：从概率判断你在不在跟它说话',
 201:'机械臂自己想到用钩子： cube 够不着就拖过来——工具使用没人编程',
 23:'无人机应用 15 分钟搭好，成本 10 美分',
 62:'纯英文一句话下目标，Jev 把硬编码动作串成机器人任务',
 198:'「我把命交给 Jev」96 万浏览的整活视频——看看就好',
 80:'电车难题里 Jev 选择牺牲人类救机器人——伦理警示，20.7 万浏览',
 196:'「Jev 不能生成文字」？给它几百个词让它挑，它说了很多',
 195:'并行预测每个像素来画画，30.2 万浏览',
 7:'日本用户发现：输入 $0.042/百万 token，输出无限免费',
 158:'OpenRouter 官方上线 beta——不等审批就能摸',
 159:'开源 Qwen 复刻版公共 API，即插即玩',
 17:'Jev-ify 开源库：把任何 HuggingFace 模型变成 Jev 式判断器',
 114:'中文玩家本地复刻「视觉版 Jev」：qwen-3.5-0.8B 量化跑在 16G M4 MacBook',
 164:'本地三大 CLI（Claude Code/Codex/opencode）之间的任务路由——和模型路由同一个思路',
 93:'90 个 skill 的 Skill Router：Claude + Jev 开源方案',
 199:'Slack agent 提速 2 倍：先让 Jev 挑好技能工具再动手',
 22:'模型路由器：判断你的请求最适合哪个模型',
 200:'模型路由 CLI：给任务+你现有的订阅，它告诉你该派给谁',
 112:'自家记忆系统接入后：token 省 94%、快 2-3 倍',
 34:'Cerebras + Qwen 3.8 27b 复刻版：质量性能接近',
}
TOP = {108, 59, 26, 170, 104, 156}
CAUTION = {18:'真钱实盘翻车：当天触及止损线', 80:'伦理警报：电车难题选了牺牲人类', 106:'承认玩 2048 不太行——能力边界实证', 194:'1 万美元实验还在连载，结果未知', 72:'等不到审批，先用别的模型复刻 Doom demo'}

def num(s):
    s = (s or '0').replace(',', '')
    m = re.match(r'^([\d.]+)(万|k|K)?$', s)
    if not m: return 0
    v = float(m.group(1))
    if m.group(2) == '万': v *= 10000
    elif m.group(2) in ('k','K'): v *= 1000
    return int(v)

for c in cases:
    c['cat'] = M[c['n']]
    c['vn'] = num(c['views'])
    c['ln'] = num(c['likes'])
    c['text'] = (c['zh'] if c['lang'] != 'zh' and c['zh'] else c['orig']) if c['lang'] != 'zh' else c['orig']
    if not c['text']: c['text'] = c['zh'] or c['orig']
    c['why'] = WHY.get(c['n'], '')
    c['top'] = c['n'] in TOP
    c['caution'] = CAUTION.get(c['n'], '')
    c['featured'] = bool(c['why'])
    c['tweet'] = f"https://x.com/i/web/status/{c['id']}"
    c['profile'] = f"https://x.com/{c['handle'].lstrip('@')}"

total_views = sum(c['vn'] for c in cases)
cat_stat = {}
for c in cases:
    cat_stat.setdefault(c['cat'], [0,0])
    cat_stat[c['cat']][0] += 1
    cat_stat[c['cat']][1] += c['vn']

print('total views:', total_views)
for k, (n, v) in sorted(cat_stat.items(), key=lambda x: -x[1][0]):
    print(f"{k:8} {n:3} 条  {v/10000:8.1f} 万浏览  featured={sum(1 for c in cases if c['cat']==k and c['featured'])}")

json.dump({'cases': cases, 'cats': {k: list(v) for k, v in CATS.items()}}, open('/tmp/jev-classified.json','w'), ensure_ascii=False)
print('OK')
