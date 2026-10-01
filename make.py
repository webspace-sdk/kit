"""Generates the Webspaces kit: small CC0 Smooth Voxel (.svox) models in the house style.

SVOX layout: each line is a z slice; each space-separated group is a y layer (bottom to top);
each character is an x voxel. '-' is empty. Run: python make.py
"""
import math, os, random

OUT = "models"

def svox(name, size, scale, materials, fill, origin="-y", extra=""):
    sx, sy, sz = size
    lines = []
    for z in range(sz):
        groups = []
        for y in range(sy):
            groups.append("".join(fill(x, y, z) or "-" for x in range(sx)))
        lines.append(" ".join(groups))
    mats = "\n".join(f"material {m}\n  colors = {c}" for m, c in materials)
    text = f"size = {sx} {sy} {sz}\nscale = {scale}\norigin = {origin}\n{extra}{mats}\nvoxels\n" + "\n".join(lines) + "\n"
    open(os.path.join(OUT, name + ".svox"), "w", newline="\n").write(text)

def dist(x, y, z, cx, cy, cz, ry=1.0):
    return math.sqrt((x - cx) ** 2 + ((y - cy) / ry) ** 2 + (z - cz) ** 2)

SOFT = "lighting = smooth, roughness = 0.9, deform = 4"
# Thin parts (trunks, stems, frames) need light smoothing or they melt away
FIRM = "lighting = smooth, roughness = 0.9, deform = 1"
SOFTER = "lighting = smooth, roughness = 1, deform = 6"
GLOSS = "lighting = smooth, roughness = 0.3, deform = 3"

# Round tree: trunk + leafy ball
def tree(x, y, z):
    if dist(x, y, z, 4, 8, 4, 0.9) < 4.2 and y >= 4: return "L" if (x * 3 + y + z) % 7 else "M"
    if 3 <= x <= 5 and 3 <= z <= 5 and y < 6: return "T"
svox("tree", (9, 13, 9), 0.125, [(FIRM, "T:#6b4a34"), (SOFTER, "L:#6fae5c M:#5c9a4c")], tree)

# Pine: a tall cone with soft tiers on a sturdy trunk
def pine(x, y, z):
    if 4 <= x <= 6 and 4 <= z <= 6 and y < 4: return "T"
    if y >= 2:
        t = (y - 2) / 15
        r = 5.2 * (1 - t) + 0.6 - 0.9 * (((y - 2) % 4) / 3)
        if math.hypot(x - 5, z - 5) <= r: return "P" if (x + y + z) % 5 else "Q"
svox("pine", (11, 18, 11), 0.125, [(FIRM, "T:#5e3f2c"), (SOFT, "P:#3f7a4f Q:#356a44")], pine)

# Rock
def rock(x, y, z):
    if dist(x, y, z, 3, 0.5, 3, 0.7) < 3.1 + 0.4 * math.sin(x * 1.7 + z * 2.3): return "R" if (x + z) % 3 else "S"
svox("rock", (7, 4, 7), 0.125, [(SOFTER, "R:#8a857c S:#77726a")], rock)

# Bush
def bush(x, y, z):
    if dist(x, y, z, 3, 1.5, 3, 0.8) < 3.2: return "B" if (x * 2 + y + z * 3) % 6 else "F"
svox("bush", (7, 5, 7), 0.125, [(SOFTER, "B:#5f9d52 F:#e58aa0")], bush)

# Mushroom
def mushroom(x, y, z):
    if y < 4 and math.hypot(x - 3, z - 3) <= 1.5: return "W"
    if y >= 4 and dist(x, y, z, 3, 4, 3, 0.6) < 3.3: return "R" if (x + z + y) % 4 else "D"
svox("mushroom", (7, 7, 7), 0.125, [(FIRM, "W:#efe6d6"), (GLOSS, "R:#d8463b D:#f4efe6")], mushroom)

