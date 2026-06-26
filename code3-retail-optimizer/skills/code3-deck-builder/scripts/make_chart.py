#!/usr/bin/env python3
"""Generate Code3-styled chart PNGs for deck refreshes and image-box swaps.

This is the general chart engine, covering the chart types real performance
decks use:

    pie  donut  bar  hbar  grouped  stacked  line  funnel

THE CARDINAL RULE: the output PNG's aspect ratio MUST match the slide image box
it's replacing, or PowerPoint stretches it. So always:
  1. python inspect_images.py SLIDE_XML        # read the chart box's cx x cy (EMU)
  2. python make_chart.py <type> OUT.png ... --width <px> --height <px>
        where width:height == box cx:cy  (e.g. box 2906700x1797297 -> 1067 x 660)
  3. swap OUT.png in for the chart's media file (map by POSITION, not filename),
     and REMOVE any <a:srcRect> crop on the target <p:pic> (inspect_images.py
     flags it) or the chart renders clipped.

The canvas is emitted at EXACTLY width x height (no bbox cropping), transparent
background, so what you ask for drops straight into the box. Pie/donut are drawn
in a centered SQUARE region so the circle stays round in any box; bar/line/funnel
fill the canvas with light margins.

------------------------------------------------------------------------------
DATA — three ways in (the JSON form is the contract a future data connector emits)
------------------------------------------------------------------------------
1) Inline pairs (single-series types: pie, donut, bar, hbar, funnel):
       python make_chart.py bar OUT.png "Jan:41,Feb:48,Mar:53" --unit "$K"

2) Normalized JSON (any type; required for multi-series grouped/stacked/line):
       python make_chart.py line OUT.png --data trend.json --width 1200 --height 560
   trend.json:
       {
         "categories": ["Jan", "Feb", "Mar"],
         "series": [
           {"name": "Instagram", "values": [33, 31, 36]},
           {"name": "Facebook",  "values": [18, 20, 17]}
         ],
         "unit": "%",          # optional, used in value labels
         "stacked": false      # optional; stacked-bar only
       }

3) Rollup CSV (history for line/bar without a connector yet). Long format:
       period,metric,dimension,value
       Jan 2026,spend,Instagram,41.0
       Jan 2026,spend,Facebook,22.0
       ...
   Read it:
       python make_chart.py line OUT.png --rollup deck_rollup.csv \
              --metric spend --series dimension --periods 12 --unit "$K"
   ('--series' names the column to split series on; omit it for a single total
   line. The future connector writes the SAME csv — see also `rollup-add`.)

Append this period's numbers to the rollup (so next refresh has history):
       python make_chart.py rollup-add deck_rollup.csv \
              --period "Apr 2026" --metric spend --values "Instagram:53.9,Facebook:24.1"

(Inline PAIRS as a bare positional must come right after OUT; --values is the
order-independent equivalent and is handy when other --options are present.)

Colors
------
The palette is the brand's OWN colors, read from the bundled template core's
theme (theme1 clrScheme accent1–6 + hlink, text from dk1), contrast-ordered so
adjacent series/slices stay distinct — so charts match the reference deck, and a
spawned variant's theme drives its own charts. `assets/brand_palette.json`
overrides if present. Platform logo colors (IG pink, FB blue, …) are OFF by
default (charts stay on-brand); pass --platform-colors to use them where
per-platform recognition matters.

Requires matplotlib (pip install matplotlib --break-system-packages if missing).
"""

import argparse
import csv
import glob
import json
import re
import sys
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Recognizable-ish platform colors; everything else cycles the brand palette.
PLATFORM_COLORS = {
    "instagram": "#E1306C", "ig": "#E1306C",
    "facebook": "#2985FD", "fb": "#2985FD", "meta": "#2985FD",
    "tiktok": "#201E20", "tt": "#201E20",
    "snapchat": "#F7D000", "snap": "#F7D000",
    "pinterest": "#E60023", "pin": "#E60023",
    "youtube": "#9C2200", "yt": "#9C2200",
    "linkedin": "#004CAF", "li": "#004CAF",
    "google": "#2985FD", "search": "#2985FD",
}
# Fallback only. load_brand_palette() normally derives the palette straight from
# the bundled core's THEME (so chart colors match the reference deck, and a
# variant's own theme drives its charts). This list is the Code3 theme's accent
# colors (theme1 clrScheme), contrast-ordered — used only if the theme can't be read.
CODE3_PALETTE = ["#C5E525", "#2985FD", "#F05024", "#ABC9F1",
                 "#2E5C00", "#E7F3AC", "#F2BBAC", "#201E20"]
