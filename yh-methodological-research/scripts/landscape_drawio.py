"""Score a pain-research data file and draw it as a .drawio file (stdlib only).

Usage: python3 landscape_drawio.py data.json out.drawio

Prints the ranking, a robustness re-score and a layout overlap check, then writes:
  Page 1 "Landscape": centre -> group -> product -> pain leaves, each leaf coloured by whether the
          product resolves that pain's cluster (green yes, amber partial, red no, grey n/a).
  Page 2 "Pain clusters": the clusters ranked by priority -> how they are resolved (with the code)
          -> where each one goes.
  Page 3 "Derivation": the method as run, left to right (only when data["derivation"] is set).

Scoring: loudness = the sum of weights[strength] over every pain in the cluster; breadth = the
number of products reporting it; priority = loudness x the resolve factor (yes 1, partial 0.5,
no 0). The data schema is in the skill's SKILL.md, under "The data file".
"""

import json
import sys
from xml.sax.saxutils import escape

INK = "#16161a"
STATUS = {
    "yes": ("#e3f4ea", "#2f8f5b"),
    "partial": ("#fdf1dc", "#b3722a"),
    "no": ("#fbe4e2", "#b8433a"),
    "na": ("#efece5", "#9a978f"),
}
FACTOR = {"yes": 1.0, "partial": 0.5, "no": 0.0, "na": 0.0}
# The re-score: does the order hold when the loudest complaints count for much more?
ROBUST_H = 5
# Where a cluster goes when data["placement"] does not say, by rank (a landing's slots).
DEFAULT_SLOTS = ["HERO", "SUB LINE", "SUB LINE", "VISUAL / PROOF", "VISUAL / PROOF", "VISUAL / PROOF"]


def resolution(cluster_def):
    """yes | partial | no | na. "kavela" is the key the 181026 Kavela data used; "resolves" is general."""
    return cluster_def.get("resolves", cluster_def.get("kavela", "na"))


def score_clusters(data, weights):
    acc = {}
    for cat in data["categories"]:
        for comp in cat["competitors"]:
            for pain in comp["pains"]:
                a = acc.setdefault(pain["cluster"], {"score": 0.0, "products": set(), "pains": 0})
                a["score"] += weights[pain["strength"]]
                a["products"].add(comp["name"])
                a["pains"] += 1
    rows = []
    for cid, a in acc.items():
        d = data["cluster_defs"][cid]
        res = resolution(d)
        if res == "na":
            continue
        rows.append({
            "id": cid, "name": d["name"], "resolves": res, "how": d.get("how", ""),
            "score": a["score"], "breadth": len(a["products"]), "pains": a["pains"],
            "priority": a["score"] * FACTOR[res],
            "where": ", ".join(sorted(a["products"])),
        })
    rows.sort(key=lambda r: (-r["priority"], -r["score"]))
    for i, r in enumerate(rows):
        r["placement"] = data.get("placement", {}).get(r["id"]) or (DEFAULT_SLOTS[i] if i < len(DEFAULT_SLOTS) else "FAQ")
    return rows


def robustness(data, rows):
    alt = score_clusters(data, dict(data["weights"], H=ROBUST_H))
    if not rows:
        return
    held = alt[0]["id"] == rows[0]["id"]
    verdict = "holds" if held else f"FLIPS to '{alt[0]['name']}': the ranking is not decisive, say so"
    print(f"\nrobustness, H weighted {ROBUST_H}: #1 {verdict}")
    for i, r in enumerate(alt[:3], 1):
        print(f"  {i}. prio {r['priority']:>5g} | {r['name']}")


def esc(s):
    return escape(s, {'"': "&quot;"}).replace("\n", "&lt;br&gt;")


