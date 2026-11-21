"""Generate figs/lamps.tex, the lamp-rig figure on coarse-graining as a change of measure.

Paper layout of the artifact draft. Panel (a) is the goal side, mixtures counted by colour. Panel (b)
is the agent's side, the class Y with its predicted law iota(y). Panel (c) is the volume a held class
occupies, split into a residual part and a goal part, with the cost of each keep set against the reset rate.
Coordinates are pixels on a strip W wide, scaled to the line width. Explanatory notes live in the caption.
Run: python3 -I make_lamps.py  (writes lamps.tex next to this file)
"""
import math
from itertools import combinations
from pathlib import Path

W = 960
INK, MUTED, RULE, EDGE, GOAL = "lampink", "lampmuted", "lamprule", "lampedge", "lampgoal"
BW, GAP, YR, BASE = 16, 4, 104, 176
ROW_NAME, NOTE1, NOTE2 = BASE + 34, BASE + 52, BASE + 68
PA, PB, PC = (0, 270), (270, 540), (540, 960)
BOTTOM = ROW_NAME + 8
out = []


def mid(p):
    return (p[0] + p[1]) / 2


def col(c):
    return "{rgb,255:red,%d;green,%d;blue,%d}" % tuple(round(255 * v) for v in c)


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def txt(x, y, s, anchor="middle", size=12, bold=False, italic=False, fill=INK):
    a = {"middle": "base", "start": "base west", "end": "base east"}[anchor]
    font = r"\footnotesize" if size >= 13 else r"\scriptsize"
    font += r"\bfseries" if bold else ""
    font += r"\itshape" if italic else ""
    out.append(rf"  \node[anchor={a}, inner sep=0pt, font={font}, text={fill}] at ({f(x)},{f(y)}) {{{s}}};")


def line(x1, y1, x2, y2, stroke=INK, width=0.4, extra=""):
    out.append(rf"  \draw[{stroke}, line width={width}pt{extra}] ({f(x1)},{f(y1)}) -- ({f(x2)},{f(y2)});")


def box(x, y, w, h, fill, stroke=EDGE, opacity=None):
    op = f", fill opacity={opacity}" if opacity is not None else ""
    out.append(rf"  \filldraw[fill={fill}, draw={stroke}, line width=0.3pt{op}] ({f(x)},{f(y)}) rectangle ++({f(w)},{f(h)});")


def title(p, s):
    txt(p[0] + 12, 18, s, anchor="start", size=13.5, bold=True)


def note(p, y, s, italic=False):
    txt(mid(p), y, s, size=11, fill=MUTED, italic=italic)


def row_label(p, y, s):
    txt(p[0] + 12, y, s, anchor="start", size=11, fill=MUTED)


def brace(left, right, y, label):
    out.append(rf"  \draw[{INK}, line width=0.4pt, decorate, decoration={{brace, amplitude=3.5pt}}] ({f(left)},{f(y)}) -- ({f(right)},{f(y)});")
    txt((left + right) / 2, y - 15, label, size=11)


LIGHTS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 1)]


def mix(cx, cy, ix, size=BW + 2):
    """A black tile with the lit lamps of a mixture, blended as light."""
    r0 = size / 2
    out.append(rf"  \fill[black!92, rounded corners=0.6pt] ({f(cx - r0)},{f(cy - r0)}) rectangle ++({f(size)},{f(size)});")
    n = len(ix)
    r = r0 * (0.62 if n == 1 else 0.5)
    off = 0 if n == 1 else r0 * 0.3
    out.append(r"  \begin{scope}[blend group=screen]")
    for i, li in enumerate(ix):
        a = -math.pi / 2 + 2 * math.pi * i / n
        out.append(rf"    \fill[fill={col(LIGHTS[li])}] ({f(cx + off * math.cos(a))},{f(cy + off * math.sin(a))}) circle[x radius={f(r)}, y radius={f(r)}];")
    out.append(r"  \end{scope}")


def lamp(cx, cy, c, size=BW + 2):
    out.append(rf"  \fill[black!92, rounded corners=0.6pt] ({f(cx - size / 2)},{f(cy - size / 2)}) rectangle ++({f(size)},{f(size)});")
    r = size / 2 - 3
    out.append(rf"  \fill[fill={col(c)}] ({f(cx)},{f(cy)}) circle[x radius={f(r)}, y radius={f(r)}];")