CODE3_BLACK = "#201E20"
GRID_GRAY = "#D9D9D9"

# Platform logo colors (IG pink, FB blue, …) are OFF by default so charts use the
# brand palette; turn on with --platform-colors when per-platform recognition matters.
USE_PLATFORM_COLORS = False

CHART_TYPES = ("pie", "donut", "bar", "hbar", "grouped", "stacked", "line", "funnel")


# --------------------------------------------------------------------------- #
#  Brand + parsing helpers
# --------------------------------------------------------------------------- #
def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _order_for_contrast(colors):
    """Lead with the brand's primary accent, then greedily pick the most visually
    distinct next color — so adjacent slices/series/bars don't blur together."""
    seen = []
    for c in colors:
        if c and c.upper() not in {s.upper() for s in seen}:
            seen.append(c)
    if len(seen) <= 2:
        return seen
    out, rest = [seen[0]], seen[1:]
    while rest:
        last = _rgb(out[-1])
        nxt = max(rest, key=lambda c: sum((a - b) ** 2 for a, b in zip(_rgb(c), last)))
        out.append(nxt)
        rest.remove(nxt)
    return out


def _theme_palette(skill_dir):
    """The brand's real colors, read straight from the bundled core's theme
    (theme1 clrScheme: accent1–6 + hlink for the palette, dk1 for text). This is
    what keeps chart colors matching the reference deck. (None, None) if unread."""
    cores = sorted(glob.glob(str(skill_dir / "assets" / "*template_core*.pptx")))
    if not cores:
        return None, None
    try:
        with zipfile.ZipFile(cores[0]) as z:
            themes = sorted(n for n in z.namelist()
                            if re.match(r"ppt/theme/theme\d+\.xml$", n))
            if not themes:
                return None, None
            t = z.read(themes[0]).decode("utf-8", "ignore")
    except Exception:
        return None, None
    m = re.search(r"<a:clrScheme.*?</a:clrScheme>", t, re.DOTALL)
    if not m:
        return None, None
    s = m.group(0)

    def slot(name):
        mm = re.search(rf"<a:{name}>(.*?)</a:{name}>", s, re.DOTALL)
        if not mm:
            return None
        c = re.search(r'(?:lastClr|val)="([0-9A-Fa-f]{6})"', mm.group(1))
        return f"#{c.group(1).upper()}" if c else None

    accents = [slot(f"accent{i}") for i in range(1, 7)] + [slot("hlink")]
    pal = _order_for_contrast([c for c in accents if c])
    return (pal or None), (slot("dk1") or CODE3_BLACK)


def load_brand_palette():
    """Chart palette + text color, in precedence order:
       1. assets/brand_palette.json — explicit override (spawned variants ship one)
       2. the bundled core's THEME accent colors — matches the reference deck
       3. the Code3 fallback constants
    """
    skill_dir = Path(__file__).resolve().parent.parent
    pj = skill_dir / "assets" / "brand_palette.json"
    if pj.exists():
        try:
            d = json.loads(pj.read_text(encoding="utf-8"))
            return (d.get("palette") or CODE3_PALETTE), (d.get("black") or CODE3_BLACK)
        except Exception:
            pass
    pal, black = _theme_palette(skill_dir)
    if pal:
        return pal, (black or CODE3_BLACK)
    return CODE3_PALETTE, CODE3_BLACK


def color_for(label, i, palette):
    """Brand-palette color by default; platform logo colors only with
    --platform-colors (and only for recognized platform labels)."""
    if USE_PLATFORM_COLORS:
        return PLATFORM_COLORS.get(str(label).lower().strip(), palette[i % len(palette)])
    return palette[i % len(palette)]


def parse_pairs(spec):
    """'IG:36,FB:18' -> (['IG','FB'], [36.0, 18.0])."""
    labels, values = [], []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" not in chunk:
            print(f"ERROR: '{chunk}' is not LABEL:VALUE")
            sys.exit(1)
        label, val = chunk.rsplit(":", 1)
        labels.append(label.strip())
        values.append(float(val.strip().rstrip("%").replace(",", "")))
    return labels, values


