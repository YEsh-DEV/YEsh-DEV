"""
All artwork for the profile, drawn as self-contained SVG (no external files, no fonts to load).
Standard library only. Logos come from icons.json (simple-icons, CC0) plus original line-art marks.
"""
import json
import math
import random
import textwrap
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ICONS = json.loads((HERE / "icons.json").read_text())

SERIF = "Georgia,'Times New Roman','DejaVu Serif',serif"
SANS = "'Segoe UI',Helvetica,Arial,'DejaVu Sans',sans-serif"
INK, INK2 = "#3a2614", "#5a4026"
RED = "#a3281f"
GOLD = "#d8b455"

EMB = dict(bone="#efe8d5", bone_line="#0b1514", jade="#3f8f5f", gold="#d8b455",
           steel="#c9d6d3", steel_line="#0b1514", ink="#0b1514", handle="#1b2b27")


# ------------------------------------------------------------------ helpers
def icon(slug, x, y, size, color, sw=1.8):
    ic, s = ICONS[slug], size / 24
    if "d" in ic:
        return f'<path transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" d="{ic["d"]}" fill="{color}"/>'
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ic["svg"]}</g>')


def wrap(text, width, max_lines=None):
    lines = textwrap.wrap(text, width)
    return lines[:max_lines] if max_lines else lines


def paper_defs(uid):
    return (f'<radialGradient id="paper{uid}" cx="50%" cy="45%" r="80%"><stop offset="0" stop-color="#ead9ab"/>'
            f'<stop offset="1" stop-color="#d3bd86"/></radialGradient>')


# ------------------------------------------------------------------ emblem (original art)
def emblem(cx, cy, s, p=EMB):
    def blade(angle):
        return f'''<g transform="rotate({angle})">
  <polygon points="0,-92 4,-72 4,42 -4,42 -4,-72" fill="{p['steel']}" stroke="{p['steel_line']}" stroke-width="1.2" stroke-linejoin="round"/>
  <line x1="0" y1="-84" x2="0" y2="36" stroke="{p['bone']}" stroke-width="1" opacity=".55"/>
  <ellipse cx="0" cy="46" rx="12" ry="4" fill="{p['gold']}" stroke="{p['steel_line']}" stroke-width="1"/>
  <rect x="-3.2" y="49" width="6.4" height="34" rx="2" fill="{p['handle']}" stroke="{p['steel_line']}" stroke-width="1"/>
  <circle cx="0" cy="86" r="4.2" fill="{p['gold']}" stroke="{p['steel_line']}" stroke-width="1"/>
</g>'''
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  <circle r="97" fill="none" stroke="{p['gold']}" stroke-width="3"/>
  <circle r="90" fill="none" stroke="{p['jade']}" stroke-width="1" opacity=".8"/>
  {blade(-38)}{blade(38)}{blade(0)}
  <ellipse cx="0" cy="-6" rx="41" ry="37" fill="{p['bone']}" stroke="{p['bone_line']}" stroke-width="2"/>
  <rect x="-23" y="20" width="46" height="23" rx="7" fill="{p['bone']}" stroke="{p['bone_line']}" stroke-width="2"/>
  <ellipse cx="-15" cy="-4" rx="9.5" ry="10.5" fill="{p['ink']}"/><ellipse cx="15" cy="-4" rx="9.5" ry="10.5" fill="{p['ink']}"/>
  <path d="M0,7 L-4.5,17 L4.5,17 Z" fill="{p['ink']}"/>
  <g stroke="{p['bone_line']}" stroke-width="2" stroke-linecap="round">
    <line x1="-13" y1="31" x2="-13" y2="42"/><line x1="-4.5" y1="31" x2="-4.5" y2="42"/>
    <line x1="4.5" y1="31" x2="4.5" y2="42"/><line x1="13" y1="31" x2="13" y2="42"/></g>
  <path d="M-42,-27 Q0,-47 42,-27 L42,-14 Q0,-34 -42,-14 Z" fill="{p['jade']}" stroke="{p['bone_line']}" stroke-width="1.6" stroke-linejoin="round"/>
  <path d="M-42,-24 L-60,-14 L-52,-26 L-62,-30 Z" fill="{p['jade']}" stroke="{p['bone_line']}" stroke-width="1.4" stroke-linejoin="round"/>
  <g fill="none" stroke="{p['gold']}" stroke-width="2.4"><circle cx="45" cy="-2" r="3"/><circle cx="46" cy="6" r="3"/><circle cx="44" cy="14" r="3"/></g>
