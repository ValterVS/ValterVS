"""Generate self-contained GitHub SVG cards; Python standard library only."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ValterVS-profile"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    request = urllib.request.Request("https://api.github.com/" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def collect(username):
    user = api(f"users/{username}")
    repos = []
    page = 1
    while True:
        batch = api(f"users/{username}/repos?per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    return {
        "repositories": len(repos), "followers": user["followers"],
        "stars": sum(r["stargazers_count"] for r in own),
        "since": user["created_at"][:4],
        "languages": dict(Counter(r["language"] for r in own if r["language"])),
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    }


def render(profile, stats, portrait, light=False):
    bg, panel, fg, muted, accent, line = (
        ("#faf8ff", "#f0eafa", "#241b38", "#655979", "#6d28d9", "#ded4ee") if light else
        ("#100d19", "#191324", "#eee7fa", "#a89abf", "#b99aff", "#332842")
    )
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="600" viewBox="0 0 1080 600" role="img" aria-labelledby="title desc">',
             '<title id="title">Perfil de Valter Silva</title>',
             '<desc id="desc">Retrato em caracteres baseado na foto de Valter; tecnologias, contatos e estatísticas públicas do GitHub.</desc>',
             f'<rect width="1080" height="600" rx="18" fill="{bg}"/>',
             f'<rect x="1" y="1" width="1078" height="598" rx="18" fill="none" stroke="{line}"/>',
             f'<path d="M0 52H1080" stroke="{line}"/>']
    def text(x, y, value, size=14, color=fg, weight="normal"):
        parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Consolas, Liberation Mono, monospace" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>')
    for x, color in [(25,"#f77888"),(45,"#e8c16c"),(65,"#69c995")]:
        parts.append(f'<circle cx="{x}" cy="27" r="5" fill="{color}"/>')
    text(92,32,"valter@github:~ / profile",13,muted)
    text(927,32,"● PÚBLICO",12,accent)
    parts.append('<rect x="22" y="74" width="392" height="480" rx="12" fill="#191324"/>')
    for row, cells in enumerate(portrait):
        for col, (char, color) in enumerate(cells):
            if char != " ":
                text(38+col*4.75, 101+row*6.75, char,8,color)
    text(44,532,"~/ValterVS",14,"#b99aff")
    text(448,100,profile["name"],29,fg,"bold")
    text(448,127,profile["headline"],16,accent)
    text(448,151,profile["location"],13,muted)
    def section(y, title):
        text(448,y,title,12,accent,"bold")
        parts.append(f'<path d="M448 {y+10}H1044" stroke="{line}"/>')
    def field(y, key, value):
        text(448,y,key,13,muted)
        text(565,y,value,13)
    section(184,"01 / SOBRE & STACK")
    for y,key,value in [(214,"Formação",profile["education"]),(239,"Linguagens",profile["languages"]),(264,"Frontend",profile["frontend"]),(289,"Backend",profile["backend"]),(314,"Ferramentas",profile["tools"]),(339,"Foco",profile["focus"])]:
        field(y,key,value)
    section(375,"02 / CONECTE-SE")
    for y,key,value,url in [(405,"Web",profile["portfolio"].removeprefix("https://"),profile["portfolio"]),(430,"LinkedIn","in/valter-silva-eng",profile["linkedin"]),(455,"Email",profile["email"],"mailto:"+profile["email"])]:
        parts.append(f'<a href="{escape(url,quote=True)}">')
        field(y,key,value)
        parts.append('</a>')
    section(489,"03 / GITHUB PÚBLICO")
    for x,value,label in [(448,stats["repositories"],"repositórios"),(653,stats["stars"],"estrelas"),(858,stats["followers"],"seguidores")]:
        text(x,527,value,25,fg,"bold")
        text(x,548,label,12,muted)
    text(25,580,"RETRATO EM ASCII · IDENTIDADE EM CÓDIGO",10,muted)
    text(608,580,f'Desde {stats["since"]} · Atualizado {stats["updated"]} UTC',11,muted)
    parts.append('</svg>')
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Use the last saved public data")
    args = parser.parse_args()
    profile = json.loads((ROOT / "profile.json").read_text(encoding="utf-8-sig"))
    path = ROOT / "assets/stats.json"
    stats = json.loads(path.read_text()) if args.offline else collect(profile["username"])
    portrait = json.loads((ROOT / "assets/portrait.json").read_text())
    # Render both before writing; an API failure never replaces valid cards with zeros.
    cards = {name: render(profile, stats, portrait, light) for name,light in [("dark_mode.svg",False),("light_mode.svg",True)]}
    for name,content in cards.items():
        (ROOT / name).write_text(content, encoding="utf-8")
    path.write_text(json.dumps(stats,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