def _compact(v):
    """1000000 -> '1M', 42000 -> '42K', 9100 -> '9.1K', 36 -> '36'."""
    a = abs(v)
    if a >= 1e6:
        return f"{v / 1e6:.1f}".rstrip("0").rstrip(".") + "M"
    if a >= 1e3:
        return f"{v / 1e3:.1f}".rstrip("0").rstrip(".") + "K"
    return f"{v:g}"


def fmt_val(v, unit):
    """Value label. '$'-prefixed units assume caller pre-scaled (no compaction);
    bare counts and %/x units get human-compact magnitudes (1M, 42K)."""
    if v is None:
        return ""
    u = (unit or "").strip()
    if u.startswith("$"):
        return f"${v:g}{u[1:]}"
    if u in ("", "%", "x", "×", "pp"):
        return f"{_compact(v)}{u}"
    return f"{v:g}{u}"


def is_platform_set(labels):
    """True if any category label is a known platform — drives per-category color."""
    return any(str(l).lower().strip() in PLATFORM_COLORS for l in labels)


def build_spec(args):
    """Return a normalized {categories, series:[{name,values}], unit, stacked}."""
    if args.data:
        d = json.loads(Path(args.data).read_text(encoding="utf-8"))
        cats = d.get("categories") or []
        series = d.get("series") or []
        if not series and "values" in d:           # tolerate a flat single-series dict
            series = [{"name": d.get("name", ""), "values": d["values"]}]
        return {
            "categories": cats,
            "series": [{"name": s.get("name", ""), "values": s.get("values", [])}
                       for s in series],
            "unit": args.unit or d.get("unit", ""),
            "stacked": d.get("stacked", args.stacked),
        }
    if args.rollup:
        return load_rollup(args.rollup, args.metric, args.series, args.periods, args.unit,
                           args.stacked)
    pairs = args.pairs or args.values
    if pairs:
        labels, values = parse_pairs(pairs)
        return {"categories": labels,
                "series": [{"name": args.metric or "", "values": values}],
                "unit": args.unit or "", "stacked": args.stacked}
    print("ERROR: no data. Pass inline PAIRS, --data FILE.json, or --rollup FILE.csv.")
    sys.exit(1)


def load_rollup(path, metric, series_col, periods, unit, stacked):
    """Read a long-format rollup CSV into a normalized spec.

    Columns: period, metric, <dimension>, value. Filters to `metric`; periods are
    taken in first-seen order (last `periods` of them). If `series_col` is given,
    one series per distinct value in that column; otherwise a single series that
    sums all rows for the period.
    """
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    if not rows:
        print(f"ERROR: rollup {path} is empty.")
        sys.exit(1)
    cols = {c.lower(): c for c in rows[0].keys()}
    pcol = cols.get("period")
    vcol = cols.get("value")
    mcol = cols.get("metric")
    if not pcol or not vcol:
        print(f"ERROR: rollup must have 'period' and 'value' columns; got {list(rows[0])}")
        sys.exit(1)
    if metric and mcol:
        rows = [r for r in rows if (r.get(mcol) or "").strip() == metric]
    if not rows:
        print(f"ERROR: no rows for metric '{metric}' in {path}.")
        sys.exit(1)

    # Period order = first-seen; keep the last N.
    period_order = []
    for r in rows:
        p = (r.get(pcol) or "").strip()
        if p and p not in period_order:
            period_order.append(p)
    if periods and periods > 0:
        period_order = period_order[-periods:]
    keep = set(period_order)

    scol = cols.get((series_col or "").lower()) if series_col else None
    if scol:
        names = []
        table = {}  # name -> {period: value}
        for r in rows:
            p = (r.get(pcol) or "").strip()
            if p not in keep:
                continue
            name = (r.get(scol) or "").strip()
            if name not in table:
                table[name] = {}
                names.append(name)
            table[name][p] = table[name].get(p, 0.0) + _num(r.get(vcol))
        series = [{"name": n, "values": [table[n].get(p) for p in period_order]}
                  for n in names]
    else:
        agg = {}
        for r in rows:
            p = (r.get(pcol) or "").strip()
            if p not in keep:
                continue
            agg[p] = agg.get(p, 0.0) + _num(r.get(vcol))
        series = [{"name": metric or "", "values": [agg.get(p) for p in period_order]}]

    return {"categories": period_order, "series": series,
            "unit": unit or "", "stacked": stacked}