class Page:
    def __init__(self, name):
        self.name = name
        self.cells = []
        self.boxes = []  # (x, y, w, h, label), for the overlap check
        self.n = 1

    def nid(self):
        self.n += 1
        return f"c{self.n}"

    def _vertex(self, x, y, w, h, value, style):
        cid = self.nid()
        self.boxes.append((x, y, w, h, value.split("\n")[0][:40]))
        self.cells.append(
            f'<mxCell id="{cid}" value="{esc(value)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>'
        )
        return cid

    def box(self, x, y, w, h, value, fill, stroke, font=INK, size=12, bold=False, rounded=12, extra=""):
        style = (
            f"rounded=1;arcSize={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
            f"fontColor={font};fontSize={size};fontStyle={1 if bold else 0};spacing=6;{extra}"
        )
        return self._vertex(x, y, w, h, value, style)

    def text(self, x, y, w, h, value, size=12, bold=False, color=INK, align="left"):
        style = (
            f"text;html=1;whiteSpace=wrap;align={align};verticalAlign=top;fontSize={size};"
            f"fontStyle={1 if bold else 0};fontColor={color};"
        )
        return self._vertex(x, y, w, h, value, style)

    def edge(self, a, b, color="#9a978f", width=1.5, style="entityRelationEdgeStyle", label=""):
        cid = self.nid()
        s = f"edgeStyle={style};curved=1;html=1;endArrow=none;strokeColor={color};strokeWidth={width};fontSize=11;"
        if style != "entityRelationEdgeStyle":
            s = f"edgeStyle={style};rounded=1;html=1;endArrow=block;endFill=1;strokeColor={color};strokeWidth={width};fontSize=11;"
        self.cells.append(
            f'<mxCell id="{cid}" value="{esc(label)}" style="{s}" edge="1" parent="1" source="{a}" target="{b}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        return cid

    def overlaps(self):
        hits = []
        for i, a in enumerate(self.boxes):
            for b in self.boxes[i + 1:]:
                if a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]:
                    hits.append((a[4], b[4]))
        return hits

    def xml(self):
        return (
            f'<diagram id="{self.name.lower().replace(" ", "-")}" name="{esc(self.name)}">'
            '<mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
            'arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0" background="#f5f2ec"><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(self.cells) + "</root></mxGraphModel></diagram>"
        )


LEAF_W, LEAF_H, GAP = 360, 46, 8
COMP_W, CAT_W = 170, 190
CAT_FILL = "#1f6f7f"


def landscape(data, product):
    p = Page("Landscape")
    cx, cw, ch = 0, 300, 90
    centre = p.box(cx - cw / 2, -ch / 2, cw, ch, data["center"], INK, INK, font="#ffffff", size=15, bold=True, rounded=20)
    top = -ch / 2

    for side in ("right", "left"):
        cats = [c for c in data["categories"] if c.get("side", "right") == side]
        rows = sum(max(1, len(cp["pains"])) for c in cats for cp in c["competitors"]) + 1.5 * len(cats)
        y = -rows * (LEAF_H + GAP) / 2
        top = min(top, y)
        sign = 1 if side == "right" else -1
        cat_x = cx + sign * 300 - (0 if side == "right" else CAT_W)
        comp_x = cx + sign * 560 - (0 if side == "right" else COMP_W)
        leaf_x = cx + sign * 800 - (0 if side == "right" else LEAF_W)
        for cat in cats:
            cat_top = y
            comp_ids = []
            for comp in cat["competitors"]:
                start = y
                leaf_ids = []
                for pain in comp["pains"]:
                    fill, stroke = STATUS[resolution(data["cluster_defs"][pain["cluster"]])]
                    label = f"{pain['text']}  [{pain['strength']}]"
                    leaf_ids.append(p.box(leaf_x, y, LEAF_W, LEAF_H, label, fill, stroke, size=11, rounded=10))
                    y += LEAF_H + GAP
                if not comp["pains"]:
                    y += LEAF_H + GAP
                mid = (start + y - GAP) / 2
                comp_id = p.box(comp_x, mid - 24, COMP_W, 48, comp["name"], "#ffffff", INK, size=13, bold=True)
                for lid in leaf_ids:
                    p.edge(comp_id, lid, color="#b0aca2", width=1)
                comp_ids.append(comp_id)
            cat_mid = (cat_top + y - GAP) / 2
            cat_id = p.box(cat_x, cat_mid - 28, CAT_W, 56, cat["name"], CAT_FILL, CAT_FILL, font="#ffffff", size=13, bold=True, rounded=16)
            p.edge(centre, cat_id, color=CAT_FILL, width=2.5)
            for cid in comp_ids:
                p.edge(cat_id, cid, color=INK, width=1.5)
            y += 1.5 * (LEAF_H + GAP)

    # The legend sits above the tallest side, clear of every leaf.
    lx, ly = -150, top - 240
    p.text(lx, ly, 300, 24, "Legend", size=13, bold=True)
    for i, (k, lab) in enumerate([("yes", f"{product} resolves it"), ("partial", f"{product} partly resolves it"), ("no", f"{product} does not resolve it")]):
        f, s = STATUS[k]
        p.box(lx, ly + 28 + i * 34, 300, 28, lab, f, s, size=11, rounded=10)
    p.text(lx, ly + 136, 300, 60, "[H] / [M] / [L] = how loudly users report it (threads, reactions, reviews). [W] = only found secondhand.", size=10, color="#6b6a6f")
    return p


