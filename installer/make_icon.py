"""
make_icon.py
============
Erzeugt das CleanSweep-Icon (cleansweep.ico) - ein Besen im Marine-/Amber-Look,
passend zur App. Reproduzierbar: einfach erneut ausfuehren.

    python make_icon.py   ->  cleansweep.ico  (mehrere Groessen 16-256)
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

# Farben (wie in der App).
MARINE = (46, 94, 140, 255)
MARINE_DARK = (28, 33, 43, 255)
AMBER = (224, 164, 88, 255)
AMBER_DARK = (176, 122, 48, 255)
WHITE = (240, 244, 248, 255)

S = 256  # in hoher Aufloesung zeichnen, danach verkleinern


def _rotate(points, cx, cy, deg):
    """Dreht eine Punktliste um (cx, cy) um deg Grad (fuer den schraegen Besen)."""
    import math
    r = math.radians(deg)
    cos, sin = math.cos(r), math.sin(r)
    out = []
    for x, y in points:
        dx, dy = x - cx, y - cy
        out.append((cx + dx * cos - dy * sin, cy + dx * sin + dy * cos))
    return out


def _sparkle(d, cx, cy, r, color):
    """Zeichnet ein kleines Vierzack-Funkeln (Sauberkeits-Symbol)."""
    d.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
               (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
               (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
               (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=color)


def build() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Hintergrund: marineblaues, abgerundetes Quadrat mit dezentem Rand.
    m = 8
    d.rounded_rectangle([m, m, S - m, S - m], radius=48, fill=MARINE)
    d.rounded_rectangle([m, m, S - m, S - m], radius=48, outline=MARINE_DARK, width=4)

    # Besen leicht schraeg (um die Mitte gedreht).
    cx, cy, angle = 128, 138, 18

    # Stiel (amber, abgerundet).
    handle = _rotate([(118, 40), (138, 40), (138, 150), (118, 150)], cx, cy, angle)
    d.polygon(handle, fill=AMBER)
    cap = _rotate([(118, 40), (138, 40), (138, 52), (118, 52)], cx, cy, angle)
    d.polygon(cap, fill=AMBER_DARK)

    # Bindung (dunkler Streifen unter dem Stiel).
    band = _rotate([(98, 150), (158, 150), (158, 168), (98, 168)], cx, cy, angle)
    d.polygon(band, fill=AMBER_DARK)

    # Borsten (weisser Trapez-Faecher, nach unten breiter).
    bristles = _rotate([(96, 168), (160, 168), (188, 226), (68, 226)], cx, cy, angle)
    d.polygon(bristles, fill=WHITE)

    # Borsten-Striche (marine), damit man die Strands sieht.
    for bx in range(80, 180, 16):
        line = _rotate([(bx, 172), (bx - 12, 224)], cx, cy, angle)
        d.line(line, fill=MARINE, width=5)

    # Ein paar Funkeln (Sauberkeit).
    _sparkle(d, 196, 96, 16, WHITE)
    _sparkle(d, 210, 150, 10, AMBER)
    _sparkle(d, 60, 80, 11, AMBER)

    return img


def main() -> None:
    out = Path(__file__).resolve().parent / "cleansweep.ico"
    img = build()
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
             (128, 128), (256, 256)]
    img.save(out, format="ICO", sizes=sizes)
    print(f"Icon gespeichert: {out}")


if __name__ == "__main__":
    main()