# data: all mixtures of one to three of six lights, blended as light
groups = {}


def add(ix):
    c = tuple(1 - math.prod(1 - LIGHTS[i][k] for i in ix) for k in range(3))
    g = groups.setdefault(c, {"c": c, "n": 0, "ex": []})
    g["n"] += 1
    if len(g["ex"]) < 3 and (len(ix) > 1 or g["n"] == 1):
        g["ex"].append(ix)


for a in range(6):
    add((a,))
    for b in range(a + 1, 6):
        add((a, b))
        for d in range(b + 1, 6):
            add((a, b, d))
assert sum(1 for k in range(1, 4) for _ in combinations(range(6), k)) == 41
hist = sorted(groups.values(), key=lambda g: g["n"])
ORDER = ["primary", "secondary", "white"]


def cls(g):
    ones = sum(v > 0.999 for v in g["c"])
    return ORDER[ones - 1]


total = sum(g["n"] for g in hist)
CL = {k: {"n": 0, "cols": 0, "gs": []} for k in ORDER}
for g in hist:
    k = cls(g)
    CL[k]["n"] += g["n"]
    CL[k]["cols"] += 1
    CL[k]["gs"].append(g)
assert [CL[k]["n"] for k in ORDER] == [3, 15, 23] and total == 41
CCOL = {"primary": [(1, 0, 0), (0, 1, 0), (0, 0, 1)], "secondary": [(1, 1, 0), (1, 0, 1), (0, 1, 1)], "white": [(1, 1, 1)]}

# (a) the goal side: mu counts every mixture once, J groups them by colour, log scale
title(PA, r"(a) Goal: $41 \to 7$ colours")
row_label(PA, 36, r"$(\Omega,\mu) \to (\mathcal{Z},\nu)$, $\nu = J_\#\mu$")
H, MINH, maxn = 100, 18, hist[-1]["n"]
GG = 30  # extra gap between classes
span = len(hist) * (BW + GAP) - GAP + 2 * GG
ax0 = round(mid(PA) + 8 - span / 2)


def h_of(n):
    return MINH + (H - MINH) * math.log(n) / math.log(maxn)


line(ax0 - 5, BASE, ax0 + span + 3, BASE)
line(ax0 - 5, BASE, ax0 - 5, BASE - H - 4, stroke=MUTED)
for t in (1, 5, maxn):
    y = BASE - h_of(t)
    line(ax0 - 8, y, ax0 - 5, y, stroke=MUTED)
    txt(ax0 - 10, y + 3.5, str(t), anchor="end", size=10, fill=MUTED)
xs = {k: [] for k in ORDER}
for i, g in enumerate(hist):
    x, h = ax0 + i * (BW + GAP) + GG * ORDER.index(cls(g)), h_of(g["n"])
    box(x, BASE - h, BW, h, col(g["c"]))
    xs[cls(g)].append(x)
    for j, ix in enumerate(g["ex"][:3]):
        mix(x + BW / 2, BASE - h + 9 + j * 14, ix, 12)
    if g["n"] > 3:
        txt(x + BW / 2, BASE - h + 9 + 3 * 14, r"$\vdots$", size=11)
for k in ORDER:
    left, right = min(xs[k]), max(xs[k]) + BW
    top = max(h_of(g["n"]) for g in CL[k]["gs"])
    if k == "white":
        txt((left + right) / 2, BASE - top - 6, str(CL[k]["n"]), size=11)
    else:
        brace(left, right, BASE - top - 8, str(CL[k]["n"]))
    txt((left + right) / 2, ROW_NAME, k, size=11.5)
line(PB[0], 28, PB[0], BOTTOM, stroke=RULE)

