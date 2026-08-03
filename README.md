# Pulsed Linear Motor Design Lab

<p align="center"><img src="reference/volley/paper/figures/F01_shot.png" alt="Corrected VOLLEY shot calculation" width="100%"></p>

A small, installable screening calculator for pulsed linear-motor stages, accompanied by
the corrected VOLLEY reference calculation and the independent checks that qualify it.

> **Status: computational screening tool.** Nothing here has been experimentally validated.
> I use it to expose force, stroke, moving-mass, source-impedance and energy trade-offs before
> a higher-fidelity electromagnetic or circuit analysis. It is not qualification software.

## What this demonstrates

- a parameterized SI-unit screening calculation with a command-line interface;
- a corrected reference point at **16.388 m/s and 10.533 g**;
- source-impedance rejection using the maximum-power limit;
- limiting-case and regression tests;
- a hashed path from every retained VOLLEY file to its reviewed source snapshot.

The reference record retains the uncomfortable results. A1 remains **PARTIAL** because two
declared field bands missed. A8 is retained as a **superseded ngspice run** and is not
presented as current. A10 shows that a purchasable single supercapacitor string does not
source the shot. No motor, bank or track has been built or measured.

## Run the standalone calculator

```bash
python -m pip install -e .
plmd cases/desktop_stage.json
plmd cases/volley_reference.json --out build/volley_reference.json
```

`desktop_stage.json` is deliberately not a VOLLEY case. It tests whether the interface is a
reusable calculator rather than a renamed project script.

## Verify the repository

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```

## Evidence boundary

The installable calculator is a transparent screening implementation. The original corrected
scripts, numerical results, FEM input, circuit input and validation outputs are retained under
`reference/volley/`. See [validation](docs/VALIDATION.md),
[toolchain](docs/TOOLCHAIN.md), [provenance](docs/PROVENANCE.md), and
[open problems](OPEN_PROBLEMS.md) before using a result.

## License

MIT. External solvers are not vendored and retain their own licenses.