def _num(s):
    try:
        return float(str(s).strip().rstrip("%").replace(",", "").replace("$", ""))
    except (TypeError, ValueError):
        return 0.0


# --------------------------------------------------------------------------- #
#  Figure scaffolding
# --------------------------------------------------------------------------- #
def new_fig(W, H, dpi):
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
    fig.patch.set_alpha(0.0)
    return fig


def style_axes(ax, black, *, keep_left=True, keep_bottom=True, grid="y"):
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_visible(keep_left)
    ax.spines["bottom"].set_visible(keep_bottom)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(black)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=black, labelsize=9, length=0)
    if grid in ("y", "both"):
        ax.yaxis.grid(True, color=GRID_GRAY, linewidth=0.8, zorder=0)
    if grid in ("x", "both"):
        ax.xaxis.grid(True, color=GRID_GRAY, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def maybe_legend(ax, black, n_series, no_legend):
    if n_series > 1 and not no_legend:
        leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13),
                        ncol=min(n_series, 4), frameon=False, fontsize=9)
        for t in leg.get_texts():
            t.set_color(black)


# --------------------------------------------------------------------------- #
#  Chart types
# --------------------------------------------------------------------------- #
def draw_pie(fig, spec, args, palette, black, donut=False):
    labels = spec["categories"]
    values = spec["series"][0]["values"]
    colors = [color_for(l, i, palette) for i, l in enumerate(labels)]
    W, H = args.width, args.height
    fill = 0.80
    if W >= H:
        wf = fill * H / W
        ax = fig.add_axes([(1 - wf) / 2, (1 - fill) / 2, wf, fill])
    else:
        hf = fill * W / H
        ax = fig.add_axes([(1 - fill) / 2, (1 - hf) / 2, fill, hf])
    total = sum(v for v in values if v) or 1
    pie_labels = [f"{l} {v / total * 100:.0f}%" if (v / total * 100) >= args.min_label
                  else "" for l, v in zip(labels, values)]
    wedges, texts, autot = ax.pie(
        values, colors=colors, labels=pie_labels, labeldistance=1.12,
        startangle=90, counterclock=False,
        autopct=lambda p: f"{p:.0f}%" if p >= 8 else "", pctdistance=0.7,
        wedgeprops={"linewidth": 1, "edgecolor": "white",
                    "width": 0.42 if donut else None},
        textprops={"fontsize": 9, "color": black})
    for t in autot:
        t.set_color("white"); t.set_fontsize(9); t.set_fontweight("bold")
    ax.set_aspect("equal")


def draw_bar(fig, spec, args, palette, black, horizontal=False):
    cats = spec["categories"]
    values = spec["series"][0]["values"]
    unit = spec["unit"]
    ax = fig.add_axes([0.10, 0.16, 0.86, 0.74])
    # Per-category color only when categories are platforms (IG/FB/...); a plain
    # single series (months, campaigns) reads cleaner in one brand color.
    if USE_PLATFORM_COLORS and is_platform_set(cats):
        colors = [color_for(c, i, palette) for i, c in enumerate(cats)]
    else:
        colors = [palette[0]] * len(cats)
    if horizontal:
        order = list(range(len(cats)))
        y = range(len(cats))
        ax.barh(list(y), values, color=colors, zorder=3, height=0.66)
        ax.set_yticks(list(y)); ax.set_yticklabels(cats)
        ax.invert_yaxis()
        style_axes(ax, black, keep_left=False, keep_bottom=True, grid="x")
        vmax = max([v for v in values if v] or [1])
        for yi, v in zip(y, values):
            if v is None:
                continue
            ax.text(v + vmax * 0.01, yi, fmt_val(v, unit), va="center",
                    ha="left", fontsize=9, color=black, fontweight="bold")
        ax.set_xlim(0, vmax * 1.14)
    else:
        x = range(len(cats))
        ax.bar(list(x), values, color=colors, zorder=3, width=0.62)
        ax.set_xticks(list(x)); ax.set_xticklabels(cats)
        style_axes(ax, black, keep_left=True, keep_bottom=True, grid="y")
        vmax = max([v for v in values if v] or [1])
        for xi, v in zip(x, values):
            if v is None:
                continue
            ax.text(xi, v + vmax * 0.02, fmt_val(v, unit), va="bottom",
                    ha="center", fontsize=9, color=black, fontweight="bold")
        ax.set_ylim(0, vmax * 1.16)


