#!/usr/bin/env python3
"""
Rebuilds every graphic in assets/ from profile.json plus live GitHub data, and refreshes the
"last seen" line in README.md. Standard library only.

  GitHub Actions (daily):   python scripts/update_profile.py
  Preview without network:  python scripts/update_profile.py --offline

Live elements: wanted poster (bounty + weekly change), living sea (commit waves, repo islands,
real moon phase), project cards (island-of-the-day ribbon), and the "last seen" line.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import art  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
LOGIN = os.environ.get("GH_LOGIN", CFG["login"])
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OFFLINE = "--offline" in sys.argv
TODAY = datetime.now(timezone.utc).date()


# ------------------------------------------------------------------ GitHub API
def gh(url, payload=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-updater"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=30) as r:
            return json.load(r)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  ! request failed: {url} ({e})")
        return None


QUERY = """query($l:String!){ user(login:$l){
  followers{totalCount}
  pullRequests{totalCount}
  repositories(ownerAffiliation:OWNER, privacy:PUBLIC, isFork:false, first:100, orderBy:{field:CREATED_AT, direction:DESC}){
    totalCount nodes{stargazerCount createdAt}}
  contributionsCollection{ totalCommitContributions
    contributionCalendar{ weeks{ contributionDays{ contributionCount date } } } }
}}"""


def fetch_live():
    """Returns (stats, weekly_commit_counts, island_week_indexes). Any part may be None."""
    stats = dict(commits=None, prs=None, repos=None, stars=None, followers=None)
    weeks, islands = None, None
    if TOKEN:
        res = gh("https://api.github.com/graphql", {"query": QUERY, "variables": {"l": LOGIN}})
        user = ((res or {}).get("data") or {}).get("user")
        if user:
            cc = user["contributionsCollection"]
            stats.update(commits=cc["totalCommitContributions"], prs=user["pullRequests"]["totalCount"],
                         repos=user["repositories"]["totalCount"], followers=user["followers"]["totalCount"],
                         stars=sum(n["stargazerCount"] for n in user["repositories"]["nodes"]))
            cal = cc["contributionCalendar"]["weeks"][-53:]
            weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal]
            first = datetime.fromisoformat(cal[0]["contributionDays"][0]["date"]).date()
            idx = sorted({min(len(weeks) - 1, (datetime.fromisoformat(n["createdAt"].replace("Z", "+00:00")).date() - first).days // 7)
                          for n in user["repositories"]["nodes"]
                          if (TODAY - datetime.fromisoformat(n["createdAt"].replace("Z", "+00:00")).date()).days <= 365})
            idx = [i for i in idx if i >= 1 and abs(i - (len(weeks) - 12)) > 4]
            if len(idx) > 6:
                idx = [idx[round(k * (len(idx) - 1) / 5)] for k in range(6)]
            islands = idx
            return stats, weeks, islands
    u = gh(f"https://api.github.com/users/{LOGIN}")
    if u:
        stats["repos"], stats["followers"] = u.get("public_repos"), u.get("followers")
        repos = gh(f"https://api.github.com/users/{LOGIN}/repos?per_page=100&type=owner") or []
        stats["stars"] = sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork"))
        prs = gh(f"https://api.github.com/search/issues?q=author:{LOGIN}+type:pr&per_page=1")
        stats["prs"] = (prs or {}).get("total_count")
    return stats, None, None


# ------------------------------------------------------------------ state (for the weekly bounty change)
STATE = ROOT / "data" / "state.json"


def weekly_delta(current):
    hist = {}
    if STATE.exists():
        try:
            hist = json.loads(STATE.read_text())
        except json.JSONDecodeError:
            hist = {}
    hist[TODAY.isoformat()] = current
    cutoff = (TODAY - timedelta(days=60)).isoformat()
    hist = {k: v for k, v in sorted(hist.items()) if k >= cutoff}
    older = [k for k in hist if k <= (TODAY - timedelta(days=7)).isoformat()]
    delta = current - hist[older[-1]] if older else None
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(hist, indent=1))
    return delta


# ------------------------------------------------------------------ last seen line
def last_seen():
    events = gh(f"https://api.github.com/users/{LOGIN}/events/public?per_page=60")
    for e in events or []:
        repo = e["repo"]["name"].split("/")[-1]
        if e["type"] != "PushEvent" or repo.lower() == LOGIN.lower():
            continue
        when = datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")).date()
        days = (TODAY - when).days
        ago = "today" if days <= 0 else "yesterday" if days == 1 else f"{days} days ago" if days < 14 else f"{days // 7} weeks ago"
        return f"Last seen: pushing to {repo}, {ago}."
    return None


def set_marker(text):
    path = ROOT / "README.md"
    src = path.read_text(encoding="utf-8")
    new = re.sub(r"<!-- LASTSEEN:START -->.*?<!-- LASTSEEN:END -->",
                 lambda _: f"<!-- LASTSEEN:START -->*{text}*<!-- LASTSEEN:END -->", src, flags=re.S)
    if new != src:
        path.write_text(new, encoding="utf-8")
        print("last-seen line updated")


# ------------------------------------------------------------------ main
def write(name, svg):
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / name).write_text(svg, encoding="utf-8")


def slug(repo):
    return re.sub(r"[^a-z0-9]+", "-", repo.lower()).strip("-")


def main():
    print(f"Refreshing profile for {LOGIN} (offline={OFFLINE}, token={'yes' if TOKEN else 'no'})")
    if OFFLINE:
        stats = dict(commits=None, prs=None, stars=None, **{k: CFG["seed_stats"].get(k) for k in ("repos", "followers")})
        weeks, islands = [2 + (i * 7) % 4 for i in range(53)], [8, 19, 28, 35]
    else:
        stats, weeks, islands = fetch_live()
    print("stats:", stats)

    # poster
    if any(v is not None for v in stats.values()):
        delta = None if OFFLINE else weekly_delta(art.bounty(stats))
        write("wanted.svg", art.poster(stats, CFG["name"], CFG["epithet"], delta))
        print(f"poster written (bounty {art.bounty(stats):,}, weekly change {delta})")
    # living sea
    if weeks:
        write("living-sea.svg", art.living_sea(weeks, islands or [], TODAY))
        print("sea written")
    # cards (island of the day rotates by date)
    projects = CFG["projects"]
    today_idx = TODAY.toordinal() % len(projects)
    for i, p in enumerate(projects):
        write(f"card-{slug(p['repo'])}.svg", art.card(p, f"{i}", today_ribbon=(i == today_idx)))
    print(f"cards written (island of the day: {projects[today_idx]['name']})")
    # static graphics, rebuilt from profile.json so edits show up automatically
    write("voyage.svg", art.voyage(CFG["voyage"], TODAY))
    write("armory.svg", art.armory(CFG["armory"]))
    if not OFFLINE:
        seen = last_seen()
        if seen:
            set_marker(seen)
        else:
            print("no public pushes found - last-seen line left as is")


if __name__ == "__main__":
    main()
