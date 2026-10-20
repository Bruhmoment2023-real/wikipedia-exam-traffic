"""v10 figures for paper 05, drawn with numpy + PIL (matplotlib and pandas are not installed here).

Figure 1 (seasonal profile) is recomputed from the pack panel with the same steps as
fig_profile() in the pack's code/07_figures.py, then drawn with a legend outside the plot area.
Figure 2 (yearly gap) is drawn from the pack's results/yearly_gaps_full_all.csv
(MAIN spec, English, article-level), the same numbers as Table 1 of the paper.

Reads only D:/Research-Compilation/05-wikipedia-exam-traffic (read-only). Writes new files only.
Usage: python -I make_figs_v10.py
"""
import csv, datetime as dt, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PACK = "D:/Research-Compilation/05-wikipedia-exam-traffic"
PAPER = "D:/Isolated/papers/05-wikipedia-exam-traffic"
OUT1 = PAPER + "/figures/fig1_seasonal_profile_en_v10.png"
OUT2 = PAPER + "/figures/fig2_yearly_gap_en_v10.png"
OUTCSV = PAPER + "/analysis/fig1_profile_values_v10.csv"

D0 = dt.date(2015, 7, 1)
NDAYS = (dt.date(2026, 9, 30) - D0).days + 1
FIRST = {2016: "2016-03-01", 2017: "2017-03-09", 2018: "2018-03-05", 2019: "2019-02-15", 2020: "2020-02-15",
         2021: "2021-05-04", 2022: "2022-04-26", 2023: "2023-02-15", 2024: "2024-02-15", 2025: "2025-02-15",
         2026: "2026-02-17"}
PRE, POST = [2017, 2018, 2019, 2020], [2023, 2024, 2025, 2026]

BLUE, ORANGE, INK, MUTED, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SHADE = "#efeeea"
FONT = "C:/Windows/Fonts/arial.ttf"
FONTB = "C:/Windows/Fonts/arialbd.ttf"
S = 2  # supersampling factor


def di(s):
    return (dt.date.fromisoformat(s) - D0).days


def load_pairs():
    rows = list(csv.DictReader(open(PACK + "/data/panel_full_en_index.csv", encoding="utf-8")))
    for r in rows:
        for k in r:
            r[k] = r[k] or ""
    fetched = lambda r: r["fetched"] == "True"
    ctl = {}
    for r in rows:
        if r["group"] == "A_same_area" and fetched(r) and r["matched_to"] not in ctl:
            ctl[r["matched_to"]] = r["article"]
    first_row = {}
    for i, r in enumerate(rows):
        first_row.setdefault(r["article"], i)
    P = []
    for i, r in enumerate(rows):
        if r["group"] == "syllabus" and r["area"] in ("SCI", "MAT") and fetched(r) and r["matched_to"] in ctl:
            P.append((i, first_row[ctl[r["matched_to"]]]))
    return np.array(P, dtype=int)


def profiles():
    z = np.load(PACK + "/data/panel_full_en.npz")
    mat = z["all_access"].astype(float)
    assert mat.shape[1] == NDAYS
    P = load_pairs()
    print("pairs", len(P))
    rel = np.arange(-150, 121)
    out = {}
    for period, yrs in (("pre", PRE), ("post", POST)):
        for col in (0, 1):
            prof = []
            for y in yrs:
                F = di(FIRST[y])
                b = np.arange(di("%d-07-01" % (y - 1)), di("%d-10-31" % (y - 1)) + 1)
                base = mat[P[:, col]][:, b].mean(1)
                ok = base >= 5
                seg = mat[P[ok, col]][:, F + rel[0] - 3: F + rel[-1] + 4] / base[ok][:, None]
                k = np.ones(7) / 7
                sm = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 1, seg)
                prof.append(np.exp(np.log(np.clip(sm, 1e-6, None)).mean(0)))
            out[(period, col)] = np.mean(prof, axis=0)
    return rel, out, len(P)


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size * S)


