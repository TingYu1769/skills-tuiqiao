#!/usr/bin/env python3
"""zh_style_scan.py: 中文技术稿的口癖扫描与改稿核对（tuiqiao skill 配套工具）

用法：
  python3 zh_style_scan.py scan FILE [FILE ...] [--all-hits]
      统计每千个汉字的分号、破折号和 B 档词频，列出 A 档强信号的候选位置
      （行号 + 片段）、短主语后单独加逗号的候选，以及分号超过一个的段落。
      命中只是候选，要回到上下文判断。
  python3 zh_style_scan.py skeleton FILE [--heading "#### 标题"]
      抽出每段的前两句（06-flow 的诊断第一步）。
  python3 zh_style_scan.py heads FILE LINE
      列出某一段（按行号）每句的句首，用来查话题链（F3）。
  python3 zh_style_scan.py diff BEFORE AFTER
      改稿核对：数字、引用 key、行内代码、公式的集合是否一致（信息守恒），
      以及改后多出来的高频词和标点（不造新口癖）。

扫描时跳过代码块、表格行、图片行和 YAML 头；行内代码和行内公式替换成占位符。
只依赖 Python 3 标准库。
"""
import re
import sys
from collections import Counter

# ---------- 规则表（与 02-ai-tics 的编号对应） ----------

A_RULES = [
    ("A1 翻案腔", r"(不是|并非|不在于)[^。！？\n]{1,40}?(而是|而在于)|与其说|看似[^。\n]{1,20}实则|说到底|答案恰恰相反|(不只|不仅仅|不止)是一[个套种]"),
    ("A2 复述式推论", r"(这意味着|换句话说|换言之|也就是说)"),
    ("A3 句首评论语", r"(^|[。！？]\s*)(值得注意的是|值得一提的是|需要指出的是|有意思的是|不难(发现|看出)|还有一个[^。\n]{0,8}值得一提)"),
    ("A4 段首连接词", r"^(然而|因此|此外|与此同时|总而言之|综上所述)[，,]?"),
    ("A5 话题壳", r"(对于|对)[^。，\n]{1,15}(来说|而言)|就[^。，\n]{1,10}而言|从[^。，\n]{1,12}的?角度(看|来看)"),
    ("A6 空转领句", r"有[两三四五六七八九十][个点条件种类][^。：\n]{0,14}[：。]\s*$|以下几点|如下几点|一句话(总结|概括)|先说结论"),
    ("A7 元话语", r"本节(分为|将)|下面(将|按|我们)|接下来(我们|将)|上一节我们|这里只需要记住|下表(比较|列出)了|下图是|(要|为了)回答这个问题"),
    ("A11 金句收尾", r"这就是[^。\n]{1,12}。\s*$|由此可见一斑|这不仅(仅)?是[^。\n]{1,20}更是|机遇与挑战并存|未来可期"),
    ("A12 越证据断言", r"证明了|彻底解决|首次|开创了|奠定了[^。\n]{0,6}基础|里程碑|不可避免地|最根本的"),
    ("A13 模糊归因", r"研究表明|有研究(发现|指出)|业内普遍认为|专家指出"),
]

B_WORDS = [
    "可以", "可以看作", "可以理解为", "正是", "恰恰", "正好", "归根结底", "这一", "对应", "进行", "实现",
    "给出", "通过", "作为", "被", "本质上", "关键", "核心", "尤其", "格外", "往往", "通常",
    "赋能", "抓手", "底层逻辑", "闭环", "收口", "兜底", "落盘", "口径", "至关重要", "深入",
]

# diff 模式里要看增量的替换词和标点
WATCH = ["因此", "于是", "所以", "就是", "则", "其", "此", "该", "对应", "相当于", "也就是",
         "——", "：", "；", "（", "“"]

HAN = re.compile(r"[一-鿿]")

# 短主语后单独加逗号（05-punctuation PN16、02-ai-tics B13）：句首八个字以内的成分，
# 逗号后紧跟判断或评价性的谓语。句首状语、连词和话题句不算，先排除。
SUBJ_COMMA = re.compile(
    r"(?:^|(?<=[。！？；：]))\s*([^，。！？；：、\s“”‘’（）()*]{1,8})，"
    r"(?=是|就是|才是|正是|也是|都是|只是|不是|并不|并非|在于|决定|取决于|本质上|其实|往往|"
    r"恰恰|意味着|能|会|可以|需要|必须|让|使|把|来自|依赖|负责)", re.M)
