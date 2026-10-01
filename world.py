"""Builds world.html (a walkable showroom of the kit) and shots.html (a spaced layout used for thumbnails)."""
import json
import math

info = json.load(open("sizes.json"))
names = sorted(info)

HEAD = """<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<meta name="description" content="Free (CC0) Smooth Voxel models in the Webspaces house style. View source to copy any of them." />
<script src="https://webspaces.space/run/0.10.0-alpha.12/webspace.js"></script>
<meta name="webspace.environment.type" content="terrain" />
<meta name="webspace.environment.terrain.type" content="flat" />
<meta name="webspace.environment.wrap" content="off" />
<meta name="webspace.environment.terrain.colors.sky" content="#9fc3e0" />
<meta name="webspace.environment.terrain.colors.ground" content="#c9c2b2" />
<meta name="webspace.environment.terrain.colors.grass" content="#b8b19f" />
<meta name="webspace.environment.terrain.colors.edge" content="#8f8878" />
<meta name="webspace.environment.terrain.colors.rock" content="#9a958c" />
<meta name="webspace.environment.terrain.colors.leaves" content="#6fae5c" />
<meta name="webspace.environment.terrain.colors.bark" content="#6b4a34" />
<meta name="webspace.environment.terrain.colors.water" content="#5f8fb8" />
<meta name="webspace.environment.spawn_point.transform" content="translate3d(0cm, 0cm, 200cm)" />
<meta name="webspace.environment.spawn_point.radius" content="0" />
</head>
<body>
"""

# Thumbnail layout: one model every 5 m along x, standing on the ground
shots = [
    f'<model id="m-{n}" src="models/{n}.svox" style="transform: translate3d({i * 500}cm, {75 + info[n]["h"] / 2:.0f}cm, -400cm)"></model>'
    for i, n in enumerate(names)
]
open("shots.html", "w", encoding="utf8", newline="\n").write(HEAD.format(title="Kit thumbnails") + "\n".join(shots) + "\n</body>\n</html>\n")

# Showroom: models on an arc, each with its name in front
items = [
    '<label id="title" style="color: #2b2533; background-color: transparent; -webkit-text-stroke-color: #f4efe6; '
    'font-family: serif; transform: translate3d(0cm, 420cm, -760cm) scale3d(2.2, 2.2, 2.2)"><h1>The Kit</h1>'
    "<p>Free models for your world. View source to copy one.</p></label>"
]
R, cz = 620, -40
for i, n in enumerate(names):
    a = math.radians(-78 + 156 * i / (len(names) - 1))
    x, z = R * math.sin(a), cz - R * math.cos(a)
    y = 75 + info[n]["h"] / 2
    items.append(f'<model id="m-{n}" src="models/{n}.svox" style="transform: translate3d({x:.0f}cm, {y:.0f}cm, {z:.0f}cm) rotateY({-a:.3f}rad)"></model>')
    tx, tz = x * 0.86, cz + (z - cz) * 0.86
    items.append(
        f'<label id="name-{n}" style="color: #2b2533; background-color: #f4efe6; font-family: monospaced; '
        f'transform: translate3d({tx:.0f}cm, 105cm, {tz:.0f}cm) rotateY({-a:.3f}rad) scale3d(1.1, 1.1, 1.1)"><p>{n}</p></label>'
    )
open("world.html", "w", encoding="utf8", newline="\n").write(HEAD.format(title="The Kit") + "\n".join(items) + "\n</body>\n</html>\n")
print("wrote shots.html and world.html")
