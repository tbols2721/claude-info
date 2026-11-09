"""Render Mermaid diagrams as monospaced text for the Info manuals.

Pure Python, standard library only. Sequence diagrams, flowcharts
(`graph`/`flowchart`), state diagrams and Gantt charts are drawn with
box-drawing characters. When a drawing does not fit the width, a structured
text rendering is used instead (participants plus a numbered message list,
or a node list with outgoing edges). Anything else is shown as its source.
Whatever the method, every label in the source appears in the output.

    uv run python -m claude_info.diagrams --check

renders every diagram in mirror/, checks the invariants and writes
build/diagram-review.txt for eyeballing.
"""

from __future__ import annotations

import functools
import html
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Rendered:
    text: str  # monospaced text: no tabs, no trailing spaces, no blank first/last line
    method: str  # sequence, sequence-list, flowchart, flowchart-list, state,
    #              state-list, gantt, gantt-list or source


class _Unsupported(Exception):
    """The parser met syntax it does not understand."""


class _NoFit(Exception):
    """A drawing could not be made within the width (or without ambiguity)."""


MIN_WIDTH = 2


def render(source: str, max_width: int = 78) -> Rendered:
    """Render Mermaid `source` as text no wider than `max_width` columns."""
    width = max(MIN_WIDTH, int(max_width))
    try:
        text, method = _render(source, width)
    except Exception:  # never raise: fall back to the source itself
        text, method = _source_text(source, width), "source"
    lines = _finish(text, width)
    if not lines:
        lines, method = _finish("(empty diagram)", width), "source"
    return Rendered("\n".join(lines), method)


def _render(source: str, width: int) -> tuple[str, str]:
    lines = _statements(source)
    if not lines:
        return "", "source"
    kind = lines[0].split()[0].rstrip(";") if lines[0].split() else ""
    try:
        if kind == "sequenceDiagram":
            return _render_sequence(_parse_sequence(lines), width)
        if kind in ("graph", "flowchart"):
            return _render_graph(_parse_flowchart(lines), width, "flowchart")
        if kind in ("stateDiagram", "stateDiagram-v2"):
            return _render_graph(_parse_state(lines), width, "state")
        if kind == "gantt":
            return _render_gantt(_parse_gantt(lines), width)
    except (_Unsupported, _NoFit, ValueError, KeyError, IndexError, RecursionError):
        pass
    return _source_text(source, width), "source"


# --- text utilities ---------------------------------------------------------


def _cw(ch: str) -> int:
    """Display width of one character."""
    if unicodedata.combining(ch) or unicodedata.category(ch) in ("Mn", "Me", "Cf"):
        return 0
    return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


def tw(s: str) -> int:
    """Display width of a string."""
    if s.isascii():
        return len(s)
    return sum(_cw(c) for c in s)


def _cut(s: str, width: int) -> tuple[str, str]:
    """Split `s` after at most `width` columns (at least one character)."""
    w = 0
    for i, c in enumerate(s):
        w += _cw(c)
        if w > width:
            return (s[:i], s[i:]) if i else (s[:1], s[1:])
    return s, ""


_AFTER = "/-_.,;:&?=+)]}|>"
_BEFORE = "([{<"


def _cuts(word: str) -> list[int]:
    """Positions where a long word may be broken (not inside runs like '...')."""
    cuts = set()
    for i in range(1, len(word)):
        a, b = word[i - 1], word[i]
        if a == b and not a.isalnum():
            continue
        if a in _AFTER or (b in _BEFORE and a != b):
            cuts.add(i)
    return sorted(cuts)


def _break_word(word: str, width: int) -> list[str]:
    """Break a word wider than `width` at punctuation, else hard."""
    out = []
    while tw(word) > width:
        head, _ = _cut(word, width)
        cut = max((i for i in _cuts(word) if i <= len(head)), default=0)
        out.append(word[: cut or len(head)])
        word = word[cut or len(head) :]
    if word:
        out.append(word)
    return out


NBSP = "\xa0"  # glues words together while wrapping


def wrap(line: str, width: int | None) -> list[str]:
    """Wrap one line of text at spaces (keeping its indentation)."""
    return list(_wrap(line, width))


@functools.lru_cache(maxsize=65536)
def _wrap(line: str, width: int | None) -> tuple[str, ...]:
    if width is None or tw(line) <= width:
        return (line.replace(NBSP, " "),)
    indent = line[: len(line) - len(line.lstrip(" "))]
    if tw(indent) > width // 2:
        indent = ""
    avail = max(1, width - tw(indent))
    out: list[str] = []
    cur = ""
    for word in line.split(" "):
        if not word:
            continue
        for piece in _break_word(word, avail):
            if not cur:
                cur = piece
            elif tw(cur) + 1 + tw(piece) <= avail:
                cur += " " + piece
            else:
                out.append(cur)
                cur = piece
    if cur or not out:
        out.append(cur)
    return tuple((indent + o).replace(NBSP, " ") for o in out)


def wrap_lines(lines: list[str], width: int | None) -> list[str]:
    return [w for line in lines for w in wrap(line, width)]


def _soft_pieces(text: str) -> list[str]:
    """The smallest pieces a label can be wrapped into without hard breaks."""
    out = []
    for word in text.split():
        cuts = [0, *_cuts(word), len(word)]
        out += [word[a:b] for a, b in zip(cuts, cuts[1:]) if b > a]
    return out


_BR = re.compile(r"<br\s*/?>", re.I)
_TAGS = re.compile(
    r"</?(?:b|i|em|strong|u|s|code|sub|sup|small|big|span|font|a|p|div|mark|del"
    r"|ins|tt|kbd|var|samp)(?:\s[^<>]*)?/?>",
    re.I,
)
_MERMAID_ENTITY = re.compile(r"#(\d+|[A-Za-z]+);")
_CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def _entity(m: re.Match) -> str:
    code = m.group(1)
    if code.isdigit():
        try:
            return chr(int(code))
        except (ValueError, OverflowError):
            return m.group(0)
    decoded = html.unescape(f"&{code};")
    return m.group(0) if decoded.startswith("&") else decoded


def clean(text: str) -> list[str]:
    """Decode a Mermaid label into display lines (`<br>` breaks, entities)."""
    s = text.replace("\t", " ")
    s = _BR.sub("\n", s)
    s = _TAGS.sub("", s)
    s = _MERMAID_ENTITY.sub(_entity, s)
    s = html.unescape(s).replace("\xa0", " ")
    s = _CONTROL.sub("", s)
    lines = []
    for i, raw in enumerate(s.split("\n")):
        raw = raw.rstrip()
        indent = "" if i == 0 else raw[: len(raw) - len(raw.lstrip())]
        if len(indent) < 2:  # a lone space after <br> is not indentation
            indent = ""
        body = " ".join(raw.split())
        if body:
            lines.append(indent + body)
    return lines


def _flat(lines: list[str]) -> str:
    return " ".join(" ".join(lines).split())


def _statements(source: str) -> list[str]:
    """Source lines without front matter, directives, comments or blanks."""
    lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = []
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].strip() == "---":
        j = i + 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        if j < len(lines):
            i = j + 1
    for line in lines[i:]:
        s = line.replace("\t", " ").strip()
        if not s or s.startswith("%%"):
            continue
        out.append(s)
    return out


def _finish(text: str, width: int) -> list[str]:
    """Enforce the output invariants, hard-wrapping as a last resort."""
    out = []
    for line in text.replace("\t", "    ").split("\n"):
        line = _CONTROL.sub("", line).rstrip()
        while tw(line) > width:
            head, line = _cut(line, width)
            out.append(head.rstrip())
            line = line.rstrip()
        out.append(line)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def _source_text(source: str, width: int) -> str:
    """The diagram source, dedented and wrapped, minus front matter."""
    lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].strip() == "---":
        j = i + 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        if j < len(lines):
            lines = lines[j + 1 :]
    lines = [_CONTROL.sub("", l.replace("\t", "    ")).rstrip() for l in lines]
    body = [l for l in lines if l.strip()]
    indent = min((len(l) - len(l.lstrip()) for l in body), default=0)
    out = []
    for line in lines:
        line = line[indent:]
        lead = line[: len(line) - len(line.lstrip())]
        for k, piece in enumerate(wrap(line, width) if line.strip() else [""]):
            if k and tw(lead) + 2 + tw(piece.lstrip()) <= width:
                piece = lead + "  " + piece.lstrip()
            out.append(piece)
    return "\n".join(out)


class Grid:
    """A character canvas that knows about double-width characters."""

    def __init__(self, width: int = 0):
        self.rows: list[list[str]] = []
        self.width = width

    def ensure(self, r: int, c: int) -> None:
        while len(self.rows) <= r:
            self.rows.append([" "] * self.width)
        row = self.rows[r]
        if len(row) <= c:
            row.extend(" " * (c + 1 - len(row)))

    def get(self, r: int, c: int) -> str:
        if 0 <= r < len(self.rows) and 0 <= c < len(self.rows[r]):
            return self.rows[r][c]
        return " "

    def put(self, r: int, c: int, ch: str) -> None:
        if r < 0 or c < 0:
            return
        w = _cw(ch)
        self.ensure(r, c + max(w, 1))
        row = self.rows[r]
        if row[c] == "" and c > 0:  # overwriting the right half of a wide char
            row[c - 1] = " "
        if c + 1 < len(row) and row[c + 1] == "" and w < 2:
            row[c + 1] = " "
        row[c] = ch
        if w == 2:
            if c + 2 < len(row) and row[c + 2] == "":
                row[c + 2] = " "
            row[c + 1] = ""

    def text(self, r: int, c: int, s: str) -> None:
        last = None
        for ch in s:
            w = _cw(ch)
            if w == 0:  # combining mark: attach to the previous character
                if last is not None:
                    self.rows[last[0]][last[1]] += ch
                continue
            self.put(r, c, ch)
            last = (r, c)
            c += w

    def lines(self) -> list[str]:
        return ["".join(row).rstrip() for row in self.rows]


# --- sequence diagrams ------------------------------------------------------


@dataclass
class _Part:
    id: str
    label: list[str]
    actor: bool = False
    box: int | None = None


@dataclass
class _Msg:
    src: str
    dst: str
    line: str  # solid / dotted
    head: str  # arrow / open / cross / none / both
    text: list[str]
    act: str = ""  # "+" activates dst, "-" deactivates src
    num: int | None = None


@dataclass
class _Note:
    pos: str  # over / left / right
    parts: list[str]
    text: list[str]


@dataclass
class _Block:
    kind: str  # loop alt opt par critical break rect ...; else/and/option; end
    label: list[str]


@dataclass
class _Act:
    part: str
    on: bool


@dataclass
class _Seq:
    parts: dict[str, _Part] = field(default_factory=dict)
    events: list = field(default_factory=list)
    boxes: list[list[str]] = field(default_factory=list)  # label lines per box
    title: list[str] = field(default_factory=list)
    descr: list[str] = field(default_factory=list)
    destroyed: set[str] = field(default_factory=set)


_ARROWS = {
    "<<-->>": ("dotted", "both"),
    "<<->>": ("solid", "both"),
    "-->>": ("dotted", "arrow"),
    "->>": ("solid", "arrow"),
    "--x": ("dotted", "cross"),
    "-x": ("solid", "cross"),
    "--)": ("dotted", "open"),
    "-)": ("solid", "open"),
    "-->": ("dotted", "none"),
    "->": ("solid", "none"),
}
_SEQ_MSG = re.compile(
    r"^(?P<a>[^:;<>+-][^:;]*?)\s*(?P<arrow>"
    + "|".join(re.escape(a) for a in _ARROWS)
    + r")(?P<act>[+-]?)\s*(?P<b>[^:;+-][^:;]*?)\s*(?::(?P<text>.*))?$"
)
_SEQ_PART = re.compile(r"^(?:create\s+)?(participant|actor)\s+(.+)$")
_SEQ_NOTE = re.compile(r"^note\s+(left of|right of|over)\s+([^:]+?)\s*:(.*)$", re.I)
_SEQ_OPEN = re.compile(r"^(loop|alt|opt|par_over|par|critical|break|rect|box)(?:\s+(.*))?$")
_SEQ_BRANCH = re.compile(r"^(else|and|option)(?:\s+(.*))?$")
_SEQ_BRANCH_OF = {"else": ("alt",), "and": ("par", "par_over"), "option": ("critical",)}
_ACC = re.compile(r"^(accTitle|accDescr)\s*:\s*(.*)$")
_COLOR = re.compile(
    r"^(?:rgba?\([^)]*\)|hsla?\([^)]*\)|#[0-9a-fA-F]{3,8}|transparent|(?:"
    + "|".join(
        """aliceblue antiquewhite aqua aquamarine azure beige bisque black
        blanchedalmond blue blueviolet brown burlywood cadetblue chartreuse
        chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan
        darkgoldenrod darkgray darkgreen darkgrey darkkhaki darkmagenta
        darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen
        darkslateblue darkslategray darkslategrey darkturquoise darkviolet
        deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite
        forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green
        greenyellow grey honeydew hotpink indianred indigo ivory khaki lavender
        lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan
        lightgoldenrodyellow lightgray lightgreen lightgrey lightpink
        lightsalmon lightseagreen lightskyblue lightslategray lightslategrey
        lightsteelblue lightyellow lime limegreen linen magenta maroon
        mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen
        mediumslateblue mediumspringgreen mediumturquoise mediumvioletred
        midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive
        olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise
        palevioletred papayawhip peachpuff peru pink plum powderblue purple
        rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown
        seagreen seashell sienna silver skyblue slateblue slategray slategrey
        snow springgreen steelblue tan teal thistle tomato turquoise violet
        wheat white whitesmoke yellow yellowgreen""".split()
    )
    + r")(?![\w-]))\s*",
    re.I,
)


def _strip_semi(line: str) -> str:
    """Drop a statement-ending ';' but not the one closing an entity (#59;)."""
    line = line.strip()
    if line.endswith(";") and not re.search(r"[#&]\w+;$", line):
        line = line[:-1].rstrip()
    return line


def _strip_color(text: str) -> str:
    m = _COLOR.match(text)
    return text[m.end() :] if m else text


def _acc(line: str, it, title: list[str], descr: list[str]) -> bool:
    """Handle accTitle/accDescr lines (including `accDescr { ... }`)."""
    if m := _ACC.match(line):
        (title if m.group(1) == "accTitle" else descr).extend(clean(m.group(2)))
        return True
    if re.match(r"^accDescr\s*\{", line):
        rest = line.split("{", 1)[1]
        while "}" not in rest:
            descr.extend(clean(rest))
            rest = next(it, "}")
        descr.extend(clean(rest.split("}", 1)[0]))
        return True
    return False


