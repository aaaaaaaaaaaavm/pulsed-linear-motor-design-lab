# Pulsed Linear Motor Design Lab

<p align="center"><img src="figures/design-screen.svg" alt="Pulsed linear motor first-order design screen for the desktop and VOLLEY reference cases" width="100%"></p>

[![CI](https://github.com/aaaaaaaaaaaavm/pulsed-linear-motor-design-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/aaaaaaaaaaaavm/pulsed-linear-motor-design-lab/actions/workflows/ci.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![Evidence: model only](https://img.shields.io/badge/evidence-model%20only%2C%20unverified-red.svg)](docs/PROVENANCE.md)

A focused, installable screening calculator for pulsed linear-motor stages, with the
committed VOLLEY reference calculation and the independent numerical checks that qualify it.

**Status: computational screening tool. Nothing here has been experimentally validated.**
I use it to expose force, stroke, moving-mass, source-impedance and energy trade-offs before
a field or circuit model is worth building. It is not qualification software.

## Why this exists

VOLLEY's full shot model answers a spacecraft-deployer question and carries years of project
history. That is the right engineering record and the wrong reusable interface. I separated
the smaller question that survives outside it:

> Given moving mass, stroke, thrust constant, sheet current, force limit, source voltage and
> ESR, what constant-force velocity is reachable, and can the source meet the requested peak
> power?

I kept the original scripts beside the smaller calculator rather than making the extraction
look more independent than it is.

## Current result, with the caveat attached

| Quantity | Standalone screen | Detailed VOLLEY reference |
|---|---:|---:|
| Exit velocity | 16.024 m/s | **16.029 m/s** |
| Acceleration | 10.071 g | **10.068 g** |
| Source check at 12 mΩ | closes | modelled assumption |
| Source check at 116 mΩ | **fails** | representative purchasable single string |

The velocity difference is 0.005 m/s, inside the declared 0.01 m/s regression band. That is
model-to-model agreement, not a force, current or velocity measurement.

<p align="center"><img src="reference/volley/paper/figures/F01_shot.png" alt="Corrected VOLLEY shot calculation" width="100%"></p>

<p align="center"><sub>The overview is regenerated from both committed case files by
<code>tools/generate_readme_figure.py</code>. The time history is the retained detailed VOLLEY
reference. Both are model output; neither is experimental validation.</sub></p>

A1 remains **PARTIAL** because two declared field bands missed. A8 is retained as a
**superseded ngspice run** and is not presented as current. A10 shows that a purchasable
single supercapacitor string does not source the shot. No motor, bank or track has been built
or measured.

## Run it

```bash
python -m pip install -e .
plmd cases/desktop_stage.json
plmd cases/volley_reference.json --out build/volley_reference.json
```

`desktop_stage.json` is deliberately not a VOLLEY case. It is the check that this is a
reusable interface rather than a renamed project script.

## Verify it

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```

The tests cover the corrected reference point, zero stroke, missing inputs, non-physical
force inputs, the realistic source-impedance failure and the payload-energy bound.

## Repository layout

- `src/plmd/` — the dependency-free screening calculator and command-line entry point;
- `cases/` — one VOLLEY reference case and one independent desktop-stage case;
- `tests/` — limiting cases, rejection paths and the declared regression band;
- `reference/volley/` — files retained byte-for-byte from VOLLEY commit `aa22a06`;
- `docs/` — validation boundary, tool versions, provenance, decisions and roadmap.

Read [validation](docs/VALIDATION.md), [toolchain](docs/TOOLCHAIN.md),
[provenance](docs/PROVENANCE.md), and [open problems](OPEN_PROBLEMS.md) before using a result.

## Licence

**CC BY 4.0** — full text in [`LICENSE`](LICENSE), attribution form in [`NOTICE`](NOTICE).
Attribution requires credit, a link to the licence, and **an indication of whether changes were
made**.

**Not retroactive:** snapshots taken before this change remain available under the MIT licence
they carried at the time, retained at [`LICENSE-MIT-superseded`](LICENSE-MIT-superseded).

This repository carries copies of VOLLEY analysis code under `reference/volley/`. CC BY 4.0 does
not license patent rights, which is why a patent-granting licence was not used here.