def clusters_page(rows, product):
    p = Page("Pain clusters")
    p.text(0, -70, 1400, 30, f"Pain clusters across every competitor, ranked by priority = loudness summed across every product that reports it, x how well {product} resolves it (yes 1, partly 0.5)", size=15, bold=True)
    cols = [(0, 330, "Pain cluster (what users say)"), (340, 110, "Score"), (460, 250, "Where it hurts"), (720, 360, f"How {product} resolves it (code)"), (1090, 230, "Placement")]
    for x, w, h in cols:
        p.text(x, -32, w, 24, h, size=11, bold=True, color="#46464d")
    y = 0
    for cl in rows:
        fill, stroke = STATUS[cl["resolves"]]
        h = 96
        lead = cl["placement"].startswith("HERO")
        a = p.box(0, y, 330, h, cl["name"], "#ffffff", INK, size=12, bold=True)
        p.box(340, y, 110, h, f"priority {cl['priority']:g}\nloudness {cl['score']:g}\n{cl['breadth']} products", "#ffffff", "#9a978f", size=11)
        p.box(460, y, 250, h, cl["where"], "#ffffff", "#9a978f", size=10)
        b = p.box(720, y, 360, h, cl["how"], fill, stroke, size=10)
        c = p.box(1090, y, 230, h, cl["placement"], INK if lead else "#ffffff", INK, font="#ffffff" if lead else INK, size=11, bold=True)
        p.edge(a, b, color="#b0aca2", width=1, style="orthogonalEdgeStyle")
        p.edge(b, c, color="#b0aca2", width=1, style="orthogonalEdgeStyle")
        y += h + 12
    return p


def derivation_page(steps):
    p = Page("Derivation")
    ids = []
    for i, s in enumerate(steps):
        last = i == len(steps) - 1
        ids.append(p.box(i * 300, 0, 260, 190, f"<b>{s['title']}</b><br><br>{s['body']}", INK if last else "#ffffff", INK, font="#ffffff" if last else INK, size=11, rounded=10, extra="align=left;verticalAlign=top;"))
    for a, b in zip(ids, ids[1:]):
        p.edge(a, b, color=INK, width=2, style="orthogonalEdgeStyle")
    return p


def main(src, dst):
    with open(src) as f:
        data = json.load(f)
    product = data.get("product", "The product")
    rows = score_clusters(data, data["weights"])
    for i, r in enumerate(rows, 1):
        print(f"{i:>2}. prio {r['priority']:>5g} | loud {r['score']:>5g} | {r['breadth']:>2} products | {r['pains']:>2} pains | {r['resolves']:<7} | {r['placement'][:24]:<24} | {r['name']}")
    robustness(data, rows)

    pages = [landscape(data, product), clusters_page(rows, product)]
    if data.get("derivation"):
        pages.append(derivation_page(data["derivation"]))
    print()
    for pg in pages:
        hits = pg.overlaps()
        print(f"overlaps on '{pg.name}': {len(hits)}" + "".join(f"\n  {a!r} x {b!r}" for a, b in hits[:5]))

    with open(dst, "w") as f:
        f.write('<mxfile host="app.diagrams.net" type="device">' + "".join(pg.xml() for pg in pages) + "</mxfile>")
    print("wrote", dst, sum(len(pg.cells) for pg in pages), "cells")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