# (b) two rulers and the link between them: colours under lambda, classes under rho, iota(y) back up
title(PB, r"(b) Residual: $7 \to 3$ classes")
row_label(PB, 36, r"$(\mathcal{Z},\lambda) \to (\mathcal{Y},\rho)$, $\iota(y)$ maps back")
COLW, TY, CY, CW = 86, 76, 160, 3 * (BW + GAP) - GAP
bx0 = mid(PB) - 1.5 * COLW
for j, k in enumerate(ORDER):
    cx, cs = bx0 + j * COLW + COLW / 2, CCOL[k]
    rw = len(cs) * (BW + GAP) - GAP
    rx0 = cx - rw / 2
    txt(cx, TY - 8, rf"$\frac{{\mathrm{{d}}\nu}}{{\mathrm{{d}}\lambda}}{{=}}{CL[k]['n'] // len(cs)}$", size=11, fill=GOAL)
    for i, c in enumerate(cs):
        x = rx0 + i * (BW + GAP)
        box(x, TY, BW, BW, col(c))
        out.append(rf"  \draw[{INK}, line width=0.4pt, ->] ({f(cx)},{f(CY - 3)}) -- ({f(x + BW / 2)},{f(TY + BW + 3)});")
    txt(cx + 15, (TY + BW + CY) / 2 + 8, r"$\iota{=}1$" if len(cs) == 1 else rf"$\iota{{=}}1/{len(cs)}$", anchor="start", size=11)
    box(cx - CW / 2, CY, CW, BW, RULE)
    txt(cx, ROW_NAME, k, size=11.5)

line(PC[0], 28, PC[0], BOTTOM, stroke=RULE)

# (c) volume a held class occupies on a log scale: residual part stacked with goal part
title(PC, r"(c) Volume: residual $\times$ goal")
row_label(PC, 36, r"predictive $H_\rho(Y)$ + residual + goal")
RH, PAIRW, CG = 78, 2 * BW + GAP, 46
cx0, LV = PC[0] + 26, math.log(CL["white"]["n"])


def stripes(x, y, w, h, k, faded):
    cs = CCOL[k]
    for i, c in enumerate(cs):
        op = ", fill opacity=0.45" if faded else ""
        out.append(rf"  \fill[fill={col(c)}{op}] ({f(x + i * w / len(cs))},{f(y)}) rectangle ++({f(w / len(cs))},{f(h)});")
    out.append(rf"  \draw[{EDGE}, line width=0.3pt] ({f(x)},{f(y)}) rectangle ++({f(w)},{f(h)});")


def goal_box(x, y, w, h):
    out.append(rf"  \fill[{GOAL}, fill opacity=0.3] ({f(x)},{f(y)}) rectangle ++({f(w)},{f(h)});")
    out.append(rf"  \draw[{GOAL}, line width=0.3pt] ({f(x)},{f(y)}) rectangle ++({f(w)},{f(h)});")


line(cx0 - 8, BASE, cx0 + 3 * PAIRW + 2 * CG + 8, BASE)
for j, k in enumerate(ORDER):
    x, vl, vn = cx0 + j * (PAIRW + CG), CL[k]["cols"], CL[k]["n"]
    per = vn // vl
    h_n, h_g = RH * math.log(vl) / LV, RH * math.log(per) / LV
    if h_n > 0:
        stripes(x, BASE - h_n, PAIRW, h_n, k, True)
        txt(x + PAIRW / 2, BASE - h_n / 2 + 3.5, str(vl), size=10.5)
    if h_g > 0:
        goal_box(x, BASE - h_n - h_g, PAIRW, h_g)
        txt(x + PAIRW / 2, BASE - h_n - h_g / 2 + 3.5, rf"$\times {per}$", size=10.5, fill=GOAL)
    txt(x + PAIRW / 2, BASE - h_n - h_g - 5, str(vn), size=11, bold=True)
    txt(x + PAIRW / 2, ROW_NAME, k, size=11.5)
lgx, lgy = PC[0] + 14, 55
stripes(lgx, lgy - 9, BW, 9, "primary", True)
txt(lgx + BW + 6, lgy, r"residual, $H_\lambda(Z \mid y)$", anchor="start", size=11, fill=MUTED)
goal_box(lgx, lgy + 10, BW, 9)
txt(lgx + BW + 6, lgy + 19, r"goal, $\mathrm{d}\nu/\mathrm{d}\lambda$", anchor="start", size=11, fill=GOAL)

# inset: stationary cost H_nu of each keep set when the rig resets with probability eps
KEEP = {"primary": ["primary"], "secondary": ["secondary"], "white": ["white"], "not white": ["primary", "secondary"]}
POL = list(KEEP)


def cost(k, e):
    w = [CL[c]["n"] / (max(e, 1e-9) if c in KEEP[k] else 1) for c in ORDER]
    s = sum(w)
    return -sum((wi / s) * math.log(wi / s / CL[c]["n"]) for wi, c in zip(w, ORDER))