</g>'''


# ------------------------------------------------------------------ wanted poster
def bounty(st):
    v = lambda k: st.get(k) or 0
    return (50_000_000 + v("commits") * 500_000 + v("prs") * 5_000_000 + v("repos") * 10_000_000
            + v("stars") * 25_000_000 + v("followers") * 20_000_000)


def poster(st, name, epithet, delta=None):
    amount = bounty(st)
    text = f"\u0e3f {amount:,}"
    size = min(62, int(440 / (len(text) * 0.60)))
    show = lambda k: "\u2014" if st.get(k) is None else f"{st[k]:,}"
    cols = [("commits this year", show("commits")), ("pull requests", show("prs")),
            ("public repos", show("repos")), ("stars earned", show("stars"))]
    stats = ""
    for i, (label, val) in enumerate(cols):
        x = 105 + i * 130
        stats += (f'<text x="{x}" y="790" font-size="26" font-weight="700" text-anchor="middle" fill="{INK}">{val}</text>'
                  f'<text x="{x}" y="810" font-size="11.5" text-anchor="middle" fill="{INK2}">{label}</text>')
    delta_xml = ""
    if delta and delta > 0:
        delta_xml = (f'<text x="300" y="750" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" '
                     f'fill="#2f7d4f">+\u0e3f {delta:,} this week</text>')
    nm = escape(name.upper())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 880" role="img" aria-label="Wanted poster for {escape(name)}, {escape(epithet)}. Bounty {amount:,} berries, computed from GitHub activity.">
<defs>{paper_defs("P")}
  <radialGradient id="sea" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="#1c3a33"/><stop offset="1" stop-color="#0b1a17"/></radialGradient></defs>
<rect width="600" height="880" rx="10" fill="url(#paperP)"/>
<path d="M0,310 C150,300 450,322 600,306" fill="none" stroke="#8a6a34" stroke-width="1" opacity=".18"/>
<path d="M0,580 C160,572 440,590 600,576" fill="none" stroke="#8a6a34" stroke-width="1" opacity=".16"/>
<rect x="14" y="14" width="572" height="852" rx="6" fill="none" stroke="{INK}" stroke-width="6"/>
<rect x="28" y="28" width="544" height="824" fill="none" stroke="{INK}" stroke-width="1.5"/>
<text x="300" y="122" text-anchor="middle" font-family="{SERIF}" font-size="100" font-weight="700" fill="{INK}" textLength="460" lengthAdjust="spacingAndGlyphs">WANTED</text>
<rect x="90" y="148" width="420" height="330" fill="url(#sea)" stroke="{INK}" stroke-width="5"/>
{emblem(300, 313, 1.52)}
<text x="300" y="540" text-anchor="middle" font-family="{SERIF}" font-size="40" font-weight="700" fill="{INK}" textLength="420" lengthAdjust="spacingAndGlyphs">DEAD OR ALIVE</text>
<text x="300" y="594" text-anchor="middle" font-family="{SERIF}" font-size="34" font-weight="700" fill="{INK}" textLength="470" lengthAdjust="spacingAndGlyphs">{nm}</text>
<text x="300" y="630" text-anchor="middle" font-family="{SERIF}" font-size="20" font-style="italic" fill="{INK2}">{escape(epithet)}</text>
<line x1="90" y1="654" x2="510" y2="654" stroke="{INK}" stroke-width="1.5"/>
<text x="300" y="722" text-anchor="middle" font-family="{SERIF}" font-size="{size}" font-weight="700" fill="{INK}">{text}</text>
{delta_xml}
<g font-family="{SANS}">{stats}</g>
<text x="300" y="840" text-anchor="middle" font-family="{SANS}" font-size="11" font-style="italic" fill="{INK2}">Bounty is computed from public GitHub activity and refreshed daily.</text>
</svg>
'''