def _parse_sequence(lines: list[str]) -> _Seq:
    seq = _Seq()
    stack: list[str] = []
    number: list[int] | None = None  # [next, step]
    box: int | None = None
    it = iter(lines[1:])
    head = lines[0].split(None, 1)
    if len(head) > 1:  # "sequenceDiagram; A->>B: x" style
        it = iter([s for s in re.split(r";\s*", head[1]) if s] + list(it))

    def part(pid: str) -> str:
        pid = pid.strip()
        if not pid:
            raise _Unsupported("empty participant")
        if pid not in seq.parts:
            seq.parts[pid] = _Part(pid, clean(pid) or [pid], box=box)
        return pid

    for line in it:
        line = _strip_semi(line)
        if not line:
            continue
        if _acc(line, it, seq.title, seq.descr):
            continue
        if m := re.match(r"^title\s*:?\s*(.*)$", line):
            seq.title.extend(clean(m.group(1)))
            continue
        if m := re.match(r"^autonumber(?:\s+(\d+))?(?:\s+(\d+))?$", line):
            number = [int(m.group(1) or 1), int(m.group(2) or 1)]
            continue
        if line == "autonumber off":
            number = None
            continue
        if m := _SEQ_PART.match(line):
            rest = re.sub(r"@\{.*?\}", "", m.group(2)).strip()
            pid, _, alias = rest.partition(" as ")
            pid = part(pid)
            if alias.strip():
                seq.parts[pid].label = clean(alias) or [pid]
            seq.parts[pid].actor = m.group(1) == "actor"
            continue
        if m := re.match(r"^(activate|deactivate)\s+(.+)$", line):
            seq.events.append(_Act(part(m.group(2)), m.group(1) == "activate"))
            continue
        if m := re.match(r"^destroy\s+(.+)$", line):
            seq.destroyed.add(part(m.group(1)))
            continue
        if m := _SEQ_NOTE.match(line):
            ids = [part(p) for p in m.group(2).split(",")]
            pos = m.group(1).lower().split()[0]
            if pos != "over":
                ids = ids[:1]
            seq.events.append(_Note(pos, ids, clean(m.group(3))))
            continue
        if line == "end":
            if not stack:
                raise _Unsupported("end without block")
            kind = stack.pop()
            if kind == "box":
                box = None
            else:
                seq.events.append(_Block("end", []))
            continue
        if m := _SEQ_OPEN.match(line):
            kind, rest = m.group(1), (m.group(2) or "").strip()
            if kind == "box":
                if stack:
                    raise _Unsupported("nested box")
                seq.boxes.append(clean(_strip_color(rest)))
                box = len(seq.boxes) - 1
            else:
                label = [] if kind == "rect" else clean(rest)
                seq.events.append(_Block(kind, label))
            stack.append(kind)
            continue
        if m := _SEQ_BRANCH.match(line):
            if not stack or stack[-1] not in _SEQ_BRANCH_OF[m.group(1)]:
                raise _Unsupported(f"{m.group(1)} outside its block")
            seq.events.append(_Block(m.group(1), clean(m.group(2) or "")))
            continue
        if m := _SEQ_MSG.match(line):
            if m.group("text") is None and not re.search(r"\w", m.group("b")):
                raise _Unsupported(line)
            text = (m.group("text") or "").strip()
            text = re.sub(r"^(?:no)?wrap:\s*", "", text)
            style, headkind = _ARROWS[m.group("arrow")]
            msg = _Msg(part(m.group("a")), part(m.group("b")), style, headkind,
                       clean(text), m.group("act"))
            if number:
                msg.num = number[0]
                number[0] += number[1]
            seq.events.append(msg)
            continue
        raise _Unsupported(line)
    while stack:  # tolerate unclosed blocks
        if stack.pop() != "box":
            seq.events.append(_Block("end", []))
    if not seq.parts:
        raise _Unsupported("no participants")
    return seq


def _render_sequence(seq: _Seq, width: int) -> tuple[str, str]:
    """Draw if possible: find the widest uniform wrap that fits, then give
    each still-wrapped label more room one at a time while it keeps fitting."""
    texts = {("p", p): part.label for p, part in seq.parts.items()}
    for k, ev in enumerate(seq.events):
        if isinstance(ev, (_Msg, _Note)):
            texts[("e", k)] = ev.text
    pieces = [p for t in texts.values() for p in _soft_pieces(" ".join(t))]
    floor = max([12] + [tw(p) for p in pieces])
    longest = max([tw(l) for t in texts.values() for l in t] + [0])
    for cap in [None] + list(range(longest - 1, floor - 1, -1)):
        try:
            _draw_sequence(seq, width, cap, {}, measure=True)
        except _NoFit:
            continue
        caps: dict = {}
        if cap is not None:
            wrapped = sorted(
                (k for k, t in texts.items() if len(wrap_lines(t, cap)) > len(t)),
                key=lambda k: -len(wrap_lines(texts[k], cap)),
            )
            for key in wrapped:
                natural = max(tw(l) for l in texts[key])
                lo, hi = cap, natural  # lo fits; find the widest that fits
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    try:
                        _draw_sequence(seq, width, cap, {**caps, key: mid}, measure=True)
                        lo = mid
                    except _NoFit:
                        hi = mid - 1
                if lo > cap:
                    caps[key] = lo
        for attempt in (caps, {}):
            try:
                lines = _draw_sequence(seq, width, cap, attempt)
            except _NoFit:
                continue
            return "\n".join(_framed(seq.title, lines, seq.descr, width)), "sequence"
    return "\n".join(_sequence_list(seq, width)), "sequence-list"


def _framed(title: list[str], body: list[str], descr: list[str], width: int) -> list[str]:
    """Title above and accessible description below a rendering."""
    out = []
    if title:
        out += wrap_lines(title, width) + [""]
    out += body
    if descr:
        out += [""] + wrap(_flat(descr), width)
    return out


_SOLID = {"solid": "─", "dotted": "╌"}


def _depth(events: list) -> int:
    depth = best = 0
    for ev in events:
        if isinstance(ev, _Block):
            if ev.kind == "end":
                depth -= 1
            elif ev.kind not in _SEQ_BRANCH_OF:
                depth += 1
                best = max(best, depth)
    return best


def _block_title(ev: _Block) -> str:
    label = _flat(ev.label)
    if ev.kind == "rect":
        return ""
    return f"{ev.kind} [{label}]" if label else ev.kind


def _msg_lines(msg: _Msg, cap: int | None) -> list[str]:
    text = list(msg.text)
    if msg.num is not None:
        text = [f"{msg.num}.{NBSP}" + (text[0] if text else "")] + text[1:]
    return wrap_lines(text, cap)


