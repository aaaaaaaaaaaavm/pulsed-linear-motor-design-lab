"""Generate the README visual set from the committed screening cases."""

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
            ("IMPLIED VELOCITY", f"{result['exit_velocity_m_s']:.3f} m/s"),
            ("ACCELERATION", f"{result['acceleration_g']:.2f} g"),
        ]
        for row, (name, value) in enumerate(metrics):
            yy = y + 98 + row * 54
            out += [text(x + 28, yy, name, 13, MUTED, 600), text(x + 442, yy, value, 23, INK, 650, "end")]
        ceiling = result["source_power_ceiling_W"]
        required = case["peak_power_required_W"]
        ratio = ceiling / required
        status = "POWER PASS" if result["source_closes_at_peak"] else "POWER FAIL"
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
        ("SOURCE", "power ceiling + total energy"),
    ]
    for i, (title, sub) in enumerate(nodes):
        yy = y + 78 + i * 68
        out += [rect(x + 28, yy, 376, 50, fill="#0a1722", radius=10), text(x + 46, yy + 22, title, 12, CYAN, 700), text(x + 46, yy + 41, sub, 15, INK)]
        if i < len(nodes) - 1:
            out.append(f'<line x1="{x + 216}" y1="{yy + 50}" x2="{x + 216}" y2="{yy + 66}" stroke="#3f718c" stroke-width="2" marker-end="url(#arrow)"/>')

    out += [
        rect(74, 626, 1452, 190, fill="#091720", stroke="#21465b"),
        text(104, 674, "WHAT A PASS MEANS", 15, CYAN, 700),
        text(104, 714, "Only total-energy and peak-power screens pass; losses and hardware remain unresolved.", 23, INK, 550),
        text(104, 758, "WHAT IT DOES NOT MEAN", 15, RED, 700),
        text(104, 798, "No finite field, switching waveform, thermal path or hardware performance is established.", 23, INK, 550),
        text(1494, 860, "MODEL OUTPUT · NOT EXPERIMENTAL VALIDATION", 15, MUTED, 650, "end"),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def force_energy() -> str:
    cases = [
        ("DESKTOP STAGE", *load("desktop_stage.json"), CYAN),
        ("VOLLEY REFERENCE", *load("volley_reference.json"), AMBER),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="860" viewBox="0 0 1600 860">',
        f'<rect width="1600" height="860" fill="{BG}"/>',
        text(72, 78, "FORCE AND ENERGY ACCOUNTING", 24, CYAN, 700),
        text(72, 124, "The useful payload is only one part of the mass the field accelerates.", 34, INK, 600),
        text(72, 162, "Bars are normalised inside each case; labels retain the computed SI values.", 19, MUTED),
    ]
    for i, (label, case, result, colour) in enumerate(cases):
        x, y = 72 + i * 744, 218
        out += [rect(x, y, 704, 516, stroke=colour), text(x + 28, y + 46, label, 18, colour, 700)]
        force_rows = [
            ("ELECTROMAGNETIC", result["electromagnetic_force_N"], colour),
            ("APPLIED", result["applied_force_N"], CYAN),
            ("FORCE LIMIT", case["force_limit_N"], RED if result["force_limited"] else MUTED),
        ]
        force_max = max(value for _, value, _ in force_rows)
        out.append(text(x + 28, y + 84, "FORCE PATH", 13, MUTED, 650))
        for row, (name, value, row_colour) in enumerate(force_rows):
            yy = y + 112 + row * 58
            out += [
                text(x + 28, yy + 16, name, 13, MUTED, 600),
                f'<rect x="{x + 190}" y="{yy}" width="{430 * value / force_max:.1f}" height="22" rx="11" fill="{row_colour}" opacity="0.88"/>',
                text(x + 660, yy + 17, f"{value:.1f} N", 15, INK, 650, "end"),
            ]
        energy_rows = [
            ("PAYLOAD KINETIC", result["payload_kinetic_energy_J"], CYAN),
            ("MOVING KINETIC", result["moving_kinetic_energy_J"], colour),
            ("ELECTRICAL INPUT", case["electrical_input_J"], MUTED),
        ]
        energy_max = max(value for _, value, _ in energy_rows)
        out.append(text(x + 28, y + 314, "ENERGY PATH", 13, MUTED, 650))
        for row, (name, value, row_colour) in enumerate(energy_rows):
            yy = y + 342 + row * 58
            out += [
                text(x + 28, yy + 16, name, 13, MUTED, 600),
                f'<rect x="{x + 190}" y="{yy}" width="{430 * value / energy_max:.1f}" height="22" rx="11" fill="{row_colour}" opacity="0.88"/>',
                text(x + 660, yy + 17, f"{value:.1f} J", 15, INK, 650, "end"),
            ]
        out.append(text(x + 660, y + 496, f"payload efficiency {result['payload_efficiency_pct']:.1f}%", 17, colour, 700, "end"))
    out += [
        rect(72, 770, 1452, 48, fill="#091720", stroke="#21465b", radius=12),
        text(98, 801, "CONSTANT-FORCE SCREEN · NO COPPER LOSS, SWITCHING WAVEFORM OR THERMAL PATH", 15, MUTED, 650),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def source_window() -> str:
    cases = [
        ("DESKTOP STAGE", *load("desktop_stage.json"), CYAN),
        ("VOLLEY REFERENCE", *load("volley_reference.json"), AMBER),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="860" viewBox="0 0 1600 860">',
        f'<rect width="1600" height="860" fill="{BG}"/>',
        text(72, 78, "SOURCE-IMPEDANCE WINDOW", 24, CYAN, 700),
        text(72, 124, "Thevenin power collapses as ESR rises: V² / 4R.", 34, INK, 600),
        text(72, 162, "The crossing is a necessary source gate, not a converter or pulse simulation.", 19, MUTED),
    ]
    for i, (label, case, result, colour) in enumerate(cases):
        x, y, w, h = 72 + i * 744, 220, 704, 500
        left, top, plot_w, plot_h = x + 86, y + 78, 574, 318
        out += [rect(x, y, w, h, stroke=colour), text(x + 28, y + 44, label, 18, colour, 700)]
        required = case["peak_power_required_W"] / 1000.0
        max_kw = max(required * 1.7, case["bank_voltage_V"] ** 2 / (4 * 0.005) / 1000.0)
        out += [
            f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#365568"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#365568"/>',
        ]
        for tick in range(0, 151, 30):
            xx = left + plot_w * tick / 150
            out += [f'<line x1="{xx}" y1="{top + plot_h}" x2="{xx}" y2="{top + plot_h + 7}" stroke="#365568"/>', text(xx, top + plot_h + 29, str(tick), 12, MUTED, 400, "middle")]
        points = []
        for milliohm in range(5, 151, 2):
            kw = case["bank_voltage_V"] ** 2 / (4 * milliohm / 1000.0) / 1000.0
            xx = left + plot_w * milliohm / 150
            yy = top + plot_h * (1.0 - min(kw / max_kw, 1.0))
            points.append(f"{xx:.1f},{yy:.1f}")
        req_y = top + plot_h * (1.0 - required / max_kw)
        actual_mohm = case["bank_esr_ohm"] * 1000.0
        actual_kw = result["source_power_ceiling_W"] / 1000.0
        actual_x = left + plot_w * actual_mohm / 150.0
        actual_y = top + plot_h * (1.0 - min(actual_kw / max_kw, 1.0))
        threshold = case["bank_voltage_V"] ** 2 / (4.0 * case["peak_power_required_W"]) * 1000.0
        out += [
            f'<line x1="{left}" y1="{req_y:.1f}" x2="{left + plot_w}" y2="{req_y:.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="8 8"/>',
            f'<polyline points="{" ".join(points)}" fill="none" stroke="{colour}" stroke-width="4"/>',
            f'<circle cx="{actual_x:.1f}" cy="{actual_y:.1f}" r="9" fill="{INK}" stroke="{colour}" stroke-width="4"/>',
            text(left, top - 14, f"power ceiling, max {max_kw:.1f} kW", 13, MUTED),
            text(left + plot_w, req_y - 10, f"required {required:.1f} kW", 13, RED, 650, "end"),
            text(left + plot_w, top + plot_h + 58, "bank ESR [mΩ]", 13, MUTED, 500, "end"),
            text(x + 28, y + 452, f"committed: {actual_mohm:.0f} mΩ → {actual_kw:.1f} kW", 17, INK, 650),
            text(x + 676, y + 452, f"gate closes below {threshold:.1f} mΩ", 17, colour, 700, "end"),
        ]
    out += [text(1494, 818, "SOURCE CEILING ONLY · MODEL OUTPUT", 15, MUTED, 650, "end"), "</svg>"]
    return "\n".join(out) + "\n"


def main() -> None:
    outputs = {
        ROOT / "figures" / "design-screen.svg": render(),
        ROOT / "figures" / "force-energy.svg": force_energy(),
        ROOT / "figures" / "source-window.svg": source_window(),
    }
    for output, body in outputs.items():
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(body, encoding="utf-8")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