# ------------------------------------------------------------------ living sea
def moon_fraction(d):
    ref = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    now = datetime(d.year, d.month, d.day, 12, tzinfo=timezone.utc)
    return (((now - ref).total_seconds() / 86400) % 29.530588853) / 29.530588853


def _moon(cx, cy, r, p):
    t = math.cos(2 * math.pi * p)
    rx, k = max(r * abs(t), 0.01), (1 - t) / 2
    glow = f'<circle cx="{cx}" cy="{cy}" r="{r*3.4}" fill="url(#moonglow)" opacity="{0.15 + 0.85*k:.2f}"/>'
    dark = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#16302a"/>'
    lit = ""
    if not (abs(t) > 0.985 and t > 0):
        waxing = p < 0.5
        limb, term = (1, 0 if t > 0 else 1) if waxing else (0, 1 if t > 0 else 0)
        lit = (f'<path d="M{cx},{cy-r} A{r},{r} 0 0 {limb} {cx},{cy+r} A{rx:.2f},{r} 0 0 {term} {cx},{cy-r} Z" fill="#f1ecd2"/>')
    ring = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#8fb5a6" stroke-width="1" opacity=".5"/>'
    return glow + dark + lit + ring


def _smooth(pts):
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def _back_wave(W, H, y, amp, wl, fill, opacity, dur):
    n = int(W / wl) + 3
    d = f"M0,{y} Q{wl/4},{y-amp} {wl/2},{y} T{wl},{y} " + " ".join(f"T{wl*(i+1)},{y}" for i in range(1, n))
    return (f'<g opacity="{opacity}"><path d="{d} L{wl*n},{H} L0,{H} Z" fill="{fill}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-wl} 0" dur="{dur}s" repeatCount="indefinite"/></path></g>')


def _ship(x, y, angle, s):
    return f'''<g transform="translate({x:.1f},{y:.1f}) rotate({angle:.1f}) scale({s})">
<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="3.6s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1"/>
<g><animateTransform attributeName="transform" type="rotate" values="-1.6;1.6;-1.6" dur="3.6s" repeatCount="indefinite"/>
  <line x1="-4" y1="-4" x2="-4" y2="-86" stroke="#2a1d12" stroke-width="3"/>
  <line x1="22" y1="-4" x2="22" y2="-66" stroke="#2a1d12" stroke-width="2.6"/>
  <path d="M-4,-82 C-30,-70 -34,-40 -30,-22 L-4,-22 Z" fill="#e8e1c9"/><path d="M-4,-82 C14,-70 18,-40 16,-22 L-4,-22 Z" fill="#d7cfb2"/>
  <path d="M22,-62 C6,-54 4,-34 7,-22 L22,-22 Z" fill="#e8e1c9"/><path d="M22,-62 C36,-54 38,-34 36,-22 L22,-22 Z" fill="#d7cfb2"/>
  <path d="M-4,-86 L-4,-98 L14,-93 L-4,-88 Z" fill="#3f8f5f"/>
  <path d="M-46,-8 L40,-8 C38,6 26,14 4,14 L-26,14 C-38,14 -46,4 -46,-8 Z" fill="#3a2716"/>
  <path d="M-46,-8 L40,-8" stroke="#d8b455" stroke-width="2"/><path d="M40,-8 L54,-14 L40,-2 Z" fill="#3a2716"/>
</g></g></g>'''


def _island(x, w, h, seed, horizon):
    rnd = random.Random(seed)
    pts = [(x - w / 2, horizon + 2)]
    for k in range(1, 6):
        pts.append((x - w / 2 + w * k / 6, horizon - h * (0.5 + rnd.random() * 0.5) * math.sin(math.pi * k / 6)))
    pts.append((x + w / 2, horizon + 2))
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + " Z"
    return (f'<path d="{d}" fill="#123b33" stroke="#1f5c4d" stroke-width=".8"/>'
            f'<line x1="{x+w*0.1:.1f}" y1="{horizon-h*0.7:.1f}" x2="{x+w*0.1:.1f}" y2="{horizon-h*0.7-9:.1f}" stroke="#123b33" stroke-width="1.6"/>')


