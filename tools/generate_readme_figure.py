"""Generate the README's first-order design-screen figure from the committed cases."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from plmd.core import calculate  # noqa: E402


INK = "#e8f0f7"
MUTED = "#8fa7ba"
BG = "#07111b"
PANEL = "#0c1d2a"
CYAN = "#38d6e8"
AMBER = "#ffb454"
RED = "#ff6b6b"


def text(x: float, y: float, value: str, size: int, colour: str = INK, weight: int = 400,
         anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{colour}" font-family="Inter,Segoe UI,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def rect(x: float, y: float, w: float, h: float, fill: str = PANEL, stroke: str = "#17384b",
         radius: int = 18) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def load(name: str) -> tuple[dict, dict]:
    case = json.loads((ROOT / "cases" / name).read_text(encoding="utf-8"))
    return case, calculate(case)


def render() -> str:
    desktop_case, desktop = load("desktop_stage.json")
    volley_case, volley = load("volley_reference.json")
    cases = [("DESKTOP STAGE", desktop_case, desktop, CYAN), ("VOLLEY REFERENCE", volley_case, volley, AMBER)]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
        f'<rect width="1600" height="900" fill="{BG}"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#3f718c"/></marker></defs>',
        text(74, 82, "PULSED LINEAR MOTOR DESIGN LAB", 24, CYAN, 700),
        text(74, 128, "A first rejection screen before higher-fidelity models are worth building.", 31, INK, 600),
        text(74, 166, "Every value below is computed from the two committed case files.", 19, MUTED),
    ]

    for index, (label, case, result, colour) in enumerate(cases):
        x = 74 + index * 510
        y = 220
        out += [rect(x, y, 470, 360, stroke=colour), text(x + 28, y + 48, label, 18, colour, 700)]
        metrics = [
            ("MOVING MASS", f"{result['moving_mass_kg']:.3f} kg"),
            ("APPLIED FORCE", f"{result['applied_force_N']:.1f} N"),
            ("EXIT VELOCITY", f"{result['exit_velocity_m_s']:.3f} m/s"),
            ("ACCELERATION", f"{result['acceleration_g']:.2f} g"),
        ]
        for row, (name, value) in enumerate(metrics):
            yy = y + 98 + row * 54
            out += [text(x + 28, yy, name, 13, MUTED, 600), text(x + 442, yy, value, 23, INK, 650, "end")]
        ceiling = result["source_power_ceiling_W"]
        required = case["peak_power_required_W"]
        ratio = ceiling / required
        status = "CLOSES" if result["source_closes_at_peak"] else "FAILS"
        status_colour = CYAN if result["source_closes_at_peak"] else RED
        out += [
            text(x + 28, y + 306, "THEVENIN SOURCE CEILING / REQUIRED PEAK", 13, MUTED, 600),
            text(x + 442, y + 342, f"{ratio:.2f}x  {status}", 21, status_colour, 700, "end"),
        ]

    x, y = 1094, 220
    out += [rect(x, y, 432, 360), text(x + 28, y + 48, "THE SCREEN", 18, CYAN, 700)]
    nodes = [
        ("INPUTS", "mass · stroke · Kt · current"),
        ("MECHANICS", "force → acceleration"),
        ("OUTPUT", "velocity · kinetic energy"),
        ("SOURCE", "V² / 4R ≥ peak power?"),
    ]
    for i, (title, sub) in enumerate(nodes):
        yy = y + 78 + i * 68
        out += [rect(x + 28, yy, 376, 50, fill="#0a1722", radius=10), text(x + 46, yy + 22, title, 12, CYAN, 700), text(x + 46, yy + 41, sub, 15, INK)]
        if i < len(nodes) - 1:
            out.append(f'<line x1="{x + 216}" y1="{yy + 50}" x2="{x + 216}" y2="{yy + 66}" stroke="#3f718c" stroke-width="2" marker-end="url(#arrow)"/>')

    out += [
        rect(74, 626, 1452, 190, fill="#091720", stroke="#21465b"),
        text(104, 674, "WHAT A PASS MEANS", 15, CYAN, 700),
        text(104, 714, "The arithmetic is internally consistent and the assumed source clears a necessary power ceiling.", 23, INK, 550),
        text(104, 758, "WHAT IT DOES NOT MEAN", 15, RED, 700),
        text(104, 798, "No finite field, switching waveform, thermal path or hardware performance is established.", 23, INK, 550),
        text(1494, 860, "MODEL OUTPUT · NOT EXPERIMENTAL VALIDATION", 15, MUTED, 650, "end"),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def main() -> None:
    output = ROOT / "figures" / "design-screen.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(), encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