def _draw_sequence(seq: _Seq, width: int, cap: int | None, caps: dict,
                   measure: bool = False) -> list[str]:
    """Draw a sequence diagram; labels wrap at caps[key] or else `cap`."""
    ids = list(seq.parts)
    idx = {p: i for i, p in enumerate(ids)}
    n = len(ids)
    labels = [wrap_lines(seq.parts[p].label, caps.get(("p", p), cap)) for p in ids]
    actor = [seq.parts[p].actor for p in ids]
    bw = [max(tw(l) for l in lab) + (0 if a else 4) for lab, a in zip(labels, actor)]
    bw = [max(b, 3) for b in bw]
    boxes = [seq.parts[p].box for p in ids]
    box_labels = [wrap_lines(b, cap) for b in seq.boxes]
    for b, blab in enumerate(box_labels):  # a lone participant's box needs room for the label
        members = [i for i in range(n) if boxes[i] == b]
        if len(members) == 1 and blab:
            bw[members[0]] = max(bw[members[0]], max(tw(l) for l in blab) + 2)
    lext = [(b - 1) // 2 for b in bw]
    rext = [b - 1 - (b - 1) // 2 for b in bw]
    cons: list[tuple[int, int, int]] = []
    left_need = lext[0]
    right_need = rext[-1]

    def box_gap(i: int) -> int:  # extra room for box borders between i and i+1
        extra = 0
        if boxes[i] is not None and boxes[i] != boxes[i + 1]:
            extra += 2
        if boxes[i + 1] is not None and boxes[i] != boxes[i + 1]:
            extra += 2
        return extra

    for i in range(n - 1):
        cons.append((i, i + 1, rext[i] + lext[i + 1] + 2 + box_gap(i)))
    if boxes[0] is not None:
        left_need += 2
    if boxes[-1] is not None:
        right_need += 2
    for b, blab in enumerate(box_labels):
        members = [i for i in range(n) if boxes[i] == b]
        if len(members) > 1 and blab:
            need = max(tw(l) for l in blab) + 2 - lext[members[0]] - rext[members[-1]]
            cons.append((members[0], members[-1], need))

    prepared = []
    for k, ev in enumerate(seq.events):
        ecap = caps.get(("e", k), cap)
        if isinstance(ev, _Msg):
            lines = _msg_lines(ev, ecap)
            L = max([tw(l) for l in lines] + [0])
            a, b = idx[ev.src], idx[ev.dst]
            if a == b:
                if a < n - 1:
                    cons.append((a, a + 1, max(L, 3) + 3))
                else:
                    right_need = max(right_need, max(L, 3) + 2)
            else:
                lo, hi = sorted((a, b))
                cons.append((lo, hi, L + 4))
            prepared.append((ev, lines))
        elif isinstance(ev, _Note):
            lines = wrap_lines(ev.text, ecap) or [""]
            nw = max(tw(l) for l in lines) + 4
            ps = sorted(idx[p] for p in ev.parts)
            if ev.pos == "over" and len(ps) == 1 or ev.pos == "over" and ps[0] == ps[-1]:
                i = ps[0]
                l, r = (nw - 1) // 2, nw - 1 - (nw - 1) // 2
                if i < n - 1:
                    cons.append((i, i + 1, r + 2))
                else:
                    right_need = max(right_need, r)
                if i > 0:
                    cons.append((i - 1, i, l + 2))
                else:
                    left_need = max(left_need, l)
            elif ev.pos == "over":
                i, j = ps[0], ps[-1]
                cons.append((i, j, nw - 5))
                if i > 0:
                    cons.append((i - 1, i, 4))
                else:
                    left_need = max(left_need, 2)
                if j < n - 1:
                    cons.append((j, j + 1, 4))
                else:
                    right_need = max(right_need, 2)
            elif ev.pos == "right":
                i = ps[0]
                if i < n - 1:
                    cons.append((i, i + 1, nw + 3))
                else:
                    right_need = max(right_need, nw + 1)
            else:
                i = ps[0]
                if i > 0:
                    cons.append((i - 1, i, nw + 3))
                else:
                    left_need = max(left_need, nw + 1)
            prepared.append((ev, lines))
        else:
            prepared.append((ev, None))

    gaps = [0] * max(n - 1, 0)
    for i, j, need in sorted(cons, key=lambda c: (c[1] - c[0], c[2])):
        have = sum(gaps[i:j])
        if have < need:
            deficit = need - have
            k = j - i
            for g in range(i, j):
                gaps[g] += deficit // k + (1 if (g - i) >= k - deficit % k else 0)
    depth = _depth(seq.events)
    inset = 2 * depth + (1 if depth else 0)
    xs = [inset + left_need]
    for g in gaps:
        xs.append(xs[-1] + g)
    W = xs[-1] + right_need + 1 + inset
    if W > width:
        raise _NoFit
    if measure:
        return []
    if cap is not None:  # give each label all the room the layout leaves it
        lo_edge, hi_edge = inset, width - 1 - inset

        def room_right(i: int) -> int:
            return (xs[i + 1] if i < n - 1 else hi_edge + 2) - xs[i] - 3

        def room_left(i: int) -> int:
            return xs[i] - (xs[i - 1] if i > 0 else lo_edge - 2) - 3

        for k, (ev, lines) in enumerate(prepared):
            ecap = caps.get(("e", k), cap)
            if isinstance(ev, _Msg):
                a, b = idx[ev.src], idx[ev.dst]
                lo, hi = sorted((a, b))
                room = xs[hi] - xs[lo] - 4 if a != b else room_right(a) - 1
                prepared[k] = (ev, _msg_lines(ev, max(ecap, room)))
            elif isinstance(ev, _Note):
                ps = sorted(idx[p] for p in ev.parts)
                if ev.pos == "over" and ps[0] != ps[-1]:
                    room = xs[ps[-1]] - xs[ps[0]] + 5 - 4
                elif ev.pos == "over":
                    half = min(room_left(ps[0]), room_right(ps[0])) + 1
                    room = 2 * half + 1 - 4
                elif ev.pos == "right":
                    room = room_right(ps[0]) - 4
                else:
                    room = room_left(ps[0]) - 4
                prepared[k] = (ev, wrap_lines(ev.text, max(ecap, room)) or [""])
        right = right_need  # the last lifeline's labels may now reach further
        for ev, lines in prepared:
            L = max([tw(l) for l in lines or [""]])
            if isinstance(ev, _Msg) and ev.src == ev.dst == ids[-1]:
                right = max(right, L + 2)
            elif isinstance(ev, _Note) and ev.parts[0] == ids[-1] and ev.pos == "right":
                right = max(right, L + 5)
            elif isinstance(ev, _Note) and ev.pos == "over" and idx[max(ev.parts, key=idx.get)] == n - 1:
                single = len({idx[p] for p in ev.parts}) == 1
                right = max(right, (L + 4) - 1 - (L + 3) // 2 if single else 2)
        W = min(width, max(W, xs[-1] + right + 1 + inset))
    grid = Grid(W)
    act = [0] * n
    frames: list[tuple[int, str]] = []  # (depth, style)
    gone: set[int] = set()

    def lifeline(i: int) -> str:
        return "┃" if act[i] > 0 else "│"

    def new_row() -> int:
        r = len(grid.rows)
        grid.ensure(r, W - 1)
        for i in range(n):
            if i not in gone:
                grid.put(r, xs[i], lifeline(i))
        for d, style in frames:
            side = "┆" if style == "rect" else "│"
            grid.put(r, 2 * d, side)
            grid.put(r, W - 1 - 2 * d, side)
        return r

    # header
    box_rows = 2 if seq.boxes else 0
    H = max(len(lab) + (2 if a else 2) for lab, a in zip(labels, actor))
    top = 1 if seq.boxes else 0
    for _ in range(H + box_rows):
        grid.ensure(len(grid.rows), W - 1)
    for i in range(n):
        x = xs[i]
        lab = labels[i]
        if actor[i]:
            r0 = top + H - (2 + len(lab))
            grid.put(r0, x, "o")
            grid.text(r0 + 1, x - 1, "/|\\")
            for k, l in enumerate(lab):
                grid.text(r0 + 2 + k, x - (tw(l) - 1) // 2, l)
        else:
            x0, x1 = x - lext[i], x + rext[i]
            _box(grid, top, x0, top + H - 1, x1, "┌┐└┘─│")
            grid.put(top + H - 1, x, "┬")
            inner = x1 - x0 - 1
            for k, l in enumerate(lab):
                pad = (inner - tw(l)) // 2
                grid.text(top + 1 + (H - 2 - len(lab)) // 2 + k, x0 + 1 + pad, l)
    for b, blab in enumerate(box_labels):
        members = [i for i in range(n) if boxes[i] == b]
        if not members:
            continue
        x0 = xs[members[0]] - lext[members[0]] - 2
        x1 = xs[members[-1]] + rext[members[-1]] + 2
        _box(grid, 0, x0, H + 1, x1, "┌┐└┘─│")
        for i in members:
            grid.put(H + 1, xs[i], "┼" if not actor[i] else "┼")
        title = _flat(blab)
        if title:
            grid.text(0, x0 + 2, f" {title} ")
    if seq.boxes:  # lifelines through the box bottoms for actors and others
        for i in range(n):
            if boxes[i] is None:
                grid.put(H + 1, xs[i], "│")

    def blank() -> None:
        new_row()

    def text_rows(lines: list[str], x0: int, x1: int) -> None:
        """Centre text lines between columns x0 and x1 (exclusive). Text that
        would end right next to a lifeline it crosses is moved to cover it."""
        inner = [x for x in xs if x0 < x < x1]
        block = any(l[:1] == " " for l in lines)  # keep indented lines aligned
        bw = max([tw(l) for l in lines] + [0])
        for l in lines:
            r = new_row()
            w = bw if block else tw(l)
            start = x0 + 1 + max((x1 - x0 - 1 - w) // 2, 0)
            for _ in range(3):
                end = start + w - 1
                if start - 1 in inner:
                    start += -2 if start - 2 > x0 else 1
                elif end + 1 in inner:
                    start += 2 if end + 2 < x1 else -1
                else:
                    break
            grid.text(r, start, l)

    for ev, lines in prepared:
        if isinstance(ev, _Act):
            i = idx[ev.part]
            act[i] = act[i] + 1 if ev.on else max(0, act[i] - 1)
            continue
        if isinstance(ev, _Msg):
            a, b = idx[ev.src], idx[ev.dst]
            blank()
            ch = _SOLID[ev.line]
            if a == b:
                for l in lines:
                    r = new_row()
                    grid.text(r, xs[a] + 2, l)
                if ev.act == "+":
                    act[b] += 1
                r = new_row()
                x = xs[a]
                grid.put(r, x, "┠" if act[a] else "├")
                grid.text(r, x + 1, ch * 2 + "┐")
                r = new_row()
                head = {"arrow": "◄", "open": "<", "cross": "x", "none": ch, "both": "◄"}[ev.head]
                grid.text(r, x + 1, head + ch + "┘")
                if ev.act == "-":
                    act[a] = max(0, act[a] - 1)
                continue
            lo, hi = sorted((a, b))
            text_rows(lines, xs[lo], xs[hi])
            if ev.act == "+":
                act[b] += 1
            r = new_row()
            for x in range(xs[lo] + 1, xs[hi]):
                grid.put(r, x, ch)
            right = b > a
            heads = {"arrow": "►◄", "open": "><", "cross": "xx", "none": "", "both": "►◄"}
            hd = heads[ev.head]
            if hd:
                grid.put(r, xs[b] - 1 if right else xs[b] + 1, hd[0] if right else hd[1])
            if ev.head == "both":
                grid.put(r, xs[a] + 1 if right else xs[a] - 1, hd[1] if right else hd[0])
            else:
                junction = ("┠" if act[a] else "├") if right else ("┨" if act[a] else "┤")
                grid.put(r, xs[a], junction)
            if ev.head == "none":
                grid.put(r, xs[b], ("┨" if act[b] else "┤") if right else ("┠" if act[b] else "├"))
            if ev.act == "-":
                act[a] = max(0, act[a] - 1)
            continue
        if isinstance(ev, _Note):
            blank()
            ps = sorted(idx[p] for p in ev.parts)
            nw = max(tw(l) for l in lines) + 4
            if ev.pos == "over" and ps[0] == ps[-1]:
                x0 = xs[ps[0]] - (nw - 1) // 2
                x1 = x0 + nw - 1
            elif ev.pos == "over":
                x0, x1 = xs[ps[0]] - 2, xs[ps[-1]] + 2
            elif ev.pos == "right":
                x0 = xs[ps[0]] + 2
                x1 = x0 + nw - 1
            else:
                x1 = xs[ps[0]] - 2
                x0 = x1 - nw + 1
            r0 = len(grid.rows)
            for _ in range(len(lines) + 2):
                new_row()
            _box(grid, r0, x0, r0 + len(lines) + 1, x1, "╭╮╰╯─│", fill=True)
            block = max(tw(l) for l in lines)
            pad = (x1 - x0 - 1 - block) // 2
            for k, l in enumerate(lines):
                grid.text(r0 + 1 + k, x0 + 1 + pad, l)
            continue
        # blocks
        if ev.kind == "end":
            blank()
            d, style = frames.pop()
            r = new_row()
            _hborder(grid, r, 2 * d, W - 1 - 2 * d, "┄" if style == "rect" else "─",
                     "└┘", xs, gone)
            continue
        if ev.kind in _SEQ_BRANCH_OF:
            d, style = frames[-1]
            blank()
            r = new_row()
            _hborder(grid, r, 2 * d, W - 1 - 2 * d, "╌", "├┤", xs, gone)
            title_lines = wrap(f"{ev.kind} [{_flat(ev.label)}]" if ev.label else ev.kind,
                               W - 4 * d - 6)
            grid.text(r, 2 * d + 2, f" {title_lines[0]} ")
            for l in title_lines[1:]:
                r = new_row()
                grid.text(r, 2 * d + 3, l)
            continue
        d = len(frames)
        style = ev.kind
        blank()
        r = new_row()
        _hborder(grid, r, 2 * d, W - 1 - 2 * d, "┄" if style == "rect" else "─", "┌┐", xs, gone)
        frames.append((d, style))
        title = _block_title(ev)
        if title:
            title_lines = wrap(title, W - 4 * d - 6)
            grid.text(r, 2 * d + 2, f" {title_lines[0]} ")
            for l in title_lines[1:]:
                r = new_row()
                grid.text(r, 2 * d + 3, l)
    blank()
    rows = len(grid.rows)
    if rows > 40:  # long diagram: repeat the participants at the bottom
        r0 = rows
        for _ in range(H):
            grid.ensure(len(grid.rows), W - 1)
        for i in range(n):
            x = xs[i]
            lab = labels[i]
            if actor[i]:
                grid.put(r0, x, "o")
                grid.text(r0 + 1, x - 1, "/|\\")
                for k, l in enumerate(lab):
                    grid.text(r0 + 2 + k, x - (tw(l) - 1) // 2, l)
            else:
                x0, x1 = x - lext[i], x + rext[i]
                _box(grid, r0, x0, r0 + H - 1, x1, "┌┐└┘─│")
                grid.put(r0, x, "┴")
                inner = x1 - x0 - 1
                for k, l in enumerate(lab):
                    pad = (inner - tw(l)) // 2
                    grid.text(r0 + 1 + (H - 2 - len(lab)) // 2 + k, x0 + 1 + pad, l)
    out = grid.lines()
    if max(tw(l) for l in out) > width:
        raise _NoFit
    return out


def _box(grid: Grid, r0: int, c0: int, r1: int, c1: int, chars: str, fill: bool = False) -> None:
    """Draw a rectangle; chars are TL TR BL BR horizontal vertical."""
    tl, tr, bl, br, h, v = chars
    for c in range(c0 + 1, c1):
        grid.put(r0, c, h)
        grid.put(r1, c, h)
    for r in range(r0 + 1, r1):
        grid.put(r, c0, v)
        grid.put(r, c1, v)
        if fill:
            for c in range(c0 + 1, c1):
                grid.put(r, c, " ")
    grid.put(r0, c0, tl)
    grid.put(r0, c1, tr)
    grid.put(r1, c0, bl)
    grid.put(r1, c1, br)


def _hborder(grid: Grid, r: int, c0: int, c1: int, h: str, ends: str, xs: list[int], gone: set) -> None:
    """A frame border row crossing the lifelines."""
    for c in range(c0 + 1, c1):
        grid.put(r, c, h)
    for i, x in enumerate(xs):
        if c0 < x < c1 and i not in gone:
            grid.put(r, x, "┼")
    grid.put(r, c0, ends[0])
    grid.put(r, c1, ends[1])


_LIST_ARROW = {
    ("solid", "arrow"): "──►",
    ("dotted", "arrow"): "╌╌►",
    ("solid", "open"): "──>",
    ("dotted", "open"): "╌╌>",
    ("solid", "cross"): "──x",
    ("dotted", "cross"): "╌╌x",
    ("solid", "none"): "───",
    ("dotted", "none"): "╌╌╌",
    ("solid", "both"): "◄─►",
    ("dotted", "both"): "◄╌►",
}


def _emit(out: list[str], prefix: str, cont: str, text_lines: list[str], width: int) -> None:
    """Append text lines after `prefix`, wrapping under the hanging indent `cont`."""
    for i, line in enumerate(text_lines or [""]):
        lead = prefix if i == 0 else cont
        pieces = wrap(line, max(1, width - max(tw(lead), tw(cont))))
        out.append(lead + pieces[0])
        out.extend(cont + piece for piece in pieces[1:])


def _sequence_list(seq: _Seq, width: int) -> list[str]:
    """Structured rendering: participants, then numbered messages and notes."""
    name = {p: _flat(part.label) for p, part in seq.parts.items()}
    out: list[str] = []
    if seq.title:
        out += wrap_lines(seq.title, width) + [""]
    out.append("Participants:")
    by_box: dict[int | None, list[str]] = defaultdict(list)
    for p, part in seq.parts.items():
        by_box[part.box].append(p)
    for b in [None] + list(range(len(seq.boxes))):
        members = by_box.get(b, [])
        if not members:
            continue
        indent = "  "
        if b is not None:
            _emit(out, "  ", "    ", [f"Group: {_flat(seq.boxes[b])}" if seq.boxes[b] else "Group:"], width)
            indent = "    "
        for p in members:
            kind = " (actor)" if seq.parts[p].actor else ""
            _emit(out, indent + "• ", indent + "  ", [name[p] + kind], width)
    out.append("")
    nums = [ev.num for ev in seq.events if isinstance(ev, _Msg) and ev.num is not None]
    count = sum(isinstance(ev, _Msg) for ev in seq.events)
    numw = len(str(max(nums + [count, 1])))
    step = 0
    depth = 0
    for ev in seq.events:
        bars = "│ " * depth
        if isinstance(ev, _Msg):
            step += 1
            num = ev.num if ev.num is not None else step
            head = f"{bars}{num:>{numw}}. "
            cont = bars + " " * (numw + 4)
            arrow = _LIST_ARROW[(ev.line, ev.head)]
            text = list(ev.text)
            first = f"{name[ev.src]} {arrow} {name[ev.dst]}" + (f": {text[0]}" if text else "")
            _emit(out, head, cont, [first], width)
            for line in text[1:]:
                _emit(out, cont, cont, [line], width)
        elif isinstance(ev, _Note):
            who = ", ".join(name[p] for p in ev.parts)
            where = {"over": "over", "left": "left of", "right": "right of"}[ev.pos]
            pad = bars + " " * (numw + 2)
            _emit(out, pad, pad + "  ", [f"Note {where} {who}: " + (ev.text[0] if ev.text else "")], width)
            for line in ev.text[1:]:
                _emit(out, pad + "  ", pad + "  ", [line], width)
        elif isinstance(ev, _Block):
            if ev.kind == "end":
                depth -= 1
                out.append("│ " * depth + "└─")
            elif ev.kind in _SEQ_BRANCH_OF:
                bars = "│ " * (depth - 1)
                _emit(out, bars + "├─ ", bars + "│    ", [_block_title(ev)], width)
            else:
                title = _block_title(ev) or "(highlighted)"
                _emit(out, bars + "┌─ ", bars + "│    ", [title], width)
                depth += 1
    if seq.descr:
        out += [""] + wrap(_flat(seq.descr), width)
    return out




# --- flowcharts and state diagrams: model and parsers -----------------------


@dataclass
class _GNode:
    id: str
    label: list[str]
    shape: str = "rect"
    notes: list[tuple[str, list[str]]] = field(default_factory=list)  # (side, lines)


@dataclass
class _GEdge:
    src: str
    dst: str
    label: list[str] = field(default_factory=list)
    line: str = "solid"  # solid / dotted / thick / invisible
    head_src: str = ""  # "" / arrow / circle / cross
    head_dst: str = "arrow"


@dataclass
class _Cluster:
    id: str
    title: list[str]
    parent: str | None


@dataclass
class _Graph:
    direction: str = "TB"
    nodes: dict[str, _GNode] = field(default_factory=dict)
    edges: list[_GEdge] = field(default_factory=list)
    clusters: dict[str, _Cluster] = field(default_factory=dict)
    member: dict[str, str] = field(default_factory=dict)  # node -> innermost cluster
    title: list[str] = field(default_factory=list)
    descr: list[str] = field(default_factory=list)
    cluster_edges: bool = False  # some edge or note is attached to a subgraph
    cluster_notes: list[tuple[str, str, list[str]]] = field(default_factory=list)


_FLOW_HEAD = re.compile(r"^(?:graph|flowchart)(?:\s+(TB|TD|BT|RL|LR))?\s*(?:;|\s|$)\s*(.*)$")
_FLOW_SKIP = re.compile(r"^(?:classDef|class|style|linkStyle|click|direction)\b")
_NODE_ID = re.compile(r"[\w$](?:[\w.$]|-(?=[\w$]))*")
_SHAPES = [
    ("(((", (")))",), "circle"),
    ("([", ("])",), "stadium"),
    ("[[", ("]]",), "subroutine"),
    ("[(", (")]",), "cylinder"),
    ("((", ("))",), "circle"),
    ("{{", ("}}",), "hexagon"),
    ("[/", ("/]", "\\]"), "lean"),
    ("[\\", ("\\]", "/]"), "lean"),
    ("[", ("]",), "rect"),
    ("(", (")",), "round"),
    ("{", ("}",), "diamond"),
    (">", ("]",), "flag"),
]
_NEW_SHAPES = {
    "rounded": "round", "event": "round", "stadium": "stadium", "pill": "stadium",
    "terminal": "stadium", "subproc": "subroutine", "subroutine": "subroutine",
    "cyl": "cylinder", "cylinder": "cylinder", "db": "cylinder", "database": "cylinder",
    "circle": "circle", "circ": "circle", "diam": "diamond", "diamond": "diamond",
    "decision": "diamond", "question": "diamond", "hex": "hexagon", "hexagon": "hexagon",
}
_EDGE = re.compile(
    r"(?:[\w-]+@)?(?P<lh>[<ox](?=[-=.]))?(?P<body>-{2,}|={2,}|-\.+-?|~{3,})(?P<rh>>|[ox](?!\w))?"
)
_EDGE_CLOSE = {
    "-": re.compile(r"\s*(?P<t>.*?)\s*(?P<c>-{2,}>|-{2,}[ox](?!\w)|-{3,})"),
    "=": re.compile(r"\s*(?P<t>.*?)\s*(?P<c>={2,}>|={2,}[ox](?!\w)|={3,})"),
    ".": re.compile(r"\s*(?P<t>.*?)\s*(?P<c>\.+-+>|\.+-+[ox](?!\w)|\.+-+)"),
}
_PIPE = re.compile(r"\s*\|(?P<t>[^|]*)\|")
_HEAD = {">": "arrow", "<": "arrow", "o": "circle", "x": "cross"}


def _unquote(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] == '"':
        text = text[1:-1]
    if len(text) >= 2 and text[0] == text[-1] == "`":  # markdown string
        text = text[1:-1].replace("**", "")
    return text


def _split_statements(line: str) -> list[str]:
    """Split on ';' outside quotes, brackets and |edge labels|."""
    out, cur, depth, quote, pipe = [], [], 0, False, False
    for ch in line:
        if ch == '"':
            quote = not quote
        elif not quote:
            if ch in "[({":
                depth += 1
            elif ch in "])}":
                depth = max(0, depth - 1)
            elif ch == "|" and depth == 0:
                pipe = not pipe
            elif ch == ";" and depth == 0 and not pipe:
                out.append("".join(cur))
                cur = []
                continue
        cur.append(ch)
    out.append("".join(cur))
    return [x.strip() for x in out if x.strip()]


class _Cursor:
    def __init__(self, s: str):
        self.s, self.i = s, 0

    def ws(self) -> None:
        while self.i < len(self.s) and self.s[self.i].isspace():
            self.i += 1

    def done(self) -> bool:
        self.ws()
        return self.i >= len(self.s)


def _flow_node(cur: _Cursor, g: _Graph, mentions: list[str]) -> str:
    cur.ws()
    m = _NODE_ID.match(cur.s, cur.i)
    if not m:
        raise _Unsupported(cur.s[cur.i :])
    nid, cur.i = m.group(0), m.end()
    label, shape = None, None
    s = cur.s
    if s.startswith("@{", cur.i):
        end = s.find("}", cur.i)
        if end < 0:
            raise _Unsupported("unclosed @{")
        body = s[cur.i + 2 : end]
        cur.i = end + 1
        if lm := re.search(r'label\s*:\s*"((?:[^"\\]|\\.)*)"', body):
            label = lm.group(1)
        elif lm := re.search(r"label\s*:\s*([^,]+)", body):
            label = lm.group(1).strip()
        if sm := re.search(r"shape\s*:\s*([\w-]+)", body):
            shape = _NEW_SHAPES.get(sm.group(1), "rect")
    else:
        for opener, closers, shp in _SHAPES:
            if not s.startswith(opener, cur.i):
                continue
            j = cur.i + len(opener)
            if j < len(s) and s[j] == '"':
                q = s.find('"', j + 1)
                if q < 0:
                    raise _Unsupported("unclosed quote")
                text, k = s[j : q + 1], q + 1
                while k < len(s) and s[k] == " ":
                    k += 1
                close = next((c for c in closers if s.startswith(c, k)), None)
                if close is None:
                    raise _Unsupported("bad shape")
                end = k
            else:
                found = [(s.find(c, j), c) for c in closers if s.find(c, j) >= 0]
                if not found:
                    raise _Unsupported("unclosed shape")
                end, close = min(found)
                text = s[j:end]
            label, shape = text, shp
            cur.i = end + len(close)
            break
    if cm := re.compile(r":::[\w-]+").match(s, cur.i):
        cur.i = cm.end()
    node = g.nodes.get(nid)
    if node is None:
        node = g.nodes[nid] = _GNode(nid, [nid])
    if label is not None:
        node.label = clean(_unquote(label))
    if shape is not None:
        node.shape = shape
    mentions.append(nid)
    return nid


def _flow_group(cur: _Cursor, g: _Graph, mentions: list[str]) -> list[str]:
    ids = [_flow_node(cur, g, mentions)]
    while True:
        cur.ws()
        if cur.s.startswith("&", cur.i):
            cur.i += 1
            ids.append(_flow_node(cur, g, mentions))
        else:
            return ids


def _flow_edge(cur: _Cursor) -> tuple[list[str], str, str, str]:
    cur.ws()
    m = _EDGE.match(cur.s, cur.i)
    if not m:
        raise _Unsupported(cur.s[cur.i :])
    cur.i = m.end()
    lh, body, rh = m.group("lh") or "", m.group("body"), m.group("rh") or ""
    text = ""
    opener = not rh and (body in ("--", "==") or re.fullmatch(r"-\.+", body))
    if opener:
        kind = "." if "." in body else body[0]
        cm = _EDGE_CLOSE[kind].match(cur.s, cur.i)
        if not cm:
            raise _Unsupported("unterminated edge label")
        text, cur.i = cm.group("t"), cm.end()
        close = cm.group("c")
        rh = close[-1] if close[-1] in ">ox" else ""
        body += close
    if pm := _PIPE.match(cur.s, cur.i):
        text, cur.i = (text + " " if text else "") + pm.group("t"), pm.end()
    if "~" in body:
        line = "invisible"
    elif "=" in body:
        line = "thick"
    elif "." in body:
        line = "dotted"
    else:
        line = "solid"
    return clean(_unquote(text)), line, _HEAD.get(lh, ""), _HEAD.get(rh, "")


def _parse_flowchart(lines: list[str]) -> _Graph:
    m = _FLOW_HEAD.match(lines[0])
    if not m:
        raise _Unsupported(lines[0])
    g = _Graph(direction={"TD": "TB"}.get(m.group(1) or "TB", m.group(1) or "TB"))
    body = ([m.group(2)] if m.group(2) else []) + lines[1:]
    stack: list[tuple[str | None, list[str]]] = [(None, [])]  # (cluster, mentions)
    it = iter(body)
    for raw in it:
        if _acc(raw, it, g.title, g.descr):
            continue
        for st in _split_statements(raw):
            if st == "end":
                if len(stack) == 1:
                    raise _Unsupported("end without subgraph")
                cid, mentions = stack.pop()
                for nid in mentions:
                    g.member.setdefault(nid, cid)
                continue
            if sm := re.match(r"^subgraph\b\s*(.*)$", st):
                rest = sm.group(1).strip()
                if bm := re.match(r"^([^\s\[]+)\s*\[(.*)\]$", rest):
                    cid, title = bm.group(1), _unquote(bm.group(2))
                else:
                    cid = title = _unquote(rest)
                if not cid or cid in g.clusters:
                    cid = f"{cid}#{len(g.clusters)}"
                g.clusters[cid] = _Cluster(cid, clean(title), stack[-1][0])
                stack[-1][1].append(cid)
                stack.append((cid, []))
                continue
            if _FLOW_SKIP.match(st) or st.startswith(("title ", "accTitle", "accDescr")):
                if st.startswith("title "):
                    g.title.extend(clean(st[6:]))
                continue
            cur = _Cursor(st)
            group = _flow_group(cur, g, stack[-1][1])
            while not cur.done():
                label, line, hs, hd = _flow_edge(cur)
                nxt = _flow_group(cur, g, stack[-1][1])
                for a in group:
                    for b in nxt:
                        g.edges.append(_GEdge(a, b, label, line, hs, hd))
                group = nxt
    while len(stack) > 1:
        cid, mentions = stack.pop()
        for nid in mentions:
            g.member.setdefault(nid, cid)
    for cid in g.clusters:  # edges to a subgraph: drop the stand-in node
        if cid in g.nodes:
            del g.nodes[cid]
            g.cluster_edges = True
    for nid in list(g.member):
        if nid in g.clusters or nid not in g.nodes:
            del g.member[nid]
    if not g.nodes and not g.clusters:
        raise _Unsupported("empty flowchart")
    return g


_STATE_ID = r"[\w.$-]+|\[\*\]"


def _parse_state(lines: list[str]) -> _Graph:
    g = _Graph(direction="TB")
    stack: list[str | None] = [None]
    it = iter(lines[1:])

    def node(raw: str, as_src: bool) -> str:
        raw = re.sub(r":::[\w-]+$", "", raw.strip())
        scope = stack[-1]
        if raw == "[*]":
            nid = f"[*]{'start' if as_src else 'end'}:{scope or ''}"
            if nid not in g.nodes:
                g.nodes[nid] = _GNode(nid, [], "start" if as_src else "end")
        else:
            nid = raw
            if nid not in g.nodes and nid not in g.clusters:
                g.nodes[nid] = _GNode(nid, [nid], "state")
        if scope is not None and nid in g.nodes:
            g.member.setdefault(nid, scope)
        return nid

    for line in it:
        line = _strip_semi(line)
        if not line or _acc(line, it, g.title, g.descr):
            continue
        if m := re.match(r"^direction\s+(TB|TD|BT|RL|LR)$", line):
            if len(stack) == 1:
                g.direction = {"TD": "TB"}.get(m.group(1), m.group(1))
            continue
        if line == "--" or _FLOW_SKIP.match(line):
            continue
        if m := re.match(r"^title\s*:?\s*(.*)$", line):
            g.title.extend(clean(m.group(1)))
            continue
        note = re.match(rf"^note\s+(left|right)\s+of\s+({_STATE_ID})\s*(?::\s*(.*))?$", line, re.I)
        if note:
            text: list[str] = []
            if note.group(3) is not None:
                text = clean(note.group(3))
            else:
                for nl in it:
                    if nl.strip().lower() == "end note":
                        break
                    text.extend(clean(nl))
            side, target = note.group(1).lower(), node(note.group(2), False)
            if target in g.clusters:
                g.cluster_notes.append((target, side, text))
                g.cluster_edges = True
            else:
                g.nodes[target].notes.append((side, text))
            continue
        if line == "}":
            if len(stack) == 1:
                raise _Unsupported("unbalanced }")
            stack.pop()
            continue
        if m := re.match(r'^state\s+"([^"]*)"\s+as\s+([\w.$-]+)\s*(\{)?$', line):
            label, sid, brace = clean(m.group(1)), m.group(2), m.group(3)
        elif m := re.match(r"^state\s+([\w.$-]+)\s*(?:<<(fork|join|choice)>>)?\s*(\{)?$", line):
            label, sid, brace = None, m.group(1), m.group(3)
            if m.group(2):
                n = g.nodes[node(sid, False)]
                n.shape = {"choice": "choice"}.get(m.group(2), "bar")
                n.label = []
                continue
        elif m := re.match(r"^state\s+([\w.$-]+)\s+as\s+\"([^\"]*)\"\s*(\{)?$", line):
            sid, label, brace = m.group(1), clean(m.group(2)), m.group(3)
        else:
            sid = None
        if sid is not None:
            if brace:
                if sid in g.clusters:
                    raise _Unsupported(f"composite state {sid} defined twice")
                title = label or [sid]
                g.clusters[sid] = _Cluster(sid, title, stack[-1])
                g.nodes.pop(sid, None)
                stack.append(sid)
            else:
                n = g.nodes[node(sid, False)]
                if label:
                    n.label = label
            continue
        if m := re.match(rf"^({_STATE_ID}(?::::[\w-]+)?)\s*-->\s*({_STATE_ID}(?::::[\w-]+)?)\s*(?::(.*))?$", line):
            a, b = node(m.group(1), True), node(m.group(2), False)
            g.edges.append(_GEdge(a, b, clean(m.group(3) or "")))
            continue
        if m := re.match(r"^(?:state\s+)?([\w.$-]+)\s*:\s*(.*)$", line):
            n = g.nodes[node(m.group(1), False)]
            n.label = n.label + clean(m.group(2))
            continue
        if m := re.match(r"^([\w.$-]+)$", line):
            node(m.group(1), False)
            continue
        raise _Unsupported(line)
    for e in g.edges:
        if e.src in g.clusters or e.dst in g.clusters:
            g.cluster_edges = True
    for cid in g.clusters:
        g.nodes.pop(cid, None)
        g.member.pop(cid, None)
    if not g.nodes and not g.clusters:
        raise _Unsupported("empty state diagram")
    return g


# --- flowcharts and state diagrams: layered drawing -------------------------

_LIGHT = {
    "NS": "│", "EW": "─", "ES": "┌", "SW": "┐", "EN": "└", "NW": "┘", "ENS": "├",
    "NSW": "┤", "ESW": "┬", "ENW": "┴", "ENSW": "┼", "N": "│", "S": "│", "E": "─", "W": "─",
}
_HEAVY = {
    "NS": "┃", "EW": "━", "ES": "┏", "SW": "┓", "EN": "┗", "NW": "┛", "ENS": "┣",
    "NSW": "┫", "ESW": "┳", "ENW": "┻", "ENSW": "╋", "N": "┃", "S": "┃", "E": "━", "W": "━",
}
_DOTTED = {"NS": "╎", "EW": "╌", "N": "╎", "S": "╎", "E": "╌", "W": "╌"}


def _dkey(dirs) -> str:
    return "".join(sorted(dirs))


class _Lines:
    """Line pieces that are merged into junctions or drawn as crossings."""

    def __init__(self) -> None:
        self.cells: dict[tuple[int, int], list[tuple[frozenset, str, frozenset]]] = defaultdict(list)

    def add(self, r: int, c: int, dirs, style: str, tags) -> None:
        self.cells[(r, c)].append((frozenset(dirs), style, frozenset(tags)))

    def draw(self, grid: Grid, vertical_wins: bool) -> None:
        for (r, c), contribs in self.cells.items():
            groups: list[list] = []
            for con in contribs:  # group pieces that belong to the same line
                hit = [gr for gr in groups if any(con[2] & o[2] for o in gr)]
                merged = [con]
                for gr in hit:
                    merged += gr
                    groups.remove(gr)
                groups.append(merged)
            if len(groups) > 1:
                main = frozenset("NS") if vertical_wins else frozenset("EW")
                cross = frozenset("EW") if vertical_wins else frozenset("NS")
                dirs = [frozenset().union(*(p[0] for p in gr)) for gr in groups]
                win = [gr for gr, d in zip(groups, dirs) if d <= main]
                lose = [d for gr, d in zip(groups, dirs) if not d <= main]
                if len(win) != 1 or not all(d <= cross for d in lose):
                    raise _NoFit("ambiguous junction")
                groups = win
            pieces = groups[0]
            dirs = frozenset().union(*(p[0] for p in pieces))
            styles = {p[1] for p in pieces}
            key = _dkey(dirs)
            if styles == {"thick"} and key in _HEAVY:
                ch = _HEAVY[key]
            elif styles == {"dotted"} and key in _DOTTED:
                ch = _DOTTED[key]
            else:
                ch = _LIGHT.get(key, "┼")
            grid.put(r, c, ch)


@dataclass(eq=False)
class _It:
    """A layout item: a node, an edge label, or a point an edge passes."""

    kind: str  # node / label / dummy
    band: int
    path: tuple
    seq: float
    node: _GNode | None = None
    lines: list[str] = field(default_factory=list)
    w: int = 1  # natural size on screen
    h: int = 1
    cs: int = 1  # size across ranks
    ms: int = 1  # size along ranks
    box: tuple[int, int, int, int] = (0, 0, 1, 1)  # node box within the item (c, m, cs, ms)
    notes: list = field(default_factory=list)  # (c, cs, ms, lines) note boxes
    ports: dict = field(default_factory=dict)  # (side, head) -> cross offset
    c0: int = 0
    m0: int = 0
    up: list = field(default_factory=list)  # segments above
    lo: list = field(default_factory=list)  # segments below


@dataclass(eq=False)
class _Seg:
    """One stretch of an edge between two adjacent bands."""

    upper: _It
    lower: _It
    head_up: str
    head_lo: str
    line: str
    key_up: tuple = ()
    key_lo: tuple = ()


def _shape_size(shape: str, lines: list[str], vertical: bool) -> tuple[int, int]:
    if shape in ("start", "end", "choice"):
        return 1, 1
    if shape == "bar":
        return (7, 1) if vertical else (1, 5)
    text_w = max([tw(l) for l in lines] + [1])
    w = text_w + 4 + (2 if shape in ("subroutine", "stadium") else 0)
    h = len(lines) + 2 + (1 if shape == "cylinder" else 0)
    return w, h


def _hier_sort(items: list[_It], key: dict, depth: int = 0) -> list[_It]:
    """Sort by key while keeping members of each subgraph together."""
    units: dict = {}
    for it in items:
        u = it.path[depth] if len(it.path) > depth else id(it)
        units.setdefault(u, []).append(it)
    def ukey(members):
        return sum(key[m] for m in members) / len(members)
    out = []
    for u, members in sorted(units.items(), key=lambda kv: ukey(kv[1])):
        if len(members) == 1 and not (len(members[0].path) > depth):
            out += members
        else:
            out += _hier_sort(members, key, depth + 1)
    return out


def _pava(targets: list[float], weights: list[float]) -> list[float]:
    """Weighted least-squares non-decreasing fit (pool adjacent violators)."""
    blocks: list[list[float]] = []
    for t, w in zip(targets, weights):
        blocks.append([w, w * t, 1])
        while len(blocks) > 1 and blocks[-2][1] / blocks[-2][0] > blocks[-1][1] / blocks[-1][0]:
            w2, s2, n2 = blocks.pop()
            blocks[-1][0] += w2
            blocks[-1][1] += s2
            blocks[-1][2] += n2
    out: list[float] = []
    for w, sw, k in blocks:
        out += [sw / w] * int(k)
    return out


def _draw_graph(g: _Graph, direction: str, cap: int | None, width: int) -> list[str]:
    vertical = direction in ("TB", "BT")
    flip = direction in ("BT", "RL")
    if g.cluster_edges or any(e.src == e.dst for e in g.edges):
        raise _Unsupported("edge to a subgraph or to itself")
    names = list(g.nodes)
    if not names:
        raise _Unsupported("no nodes")
    order_of = {n: i for i, n in enumerate(names)}
    edges = g.edges
    cpath: dict[str, tuple] = {}
    for n in names:
        c = g.member.get(n)
        cpath[n] = tuple(reversed(_cluster_chain(g, c))) if c is not None else ()
    used = {c for p in cpath.values() for c in p}
    if set(g.clusters) - used:
        raise _Unsupported("empty subgraph")

    # 1. ranks: reverse back edges found by DFS, then longest path
    succ = defaultdict(list)
    for i, e in enumerate(edges):
        succ[e.src].append(i)
    indeg = defaultdict(int)
    for e in edges:
        indeg[e.dst] += 1
    state: dict[str, int] = {}
    back: set[int] = set()
    for root in [n for n in names if not indeg[n]] + names:
        if root in state:
            continue
        state[root] = 1
        stack = [(root, iter(succ[root]))]
        while stack:
            v, itr = stack[-1]
            for i in itr:
                w = edges[i].dst
                if state.get(w) == 1:
                    back.add(i)
                elif w not in state:
                    state[w] = 1
                    stack.append((w, iter(succ[w])))
                    break
            else:
                state[v] = 2
                stack.pop()
    arcs = []
    for i, e in enumerate(edges):
        u, v = (e.dst, e.src) if i in back else (e.src, e.dst)
        length = 2 if e.label and e.line != "invisible" else 1
        arcs.append((u, v, length, i))
    out = defaultdict(list)
    deg = defaultdict(int)
    for u, v, length, _ in arcs:
        out[u].append((v, length))
        deg[v] += 1
    rank = {n: 0 for n in names}
    ready = [n for n in names if not deg[n]]
    topo = []
    while ready:
        n = ready.pop(0)
        topo.append(n)
        for v, length in out[n]:
            rank[v] = max(rank[v], rank[n] + length)
            deg[v] -= 1
            if not deg[v]:
                ready.append(v)
    if len(topo) != len(names):
        raise _NoFit("cycle")
    for n in reversed(topo):  # pull sources down next to their successors
        if out[n]:
            rank[n] = max(rank[n], min(rank[v] - length for v, length in out[n]))
    R = max(rank.values()) + 1

    # 2. items and segments
    items: list[_It] = []
    node_item: dict[str, _It] = {}
    for n in names:
        nd = g.nodes[n]
        lines = wrap_lines(nd.label, cap)
        w, h = _shape_size(nd.shape, lines, vertical)
        it = _It("node", rank[n], cpath[n], float(order_of[n]), node=nd, lines=lines, w=w, h=h)
        items.append(it)
        node_item[n] = it
    segs: list[_Seg] = []
    for u, v, _, i in arcs:
        e = edges[i]
        if e.line == "invisible":
            continue
        rev = i in back
        common = []
        for a, b in zip(cpath[u], cpath[v]):
            if a != b:
                break
            common.append(a)
        chain = [node_item[u]]
        b = rank[u] + 1
        seq = order_of[u] + 0.5 + i * 1e-4
        if e.label:
            lines = wrap_lines(e.label, cap)
            lw = max(tw(l) for l in lines)
            it = _It("label", b, tuple(common), seq, lines=lines,
                     w=lw if vertical else lw + 2, h=len(lines) if vertical else len(lines) + 1)
            items.append(it)
            chain.append(it)
            b += 1
        while b < rank[v]:
            it = _It("dummy", b, tuple(common), seq)
            items.append(it)
            chain.append(it)
            b += 1
        chain.append(node_item[v])
        hu = e.head_dst if rev else e.head_src
        hl = e.head_src if rev else e.head_dst
        for k in range(len(chain) - 1):
            sg = _Seg(chain[k], chain[k + 1], hu if k == 0 else "",
                      hl if k == len(chain) - 2 else "", e.line)
            chain[k].lo.append(sg)
            chain[k + 1].up.append(sg)
            segs.append(sg)

    # 3. order within bands (barycentres, subgraphs kept together)
    bands: list[list[_It]] = [[] for _ in range(R)]
    for it in items:
        bands[it.band].append(it)
    for b in range(R):
        bands[b] = _hier_sort(bands[b], {it: it.seq for it in bands[b]})
    pos = {it: k for band in bands for k, it in enumerate(band)}

    def crossings() -> int:
        total = 0
        for b in range(R - 1):
            pairs = [(pos[s.upper], pos[s.lower]) for it in bands[b] for s in it.lo]
            for x in range(len(pairs)):
                for y in range(x + 1, len(pairs)):
                    if (pairs[x][0] - pairs[y][0]) * (pairs[x][1] - pairs[y][1]) < 0:
                        total += 1
        return total

    best = (crossings(), [list(b) for b in bands])
    for _ in range(8):
        for rng, attr, other in ((range(1, R), "up", "upper"), (range(R - 2, -1, -1), "lo", "lower")):
            for b in rng:
                key = {}
                for it in bands[b]:
                    nb = [pos[getattr(s, other)] for s in getattr(it, attr)]
                    key[it] = sum(nb) / len(nb) if nb else pos[it]
                bands[b] = _hier_sort(bands[b], key)
                for k, it in enumerate(bands[b]):
                    pos[it] = k
            c = crossings()
            if c < best[0]:
                best = (c, [list(b) for b in bands])
    bands = best[1]
    pos = {it: k for band in bands for k, it in enumerate(band)}

    # 4. sizes and ports
    for it in items:
        if it.kind == "node":
            sides: dict[str, list] = {"start": [], "end": []}
            for s in it.up:
                key = ("start", s.head_lo)
                if key not in sides["start"]:
                    sides["start"].append(key)
            for s in it.lo:
                key = ("end", s.head_up)
                if key not in sides["end"]:
                    sides["end"].append(key)
            bcs, bms = (it.w, it.h) if vertical else (it.h, it.w)
            need = max(len(sides["start"]), len(sides["end"]))
            if it.node.shape in ("start", "end", "choice", "bar"):
                if need > 1:
                    raise _NoFit("too many ports on a small node")
            elif bcs < 2 * need + 1:
                bcs = 2 * need + 1
            if vertical:
                it.w = bcs
            else:
                it.h = bcs
            for side, keys in sides.items():  # spread port groups along the side
                other = "lower" if side == "end" else "upper"
                segl = it.lo if side == "end" else it.up
                def where(k, segl=segl, other=other, side=side):
                    xs = [pos[getattr(s, other)] for s in segl
                          if (side, s.head_up if side == "end" else s.head_lo) == k]
                    return sum(xs) / len(xs)
                keys.sort(key=where)
                if bcs == 1:
                    for k in keys:
                        it.ports[k] = 0
                    continue
                for j, k in enumerate(keys):
                    off = (bcs - 1) // 2 if len(keys) == 1 else round((j + 1) * (bcs - 1) / (len(keys) + 1))
                    it.ports[k] = min(max(off, 1), bcs - 2)
            # notes beside the box (state diagrams)
            before = [l for side, ls in it.node.notes if side == "left" for l in ls + [""]][:-1]
            after = [l for side, ls in it.node.notes if side == "right" for l in ls + [""]][:-1]
            note_parts = []
            for side, text in (("left", before), ("right", after)):
                if not any(t.strip() for t in text):
                    if any(s == side for s, _ in it.node.notes):
                        text = text or [""]
                    else:
                        continue
                text = wrap_lines(text, cap) or [""]
                nw, nh = max([tw(t) for t in text] + [1]) + 4, len(text) + 2
                ncs, nms = (nw, nh) if vertical else (nh, nw)
                note_parts.append((side, ncs, nms, text))
            gap = 3 if vertical else 1
            left = [p for p in note_parts if p[0] == "left"]
            right = [p for p in note_parts if p[0] == "right"]
            cur = 0
            for _, ncs, nms, text in left:
                it.notes.append((cur, ncs, nms, text))
                cur += ncs + gap
            it.box = (cur, 0, bcs, bms)
            for k in it.ports:
                it.ports[k] += cur
            cur += bcs
            for _, ncs, nms, text in right:
                cur += gap
                it.notes.append((cur, ncs, nms, text))
                cur += ncs
            it.cs = cur
            it.ms = max([bms] + [nms for _, _, nms, _ in it.notes])
        elif it.kind == "label":
            it.cs, it.ms = (it.w, it.h) if vertical else (it.h, it.w)
            off = (it.cs - 1) // 2 if vertical else it.cs - 1
            it.ports = {"start": off, "end": off}
        else:
            it.cs, it.ms = 1, 1
            it.ports = {"start": 0, "end": 0}
    for s in segs:
        s.key_up = ("end", s.head_up) if s.upper.kind == "node" else "end"
        s.key_lo = ("start", s.head_lo) if s.lower.kind == "node" else "start"

    # 5. positions across the bands
    base = 2 if vertical else 1

    def sep(a: _It, b: _It) -> int:
        k = 0
        while k < min(len(a.path), len(b.path)) and a.path[k] == b.path[k]:
            k += 1
        return base + 2 * ((len(a.path) - k) + (len(b.path) - k))

    for band in bands:
        x = 0
        for k, it in enumerate(band):
            if k:
                x += sep(band[k - 1], it)
            it.c0 = x
            x += it.cs

    def port(it: _It, key) -> int:
        return it.c0 + it.ports[key]

    def place(band: list[_It], use_up: bool, use_lo: bool) -> None:
        targets, weights, offs = [], [], []
        x = 0
        for k, it in enumerate(band):
            if k:
                x += band[k - 1].cs + sep(band[k - 1], it)
            offs.append(x)
            want = []
            if use_up:
                want += [port(s.upper, s.key_up) - it.ports[s.key_lo] for s in it.up]
            if use_lo:
                want += [port(s.lower, s.key_lo) - it.ports[s.key_up] for s in it.lo]
            weight = len(want) * (2.0 if it.kind != "node" else 1.0)
            targets.append((sum(want) / len(want) if want else it.c0) - x)
            weights.append(weight or 0.05)
        fit = _pava(targets, weights)
        for it, y, x in zip(band, fit, offs):
            it.c0 = int(y + x + 0.5) if y + x >= 0 else -int(-(y + x) + 0.5)

    for _ in range(4):
        for b in range(1, R):
            place(bands[b], True, False)
        for b in range(R - 2, -1, -1):
            place(bands[b], False, True)
    for _ in range(2):
        for b in range(R):
            place(bands[b], True, True)

    def legal(band: list[_It], k: int, c0: int) -> bool:
        it = band[k]
        if k and c0 < band[k - 1].c0 + band[k - 1].cs + sep(band[k - 1], it):
            return False
        if k + 1 < len(band) and c0 + it.cs + sep(it, band[k + 1]) > band[k + 1].c0:
            return False
        return True

    for _ in range(4):  # straighten small jogs
        moved = False
        for band in bands:
            for k, it in enumerate(band):
                ds = [port(s.upper, s.key_up) - port(it, s.key_lo) for s in it.up]
                ds += [port(s.lower, s.key_lo) - port(it, s.key_up) for s in it.lo]
                ds = [d for d in ds if d]
                if not ds:
                    continue
                for d in sorted(set(ds), key=lambda d: (-ds.count(d), abs(d))):
                    if abs(d) <= 4 and legal(band, k, it.c0 + d):
                        it.c0 += d
                        moved = True
                        break
        if not moved:
            break

    # 6. subgraph rectangles across the bands; push things apart until legal
    cl_items: dict[str, list[_It]] = defaultdict(list)
    for it in items:
        for c in it.path:
            cl_items[c].append(it)
    depth_of = {c: len(cpath_of) for c, cpath_of in ((c, _cluster_chain(g, c)) for c in g.clusters)}
    clusters = sorted(cl_items, key=lambda c: -depth_of[c])  # innermost first
    titles = {c: _flat(wrap_lines(g.clusters[c].title, None)) for c in clusters}

    def extents() -> dict[str, list[int]]:
        ext: dict[str, list[int]] = {}
        for c in clusters:
            lo = min(it.c0 for it in cl_items[c])
            hi = max(it.c0 + it.cs - 1 for it in cl_items[c])
            for d in clusters:
                if d in ext and g.clusters[d].parent == c:
                    lo, hi = min(lo, ext[d][0]), max(hi, ext[d][1])
            lo, hi = lo - 2, hi + 2
            if vertical and titles[c]:
                hi = max(hi, lo + tw(titles[c]) + 6)
            bl = min(it.band for it in cl_items[c])
            bh = max(it.band for it in cl_items[c])
            ext[c] = [lo, hi, bl, bh]
        return ext

    for _ in range(300):
        changed = False
        for band in bands:
            for k in range(1, len(band)):
                need = band[k - 1].c0 + band[k - 1].cs + sep(band[k - 1], band[k])
                if band[k].c0 < need:
                    band[k].c0 = need
                    changed = True
        ext = extents()
        for c in clusters:
            lo, hi, bl, bh = ext[c]
            for b in range(bl, bh + 1):
                members = [k for k, it in enumerate(bands[b]) if c in it.path]
                for k, it in enumerate(bands[b]):
                    if c in it.path or it.c0 > hi + 1 or it.c0 + it.cs - 1 < lo - 1:
                        continue
                    after = members and k > members[-1] or not members and it.c0 >= lo
                    if after:
                        delta = hi + 2 - it.c0
                        for x in bands[b][k:]:
                            x.c0 += delta
                    else:
                        delta = it.c0 + it.cs + 1 - lo
                        for x in cl_items[c]:
                            x.c0 += delta
                    changed = True
                    break
                if changed:
                    break
            if changed:
                break
            for d in clusters:  # sibling subgraphs must not overlap
                if d == c or g.clusters[d].parent != g.clusters[c].parent:
                    continue
                dlo, dhi, dbl, dbh = ext[d]
                if dbh < bl or dbl > bh or dhi < lo - 1 or dlo > hi + 1:
                    continue
                ca = sum(it.c0 for it in cl_items[c]) / len(cl_items[c])
                da = sum(it.c0 for it in cl_items[d]) / len(cl_items[d])
                if (ca, c) < (da, d):
                    delta = hi + 2 - dlo
                    move = cl_items[d]
                else:
                    delta = dhi + 2 - lo
                    move = cl_items[c]
                for x in move:
                    x.c0 += delta
                changed = True
                break
            if changed:
                break
        if not changed:
            break
    else:
        raise _NoFit("subgraphs do not settle")
    ext = extents()
    shift = min([it.c0 for it in items] + [e[0] for e in ext.values()])
    for it in items:
        it.c0 -= shift
    for e in ext.values():
        e[0] -= shift
        e[1] -= shift
    cross = max([it.c0 + it.cs for it in items] + [e[1] + 1 for e in ext.values()])
    if vertical and cross > width:
        raise _NoFit("too wide")

    # 7. route each channel between bands
    band_ms = [max([it.ms for it in band if it.kind != "dummy"] + [1]) for band in bands]
    opens = defaultdict(list)  # band -> clusters starting there (outermost first)
    closes = defaultdict(list)  # band -> clusters ending there (innermost first)
    for c in sorted(clusters, key=lambda c: depth_of[c]):
        opens[ext[c][2]].append(c)
    for c in clusters:
        closes[ext[c][3]].append(c)
    channels = []
    for b in range(R - 1):
        nets: dict = {}
        for it in bands[b]:
            for s in it.lo:
                nets.setdefault((id(s.upper), s.key_up), []).append(s)
        netlist = list(nets.values())
        for attempt in range(2):
            info = []
            for nsegs in netlist:
                x = port(nsegs[0].upper, nsegs[0].key_up)
                drops = {}
                for s in nsegs:
                    drops.setdefault((id(s.lower), s.key_lo), (port(s.lower, s.key_lo), s.lower, s.key_lo))
                xs = [d[0] for d in drops.values()]
                span = (min(xs + [x]), max(xs + [x]))
                info.append({"x": x, "drops": drops, "span": span,
                             "track": any(d != x for d in xs), "segs": nsegs})
            after: dict[int, set[int]] = defaultdict(set)  # net -> nets that must be below it
            conflict = False
            for a, A in enumerate(info):
                for c_, C in enumerate(info):
                    if a == c_:
                        continue
                    for key, (dx, _, _) in C["drops"].items():
                        if dx == A["x"] and A["track"] and key not in A["drops"]:
                            after[a].add(c_)
                        if key in A["drops"] and A["span"][0] < dx < A["span"][1]:
                            if not C["track"]:
                                conflict = True
                            after[a].add(c_)
            order, seen, temp = [], set(), set()

            def visit(a: int) -> None:
                nonlocal conflict
                if a in temp:
                    conflict = True
                    return
                if a in seen:
                    return
                temp.add(a)
                for c_ in after[a]:
                    visit(c_)
                temp.discard(a)
                seen.add(a)
                order.append(a)

            for a in sorted(range(len(info)), key=lambda a: info[a]["span"]):
                visit(a)
            if not conflict:
                break
            netlist = [[s] for nsegs in netlist for s in nsegs]
        else:
            raise _NoFit("cannot route channel")
        order.reverse()
        tracks: list[list[tuple[int, int]]] = []
        track_of: dict[int, int] = {}
        preds = defaultdict(set)
        for a, cs_ in after.items():
            for c_ in cs_:
                preds[c_].add(a)
        for a in order:
            if not info[a]["track"]:
                continue
            t = max([track_of[p] + 1 for p in preds[a] if p in track_of] + [0])
            lo_, hi_ = info[a]["span"]
            while t < len(tracks) and any(not (hi_ + 1 < l or lo_ > h + 1) for l, h in tracks[t]):
                t += 1
            if t == len(tracks):
                tracks.append([])
            tracks[t].append((lo_, hi_))
            track_of[a] = t
        down = any(s.head_lo for it in bands[b] for s in it.lo)
        both = any(s.head_lo and s.head_up for it in bands[b] for s in it.lo)
        T = len(tracks) or (1 if both else 0)
        channels.append({"info": info, "track_of": track_of, "T": T, "down": down})

    # 8. positions along the bands
    pad = defaultdict(int)  # extra room before the closing borders of channel b

    def levels(cs_: list[str]) -> list[list[str]]:
        by_depth = defaultdict(list)
        for c in cs_:
            by_depth[depth_of[c]].append(c)
        return [by_depth[d] for d in sorted(by_depth)]

    for _ in range(8):
        m = 0
        border_m: dict[str, list[int]] = {c: [0, 0] for c in clusters}
        band_m0 = []
        for level in levels(opens[0]):
            for c in level:
                border_m[c][0] = m
            m += 1
        if opens[0] and not vertical:
            m += 1
        chan_rows = []
        for b in range(R):
            band_m0.append(m)
            m += band_ms[b]
            if b == R - 1:
                break
            ch = channels[b]
            row0 = m
            m += 1 + pad[b]
            for level in reversed(levels(closes[b])):
                for c in level:
                    border_m[c][1] = m
                m += 1
            track0 = m
            m += ch["T"]
            if not ch["T"] and closes[b] and opens[b + 1]:
                m += 1
            for level in levels(opens[b + 1]):
                for c in level:
                    border_m[c][0] = m
                m += 1
            if ch["T"] or ch["down"] or opens[b + 1]:
                m += 1
            chan_rows.append((row0, track0))
        m += pad[R - 1] + (1 if closes[R - 1] and not vertical else 0)
        for level in reversed(levels(closes[R - 1])):
            for c in level:
                border_m[c][1] = m
            m += 1
        total_m = m
        short = False
        if not vertical:  # titles run along the top border: make room
            for c in clusters:
                need = tw(titles[c]) + 6 if titles[c] else 0
                have = border_m[c][1] - border_m[c][0] + 1
                if need > have:
                    pad[ext[c][3]] += need - have
                    short = True
        if not short:
            break
    else:
        raise _NoFit("subgraph titles do not fit")
    if not vertical and total_m > width:
        raise _NoFit("too wide")
    for b, band in enumerate(bands):
        for it in band:
            it.m0 = band_m0[b]
            if it.kind == "dummy":
                it.ms = band_ms[b]

    # 9. draw
    grid = Grid()
    lines = _Lines()

    def rc(mm: int, cc: int) -> tuple[int, int]:
        if flip:
            mm = total_m - 1 - mm
        return (mm, cc) if vertical else (cc, mm)

    def screen_rect(mm: int, cc: int, ms: int, cs: int) -> tuple[int, int, int, int]:
        if flip:
            mm = total_m - mm - ms
        return (mm, cc, ms, cs) if vertical else (cc, mm, cs, ms)

    if vertical:
        MP, MN, CP, CN = ("N", "S", "E", "W") if flip else ("S", "N", "E", "W")
    else:
        MP, MN, CP, CN = ("W", "E", "S", "N") if flip else ("E", "W", "S", "N")
    arrow_for = {"S": "▼", "N": "▲", "E": "►", "W": "◄"}

    def head_char(head: str, pointing: str) -> str:
        return {"arrow": arrow_for[pointing], "circle": "o", "cross": "x"}[head]

    def mline(cc: int, m_a: int, m_b: int, style: str, tags, cap_a: bool = True, cap_b: bool = True) -> None:
        """A line along the main axis from m_a to m_b (inclusive)."""
        if m_a > m_b:
            m_a, m_b = m_b, m_a
            cap_a, cap_b = cap_b, cap_a
        for mm in range(m_a, m_b + 1):
            dirs = set()
            if mm > m_a or cap_a:
                dirs.add(MN)
            if mm < m_b or cap_b:
                dirs.add(MP)
            r, c = rc(mm, cc)
            lines.add(r, c, dirs, style, tags)

    def cline(mm: int, c_a: int, c_b: int, style: str, tags) -> None:
        """A line across the bands from c_a to c_b (inclusive, open ends)."""
        c_a, c_b = min(c_a, c_b), max(c_a, c_b)
        for cc in range(c_a, c_b + 1):
            dirs = set()
            if cc > c_a:
                dirs.add(CN)
            if cc < c_b:
                dirs.add(CP)
            r, c = rc(mm, cc)
            lines.add(r, c, dirs, style, tags)

    heads: list[tuple[int, int, str]] = []
    border_marks: list[tuple[_It, int, str]] = []  # (item, cross pos, side)
    for b in range(R - 1):
        ch = channels[b]
        row0, track0 = chan_rows[b]
        for a, net in enumerate(ch["info"]):
            s0 = net["segs"][0]
            up = s0.upper
            x = net["x"]
            m_start = _item_end(up)
            style = s0.line if all(s.line == s0.line for s in net["segs"]) else "solid"
            tag = {("net", b, a)}
            if s0.head_up:
                heads.append((m_start, x, head_char(s0.head_up, MN)))
            elif up.kind == "node" and up.node.shape not in ("start", "end", "choice", "bar"):
                border_marks.append((up, x, "end"))
            if a in ch["track_of"]:
                mt = track0 + ch["track_of"][a]
                mline(x, m_start, mt, style, tag, cap_a=True, cap_b=False)
                cline(mt, *net["span"], style, tag)
                for key, (dx, low, lkey) in net["drops"].items():
                    m_end = low.m0 - 1
                    mline(dx, mt, m_end, style, tag | {("port", b, key)}, cap_a=False, cap_b=True)
            else:
                (key, (dx, low, lkey)), = net["drops"].items()
                mline(x, m_start, low.m0 - 1, style, tag | {("port", b, key)})
        for it in bands[b + 1]:
            for s in it.up:
                x = port(it, s.key_lo)
                if s.head_lo:
                    heads.append((it.m0 - 1, x, head_char(s.head_lo, MP)))
                elif it.kind == "node" and it.node.shape not in ("start", "end", "choice", "bar"):
                    border_marks.append((it, x, "start"))
    for it in items:  # lines through labels and passing points
        if it.kind == "dummy":
            mline(it.c0, it.m0, it.m0 + it.ms - 1, "solid", {("item", id(it))})
        elif it.kind == "label" and not vertical:  # LR labels sit above their line
            st = it.up[0].line if it.up else "solid"
            mline(port(it, "start"), it.m0, it.m0 + it.ms - 1, st, {("item", id(it))})
    for c in clusters:  # subgraph borders
        lo, hi = ext[c][0], ext[c][1]
        m_a, m_b = border_m[c]
        tag = {("cluster", c)}
        cline(m_a, lo, hi, "solid", tag)
        cline(m_b, lo, hi, "solid", tag)
        mline(lo, m_a, m_b, "solid", tag, cap_a=False, cap_b=False)
        mline(hi, m_a, m_b, "solid", tag, cap_a=False, cap_b=False)
        for mm in (m_a, m_b):
            for cc in (lo, hi):
                r, cl = rc(mm, cc)
                dirs = {MP if mm == m_a else MN, CP if cc == lo else CN}
                lines.add(r, cl, dirs, "solid", tag)
    lines.draw(grid, vertical_wins=vertical)

    for it in items:  # boxes and text on top of the lines
        if it.kind == "node":
            _draw_node(grid, it, screen_rect, vertical)
        elif it.kind == "label":
            r0, c0, h, w = screen_rect(it.m0, it.c0, it.ms, it.cs)
            if vertical:
                for k, l in enumerate(it.lines):
                    grid.text(r0 + k, c0 + (w - tw(l)) // 2, l)
            else:
                for k, l in enumerate(it.lines):
                    grid.text(r0 + k, c0 + 1, l)
    for it, x, side in border_marks:
        bc, bm, bcs, bms = it.box
        mm = it.m0 + (bms - 1 if side == "end" else 0)
        r, c = rc(mm, x)
        border = {"N", "S"} if not vertical else {"E", "W"}
        out_dir = MP if side == "end" else MN
        grid.put(r, c, _LIGHT[_dkey(border | {out_dir})])
    for mm, cc, ch_ in heads:
        r, c = rc(mm, cc)
        grid.put(r, c, ch_)
    for c in clusters:
        if titles[c]:
            lo = ext[c][0]
            m_a, m_b = border_m[c]
            if vertical:  # the title goes on the top border
                r, cl = rc(m_b if flip else m_a, lo)
            else:
                r, cl = lo, min(rc(m_a, lo)[1], rc(m_b, lo)[1])
            grid.text(r, cl + 2, f" {titles[c]} ")
    out_lines = grid.lines()
    if max(tw(l) for l in out_lines) > width:
        raise _NoFit("too wide")
    return out_lines


def _cluster_chain(g: _Graph, c: str) -> list[str]:
    """A subgraph and its ancestors, innermost first."""
    chain: list[str] = []
    while c is not None:
        if c in chain or c not in g.clusters:
            raise _Unsupported("subgraph nesting is cyclic")
        chain.append(c)
        c = g.clusters[c].parent
    return chain


def _item_end(it: _It) -> int:
    """First main-axis position past the item where its lower edges start."""
    if it.kind == "node":
        return it.m0 + it.box[3]
    return it.m0 + it.ms


def _draw_node(grid: Grid, it: _It, screen_rect, vertical: bool) -> None:
    bc, bm, bcs, bms = it.box
    r0, c0, h, w = screen_rect(it.m0 + bm, it.c0 + bc, bms, bcs)
    nd = it.node
    shape = nd.shape
    if shape == "start":
        grid.put(r0, c0, "●")
    elif shape == "end":
        grid.put(r0, c0, "◉")
    elif shape == "choice":
        grid.put(r0, c0, "◇")
    elif shape == "bar":
        for r in range(r0, r0 + h):
            for c in range(c0, c0 + w):
                grid.put(r, c, "━" if vertical else "┃")
    else:
        chars = {
            "round": "╭╮╰╯─│", "stadium": "╭╮╰╯─│", "circle": "╭╮╰╯─│", "state": "╭╮╰╯─│",
            "diamond": "╱╲╲╱─│", "hexagon": "╱╲╲╱─│",
        }.get(shape, "┌┐└┘─│")
        _box(grid, r0, c0, r0 + h - 1, c0 + w - 1, chars, fill=True)
        top = r0 + 1
        if shape == "cylinder":
            for c in range(c0 + 1, c0 + w - 1):
                grid.put(r0 + 1, c, "─")
            grid.put(r0, c0, "╭")
            grid.put(r0, c0 + w - 1, "╮")
            grid.put(r0 + 1, c0, "├")
            grid.put(r0 + 1, c0 + w - 1, "┤")
            grid.put(r0 + h - 1, c0, "╰")
            grid.put(r0 + h - 1, c0 + w - 1, "╯")
            top = r0 + 2
        inner_h = r0 + h - 1 - top
        for r in range(top, r0 + h - 1):
            if shape == "stadium":
                grid.put(r, c0, "(")
                grid.put(r, c0 + w - 1, ")")
            elif shape == "subroutine":
                grid.put(r, c0 + 1, "│")
                grid.put(r, c0 + w - 2, "│")
            elif shape == "lean":
                grid.put(r, c0, "╱")
                grid.put(r, c0 + w - 1, "╱")
            elif shape == "flag":
                grid.put(r, c0, ">")
        lines = it.lines
        start = top + (inner_h - len(lines)) // 2
        for k, l in enumerate(lines):
            grid.text(start + k, c0 + (w - tw(l)) // 2, l)
    for nc, ncs, nms, text in it.notes:  # note boxes and their connectors
        nr0, ncol0, nh, nw = screen_rect(it.m0, it.c0 + nc, nms, ncs)
        _box(grid, nr0, ncol0, nr0 + nh - 1, ncol0 + nw - 1, "╭╮╰╯─│", fill=True)
        for k, l in enumerate(text):
            grid.text(nr0 + 1 + k, ncol0 + 2, l)
        if vertical:
            row = r0 + (h - 1) // 2
            a, b = (c0 + w, ncol0 - 1) if ncol0 > c0 else (ncol0 + nw, c0 - 1)
            for c in range(a, b + 1):
                grid.put(row, c, "╌")
        else:
            col = c0 + (w - 1) // 2
            a, b = (r0 + h, nr0 - 1) if nr0 > r0 else (nr0 + nh, r0 - 1)
            for r in range(a, b + 1):
                grid.put(r, col, "╎")


_GRAPH_ATTEMPTS = (None, 24, 18, 14)


def _render_graph(g: _Graph, width: int, kind: str) -> tuple[str, str]:
    given = g.direction
    other = "LR" if given in ("TB", "BT") else "TB"
    texts = [n.label for n in g.nodes.values()] + [e.label for e in g.edges]
    texts += [t for n in g.nodes.values() for _, t in n.notes]
    floor = max([0] + [tw(p) for t in texts for p in _soft_pieces(" ".join(t))])
    for cap in [c for c in _GRAPH_ATTEMPTS if c is None or c >= floor]:
        for d in (given, other):
            try:
                lines = _draw_graph(g, d, cap, width)
            except _NoFit:
                continue
            except _Unsupported:
                return "\n".join(_graph_list(g, width)), kind + "-list"
            return "\n".join(_framed(g.title, lines, g.descr, width)), kind
    return "\n".join(_graph_list(g, width)), kind + "-list"


def _node_name(g: _Graph, nid: str) -> str:
    if nid in g.clusters:
        return _flat(g.clusters[nid].title) or nid
    nd = g.nodes[nid]
    if nd.shape in ("start", "end") and not nd.label:
        return f"({nd.shape})"
    if nd.shape in ("bar", "choice") and not nd.label:
        return f"{nid} ({'choice' if nd.shape == 'choice' else 'fork/join'})"
    return _flat(nd.label) or nid


_LIST_LINE = {"solid": "─", "dotted": "╌", "thick": "━", "invisible": "─"}
_LIST_HEAD = {"arrow": ("◄", "►"), "circle": ("o", "o"), "cross": ("x", "x")}


def _graph_list(g: _Graph, width: int) -> list[str]:
    """Structured rendering: every node with its outgoing edges, by subgraph."""
    names = list(g.nodes)
    succ = defaultdict(list)
    for e in g.edges:
        succ[e.src].append(e.dst)
    indeg = defaultdict(int)
    for e in g.edges:
        indeg[e.dst] += 1
    rank: dict[str, int] = {}
    for root in [n for n in names if not indeg[n]] + names:  # DFS preorder
        if root in rank:
            continue
        stack = [root]
        while stack:
            v = stack.pop()
            if v in rank or v not in g.nodes:
                continue
            rank[v] = len(rank)
            stack.extend(reversed([w for w in succ[v] if w not in rank]))
    children = defaultdict(list)  # cluster (None = top) -> nodes and subclusters
    for n in names:
        children[g.member.get(n)].append(("node", n))
    for c, cl in g.clusters.items():
        children[cl.parent].append(("cluster", c))

    def first(entry) -> float:
        kind, x = entry
        if kind == "node":
            return rank.get(x, 1e9)
        return min([first(e) for e in children[x]] + [1e9])

    out: list[str] = []
    if g.title:
        out += wrap_lines(g.title, width) + [""]

    def emit(parent, bars: str) -> None:
        for kind, x in sorted(children[parent], key=first):
            if kind == "cluster":
                _emit(out, bars + "┌─ ", bars + "│    ", [_node_name(g, x)], width)
                for cid, side, text in g.cluster_notes:
                    if cid == x:
                        _emit(out, bars + "│   ", bars + "│     ",
                              [f"Note ({side}): " + " ".join(text)], width)
                emit(x, bars + "│ ")
                out.append(bars + "└─")
                continue
            _emit(out, bars, bars + "  ", [_node_name(g, x)], width)
            for side, text in g.nodes[x].notes:
                _emit(out, bars + "  ", bars + "    ", [f"Note ({side}): " + " ".join(text)], width)
            mine = [e for e in g.edges if e.src == x and e.line != "invisible"]
            for k, e in enumerate(mine):
                last = k == len(mine) - 1
                ch = _LIST_LINE[e.line]
                hs = _LIST_HEAD[e.head_src][0] if e.head_src else ch
                hd = _LIST_HEAD[e.head_dst][1] if e.head_dst else ch
                conn = "└" if last else "├"
                label = _flat(e.label)
                arrow = f"{hs}{ch} {label} {ch}{hd}" if label else f"{hs}{ch}{hd}"
                _emit(out, f"{bars}  {conn}", bars + ("     " if last else "  │  "),
                      [f"{arrow} {_node_name(g, e.dst)}"], width)

    emit(None, "")
    for e in g.edges:  # edges that start at a subgraph
        if e.src in g.clusters and e.line != "invisible":
            ch = _LIST_LINE[e.line]
            label = _flat(e.label)
            arrow = f"{ch} {label} {ch}►" if label else f"{ch}{ch}►"
            _emit(out, f"{_node_name(g, e.src)} {arrow} ", "    ", [_node_name(g, e.dst)], width)
    if g.descr:
        out += [""] + wrap(_flat(g.descr), width)
    return out


# --- Gantt charts -------------------------------------------------------------


@dataclass
class _Task:
    name: list[str]
    section: list[str]
    spec: str
    tags: list[str] = field(default_factory=list)
    tid: str | None = None
    start: date | None = None
    end: date | None = None


@dataclass
class _Gantt:
    title: list[str] = field(default_factory=list)
    descr: list[str] = field(default_factory=list)
    tasks: list[_Task] = field(default_factory=list)
    date_format: str = "YYYY-MM-DD"
    excludes: str = ""


_GANTT_IGNORE = re.compile(
    r"^(?:axisFormat|tickInterval|todayMarker|weekday|weekend|includes|inclusiveEndDates"
    r"|topAxis|displayMode|click)\b"
)
_TAGS_GANTT = ("done", "active", "crit", "milestone")
_MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def _parse_gantt(lines: list[str]) -> _Gantt:
    gt = _Gantt()
    section: list[str] = []
    it = iter(lines[1:])
    for line in it:
        if _acc(line, it, gt.title, gt.descr):
            continue
        if m := re.match(r"^title\s+(.*)$", line):
            gt.title.extend(clean(m.group(1)))
        elif m := re.match(r"^dateFormat\s+(.*)$", line):
            gt.date_format = m.group(1).strip()
        elif m := re.match(r"^excludes\s+(.*)$", line):
            gt.excludes = m.group(1).strip()
        elif _GANTT_IGNORE.match(line):
            continue
        elif m := re.match(r"^section\s+(.*)$", line):
            section = clean(m.group(1))
        elif m := re.match(r"^([^:]+?)\s*:\s*(.*)$", line):
            gt.tasks.append(_Task(clean(m.group(1)), section, m.group(2).strip()))
        else:
            raise _Unsupported(line)
    if not gt.tasks:
        raise _Unsupported("no tasks")
    _schedule(gt)
    return gt


def _schedule(gt: _Gantt) -> None:
    """Work out task dates where the syntax allows it (YYYY-MM-DD only)."""
    if gt.date_format != "YYYY-MM-DD":
        return
    by_id: dict[str, _Task] = {}
    prev: _Task | None = None
    for t in gt.tasks:
        items = [x.strip() for x in t.spec.split(",")]
        while items and items[0] in _TAGS_GANTT:
            t.tags.append(items.pop(0))
        if len(items) == 3:
            t.tid, start_s, end_s = items
        elif len(items) == 2:
            start_s, end_s = items
        elif len(items) == 1:
            start_s, end_s = "", items[0]
        else:
            return
        if t.tid:
            by_id[t.tid] = t
        try:
            if not start_s:
                t.start = prev.end if prev else None
            elif start_s.startswith("after "):
                ends = [by_id[x].end for x in start_s[6:].split()]
                t.start = max(ends) if all(ends) else None
            else:
                t.start = date.fromisoformat(start_s)
            if t.start is None:
                return
            if m := re.fullmatch(r"(\d+(?:\.\d+)?)\s*([dw])", end_s):
                if gt.excludes:
                    return  # working-day arithmetic is not reproduced
                days = float(m.group(1)) * (7 if m.group(2) == "w" else 1)
                t.end = t.start + timedelta(days=days)
            elif end_s.startswith("until "):
                t.end = by_id[end_s[6:].strip()].start
            else:
                t.end = date.fromisoformat(end_s)
        except (KeyError, ValueError, TypeError, AttributeError):
            for x in gt.tasks:
                x.start = x.end = None
            return
        prev = t


def _gantt_table(gt: _Gantt, width: int) -> list[str]:
    out: list[str] = []
    section = None
    name_w = min(28, max(tw(_flat(t.name)) for t in gt.tasks) + 2)
    for t in gt.tasks:
        if t.section != section:
            section = t.section
            if section:
                _emit(out, "", "  ", [_flat(section)], width)
        name = _flat(t.name)
        if t.start and t.end is not None:
            when = t.start.isoformat() if t.start == t.end or "milestone" in t.tags \
                else f"{t.start.isoformat()} to {t.end.isoformat()}"
        else:
            when = t.spec
        tags = [x for x in t.tags]
        if tags:
            when += f" ({', '.join(tags)})"
        lead = "  " + name + " " * max(1, name_w - tw(name))
        if tw(lead) + tw(when) > width:
            _emit(out, "  ", "    ", [name], width)
            _emit(out, "      ", "      ", [when], width)
        else:
            out.append(lead + when)
    return out


def _render_gantt(gt: _Gantt, width: int) -> tuple[str, str]:
    table = _gantt_table(gt, width)
    head = wrap_lines(gt.title, width) + ([""] if gt.title else [])
    tail = ([""] + wrap(_flat(gt.descr), width)) if gt.descr else []
    dated = [t for t in gt.tasks if t.start and t.end is not None]
    names = [_flat(t.name) for t in gt.tasks]
    name_w = min(26, max(tw(n) for n in names) + 3)
    chart_w = width - name_w
    if len(dated) != len(gt.tasks) or chart_w < 24:
        return "\n".join(head + table + tail), "gantt-list"
    t0 = min(t.start for t in dated)
    t1 = max(max(t.end, t.start) for t in dated)
    span = max(1, (t1 - t0).days)

    def col(d: date) -> int:
        return name_w + round((d - t0).days / span * (chart_w - 1))

    grid = Grid(width)
    ticks: list[tuple[date, str, str]] = []  # (date, label, year label)
    if span > 62:
        d = date(t0.year, t0.month, 1)
        while d <= t1:
            if d >= t0:
                ticks.append((d, _MONTHS[d.month - 1], str(d.year)))
            d = date(d.year + d.month // 12, d.month % 12 + 1, 1)
    else:
        step = max(1, span // max(1, chart_w // 8))
        d = t0
        while d <= t1:
            ticks.append((d, f"{d.month:02d}-{d.day:02d}", str(d.year)))
            d += timedelta(days=step)
    last_label = last_year = -1
    year_seen = None
    for d, label, year in ticks:
        x = col(d)
        if x > last_label and x + tw(label) <= width:
            grid.text(1, x, label)
            last_label = x + tw(label)
            if year != year_seen and x > last_year:
                grid.text(0, x, year)
                last_year = x + len(year)
                year_seen = year
        grid.put(2, x, "┬")
    for x in range(name_w, width):
        if grid.get(2, x) != "┬":
            grid.put(2, x, "─")
    r = 3
    section = None
    for t in gt.tasks:
        if t.section != section:
            section = t.section
            if section:
                for l in wrap(_flat(section), width):
                    grid.text(r, 0, l)
                    r += 1
        name_lines = wrap(_flat(t.name), name_w - 3)
        for k, l in enumerate(name_lines):
            grid.text(r + k, 2, l)
        a, b = col(t.start), col(t.end)
        if "milestone" in t.tags or b <= a:
            grid.put(r, a, "◆")
        else:
            for x in range(a, b):
                grid.put(r, x, "▒" if "done" in t.tags else "█")
        r += len(name_lines)
    chart = grid.lines()
    return "\n".join(head + chart + [""] + table + tail), "gantt"


# --- checking -----------------------------------------------------------------
#
# The label extractor below is deliberately independent of the parsers above:
# it finds label text with plain regular expressions so that a parser bug that
# drops something shows up as a missing label.

_X_ARROW = re.compile(r"<<-->>|<<->>|-->>|->>|--x|-x|--\)|-\)|-->|->")
_X_SHAPE = re.compile(
    r"(?P<id>[\w$][\w.$-]*?)(?::::[\w-]+)?"
    r"(?P<open>\(\(\(|\(\[|\[\[|\[\(|\(\(|\{\{|\[/|\[\\|\[|\(|\{|(?<![-=.])>)"
    r"(?P<text>\"[^\"]*\"|[^\"\])}]*?)"
    r"(?P<close>\)\)\)|\]\)|\]\]|\)\]|\)\)|\}\}|/\]|\\\]|\]|\)|\})"
)
_X_FLOW_ARROW = re.compile(r"\s*(?:[\w-]+@)?[<ox]?(?:-{2,}|={2,}|-\.+-?|~{3,})[>ox]?\s*")
_X_DASH_LABEL = re.compile(
    r"(?:--|==|-\.)\s+(?P<t>[^|]+?)\s+(?:-{2,}>|-{3,}|-{2,}[ox]|={2,}>|={3,}|\.-+>?)"
)


def labels(source: str) -> list[str]:
    """Every label in a diagram's source as display lines (for checking)."""
    body = _statements(source)
    if not body:
        return []
    kind = body[0].split()[0] if body[0].split() else ""
    out: list[str] = []
    if m := re.search(r"(?m)^title:\s*(.+)$", _front_matter(source)):
        out += clean(_unquote(m.group(1)))
    acc = re.compile(r"^(?:accTitle|accDescr)\s*:\s*(.*)$")
    if kind == "sequenceDiagram":
        declared, ids = set(), []
        for line in body[1:]:
            line = _strip_semi(line)
            if m := re.match(r"^(?:create\s+)?(?:participant|actor)\s+(.+)$", line):
                rest = re.sub(r"@\{.*?\}", "", m.group(1)).strip()
                pid, sep, alias = rest.partition(" as ")
                declared.add(pid.strip())
                out += clean(alias if sep and alias.strip() else pid)
            elif m := re.match(r"^note\s+(?:left of|right of|over)\s+([^:]+):(.*)$", line, re.I):
                out += clean(m.group(2))
                ids += [p.strip() for p in m.group(1).split(",")]
            elif m := re.match(r"^(?:loop|alt|else|opt|par_over|par|and|critical|option|break)\b\s*(.*)$", line):
                out += clean(m.group(1))
            elif m := re.match(r"^box\b\s*(.*)$", line):
                out += clean(_strip_color(m.group(1)))
            elif m := acc.match(line) or re.match(r"^title\s*:?\s*(.*)$", line):
                out += clean(m.group(1))
            elif m := re.match(r"^(?:activate|deactivate|destroy)\s+(.+)$", line):
                ids.append(m.group(1).strip())
            elif _X_ARROW.search(line.split(":", 1)[0]):
                head, _, text = line.partition(":")
                out += clean(re.sub(r"^(?:no)?wrap:\s*", "", text.strip()))
                ids += [p.strip(" +-") for p in _X_ARROW.split(head, maxsplit=1)]
        for pid in dict.fromkeys(ids):
            if pid and pid not in declared:
                declared.add(pid)
                out += clean(pid)
    elif kind in ("graph", "flowchart"):
        labelled, ids, subgraphs = set(), [], set()
        statements = [st for line in body for st in _split_statements(line)]
        first = re.sub(r"^(?:graph|flowchart)(?:\s+(?:TB|TD|BT|RL|LR))?\s*", "", statements[0])
        statements = ([first] if first else []) + statements[1:]
        for st in statements:
            if m := re.match(r"^subgraph\b\s*(.*)$", st):
                rest = m.group(1).strip()
                if bm := re.match(r"^([^\s\[]+)\s*\[(.*)\]$", rest):
                    subgraphs.add(bm.group(1))
                    out += clean(_unquote(bm.group(2)))
                else:
                    subgraphs.add(_unquote(rest))
                    out += clean(_unquote(rest))
                continue
            if m := acc.match(st):
                out += clean(m.group(1))
                continue
            if st == "end" or _FLOW_SKIP.match(st):
                continue
            rest = st
            for m in re.finditer(r"([\w$][\w.$-]*)@\{[^}]*label\s*:", st):
                labelled.add(m.group(1))
            for m in _X_SHAPE.finditer(st):
                out += clean(_unquote(m.group("text")))
                labelled.add(m.group("id"))
            rest = _X_SHAPE.sub(lambda m: m.group("id"), rest)
            for m in re.finditer(r"@\{[^}]*\}", rest):
                if lm := re.search(r'label\s*:\s*"([^"]*)"', m.group(0)):
                    out += clean(lm.group(1))
            rest = re.sub(r"(\w)@\{[^}]*\}", r"\1", rest)
            for m in re.finditer(r"\|([^|]*)\|", rest):
                out += clean(_unquote(m.group(1)))
            rest = re.sub(r"\|[^|]*\|", " ", rest)
            for m in _X_DASH_LABEL.finditer(rest):
                out += clean(_unquote(m.group("t")))
            rest = _X_DASH_LABEL.sub(" --> ", rest)
            for token in re.split(r"&", _X_FLOW_ARROW.sub(" & ", rest)):
                token = re.sub(r":::[\w-]+$", "", token.strip())
                if re.fullmatch(r"[\w$][\w.$-]*", token):
                    ids.append(token)
        for nid in dict.fromkeys(ids):
            if nid not in labelled and nid not in subgraphs:
                out += clean(nid)
    elif kind in ("stateDiagram", "stateDiagram-v2"):
        alias, states, pseudo = {}, {}, set()
        for line in body[1:]:
            if m := re.match(r'^state\s+"([^"]*)"\s+as\s+([\w.$-]+)', line):
                alias[m.group(2)] = m.group(1)
        it = iter(body[1:])
        for line in it:
            line = _strip_semi(line)
            if m := re.match(r"^note\s+(?:left|right)\s+of\s+\S+\s*:\s*(.*)$", line, re.I):
                out += clean(m.group(1))
            elif re.match(r"^note\s+(?:left|right)\s+of\s+\S+\s*$", line, re.I):
                for nl in it:
                    if nl.strip().lower() == "end note":
                        break
                    out += clean(nl)
            elif m := re.match(r'^state\s+"([^"]*)"\s+as\s+', line):
                out += clean(m.group(1))
            elif m := re.match(r"^state\s+([\w.$-]+)\s*<<\w+>>", line):
                pseudo.add(m.group(1))  # choice/fork/join: drawn without a name
            elif m := re.match(r"^state\s+([\w.$-]+)", line):
                states[m.group(1)] = None
            elif m := re.match(r"^(\S+?)\s*-->\s*(\S+?)\s*(?::(.*))?$", line):
                for sid in (m.group(1), m.group(2)):
                    sid = re.sub(r":::[\w-]+$", "", sid)
                    if sid != "[*]":
                        states[sid] = None
                out += clean(m.group(3) or "")
            elif m := acc.match(line) or re.match(r"^title\s*:?\s*(.*)$", line):
                out += clean(m.group(1))
            elif m := re.match(r"^([\w.$-]+)\s*:\s*(.*)$", line):
                states[m.group(1)] = None
                out += clean(m.group(2))
        for sid in states:
            if sid not in pseudo:
                out += clean(alias.get(sid, sid))
    elif kind == "gantt":
        for line in body[1:]:
            if m := re.match(r"^(?:title|section)\s+(.*)$", line) or acc.match(line):
                out += clean(m.group(1))
            elif not re.match(r"^\w+\s", line) and (m := re.match(r"^([^:]+?)\s*:", line)):
                out += clean(m.group(1))
            elif (m := re.match(r"^([^:]+?)\s*:", line)) and not re.match(
                r"^(?:dateFormat|axisFormat|tickInterval|todayMarker|excludes|weekday|includes)\b", line
            ):
                out += clean(m.group(1))
    return [" ".join(l.split()) for l in out if l.strip()]


def _front_matter(source: str) -> str:
    lines = source.strip("\n").split("\n")
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                return "\n".join(lines[1:j])
    return ""


def _covered(label: str, hay: str) -> bool:
    """Is `label` in `hay`, possibly wrapped into several pieces?"""
    if label in hay:
        return True
    p = 0
    n = len(label)
    while p < n:
        while p < n and label[p] == " ":
            p += 1
        if p >= n:
            return True
        ends = [q for q in range(n, p, -1)
                if q == n or label[q] == " " or not label[q - 1].isalnum()
                or (label[q] in _BEFORE)]
        for q in ends:
            if label[p:q].strip() and label[p:q].strip() in hay:
                p = q
                break
        else:  # a hard break inside a word
            for q in range(n, p + 5, -1):
                if label[p:q] in hay:
                    p = q
                    break
            else:
                return False
    return True


def missing_labels(source: str, text: str) -> list[str]:
    """Labels of `source` that do not appear in the rendering `text`."""
    hay = "\n".join(" ".join(line.split()) for line in text.split("\n"))
    hay += "\n" + text
    return [l for l in dict.fromkeys(labels(source)) if not _covered(l, hay)]


def problems(source: str, rendered: Rendered, width: int) -> list[str]:
    """Invariant violations of one rendering."""
    out = []
    lines = rendered.text.split("\n")
    if not rendered.text.strip():
        out.append("empty output")
    if "\t" in rendered.text:
        out.append("tab in output")
    if lines and (not lines[0].strip() or not lines[-1].strip()):
        out.append("blank first or last line")
    for k, line in enumerate(lines, 1):
        if line != line.rstrip():
            out.append(f"line {k}: trailing space")
        if tw(line) > width:
            out.append(f"line {k}: {tw(line)} columns")
    for label in missing_labels(source, rendered.text):
        out.append(f"missing label: {label!r}")
    want = defaultdict(int)  # every word of every label, as often as it occurs
    for label in labels(source):
        for word in re.findall(r"[^\W_]+", label):
            want[word] += 1
    have = defaultdict(int)
    for word in re.findall(r"[^\W_]+", rendered.text):
        have[word] += 1
    for word, k in want.items():
        if have[word] < k:
            out.append(f"word {word!r} appears {have[word]} times, wanted {k}")
    return out


_OPEN_FENCE = re.compile(r"^(?P<indent> *)(?P<fence>`{3,}|~{3,})(?P<info>.*)$")


def mermaid_blocks(text: str) -> list[tuple[int, str]]:
    """(line number, source) of each ```mermaid fenced block in Markdown."""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        m = _OPEN_FENCE.match(lines[i].replace("\t", "    "))
        if not m or (m.group("fence")[0] == "`" and "`" in m.group("info")):
            i += 1
            continue
        fence, indent = m.group("fence"), len(m.group("indent"))
        close = re.compile(rf"^ *{re.escape(fence[0])}{{{len(fence)},}}\s*$")
        j = i + 1
        while j < len(lines) and not close.match(lines[j].replace("\t", "    ")):
            j += 1
        info = m.group("info").strip().split()
        if info and info[0].lower() == "mermaid":
            body = []
            for line in lines[i + 1 : j]:
                k = 0
                while k < indent and k < len(line) and line[k] == " ":
                    k += 1
                body.append(line[k:])
            out.append((i + 1, "\n".join(body)))
        i = j + 1
    return out


def check(width: int = 78) -> int:
    """Render every mirrored diagram, verify it, write build/diagram-review.txt."""
    from .config import BUILD, MIRROR

    counts: dict[str, int] = defaultdict(int)
    failures = []
    entries = []
    total = 0
    for path in sorted(MIRROR.glob("*/pages/**/*.md")):
        rel = path.relative_to(MIRROR.parent)
        for line, source in mermaid_blocks(path.read_text(encoding="utf-8")):
            total += 1
            r = render(source, width)
            counts[r.method] += 1
            bad = problems(source, r, width)
            if bad:
                failures.append((f"{rel}:{line}", bad))
            entries.append(f"==== {rel}:{line}  [{r.method}]\n\n{r.text}\n")
    summary = [f"{total} diagrams: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))]
    summary.append(f"{len(failures)} with problems")
    for where, bad in failures:
        summary.append(f"  {where}")
        summary.extend(f"    {b}" for b in bad[:20])
    BUILD.mkdir(parents=True, exist_ok=True)
    review = BUILD / "diagram-review.txt"
    review.write_text("\n".join(summary) + "\n\n" + "\n".join(entries), encoding="utf-8")
    print("\n".join(summary))
    print(f"wrote {review}")
    return 1 if failures or not total else 0


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    width = 78
    if "--width" in args:
        k = args.index("--width")
        width = int(args[k + 1])
        del args[k : k + 2]
    if args == ["--check"]:
        return check(width)
    if args:
        print("usage: python -m claude_info.diagrams [--width N] [--check] < diagram.mmd",
              file=sys.stderr)
        return 2
    r = render(sys.stdin.read(), width)
    print(r.text)
    print(f"[{r.method}]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
