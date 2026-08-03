"""Screening calculations for a pulsed linear-motor stage.

This module uses SI units. It is a preliminary calculator, not a qualification model.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


REQUIRED = {
    "payload_mass_kg", "carriage_mass_kg", "stroke_m",
    "thrust_constant_N_per_kA_m", "sheet_current_kA_m",
    "force_limit_N", "electrical_input_J", "bank_voltage_V",
    "bank_esr_ohm", "peak_power_required_W",
}


def calculate(case: dict[str, float]) -> dict[str, float | bool]:
    missing = sorted(REQUIRED - case.keys())
    if missing:
        raise ValueError("missing fields: " + ", ".join(missing))
    values = {key: float(case[key]) for key in REQUIRED}
    if values["payload_mass_kg"] <= 0 or values["carriage_mass_kg"] < 0:
        raise ValueError("masses must be positive, with a non-negative carriage mass")
    if values["stroke_m"] < 0:
        raise ValueError("stroke_m must be non-negative")
    if values["bank_esr_ohm"] <= 0 or values["electrical_input_J"] <= 0:
        raise ValueError("bank_esr_ohm and electrical_input_J must be positive")

    moving_mass = values["payload_mass_kg"] + values["carriage_mass_kg"]
    electromagnetic_force = (
        values["thrust_constant_N_per_kA_m"] * values["sheet_current_kA_m"]
    )
    applied_force = min(electromagnetic_force, values["force_limit_N"])
    acceleration = applied_force / moving_mass
    exit_velocity = math.sqrt(2.0 * acceleration * values["stroke_m"])
    payload_ke = 0.5 * values["payload_mass_kg"] * exit_velocity**2
    moving_ke = 0.5 * moving_mass * exit_velocity**2
    source_power_ceiling = values["bank_voltage_V"]**2 / (4.0 * values["bank_esr_ohm"])
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
        "source_closes_at_peak": source_power_ceiling >= values["peak_power_required_W"],
    }


def load_case(path: str | Path) -> dict[str, float]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
