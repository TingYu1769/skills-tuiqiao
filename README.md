<h1 align="center">推敲</h1>

<p align="center">
  中文技术写作的 agent skill：<br>
  去 AI 味，改准用词，理顺行文，写出技术文章该有的文采。
</p>

<p align="center">
  <b>简体中文</b> &nbsp;·&nbsp; <a href="README.en.md">English</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="许可：MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://agentskills.io"><img alt="Agent Skills 格式" src="https://img.shields.io/badge/format-Agent%20Skills-6f42c1"></a>
  <img alt="适用于 Claude Code、Codex 与其他 agent" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20more-2ea44f">
</p>

<p align="center"><code>npx skills add TingYu1769/skills-tuiqiao</code></p>

> **改前：** 值得注意的是，索引，本质上是一种用写入速度换取读取速度的策略。这意味着，每多建一个索引，写入就会变慢——这正是很多团队在上线之后才发现的问题。
>
> **改后：** 索引用写入速度换读取速度。这意味着，每多建一个索引，写入就会变慢。很多团队在上线之后才发现这个问题。
>
> - 改 1：删掉句首评论语“值得注意的是”（A3）。
> - 改 2：“索引”是短主语，后面的逗号删掉（PN16）。
> - 改 3：“本质上是一种……的策略”空转，还原成动词“用……换……”（R24）。
> - 改 4：破折号和“这正是”制造揭晓式停顿，拆成一句平说（PN1、R15）。
> - 没改的：“这意味着”带出了新推论（P9）；“每多建一个索引”的“一个”在计数（W11）；“很多团队”是原文的限定，不删也不加强（P3）。