# 前面是逗号时（“值得注意的是，索引，本质上是……”），只认判断性的谓语，免得把分句当主语。
SUBJ_COMMA_MID = re.compile(
    r"(?<=，)\s*([^，。！？；：、\s“”‘’（）()*]{1,8})，(?=是|就是|才是|正是|在于|本质上|意味着)")
NOT_SUBJ = re.compile(
    r"^(在|当|对|如果|若|假如|虽然|尽管|因为|由于|为了|随着|除了|根据|按照|通过|经过|从|自从|即使|只要|只有|"
    r"无论|不管|一旦|比如|例如|而|但)|是|(时|后|前|中|里|来说|而言|看来|以来|上|下)$|^(因此|所以|但是|然而|此外|"
    r"同时|首先|其次|最后|另外|当然|于是|而且|不过|可是|其实|总之|事实上|实际上|显然|一般|通常|目前|现在|"
    r"今天|过去|后来|最终|结果|反过来|相反|同样|那么|这样|这时|此时|换句话说|也就是说)$")


# ---------- 读取与清洗 ----------

def load_lines(path):
    """返回 [(行号, 清洗后的文本)]，跳过代码块、表格、图片和 YAML 头。"""
    raw = open(path, encoding="utf-8").read().split("\n")
    out, in_code, in_yaml = [], False, False
    for i, line in enumerate(raw, 1):
        s = line.strip()
        if i == 1 and s == "---":
            in_yaml = True
            continue
        if in_yaml:
            if s == "---":
                in_yaml = False
            continue
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or s.startswith("|") or s.startswith("![") or s.startswith("$$"):
            continue
        text = re.sub(r"`[^`]*`", "〔码〕", line)
        text = re.sub(r"\$[^$\n]+\$", "〔式〕", text)
        out.append((i, text))
    return out


def han_count(lines):
    return sum(len(HAN.findall(t)) for _, t in lines)


def per_k(n, han):
    return n * 1000.0 / han if han else 0.0


def snippet(text, start, end, width=18):
    a, b = max(0, start - width), min(len(text), end + width)
    return text[a:b].replace("\n", " ").strip()


# ---------- scan ----------

def scan(paths, all_hits=False):
    for path in paths:
        lines = load_lines(path)
        han = han_count(lines)
        body = "\n".join(t for _, t in lines)
        print(f"\n=== {path}")
        print(f"汉字 {han}；以下密度均为每千个汉字")
        semi, dash = body.count("；"), body.count("——")
        print(f"分号 {semi}（{per_k(semi, han):.1f}）  破折号 {dash}（{per_k(dash, han):.1f}）")

        print("\n-- A 档候选（02-ai-tics，命中只是候选）")
        total = 0
        for name, pat in A_RULES:
            rx = re.compile(pat, re.M)
            hits = [(ln, m) for ln, t in lines for m in rx.finditer(t.lstrip("> "))]
            if not hits:
                continue
            total += len(hits)
            print(f"{name}: {len(hits)} 处（{per_k(len(hits), han):.2f}）")
            shown = hits if all_hits else hits[:6]
            for ln, m in shown:
                t = dict(lines)[ln].lstrip("> ")
                print(f"    L{ln}: …{snippet(t, m.start(), m.end())}…")
            if len(hits) > len(shown):
                print(f"    ……另有 {len(hits) - len(shown)} 处，加 --all-hits 全部列出")
        if not total:
            print("（无）")

        subj = sorted(((ln, m) for ln, t in lines
                       for rx in (SUBJ_COMMA, SUBJ_COMMA_MID) for m in rx.finditer(t.lstrip("> "))
                       if not NOT_SUBJ.search(m.group(1))), key=lambda h: (h[0], h[1].start()))
        if subj:
            print(f"\n-- 短主语后的逗号：{len(subj)} 处（{per_k(len(subj), han):.2f}；PN16、B13，"
                  "长主语、话题句、带语气词的主语要留）")
            shown = subj if all_hits else subj[:6]
            for ln, m in shown:
                t = dict(lines)[ln].lstrip("> ")
                print(f"    L{ln}: …{snippet(t, m.start(1), m.end())}…")
            if len(subj) > len(shown):
                print(f"    ……另有 {len(subj) - len(shown)} 处，加 --all-hits 全部列出")

        print("\n-- B 档词频（成片才改，看是否扎堆）")
        counts = [(w, body.count(w)) for w in B_WORDS]
        counts = [(w, c) for w, c in counts if c]
        counts.sort(key=lambda x: -x[1])
        print("  ".join(f"{w} {c}（{per_k(c, han):.1f}）" for w, c in counts) or "（无）")

        dense = [(ln, t.count("；")) for ln, t in lines if t.count("；") >= 2]
        if dense:
            print("\n-- 分号两个以上的段落（逐个说出用途，见 05-punctuation）")
            print("  " + "  ".join(f"L{ln}×{n}" for ln, n in dense[:40]))
            if len(dense) > 40:
                print(f"  ……共 {len(dense)} 段")


