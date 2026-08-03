import json
import math
import unittest
from pathlib import Path

from plmd import calculate


class ScreeningTests(unittest.TestCase):
    def case(self):
        root = Path(__file__).resolve().parents[1]
        return json.loads((root / "cases/volley_reference.json").read_text())

    def test_screen_agrees_with_corrected_reference_within_one_centimetre_per_second(self):
        result = calculate(self.case())
        self.assertLess(abs(result["exit_velocity_m_s"] - 16.388), 0.01)
        self.assertLess(abs(result["acceleration_g"] - 10.533), 0.01)

    def test_zero_stroke_has_zero_exit_velocity(self):
        case = self.case()
        case["stroke_m"] = 0.0
        self.assertEqual(calculate(case)["exit_velocity_m_s"], 0.0)

    def test_realistic_single_string_fails_peak_power(self):
        case = self.case()
        case["bank_esr_ohm"] = 0.116
        self.assertFalse(calculate(case)["source_closes_at_peak"])

    def test_payload_energy_is_below_total_moving_energy(self):
        result = calculate(self.case())
        self.assertLess(result["payload_kinetic_energy_J"], result["moving_kinetic_energy_J"])
