#!/usr/bin/env python3
"""
Refresh the dynamic parts of the profile README.

 1. assets/wanted.svg  - the Wanted poster, with a bounty computed from public GitHub activity

Standard library only. Runs inside GitHub Actions (see .github/workflows/update-profile.yml)
and also locally:  GITHUB_TOKEN=<token> python scripts/update_profile.py
"""
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGIN = os.environ.get("GH_LOGIN", "YEsh-DEV")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# ---------------------------------------------------------------- palettes
DARK = dict(bone="#efe8d5", bone_line="#0b1514", jade="#3f8f5f", gold="#d8b455",
            steel="#c9d6d3", steel_line="#0b1514", ink="#0b1514", handle="#1b2b27")
LIGHT = dict(bone="#f6f1e1", bone_line="#12281f", jade="#2f7d4f", gold="#b8912f",
             steel="#a9b8b3", steel_line="#12281f", ink="#12281f", handle="#2a3d37")


# ---------------------------------------------------------------- emblem
def emblem(cx, cy, s, p):
    """Original pirate emblem: skull, green bandana, three blades. Drawn in a 200x200 box."""
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
  <ellipse cx="-15" cy="-4" rx="9.5" ry="10.5" fill="{p['ink']}"/>
  <ellipse cx="15" cy="-4" rx="9.5" ry="10.5" fill="{p['ink']}"/>
  <path d="M0,7 L-4.5,17 L4.5,17 Z" fill="{p['ink']}"/>
  <g stroke="{p['bone_line']}" stroke-width="2" stroke-linecap="round">
    <line x1="-13" y1="31" x2="-13" y2="42"/><line x1="-4.5" y1="31" x2="-4.5" y2="42"/>
    <line x1="4.5" y1="31" x2="4.5" y2="42"/><line x1="13" y1="31" x2="13" y2="42"/>
  </g>
  <path d="M-42,-27 Q0,-47 42,-27 L42,-14 Q0,-34 -42,-14 Z" fill="{p['jade']}" stroke="{p['bone_line']}" stroke-width="1.6" stroke-linejoin="round"/>
  <path d="M-42,-24 L-60,-14 L-52,-26 L-62,-30 Z" fill="{p['jade']}" stroke="{p['bone_line']}" stroke-width="1.4" stroke-linejoin="round"/>
  <g fill="none" stroke="{p['gold']}" stroke-width="2.4">
    <circle cx="45" cy="-2" r="3"/><circle cx="46" cy="6" r="3"/><circle cx="44" cy="14" r="3"/>
  </g>