# ---------- skeleton / heads ----------

SENT = re.compile(r".+?[。？！](?:\*\*)?|.+$")


def skeleton(path, heading=None):
    raw = open(path, encoding="utf-8").read().split("\n")
    start = 0
    if heading:
        start = next(i for i, l in enumerate(raw) if l.strip() == heading.strip()) + 1
    in_code = False
    for l in raw[start:]:
        if heading and re.match(r"#{1,4} ", l):
            break
        if l.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not l.strip() or l.startswith(("|", "!", "*图", "$$", "#", "---")):
            continue
        body = l.lstrip("> ").strip()
        if not body:
            continue
        s = SENT.findall(body)
        print("·", "".join(s[:2])[:180])


def heads(path, line_no):
    para = open(path, encoding="utf-8").read().split("\n")[line_no - 1]
    para = re.sub(r"^\*\*[^*]{1,12}\*\*\s*", "", para)
    for s in SENT.findall(para):
        print("·", re.split(r"[，：；]", s.strip())[0][:24])


# ---------- diff ----------

FACT = re.compile(r"\[@[^\]]+\]|`[^`]+`|\$\$.+?\$\$|\$[^$\n]+\$|\d+(?:\.\d+)?%?", re.S)


FENCE = re.compile(r"```.*?```", re.S)


def facts(path):
    text = open(path, encoding="utf-8").read()
    fences = FENCE.findall(text)  # 代码块整块比对，先取出来，免得三个反引号打乱行内代码的配对
    rest = FENCE.sub(" ", text)
    return Counter(fences) + Counter(FACT.findall(rest))


def diff(before, after):
    fb, fa = facts(before), facts(after)
    lost, added = fb - fa, fa - fb
    print("== 信息守恒：数字、引用 key、行内代码、公式")
    if not lost and not added:
        print("一致。")
    for k, v in sorted(lost.items()):
        print(f"  少了 {k} ×{v}")
    for k, v in sorted(added.items()):
        print(f"  多了 {k} ×{v}")
    print("  （脚本只查形状。限定词、否定、施事有没有变，要逐句读。）")

    tb = open(before, encoding="utf-8").read()
    ta = open(after, encoding="utf-8").read()
    print("\n== 不造新口癖：改后增加的词和标点")
    rows = [(w, tb.count(w), ta.count(w)) for w in WATCH]
    rows = [r for r in rows if r[2] > r[1]]
    if not rows:
        print("没有增加。")
    for w, b, a in rows:
        flag = "  ← 留意" if a - b >= 3 else ""
        print(f"  {w}: {b} → {a}{flag}")


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = argv[1]
    if cmd == "scan":
        paths = [a for a in argv[2:] if not a.startswith("--")]
        scan(paths, all_hits="--all-hits" in argv)
    elif cmd == "skeleton":
        h = argv[argv.index("--heading") + 1] if "--heading" in argv else None
        skeleton(argv[2], h)
    elif cmd == "heads":
        heads(argv[2], int(argv[3]))
    elif cmd == "diff":
        diff(argv[2], argv[3])
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