# Lantern: frame + glowing core
def lantern(x, y, z):
    edge = x in (0, 4) and z in (0, 4)
    if y in (0, 7) and 0 <= x <= 4 and 0 <= z <= 4: return "F"
    if edge and 0 < y < 7: return "F"
    if 1 <= x <= 3 and 1 <= z <= 3 and 1 <= y <= 6: return "G"
    if y == 8 and x == 2 and z == 2: return "F"
svox("lantern", (5, 9, 5), 0.125, [("lighting = smooth, roughness = 0.3, deform = 0", "F:#2d2a33"), ("lighting = smooth, emissive = #ffcf6b 0.9, deform = 2", "G:#ffcf6b")], lantern)

# Bench
def bench(x, y, z):
    if y == 3 and 0 <= z <= 2: return "W"
    if y < 3 and x in (1, 12) and z in (0, 2): return "L"
    if y in (5, 6) and z == 2: return "W"
    if y == 4 and z == 2 and x in (1, 12): return "L"
svox("bench", (14, 7, 3), 0.125, [("lighting = smooth, roughness = 0.8, deform = 2", "W:#a8743f"), (FIRM, "L:#3a3a40")], bench)

# Crate
def crate(x, y, z):
    edge = (x in (0, 5)) + (y in (0, 5)) + (z in (0, 5)) >= 2
    return "E" if edge else "C"
svox("crate", (6, 6, 6), 0.125, [("lighting = flat, roughness = 0.9, deform = 1", "C:#b98a52 E:#8a6236")], crate)

# Crystal: tall faceted shard cluster
def crystal(x, y, z):
    for cx, cz, h in ((3, 3, 10), (1, 2, 6), (5, 4, 7), (2, 5, 5)):
        r = 1.4 * (1 - y / (h + 0.5))
        if y < h and math.hypot(x - cx, z - cz) <= max(r, 0.3): return "A" if (x + y) % 3 else "B"
svox("crystal", (7, 11, 7), 0.125, [("lighting = smooth, roughness = 0.1, emissive = #8fd8ff 0.4, deform = 1", "A:#8fd8ff B:#c7b2ff")], crystal)

# Flower
def flower(x, y, z):
    if x in (3, 4) and z in (3, 4) and y < 6: return "S"
    if y in (6, 7) and math.hypot(x - 3.5, z - 3.5) <= 2.6: return "Y" if math.hypot(x - 3.5, z - 3.5) < 1 else "P"
svox("flower", (8, 8, 8), 0.125, [(FIRM, "S:#5e9e4e"), (SOFTER, "P:#f2a1c4 Y:#ffd65c")], flower)

# Cloud
def cloud(x, y, z):
    for cx, cy, cz, r in ((4, 2, 3, 2.6), (8, 3, 3, 3.2), (12, 2, 3, 2.4)):
        if dist(x, y, z, cx, cy, cz, 0.8) < r: return "C"
svox("cloud", (16, 6, 7), 0.125, [(SOFTER, "C:#f7f8fc")], cloud, origin="")

# Campfire stone
def stone(x, y, z):
    edge = x in (0, 4) or z in (0, 4)
    corner = x in (0, 4) and z in (0, 4)
    if (y < 2 and not corner) or (y == 2 and not edge): return "D" if (x + z + y) % 3 else "E"
svox("stone", (5, 3, 5), 0.125, [(SOFTER, "D:#6f6a63 E:#57524c")], stone)

# Log
def log(x, y, z):
    if (y in (0, 3)) and (z in (0, 3)): return None
    if x in (0, 11): return "C"
    return "B" if (x * 7 + y * 3 + z) % 5 == 0 else "A"
svox("log", (12, 4, 4), 0.125, [("lighting = smooth, roughness = 0.9, deform = 4", "A:#5a3a24 B:#3f2819 C:#c9955e")], log)

print(sorted(os.listdir(OUT)))