`tuiqiao` 的名字取自“推敲”：贾岛骑在驴背上，拿不定该写“僧推月下门”还是“僧敲月下门”。改稿的功夫在于一个字一个字地掂量，改得准，也知道哪里不该改。这个 skill 面向中文技术文字，包括技术书、技术报告、调研报告、论文正文、设计文档、README 和技术博客，起草、润色、审稿都用得上。它在 Claude Code、Codex 以及任何支持 [Agent Skills](https://agentskills.io) 格式的 agent 里都能用。上面的段落是虚构的。

## 要解决的问题

AI 起草的中文技术稿有一套认得出来的写法：句首“值得注意的是”，句尾“这正是……”，破折号制造停顿，短主语后面加逗号，“进行了优化”代替“优化了”，段尾再收一句金句。单看每一句都说得通，连成一篇，读者就认出了是谁写的。

常见的去 AI 味办法是一张禁用词表，见词就换。这样改容易出两种新毛病。一种是丢信息：“通常”“据……报告”“之一”被当成口癖删掉，原文的保留和出处跟着没了。另一种是造新口癖：“正是”全换成“就是”，破折号全换成冒号，腔调换了一种，AI 味还在。

推敲先守边界，再动字句。

## 这个 skill 做什么

**三条边界优先于所有规则。** 信息守恒：事实、数字、公式、符号、引用 key、术语、限定词、否定、条件、归因，一个不增，一个不减。语体不降级：目标是正式、平实的书面语，不拿“说白了”“讲真”冒充人味。不造新口癖：替换进去的词在一页里出现三次以上，就换一种改法。

**按五遍改稿。** 锁定不能动的内容，理行文，改用词与句法，去口癖、改标点，最后才添文采。结构不对，字句改得再细也要返工，所以行文排在前面。

**每条规则都写“不改”。** 保护清单列了 17 类看着像毛病、其实该留的写法，比如下定义的“即”、证据性限定、推理里的“因此”、带来新推论的“这意味着”、交代证据来源的主语和动词。拿不准是否命中规则，就不改。

**知识库按需读取。** SKILL.md 只放边界、流程、路由表和一份精简规则。规则的展开、成批的例句和范文放在 12 张卡里，每次只读当前问题需要的一到三张。

**有名家范文可以对照。** 范文库收了 48 条书目和文章，从华罗庚《统筹方法》、竺可桢《大自然的语言》到吕叔湘《语文常谈》、余光中《怎样改进英式中文》，每条写明技术写作者能从中学什么。其中 9 篇公版作品收了原文选段。

**带一个扫描脚本。** 列出口癖候选和标点密度，抽每段前两句查论证，改完比对数字、引用 key、代码和公式有没有丢。

## 知识库

| 卡片 | 内容 |
| --- | --- |
| `00-index` | 目录、路由、编号登记、证据等级、维护规则 |
| `01-boundaries` | 三条边界，保护清单 P1–P17，矫枉过正 O1–O9 |
| `02-ai-tics` | 口癖词典：A 档强信号 A1–A13，B 档成片才改 B1–B13，C 档已被推翻 C1–C10，各模型的特点 |
| `03-word-syntax` | 用词与欧化句法 W1–W20 |
| `04-replacements` | 24 个高频词和框架的正当用法与替换办法 R1–R24 |
| `05-punctuation` | 标点 PN1–PN16（依据 GB/T 15834—2011），中英混排、数字与单位 |
| `06-flow` | 行文 F1–F12：开头、段内、段间、节尾 |
| `07-elegance` | 技术文采 T1–T12，出界清单 X1–X13，名家选段赏析 |
| `08-genres` | 体裁 G1–G6：技术书、论文、技术报告与调研报告、设计文档、README、技术博客 |
| `09-cases` | 改稿案例：整段的原文、改后、改了什么、没改什么 |
| `10-sources` | 依据与证据等级，未核实事项 |
| `11-exemplars` | 范文库 E1–E48 |

每条规则标了证据等级：【规范】指国家标准、词典和权威语法著作，【实测】指语料统计，【名家】指写作名家的主张，【经验】指社区文章和开源 skill 的归纳，【改稿】指在一部中文技术书稿的改稿中验证过。规则冲突时，【规范】和【改稿】优先于【经验】。

## 名家选段

`skills/tuiqiao/references/exemplars/` 收了下面几篇公版作品的选段，每篇开头写明出处、核对办法和公版依据：

| 作品 | 作者 | 选段 |
| --- | --- | --- |
| 《中国建筑的特征》 | 梁思成 | 节录 |
| 《大自然的语言》 | 竺可桢 | 节录 |
| 《敬业与乐业》 | 梁启超 | 节录 |
| 《背影》 | 朱自清 | 车站与买橘子两段 |
| 《答北斗杂志社问》 | 鲁迅 | 全文，附《关于翻译的通信》两段 |
| 《作文秘诀》 | 鲁迅 | 全文 |
| 《不应该那么写》 | 鲁迅 | 全文 |
| 《文学改良刍议》 | 胡适 | 八事总纲与四节 |
| 《差不多先生传》 | 胡适 | 全文 |

在世或仍在版权期内的作者，卡片里只做短引，或者只给书名和看点。

## 安装

使用 [`skills` CLI](https://github.com/vercel-labs/skills)（支持 Claude Code、Codex、Cursor 等多种 agent）：

```bash
npx skills add TingYu1769/skills-tuiqiao
```

仓库地址：[github.com/TingYu1769/skills-tuiqiao](https://github.com/TingYu1769/skills-tuiqiao)。

手动安装：把 `skills/tuiqiao/` 整个目录（`SKILL.md`、`references/`、`scripts/`、`agents/` 保持在一起）复制到 agent 扫描的位置：

| Agent | 个人级 | 项目级 |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/tuiqiao/` | `.claude/skills/tuiqiao/` |
| Codex | `~/.codex/skills/tuiqiao/` 或 `~/.agents/skills/tuiqiao/` | `.agents/skills/tuiqiao/` |
| 其他 agent | 参见该 agent 的文档 | |

agent 不能自动发现 skill 时，直接让它读 `skills/tuiqiao/SKILL.md` 并照着做。

指令和知识库都是中文。扫描脚本只依赖 Python 3 标准库；不能跑代码的环境里，skill 照样能用，只是少了自动定位和核对。

## 用法

用 `/tuiqiao`（Claude Code）、`$tuiqiao`（Codex）调用，或者直接用自然语言：

> 用推敲改一下这一节，去掉 AI 味，原文和改后对照给我看。

> 这段 README 读着像 AI 写的，帮我改改，只要成稿。

> 我要写一篇讲 Raft 选举的技术博客，先帮我起草第一节。

> 想学说明文怎么讲清一个东西的构造，找篇范文给我对照。

要对照时，每段先给原文、再给改后，改动处行尾标“⇐ 改N”；正文后逐条批注原句、改句、理由和规则编号，每段列出“没改的”，文末汇总“需作者确认”和“范围外、建议一起改”。只要成稿，就只给成稿。整节或整章的改写，先拿一小段做样板，认可了再铺开。

项目有自己的体例时（引用格式、符号表、正文用不用破折号等），写进 `CLAUDE.md`、`AGENTS.md` 或单独的风格说明。skill 动手前会先找这些约定，和通用规则冲突时听约定。

## 扫描脚本

在 `skills/tuiqiao/` 下运行：

```bash
python3 scripts/zh_style_scan.py scan FILE        # 口癖候选、短主语后的逗号、分号与破折号密度、B 档词频
python3 scripts/zh_style_scan.py skeleton FILE    # 抽每段前两句，查论证串不串得起来
python3 scripts/zh_style_scan.py heads FILE 行号   # 列出一段里每句的句首，查话题链
python3 scripts/zh_style_scan.py diff 改前 改后    # 核对数字、引用 key、代码、公式，列出改后多出来的高频词
```

命中只是候选，要回到上下文判断。

## 仓库结构

```text
skills-tuiqiao/
├── README.md
├── README.en.md
├── CHANGELOG.md
├── LICENSE
├── evals/
│   └── scenarios.md              维护者用的行为场景，agent 不会加载
└── skills/
    └── tuiqiao/
        ├── SKILL.md              边界、流程、路由和精简规则，skill 运行时加载
        ├── agents/
        │   └── openai.yaml       Codex 的显示元数据，其他宿主忽略
        ├── references/
        │   ├── 00-index.md … 11-exemplars.md   知识卡，按问题读取
        │   └── exemplars/        公版名家选段
        └── scripts/
            └── zh_style_scan.py  扫描与核对脚本
```

## 参考的同类工作

下面这些项目和资料影响了本设计，完整的出处和证据等级见 [`10-sources`](skills/tuiqiao/references/10-sources.md)。

- [goutoujunshi（狗头军师）](https://github.com/shengjidaguai-china/goutoujunshi)：薄内核加分层知识库的结构，以及知识库的维护办法。
- [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)：中文人机语料对比，口癖分档用到的多数倍率出自这里。
- [humanizer](https://github.com/blader/humanizer)、[Humanizer-zh](https://github.com/op7418/Humanizer-zh)、[humanizer-zh-next](https://github.com/Hyacehila/humanizer-zh-next)：AI 写作痕迹的归纳。
- [中文技术文档的写作规范](https://github.com/ruanyf/document-style-guide)：段落、句长和中英混排。
- GB/T 15834—2011《标点符号用法》，吕叔湘、朱德熙《语法修辞讲话》，余光中、思果、朱光潜谈中文与翻译，Joseph Williams《Style》，Steven Pinker《The Sense of Style》。

## 参与贡献

新增口癖条目之前先抽样：在至少两份人写的技术文本和两份 AI 稿里各抽 20 处命中，逐处读上下文，再看频率。每条规则写清“不改”的情形，想不清例外就先不收。例句一律虚构，或者取自公版作品，不要提交自己或别人未公开的稿子。行为上的问题，最好写成 [`evals/scenarios.md`](evals/scenarios.md) 里的一个新场景，优先做窄小的修正。

## 许可

仓库按 [MIT](LICENSE) 许可发布。`references/exemplars/` 下的选段是已进入公有领域的作品，不受 MIT 约束，每篇开头写明出处和公版依据。卡片里对在世作者的短引，版权归原作者。
