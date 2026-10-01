<h1 align="center">Tuiqiao 推敲</h1>

<p align="center">
  An agent skill for Chinese technical writing:<br>
  remove AI tics, choose precise words, fix the flow, and write with restraint and craft.
</p>

<p align="center">
  <a href="README.md">简体中文</a> &nbsp;·&nbsp; <b>English</b>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://agentskills.io"><img alt="Agent Skills format" src="https://img.shields.io/badge/format-Agent%20Skills-6f42c1"></a>
  <img alt="Works with Claude Code, Codex and more" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20more-2ea44f">
</p>

<p align="center"><code>npx skills add TingYu1769/skills-tuiqiao</code></p>

`tuiqiao` is named after *tuīqiāo* (推敲), the Chinese word for weighing one's words. It comes from the Tang poet Jia Dao, who could not decide whether a monk should *push* (推) or *knock on* (敲) a gate under the moon. The skill is for Chinese technical prose: books, technical and research reports, paper bodies, design docs, READMEs, and engineering blogs. It covers drafting, revising, and reviewing. It works in Claude Code, Codex, and any agent that reads the [Agent Skills](https://agentskills.io) format.

The instructions and the knowledge base are written in Chinese, because the rules are about Chinese.

## The problem

Chinese drafts written by language models share recognizable habits: opening with 值得注意的是 ("it is worth noting that"), closing with 这正是…… ("this is exactly…"), dashes used for dramatic reveals, a lone comma after a short subject (缓存，是……), nominalized verbs (进行了优化 instead of 优化了), and an aphorism at the end of each paragraph.

The usual fix is a banned-word list with mechanical substitutions. That tends to cause two new problems. Hedges, sources, and qualifiers such as 通常, 据……报告, and 之一 get deleted as "tics", so information is lost. And one tic is swapped for another: every 正是 becomes 就是, every dash becomes a colon, and the text still reads as machine-written.

## What the skill does

- **Three boundaries come first.** Information is conserved: facts, numbers, formulas, symbols, citation keys, terms, qualifiers, negations, conditions, and attributions are neither added nor removed. Register is not lowered: the target is formal, plain written Chinese, not chatty slang. No new tics: if a replacement word appears three or more times on a page, use a different fix.
- **Five passes.** Lock what must not change, fix the flow, fix words and syntax, remove tics and fix punctuation, and only then add craft.
- **Every rule says when not to apply it.** A protection list names 17 patterns that look like flaws but should stay, such as the definitional 即, evidential hedges, inferential 因此, and source attributions. When in doubt, leave it.
- **A knowledge base read on demand.** `SKILL.md` holds the boundaries, the workflow, a routing table, and a condensed rule set. Twelve cards hold the details, and the agent reads one to three of them per question.
- **Exemplars from respected Chinese writers.** A catalog of 48 works on expository, technical, and craft writing, with public-domain excerpts stored in full.
- **A scanning script.** `scripts/zh_style_scan.py` lists tic candidates and punctuation density, extracts the first two sentences of each paragraph to check the argument, and diffs numbers, citation keys, code, and formulas before and after a revision. It uses only the Python 3 standard library.

## Install

With the [`skills` CLI](https://github.com/vercel-labs/skills) (Claude Code, Codex, Cursor, and other agents):

```bash
npx skills add TingYu1769/skills-tuiqiao
```

Manual install: copy the whole `skills/tuiqiao/` directory (keep `SKILL.md`, `references/`, `scripts/`, and `agents/` together) to where your agent looks for skills:

| Agent | Personal | Project |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/tuiqiao/` | `.claude/skills/tuiqiao/` |
| Codex | `~/.codex/skills/tuiqiao/` or `~/.agents/skills/tuiqiao/` | `.agents/skills/tuiqiao/` |
| Other agents | see the agent's documentation | |

If your agent does not discover skills automatically, ask it to read `skills/tuiqiao/SKILL.md` and follow it.

## Usage

Invoke it with `/tuiqiao` (Claude Code) or `$tuiqiao` (Codex), or just ask in Chinese, for example 用推敲改一下这一节，原文和改后对照给我看 ("revise this section with tuiqiao, showing original and revision side by side").

Project-specific conventions, such as citation style, notation, or whether dashes are allowed, can go in `CLAUDE.md`, `AGENTS.md`, or a separate style note. The skill looks for them first and lets them override its general rules.

## Repository layout

```text
skills-tuiqiao/
├── README.md / README.en.md
├── CHANGELOG.md
├── LICENSE
├── evals/scenarios.md        behavior scenarios for maintainers; agents do not load this
└── skills/tuiqiao/
    ├── SKILL.md              loaded when the skill runs
    ├── agents/openai.yaml    Codex display metadata
    ├── references/           knowledge cards 00–11 and public-domain exemplars
    └── scripts/zh_style_scan.py
```

## Prior work

Influenced by [goutoujunshi](https://github.com/shengjidaguai-china/goutoujunshi) (thin core plus a layered knowledge base), [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) (a Chinese human-versus-model corpus study), [humanizer](https://github.com/blader/humanizer), [Humanizer-zh](https://github.com/op7418/Humanizer-zh), [humanizer-zh-next](https://github.com/Hyacehila/humanizer-zh-next), and [ruanyf/document-style-guide](https://github.com/ruanyf/document-style-guide), as well as GB/T 15834—2011 and classic Chinese works on grammar and style. Full sources are in [`10-sources`](skills/tuiqiao/references/10-sources.md).

## License

[MIT](LICENSE). The excerpts under `references/exemplars/` are public-domain works and are not covered by the MIT license; each file states its source and public-domain basis. Short quotations from living authors in the cards remain the property of their authors.
