"""Constant-force screening for a pulsed linear-motor stage.

WHY THIS IS SMALL
-----------------
VOLLEY's reference model resolves the winding, bank sag, copper loss, regeneration and the
stroke in time. Copying that whole model into a general package would preserve its project
assumptions while hiding where they came from. This module keeps only the inputs that can be
named without VOLLEY.

The result is a first rejection screen. It can show that a mass, stroke or source-impedance
combination cannot close. It cannot establish a finite field, switching waveform, thermal
path or hardware performance. All inputs and outputs use SI units.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


REQUIRED = {
    "payload_mass_kg",
    "carriage_mass_kg",
    "stroke_m",
    "thrust_constant_N_per_kA_m",
    "sheet_current_kA_m",
    "force_limit_N",
    "electrical_input_J",
    "bank_voltage_V",
    "bank_esr_ohm",
    "peak_power_required_W",
}

_STRICTLY_POSITIVE = {
    "payload_mass_kg",
    "thrust_constant_N_per_kA_m",
    "sheet_current_kA_m",
    "force_limit_N",
    "electrical_input_J",
    "bank_voltage_V",
    "bank_esr_ohm",
    "peak_power_required_W",
}


def calculate(case: dict[str, float]) -> dict[str, float | bool]:
    """Evaluate one constant-force screening case.

    The source test is the Thevenin maximum-power ceiling, V²/(4R). Passing it is necessary,
    not sufficient: no converter, current waveform or state-of-charge history is solved here.
    Invalid physical inputs are rejected before they can turn into a square-root or division
    error whose meaning would be ambiguous.
    """
    missing = sorted(REQUIRED - case.keys())
    if missing:
        raise ValueError("missing fields: " + ", ".join(missing))

    values = {key: float(case[key]) for key in REQUIRED}
    non_finite = sorted(key for key, value in values.items() if not math.isfinite(value))
    if non_finite:
        raise ValueError("non-finite fields: " + ", ".join(non_finite))

    non_positive = sorted(key for key in _STRICTLY_POSITIVE if values[key] <= 0.0)
    if non_positive:
        raise ValueError("fields must be positive: " + ", ".join(non_positive))
    if values["carriage_mass_kg"] < 0.0:
        raise ValueError("carriage_mass_kg must be non-negative")
    if values["stroke_m"] < 0.0:
        raise ValueError("stroke_m must be non-negative")

    moving_mass = values["payload_mass_kg"] + values["carriage_mass_kg"]
    electromagnetic_force = (
        values["thrust_constant_N_per_kA_m"] * values["sheet_current_kA_m"]
    )
    applied_force = min(electromagnetic_force, values["force_limit_N"])
    acceleration = applied_force / moving_mass
    exit_velocity = math.sqrt(2.0 * acceleration * values["stroke_m"])

    payload_ke = 0.5 * values["payload_mass_kg"] * exit_velocity**2
    moving_ke = 0.5 * moving_mass * exit_velocity**2

    # A source behind resistance R cannot deliver more than V²/(4R). A10 needed this guard:
    # the time-domain integrator once substituted a current after the bank stopped closing,
    # so an impossible source appeared to complete the shot.
    source_power_ceiling = values["bank_voltage_V"] ** 2 / (
        4.0 * values["bank_esr_ohm"]
    )

    return {
        "moving_mass_kg": moving_mass,
        "electromagnetic_force_N": electromagnetic_force,
        "applied_force_N": applied_force,
        "force_limited": applied_force < electromagnetic_force,
        "acceleration_m_s2": acceleration,
        "acceleration_g": acceleration / 9.80665,
        "exit_velocity_m_s": exit_velocity,
        "payload_kinetic_energy_J": payload_ke,
        "moving_kinetic_energy_J": moving_ke,
        "payload_efficiency_pct": 100.0 * payload_ke / values["electrical_input_J"],
        "source_power_ceiling_W": source_power_ceiling,
        "source_closes_at_peak": (
            source_power_ceiling >= values["peak_power_required_W"]
        ),
    }


def load_case(path: str | Path) -> dict[str, float]:
    """Load a UTF-8 JSON case without adding project-specific defaults."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