def draw_grouped(fig, spec, args, palette, black):
    cats = spec["categories"]
    series = spec["series"]
    unit = spec["unit"]
    ax = fig.add_axes([0.10, 0.16, 0.86, 0.72])
    n = len(series)
    group_w = 0.8
    bar_w = group_w / max(n, 1)
    x = list(range(len(cats)))
    for si, s in enumerate(series):
        offs = [xi - group_w / 2 + bar_w * (si + 0.5) for xi in x]
        ax.bar(offs, s["values"], width=bar_w, label=s["name"],
               color=color_for(s["name"], si, palette), zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(cats)
    style_axes(ax, black, grid="y")
    allv = [v for s in series for v in s["values"] if v is not None] or [1]
    ax.set_ylim(0, max(allv) * 1.16)
    if unit:
        ax.set_ylabel(unit, color=black, fontsize=9)
    maybe_legend(ax, black, n, args.no_legend)


def draw_stacked(fig, spec, args, palette, black):
    cats = spec["categories"]
    series = spec["series"]
    ax = fig.add_axes([0.10, 0.16, 0.86, 0.72])
    x = list(range(len(cats)))
    bottoms = [0.0] * len(cats)
    for si, s in enumerate(series):
        vals = [v or 0.0 for v in s["values"]]
        ax.bar(x, vals, bottom=bottoms, width=0.6, label=s["name"],
               color=color_for(s["name"], si, palette), zorder=3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.set_xticks(x); ax.set_xticklabels(cats)
    style_axes(ax, black, grid="y")
    ax.set_ylim(0, max(bottoms or [1]) * 1.12)
    maybe_legend(ax, black, len(series), args.no_legend)


def draw_line(fig, spec, args, palette, black):
    cats = spec["categories"]
    series = spec["series"]
    unit = spec["unit"]
    ax = fig.add_axes([0.10, 0.16, 0.86, 0.72])
    x = list(range(len(cats)))
    for si, s in enumerate(series):
        ax.plot(x, s["values"], marker="o", markersize=5, linewidth=2.4,
                color=color_for(s["name"], si, palette), label=s["name"], zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(cats)
    style_axes(ax, black, keep_left=True, keep_bottom=True, grid="y")
    if unit:
        ax.set_ylabel(unit, color=black, fontsize=9)
    maybe_legend(ax, black, len(series), args.no_legend)


def draw_funnel(fig, spec, args, palette, black):
    """Centered funnel. Ad funnels are very top-heavy (1M -> 3K), so band width is
    true-proportional with only a thin visibility floor, and every stage's label
    (name · value · % of top) is drawn in black on the row so it reads at any
    width — never white text that vanishes on a sliver."""
    labels = spec["categories"]
    values = spec["series"][0]["values"]
    unit = spec["unit"]
    n = len(labels)
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.88])
    ax.set_xlim(0, 1); ax.set_ylim(0, n)
    ax.invert_yaxis(); ax.axis("off")
    top = next((v for v in values if v), 0) or 1
    for i, (lab, v) in enumerate(zip(labels, values)):
        v = v or 0.0
        w = max(v / top, 0.006)              # true proportion; sliver stays visible
        ax.barh(i + 0.5, w, left=(1 - w) / 2, height=0.6,
                color=color_for(lab, i, palette), zorder=3)
        p = v / top * 100
        pct = f"{p:.1f}%" if 0 < p < 10 else f"{p:.0f}%"   # keep sub-1% from reading as 0%
        ax.text(0.5, i + 0.5, f"{lab}  ·  {fmt_val(v, unit)}  ({pct})",
                va="center", ha="center", fontsize=10, color=black,
                fontweight="bold", zorder=4)


DRAWERS = {
    "pie": lambda f, sp, a, p, b: draw_pie(f, sp, a, p, b, donut=False),
    "donut": lambda f, sp, a, p, b: draw_pie(f, sp, a, p, b, donut=True),
    "bar": lambda f, sp, a, p, b: draw_bar(f, sp, a, p, b, horizontal=False),
    "hbar": lambda f, sp, a, p, b: draw_bar(f, sp, a, p, b, horizontal=True),
    "grouped": draw_grouped,
    "stacked": draw_stacked,
    "line": draw_line,
    "funnel": draw_funnel,
}


# --------------------------------------------------------------------------- #
#  rollup-add (append this period's numbers so next refresh has history)
# --------------------------------------------------------------------------- #
def rollup_add(args):
    pairs = args.pairs or args.values
    if not (args.period and pairs):
        print("ERROR: rollup-add needs --period and values "
              "(--values \"Instagram:53.9,Facebook:24.1\").")
        sys.exit(1)
    labels, values = parse_pairs(pairs)
    path = Path(args.out)  # for rollup-add, OUT is the csv path
    header = ["period", "metric", "dimension", "value"]
    exists = path.exists()
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if not exists:
            w.writerow(header)
        for lab, v in zip(labels, values):
            w.writerow([args.period, args.metric or "", lab, v])
    print(f"Appended {len(labels)} row(s) to {path} for period '{args.period}'"
          f"{f', metric {args.metric}' if args.metric else ''}.")


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(
        description="Code3-styled chart PNGs (aspect-matched, transparent).")
    ap.add_argument("type", help="chart type: " + " ".join(CHART_TYPES)
                    + " | rollup-add")
    ap.add_argument("out", help="output PNG path (or rollup CSV path for rollup-add)")
    ap.add_argument("pairs", nargs="?", help='inline "Label:Value,Label:Value" '
                    "(bare positional — must come right after OUT)")
    ap.add_argument("--values", help='order-independent equivalent of inline PAIRS')
    ap.add_argument("--data", help="normalized JSON data file")
    ap.add_argument("--rollup", help="rollup CSV (long: period,metric,dimension,value)")
    ap.add_argument("--metric", help="rollup metric to filter on / series name")
    ap.add_argument("--series", help="rollup column to split series on (e.g. dimension)")
    ap.add_argument("--periods", type=int, default=0, help="keep last N periods (0=all)")
    ap.add_argument("--period", help="rollup-add: the period label to append")
    ap.add_argument("--unit", default="", help='value unit, e.g. "%%" or "$K"')
    ap.add_argument("--title", default="", help="optional chart title (usually omit)")
    ap.add_argument("--stacked", action="store_true", help="stacked bars (stacked type)")
    ap.add_argument("--no-legend", action="store_true")
    ap.add_argument("--platform-colors", action="store_true",
                    help="use each platform's logo color (IG pink, FB blue, …) "
                         "instead of the brand palette, for recognized platform labels")
    ap.add_argument("--width", type=int, default=1100, help="px width = box cx")
    ap.add_argument("--height", type=int, default=620, help="px height = box cy")
    ap.add_argument("--dpi", type=int, default=96)
    ap.add_argument("--min-label", type=float, default=3.0,
                    help="pie: hide labels for slices below this percent")
    args = ap.parse_args()

    global USE_PLATFORM_COLORS
    USE_PLATFORM_COLORS = args.platform_colors

    if args.type == "rollup-add":
        rollup_add(args)
        return

    if args.type not in CHART_TYPES:
        print(f"ERROR: unknown type '{args.type}'. Use one of: "
              + ", ".join(CHART_TYPES) + ", or rollup-add.")
        sys.exit(1)

    palette, black = load_brand_palette()
    spec = build_spec(args)
    if not spec["series"] or not spec["categories"]:
        print("ERROR: no plottable data (need categories + at least one series).")
        sys.exit(1)
    if args.type in ("grouped", "stacked", "line") and len(spec["series"]) == 0:
        print(f"ERROR: {args.type} needs at least one series.")
        sys.exit(1)

    W, H = args.width, args.height
    fig = new_fig(W, H, args.dpi)
    DRAWERS[args.type](fig, spec, args, palette, black)
    if args.title:
        fig.suptitle(args.title, color=black, fontsize=11, fontweight="bold", y=0.99)
    fig.savefig(args.out, transparent=True, dpi=args.dpi)
    print(f"Wrote {args.out} ({args.type}) at {W}x{H}px (aspect {W / H:.2f}). "
          f"Confirm width:height matches the box's cx:cy so it isn't stretched.")


if __name__ == "__main__":
    main()