class Axes:
    def __init__(self, draw, box, xlim, ylim):
        self.d, self.box, self.xlim, self.ylim = draw, [v * S for v in box], xlim, ylim

    def px(self, x, y):
        x0, y0, x1, y1 = self.box
        X = x0 + (x - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * (x1 - x0)
        Y = y1 - (y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * (y1 - y0)
        return X, Y

    def hgrid(self, ys, color=GRID, w=1):
        for y in ys:
            a, b = self.px(self.xlim[0], y), self.px(self.xlim[1], y)
            self.d.line([a, b], fill=hexc(color), width=w * S)

    def vspan(self, xa, xb, color=SHADE):
        a, b = self.px(xa, self.ylim[1]), self.px(xb, self.ylim[0])
        self.d.rectangle([a, b], fill=hexc(color))

    def vdotted(self, x, color=MUTED):
        X = self.px(x, 0)[0]
        y0, y1 = self.box[1], self.box[3]
        y = y0
        while y < y1:
            self.d.line([(X, y), (X, min(y + 2 * S, y1))], fill=hexc(color), width=S)
            y += 5 * S

    def line(self, xs, ys, color, w=2):
        pts = [self.px(x, y) for x, y in zip(xs, ys)]
        self.d.line(pts, fill=hexc(color), width=int(w * S), joint="curve")

    def frame(self):
        x0, y0, x1, y1 = self.box
        self.d.line([(x0, y0), (x0, y1)], fill=hexc("#b9b8b3"), width=S)
        self.d.line([(x0, y1), (x1, y1)], fill=hexc("#b9b8b3"), width=S)

    def xticks(self, ticks, labels, f, ink=MUTED):
        for t, l in zip(ticks, labels):
            X, Y = self.px(t, self.ylim[0])
            self.d.line([(X, Y), (X, Y + 4 * S)], fill=hexc("#b9b8b3"), width=S)
            self.d.text((X, Y + 6 * S), l, font=f, fill=hexc(ink), anchor="ma")

    def yticks(self, ticks, labels, f, ink=MUTED, show=True):
        for t, l in zip(ticks, labels):
            X, Y = self.px(self.xlim[0], t)
            self.d.line([(X - 4 * S, Y), (X, Y)], fill=hexc("#b9b8b3"), width=S)
            if show:
                self.d.text((X - 7 * S, Y), l, font=f, fill=hexc(ink), anchor="rm")


def vtext(img, xy, text, f, color):
    """vertical text, centred on xy, reading bottom to top"""
    lines = text.split("\n")
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w = max(tmp.textlength(l, font=f) for l in lines)
    lh = f.size * 1.2
    t = Image.new("RGBA", (int(w) + 4, int(lh * len(lines)) + 4), (0, 0, 0, 0))
    dd = ImageDraw.Draw(t)
    for i, l in enumerate(lines):
        dd.text((t.width / 2, i * lh), l, font=f, fill=hexc(color), anchor="ma")
    t = t.rotate(90, expand=True)
    img.paste(t, (int(xy[0] - t.width / 2), int(xy[1] - t.height / 2)), t)


def legend(d, x, y, items, f):
    """items: list of (kind, color, label). kind in line|dot|hollow|shade|dotted. Draws a framed box; returns its width."""
    pad, sw, gap = 10 * S, 26 * S, 22 * S
    widths = [sw + 8 * S + d.textlength(lab, font=f) for _, _, lab in items]
    W = sum(widths) + gap * (len(items) - 1) + 2 * pad
    H = f.size + 2 * pad
    d.rectangle([x, y, x + W, y + H], fill=hexc("#ffffff"), outline=hexc("#c9c8c3"), width=S)
    cx, cy = x + pad, y + H / 2
    for (kind, color, lab), w in zip(items, widths):
        if kind == "line":
            d.line([(cx, cy), (cx + sw, cy)], fill=hexc(color), width=3 * S)
        elif kind == "shade":
            d.rectangle([cx, cy - 7 * S, cx + sw, cy + 7 * S], fill=hexc(SHADE), outline=hexc("#d6d5d0"), width=S)
        elif kind == "dotted":
            yy = cy - 8 * S
            while yy < cy + 8 * S:
                d.line([(cx + sw / 2, yy), (cx + sw / 2, yy + 2 * S)], fill=hexc(color), width=S)
                yy += 5 * S
        elif kind in ("dot", "hollow"):
            m = cx + sw / 2
            d.line([(m, cy - 8 * S), (m, cy + 8 * S)], fill=hexc(color) if kind == "dot" else hexc("#9fc1ea"), width=2 * S)
            r = 5 * S
            d.ellipse([m - r, cy - r, m + r, cy + r], fill=hexc(color) if kind == "dot" else hexc(SURF),
                      outline=hexc(color), width=2 * S)
        d.text((cx + sw + 8 * S, cy), lab, font=f, fill=hexc(INK), anchor="lm")
        cx += w + gap
    return W


def fig1(rel, out):
    W, H = 1180, 500
    img = Image.new("RGB", (W * S, H * S), hexc(SURF))
    d = ImageDraw.Draw(img)
    fT, fS, fL, fN = font(15, True), font(13, True), font(12), font(11)
    d.text((12 * S, 10 * S), "English Wikipedia, science and mathematics: traffic through the exam year",
           font=fT, fill=hexc(INK))
    items = [("line", BLUE, "Syllabus articles"), ("line", ORANGE, "Matched control articles"),
             ("shade", SHADE, "Exam window (28 days before to 20 days after)"), ("dotted", MUTED, "First CBSE paper")]
    legend(d, 96 * S, 38 * S, items, fN)
    ylim = (0.74, 1.28)
    yt = [0.8, 0.9, 1.0, 1.1, 1.2]
    boxes = [(96, 112, 580, 430), (650, 112, 1134, 430)]
    for k, (box, (period, title)) in enumerate(zip(boxes, [("pre", "Before: exam years 2017-2020"),
                                                         ("post", "After: exam years 2023-2026")])):
        ax = Axes(d, box, (-150, 125), ylim)
        ax.vspan(-28, 20)
        ax.hgrid([0.8, 0.9, 1.1, 1.2])
        ax.hgrid([1.0], color="#d3d2cd", w=1)
        ax.vdotted(0)
        ax.line(rel, out[(period, 1)], ORANGE)
        ax.line(rel, out[(period, 0)], BLUE)
        ax.frame()
        ax.xticks([-150, -100, -50, 0, 50, 100], ["-150", "-100", "-50", "0", "50", "100"], fL)
        ax.yticks(yt, ["%.1f" % v for v in yt], fL, show=True)
        d.text((box[0] * S, (box[1] - 22) * S), title, font=fS, fill=hexc(INK))
        d.text(((box[0] + box[2]) / 2 * S, (box[3] + 26) * S), "Days from the first CBSE board paper",
               font=fL, fill=hexc(MUTED), anchor="ma")
    vtext(img, (30 * S, 271 * S), "Daily views / article's own Jul-Oct average\n(7-day mean, geometric mean over articles)",
          fL, MUTED)
    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT1, dpi=(160, 160))


def fig2():
    rows = [r for r in csv.DictReader(open(PACK + "/results/yearly_gaps_full_all.csv", encoding="utf-8"))
            if r["spec"].startswith("MAIN") and r["lang"] == "en" and r["estimator"] == "article-level"]
    rows = [r for r in rows if 2017 <= int(r["year"]) <= 2026]
    rows.sort(key=lambda r: int(r["year"]))
    W, H = 900, 470
    img = Image.new("RGB", (W * S, H * S), hexc(SURF))
    d = ImageDraw.Draw(img)
    fT, fL, fN = font(15, True), font(12), font(11)
    d.text((12 * S, 10 * S), "English Wikipedia, science and mathematics: exam-season gap by year (711 pairs)",
           font=fT, fill=hexc(INK))
    legend(d, 96 * S, 38 * S, [("dot", BLUE, "Pre- or post-period year"), ("hollow", BLUE, "Set-aside year"),
                                ("shade", SHADE, "Post-period (after ChatGPT's launch)")], fN)
    box = (96, 100, 870, 400)
    ylim = (-0.10, 0.16)
    ax = Axes(d, box, (2016.4, 2026.6), ylim)
    ax.vspan(2022.5, 2026.6)
    yt = [-0.10, -0.05, 0.0, 0.05, 0.10, 0.15]
    ax.hgrid([v for v in yt if v != 0])
    ax.hgrid([0.0], color=MUTED, w=1)
    for r in rows:
        y, g, lo, hi = int(r["year"]), float(r["gap"]), float(r["ci_lo"]), float(r["ci_hi"])
        solid = r["role"] in ("pre", "post")
        a, b = ax.px(y, lo), ax.px(y, hi)
        d.line([a, b], fill=hexc(BLUE) if solid else hexc("#9fc1ea"), width=3 * S)
        cx, cy = ax.px(y, g)
        rr = 6 * S
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=hexc(BLUE) if solid else hexc(SURF),
                  outline=hexc(BLUE), width=2 * S)
    ax.frame()
    yrs = list(range(2017, 2027))
    ax.xticks(yrs, [str(v) for v in yrs], fL)
    for lab, xa, xb in (("pre", 2017, 2020), ("set aside", 2021, 2022), ("post", 2023, 2026)):
        X = (ax.px(xa, 0)[0] + ax.px(xb, 0)[0]) / 2
        d.text((X, (box[3] + 26) * S), lab, font=fN, fill=hexc(MUTED), anchor="ma")
    ax.yticks(yt, ["%.2f" % v for v in yt], fL)
    d.text(((box[0] + box[2]) / 2 * S, (box[3] + 46) * S), "Exam year", font=fL, fill=hexc(MUTED), anchor="ma")
    vtext(img, (28 * S, 250 * S), "Gap in exam-season uplift, syllabus minus control\n(log points; 0.10 is about 10%)", fL, MUTED)
    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT2, dpi=(160, 160))
    return rows


if __name__ == "__main__":
    for p in (OUT1, OUT2, OUTCSV):
        if os.path.exists(p):
            sys.exit("exists, will not overwrite: " + p)
    rel, out, n = profiles()
    with open(OUTCSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["day_rel_first_paper", "pre_syllabus", "pre_control", "post_syllabus", "post_control"])
        for i, r in enumerate(rel):
            w.writerow([int(r)] + ["%.5f" % out[k][i] for k in (("pre", 0), ("pre", 1), ("post", 0), ("post", 1))])
    fig1(rel, out)
    rows = fig2()
    for r in rows:
        print(r["year"], r["role"], r["gap"], r["ci_lo"], r["ci_hi"])
    print("wrote", OUT1, OUT2, OUTCSV)