</g>'''


# ---------------------------------------------------------------- GitHub API
def gh(url, payload=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-updater"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  ! request failed: {url} ({e})")
        return None


def fetch_stats():
    """Returns dict(commits, prs, repos, stars, followers); unknown values are None."""
    stats = dict(commits=None, prs=None, repos=None, stars=None, followers=None)
    if TOKEN:
        q = """query($l:String!){ user(login:$l){
            followers{totalCount}
            repositories(ownerAffiliation:OWNER, privacy:PUBLIC, isFork:false, first:100){
              totalCount nodes{stargazerCount}}
            pullRequests{totalCount}
            contributionsCollection{totalCommitContributions}
        }}"""
        res = gh("https://api.github.com/graphql", {"query": q, "variables": {"l": LOGIN}})
        user = ((res or {}).get("data") or {}).get("user")
        if user:
            stats.update(
                commits=user["contributionsCollection"]["totalCommitContributions"],
                prs=user["pullRequests"]["totalCount"],
                repos=user["repositories"]["totalCount"],
                stars=sum(n["stargazerCount"] for n in user["repositories"]["nodes"]),
                followers=user["followers"]["totalCount"],
            )
            return stats
    u = gh(f"https://api.github.com/users/{LOGIN}")
    if u:
        stats["repos"], stats["followers"] = u.get("public_repos"), u.get("followers")
        repos = gh(f"https://api.github.com/users/{LOGIN}/repos?per_page=100&type=owner") or []
        stats["stars"] = sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork"))
        prs = gh(f"https://api.github.com/search/issues?q=author:{LOGIN}+type:pr&per_page=1")
        stats["prs"] = (prs or {}).get("total_count")
    return stats


def bounty(st):
    """Fun, transparent formula. Tweak the weights however you like."""
    v = lambda k: st.get(k) or 0
    return (50_000_000
            + v("commits") * 500_000
            + v("prs") * 5_000_000
            + v("repos") * 10_000_000
            + v("stars") * 25_000_000
            + v("followers") * 20_000_000)


# ---------------------------------------------------------------- poster
def wanted_svg(st):
    amount = bounty(st)
    text = f"\u0e3f {amount:,}"
    size = min(62, int(440 / (len(text) * 0.60)))
    show = lambda k: "\u2014" if st.get(k) is None else f"{st[k]:,}"
    cols = [("commits this year", show("commits")), ("pull requests", show("prs")),
            ("public repos", show("repos")), ("stars earned", show("stars"))]
    stat_xml = ""
    for i, (label, val) in enumerate(cols):
        x = 105 + i * 130
        stat_xml += (f'<text x="{x}" y="770" font-size="26" font-weight="700" text-anchor="middle" fill="#3a2614">{val}</text>'
                     f'<text x="{x}" y="790" font-size="11.5" text-anchor="middle" fill="#5a4026">{label}</text>')
    serif = "Georgia,'Times New Roman','DejaVu Serif',serif"
    sans = "'Segoe UI',Helvetica,Arial,'DejaVu Sans',sans-serif"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 860" role="img" aria-label="Wanted poster for Yeshwanth Atmakuri, bounty {amount:,} berries">
<defs>
  <radialGradient id="paper" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#ead9ab"/><stop offset="1" stop-color="#d3bd86"/></radialGradient>
  <radialGradient id="sea" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="#1c3a33"/><stop offset="1" stop-color="#0b1a17"/></radialGradient>
</defs>
<rect width="600" height="860" rx="10" fill="url(#paper)"/>
<path d="M0,310 C150,300 450,322 600,306" fill="none" stroke="#8a6a34" stroke-width="1" opacity=".18"/>
<path d="M0,560 C160,552 440,570 600,556" fill="none" stroke="#8a6a34" stroke-width="1" opacity=".16"/>
<rect x="14" y="14" width="572" height="832" rx="6" fill="none" stroke="#3a2614" stroke-width="6"/>
<rect x="28" y="28" width="544" height="804" fill="none" stroke="#3a2614" stroke-width="1.5"/>
<text x="300" y="122" text-anchor="middle" font-family="{serif}" font-size="100" font-weight="700" fill="#3a2614" textLength="460" lengthAdjust="spacingAndGlyphs">WANTED</text>
<rect x="90" y="148" width="420" height="330" fill="url(#sea)" stroke="#3a2614" stroke-width="5"/>
{emblem(300, 313, 1.52, DARK)}
<text x="300" y="540" text-anchor="middle" font-family="{serif}" font-size="40" font-weight="700" fill="#3a2614" textLength="420" lengthAdjust="spacingAndGlyphs">DEAD OR ALIVE</text>
<text x="300" y="594" text-anchor="middle" font-family="{serif}" font-size="34" font-weight="700" fill="#3a2614" textLength="470" lengthAdjust="spacingAndGlyphs">YESHWANTH ATMAKURI</text>
<text x="300" y="628" text-anchor="middle" font-family="{serif}" font-size="19" font-style="italic" fill="#5a4026">The Graph-Slashing Agent Builder</text>
<line x1="90" y1="650" x2="510" y2="650" stroke="#3a2614" stroke-width="1.5"/>
<text x="300" y="718" text-anchor="middle" font-family="{serif}" font-size="{size}" font-weight="700" fill="#3a2614">{text}</text>
<g font-family="{sans}">{stat_xml}</g>
<text x="300" y="820" text-anchor="middle" font-family="{sans}" font-size="11" font-style="italic" fill="#5a4026">Bounty is computed from public GitHub activity and refreshed daily.</text>
</svg>
'''


def main():
    print(f"Refreshing profile for {LOGIN} (token: {'yes' if TOKEN else 'no'})")
    st = fetch_stats()
    print("stats:", st)
    if any(v is not None for v in st.values()):
        (ROOT / "assets").mkdir(exist_ok=True)
        (ROOT / "assets" / "wanted.svg").write_text(wanted_svg(st), encoding="utf-8")
        print(f"poster written, bounty = {bounty(st):,}")
    else:
        print("no stats available - poster left untouched")


if __name__ == "__main__":
    main()