def living_sea(weeks, island_weeks, today):
    W, H, horizon, base = 900, 250, 150, 205
    n = len(weeks)
    sm = [sum(weeks[max(0, i - 1):i + 2]) / len(weeks[max(0, i - 1):i + 2]) for i in range(n)]
    pts = [(i * W / (n - 1), base - min(58, 10 * math.sqrt(c))) for i, c in enumerate(sm)]
    si = n - 12
    sx, sy = pts[si]
    ang = max(-9, min(9, math.degrees(math.atan2(pts[si + 1][1] - pts[si - 1][1], pts[si + 1][0] - pts[si - 1][0]))))
    rnd = random.Random(11)
    stars = "".join(
        f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(6, 120):.0f}" r="{rnd.choice([0.7, 0.9, 1.2])}" '
        f'fill="#dfeee6" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(55))
    isl = "".join(_island(i * W / (n - 1), 46 + (k % 3) * 14, 16 + (k % 2) * 8, k + 4, horizon)
                  for k, i in enumerate(island_weeks))
    front = _smooth(pts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="A pirate ship sailing on a night sea. Wave height follows the number of commits in each week of the past year.">
<defs>
  <linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#040b0a"/><stop offset=".65" stop-color="#0a1f1b"/><stop offset="1" stop-color="#0d2b25"/></linearGradient>
  <radialGradient id="moonglow"><stop offset="0" stop-color="#cfe9dc" stop-opacity=".30"/><stop offset="1" stop-color="#cfe9dc" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#night)"/>
{stars}
{_moon(150, 62, 22, moon_fraction(today))}
<rect x="0" y="{horizon}" width="{W}" height="2" fill="#1a4a3d" opacity=".6"/>
{isl}
{_back_wave(W, H, 176, 7, 180, "#0b3a30", .9, 26)}
{_back_wave(W, H, 190, 6, 140, "#08302a", .95, 19)}
{_ship(sx, sy - 1, ang, 0.95)}
<path d="{front} L{W},{H} L0,{H} Z" fill="#0f4a3c"/>
<path d="{front}" fill="none" stroke="#7fd9aa" stroke-width="1.6" opacity=".55"/>
<path d="{front}" fill="none" stroke="#e9f6ee" stroke-width=".8" stroke-dasharray="2 9" opacity=".5"/>
<rect x="0" y="{H-14}" width="{W}" height="14" fill="#0a3329" opacity=".7"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#2a5c4d" stroke-width="1"/>
</svg>
'''


# ------------------------------------------------------------------ project card (landscape mini poster)
def card(p, uid, today_ribbon=False):
    W, H = 360, 150
    lines = wrap(p["line"], 30, 3)
    text = "".join(f'<text x="22" y="{66 + i*17}" font-family="{SANS}" font-size="13" fill="{INK2}">{escape(l)}</text>'
                   for i, l in enumerate(lines))
    tiles = ""
    for i, slug in enumerate(p["stack"][:4]):
        x, y, s = 22 + i * 34, 106, 28
        tiles += (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="7" fill="{INK}"/>'
                  + icon(slug, x + s * 0.2, y + s * 0.2, s * 0.6, "#ead9ab", 1.9))
    stamp = f'''<g transform="translate(292,112) rotate(-5)">
  <rect x="-56" y="-30" width="112" height="60" rx="6" fill="none" stroke="{RED}" stroke-width="2.2"/>
  <rect x="-51" y="-25" width="102" height="50" rx="4" fill="none" stroke="{RED}" stroke-width=".8" opacity=".7"/>
  <text y="-12" text-anchor="middle" font-family="{SANS}" font-size="9" font-weight="700" letter-spacing="2.2" fill="{RED}">BOUNTY</text>
  <text y="8" text-anchor="middle" font-family="{SERIF}" font-size="{22 if len(p['bounty']) <= 5 else 19}" font-weight="700" fill="{RED}">{escape(p['bounty'])}</text>
  <text y="21" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{RED}">{escape(p['bounty_sub'])}</text>
</g>'''
    ribbon = ""
    if today_ribbon:
        ribbon = (f'<path d="M296,0 L360,0 L360,64 Z" fill="{GOLD}"/><path d="M296,0 L360,64" stroke="{INK}" stroke-width="1" opacity=".5"/>'
                  f'<text transform="translate(334,25) rotate(45)" text-anchor="middle" font-family="{SANS}" font-size="10" '
                  f'font-weight="700" letter-spacing="1" fill="{INK}">TODAY</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p['name'])}: {escape(p['line'])}. {escape(p['bounty'])} {escape(p['bounty_sub'])}. Stack: {escape(', '.join(p['stack']))}.">
<defs>{paper_defs(uid)}<clipPath id="c{uid}"><rect width="{W}" height="{H}" rx="9"/></clipPath></defs>
<g clip-path="url(#c{uid})">
<rect width="{W}" height="{H}" fill="url(#paper{uid})"/>
<path d="M0,52 C90,46 270,58 360,50" fill="none" stroke="#8a6a34" stroke-width="1" opacity=".16"/>
{ribbon}
</g>
<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="7" fill="none" stroke="{INK}" stroke-width="3"/>
<rect x="9" y="9" width="{W-18}" height="{H-18}" rx="4" fill="none" stroke="{INK}" stroke-width=".9" opacity=".6"/>
<text x="22" y="42" font-family="{SERIF}" font-size="23" font-weight="700" fill="{INK}">{escape(p['name'])}</text>
{text}
{tiles}
{stamp}
</svg>
'''


# ------------------------------------------------------------------ voyage scroll
def _month_index(s, now):
    if s == "now":
        return (now.year - 2026) * 12 + now.month  # end of the current month
    y, m = int(s[:4]), int(s[5:7])
    return (y - 2026) * 12 + m - 1


def voyage(cfg, now):
    W, ppm, top, bot = 600, 58, 76, 40
    t_end = (now.year - 2026) * 12 + now.month        # end of current month
    H = top + t_end * ppm + bot
    y_of = lambda t: top + (t_end - t) * ppm
    lane_x = [64, 320]
    lane_w = 240
    body = ""
    # gutter: route line, month ticks, flag at "now"
    body += f'<line x1="26" y1="{top-6}" x2="26" y2="{H-bot+6}" stroke="{INK}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round" opacity=".7"/>'
    for m, label in [(0, "Jan"), (3, "Apr"), (6, "Jul"), (9, "Oct")]:
        if m <= t_end:
            yy = y_of(m)
            body += (f'<circle cx="26" cy="{yy:.1f}" r="3.4" fill="{INK}"/>'
                     f'<text x="38" y="{yy+4:.1f}" font-family="{SANS}" font-size="11" fill="{INK2}">{label}</text>')
    body += (f'<line x1="26" y1="{top-6}" x2="26" y2="{top-30}" stroke="{INK}" stroke-width="2"/>'
             f'<path d="M26,{top-30} L44,{top-24} L26,{top-18} Z" fill="{RED}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>')
    for i, name in enumerate(cfg["lanes"]):
        body += (f'<text x="{lane_x[i]}" y="46" font-family="{SERIF}" font-size="15" font-style="italic" font-weight="700" fill="{INK}">{escape(name)}</text>')
    for it in cfg["items"]:
        x = lane_x[it["lane"]]
        if it.get("ongoing"):
            y0, y1 = y_of(t_end) + 3, y_of(t_end) + 3 + it.get("height", 98)
        else:
            end_t = t_end if it["end"] == "now" else _month_index(it["end"], now) + 1
            y0 = y_of(end_t) + 3
            y1 = y_of(_month_index(it["start"], now)) - 3
        h = y1 - y0
        tl = wrap(it["title"], 21, 2)
        bl = wrap(it["line"], 27, 4)
        cy = y0 + 22
        txt = f'<text x="{x+18}" y="{cy:.1f}" font-family="{SANS}" font-size="12" fill="{INK2}">{escape(it["dates"])}</text>'
        cy += 21
        for t in tl:
            txt += f'<text x="{x+18}" y="{cy:.1f}" font-family="{SERIF}" font-size="15.5" font-weight="700" fill="{INK}">{escape(t)}</text>'
            cy += 19
        txt += f'<text x="{x+18}" y="{cy:.1f}" font-family="{SANS}" font-size="12.5" font-weight="700" fill="{RED}">{escape(it["org"])}</text>'
        cy += 21
        for l in bl:
            txt += f'<text x="{x+18}" y="{cy:.1f}" font-family="{SANS}" font-size="13" fill="{INK2}">{escape(l)}</text>'
            cy += 17
        arrow = ""
        if it.get("ongoing"):
            arrow = (f'<path d="M{x+lane_w-24},{y1-12:.1f} l8,-12 l8,12 M{x+lane_w-16},{y1-24:.1f} v22" fill="none" stroke="{INK}" '
                     f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>')
        body += (f'<rect x="{x}" y="{y0:.1f}" width="{lane_w}" height="{h:.1f}" rx="9" fill="#3a2614" fill-opacity=".07" stroke="{INK}" stroke-width="1.6"/>'
                 f'<rect x="{x}" y="{y0+8:.1f}" width="5" height="{h-16:.1f}" rx="2.5" fill="{GOLD}"/>' + txt + arrow)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="Timeline of 2026: {escape('; '.join(i['title'] + ', ' + i['org'] + ', ' + i['dates'] for i in cfg['items']))}">
<defs>{paper_defs("V")}</defs>
<rect width="{W}" height="{H:.0f}" rx="12" fill="url(#paperV)"/>
<path d="M0,{H*0.33:.0f} C140,{H*0.33-8:.0f} 420,{H*0.33+8:.0f} 560,{H*0.33-2:.0f}" fill="none" stroke="#8a6a34" stroke-width="1" opacity=".16"/>
<path d="M0,{H*0.66:.0f} C140,{H*0.66-8:.0f} 420,{H*0.66+8:.0f} 560,{H*0.66-2:.0f}" fill="none" stroke="#8a6a34" stroke-width="1" opacity=".14"/>
<rect x="4" y="4" width="{W-8}" height="{H-8:.0f}" rx="9" fill="none" stroke="{INK}" stroke-width="3.5"/>
<rect x="11" y="11" width="{W-22}" height="{H-22:.0f}" rx="6" fill="none" stroke="{INK}" stroke-width=".9" opacity=".6"/>
{body}
</svg>
'''


# ------------------------------------------------------------------ armory (categorised logo board)
def armory(cats):
    W, margin, gutter = 640, 26, 26
    colw = (W - 2 * margin - gutter) / 2
    tile, gap, per_row = 41, 7, 6
    label_h, pad_b, row_gap = 30, 22, 0

    def cell_h(c):
        rows = math.ceil(len(c["items"]) / per_row)
        return label_h + rows * tile + (rows - 1) * gap + pad_b

    body, names = "", []
    col_y = [margin + 4, margin + 4]
    for idx, c in enumerate(cats):
        ci = idx % 2                      # even categories left, odd categories right
        y, x0 = col_y[ci], margin + ci * (colw + gutter)
        body += (f'<text x="{x0:.1f}" y="{y+16:.1f}" font-family="{SERIF}" font-size="17" font-weight="700" fill="#e9efe9">{escape(c["name"])}</text>'
                 f'<rect x="{x0:.1f}" y="{y+23:.1f}" width="30" height="2" rx="1" fill="{GOLD}"/>')
        for k, (slug, label, hot) in enumerate(c["items"]):
            rr, cc = divmod(k, per_row)
            tx, ty = x0 + cc * (tile + gap), y + label_h + rr * (tile + gap)
            color = "#e3c46f" if hot else "#dfe9e2"
            body += (f'<rect x="{tx:.1f}" y="{ty:.1f}" width="{tile}" height="{tile}" rx="9" fill="#10211d" stroke="#25453c" stroke-width="1.2"/>'
                     + icon(slug, tx + tile * 0.22, ty + tile * 0.22, tile * 0.56, color, 1.9))
            names.append(label)
        col_y[ci] += cell_h(c)
    H = max(col_y) + margin - 12
    alt = "Tech stack by category: " + "; ".join(f'{c["name"]}: ' + ", ".join(i[1] for i in c["items"]) for c in cats)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{escape(alt)}">
<defs><linearGradient id="rack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1815"/><stop offset="1" stop-color="#091210"/></linearGradient></defs>
<rect width="{W}" height="{H:.0f}" rx="14" fill="url(#rack)"/>
<rect x="6" y="6" width="{W-12}" height="{H-12:.0f}" rx="10" fill="none" stroke="#b8963f" stroke-width="1" opacity=".55"/>
{body}
</svg>
'''
