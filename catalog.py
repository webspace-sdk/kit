"""Builds index.html, the kit catalog page, from sizes.json and thumbs/. Run after make.py and the thumbnail pass."""
import html as H
import json

info = json.load(open("sizes.json"))
blurbs = {
    "bench": "A park bench to sit on.",
    "bush": "A round bush with blossoms.",
    "cloud": "A puffy cloud. Scale it up and put it high.",
    "crate": "A wooden crate.",
    "crystal": "A cluster of glowing crystals.",
    "flower": "A single flower. Scale it down for a meadow.",
    "lantern": "A lantern with a warm glow.",
    "log": "A log: firewood or a seat.",
    "mushroom": "A red-capped mushroom.",
    "pine": "A pine tree.",
    "rock": "A smooth boulder.",
    "stone": "A small fieldstone.",
    "tree": "A round, leafy tree.",
}
suggest = {"cloud": 4, "flower": 0.35, "lantern": 0.6, "mushroom": 0.5, "pine": 1.6, "tree": 2}

cards = []
for n in sorted(info):
    i = info[n]
    s = suggest.get(n, 1)
    y = 800 if n == "cloud" else 75 + i["h"] * s / 2
    sc = f" scale3d({s}, {s}, {s})" if s != 1 else ""
    tag = f'<model src="https://webspaces.space/kit/models/{n}.svox"\n  style="transform: translate3d(0cm, {y:.0f}cm, -300cm){sc}"></model>'
    cards.append(f"""    <article class="card">
      <img src="thumbs/{n}.png" alt="{n}" loading="lazy" />
      <div class="meta"><h2>{n}</h2><span>{i["w"] / 100:.2f} × {i["h"] / 100:.2f} × {i["d"] / 100:.2f} m</span></div>
      <p>{blurbs[n]}</p>
      <pre>{H.escape(tag)}</pre>
      <div class="links"><button data-copy>Copy tag</button><a href="models/{n}.svox">.svox</a></div>
    </article>""")

template = open("catalog.template.html", encoding="utf8").read()
open("index.html", "w", encoding="utf8", newline="\n").write(template.replace("{{CARDS}}", "\n".join(cards)))
print("wrote index.html with", len(cards), "models")