CCOL["not white"] = CCOL["primary"] + CCOL["secondary"]
IX0, IX1, IY0, IY1 = PC[0] + 268, PC[1] - 10, 50, BASE - 16
KN, DL = [0, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 1], 0.03


def lg(e):
    u = DL + (1 - 2 * DL) * e
    return math.log(u / (1 - u))


def ex(e):
    return IX0 + (IX1 - IX0) * (lg(e) - lg(0)) / (lg(1) - lg(0))


def hy(v):
    return IY1 - (IY1 - IY0) * (v - 1) / (math.log(total) - 1)


line(IX0, IY1, IX1, IY1, stroke=MUTED)
line(IX0, IY0 - 4, IX0, IY1, stroke=MUTED)
for v, s in ((1, "1"), (math.log(total), r"$\ln 41$")):
    line(IX0 - 3, hy(v), IX0, hy(v), stroke=MUTED)
    txt(IX0 - 5, hy(v) + 3.5, s, anchor="end", size=10, fill=MUTED)
txt(IX0 + 4, IY0 - 8, r"$H_\nu(Z)$", anchor="start", size=10.5)
LS = {
    "primary": ("lampred", ""),
    "secondary": ("lampyellow", ", dash pattern=on 2pt off 1pt"),
    "white": (EDGE, ", dash pattern=on 0.7pt off 0.7pt"),
    "not white": ("lampblue", ", dash pattern=on 3pt off 1pt on 0.7pt off 1pt"),
}
ES = [i / 700 for i in range(701)]
for k in POL:
    stroke, dash = LS[k]
    pts = " -- ".join(f"({f(ex(e))},{f(hy(cost(k, e)))})" for e in ES[::5])
    out.append(rf"  \draw[{stroke}, line width=0.6pt{dash}] {pts};")
    ly = IY1 - 62 + POL.index(k) * 17
    line(IX1 - 104, ly - 4, IX1 - 88, ly - 4, stroke=stroke, width=0.6, extra=dash)
    txt(IX1 - 84, ly, k, anchor="start", size=9.5, fill=MUTED)
# band: the keep set with the lowest cost at each eps
seg = []
for e in ES:
    k = min(POL, key=lambda q: cost(q, e))
    if not seg or seg[-1]["k"] != k:
        seg.append({"k": k, "a": e})
    seg[-1]["b"] = e
for i, s in enumerate(seg):
    xa = ex(s["a"])
    xb = ex(seg[i + 1]["a"]) if i < len(seg) - 1 else ex(s["b"])
    cs = CCOL[s["k"]]
    for j, c in enumerate(cs):
        out.append(rf"  \fill[fill={col(c)}] ({f(xa)},{f(IY1 + 3 + j * 8 / len(cs))}) rectangle ++({f(xb - xa)},{f(8 / len(cs))});")
    out.append(rf"  \draw[{EDGE}, line width=0.3pt] ({f(xa)},{f(IY1 + 3)}) rectangle ++({f(xb - xa)},8);")
for e in KN:
    line(ex(e), IY1 + 11, ex(e), IY1 + 14, stroke=MUTED)
for e, s in ((0, "0"), (0.1, "0.1"), (0.5, "0.5"), (0.9, "0.9"), (1, "1")):
    txt(ex(e), IY1 + 29, s, size=10, fill=MUTED)
txt((IX0 + IX1) / 2, ROW_NAME, r"reset rate $\eta$", size=11.5)

head = [
    "% Generated by make_lamps.py, do not edit by hand.",
    "% Lamp rig: (a) mixtures counted by colour, (b) the class Y and its law iota(y), (c) volume held as residual times goal.",
    r"\definecolor{lampink}{HTML}{1D2129}\definecolor{lampmuted}{HTML}{5B6170}\definecolor{lamprule}{HTML}{C9CED8}",
    r"\definecolor{lampedge}{HTML}{7D8494}\definecolor{lampgoal}{HTML}{7A5AA6}\definecolor{lampred}{HTML}{C0392B}",
    r"\definecolor{lampyellow}{HTML}{B08A00}\definecolor{lampblue}{HTML}{3B5F9E}",
    rf"\begin{{tikzpicture}}[x={{(\linewidth/{W},0)}}, y={{(0,-\linewidth/{W})}}]",
]
Path(__file__).with_name("lamps.tex").write_text("\n".join(head + out + [r"\end{tikzpicture}"]) + "\n")
