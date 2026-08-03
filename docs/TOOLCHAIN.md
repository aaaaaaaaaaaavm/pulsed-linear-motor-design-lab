# Toolchain record

| Tool | Version | License | Role | Inputs and settings | Output |
|---|---:|---|---|---|---|
| Python | 3.11.9 | PSF License | corrected reference scripts | exact source hashes in `SOURCE_MANIFEST.json` | committed JSON fixtures |
| NumPy | 2.3.5 | BSD-3-Clause | integration and arrays | settings recorded in each result JSON | result JSON |
| Magpylib | 5.2.3 | BSD-3-Clause | analytic magnet fields and A12 force methods | source hashes and grids in A12 JSON | `A12_inter_array_force.json` |
| scikit-fem | 12.0.2 | BSD | A1 differential magnetostatic solve | P1 Lagrange, 140,750 elements, 0.6 mm airgap mesh | `A1_femm.json` |
| gmsh | 4.15.2 | GPLv2+ | A1 mesh generation | 500 mm box, `Az = 0` far boundary | mesh consumed by A1 script |
| ngspice | 42 | BSD-3-Clause | superseded A8 pulse-chain comparison | retained netlist, 12 mΩ ESR assumption | `A8_pulse.json`, superseded |

File hashes are recorded in `SOURCE_MANIFEST.json`. The external tools are not vendored.
A8 is retained because an old result should remain visible, not because it is current.
