# Validation record

| Item | Method | Current outcome |
|---|---|---|
| Standalone screening core | zero-stroke, carriage-energy, impossible-energy and corrected-reference tests | PASS for the declared software tests |
| Input boundary | missing, non-positive and non-finite input tests | PASS; invalid cases fail before a derived result |
| A1 airgap field | scikit-fem 12.0.2 on a gmsh 4.15.2 mesh | **PARTIAL**; thrust agrees to 0.03%, two declared bands miss |
| A8 pulsed power | ngspice 42 | **SUPERSEDED**; retained for history, predates the corrected operating point |
| A10 source ESR | corrected Python shot sweep | **FAIL** for a purchasable single string |
| A11 regeneration | independent numerical implementation within the same physics model | corrected to 291.4 J recovered; requires hardware testing |
| A12 inter-array force | two Magpylib-based force integrals | model-to-model agreement; not experimental evidence |

Passing the software tests establishes implementation consistency. It does not establish the
two-dimensional field approximation, winding construction, switching hardware, thermal path,
magnet retention or flight suitability.

The impossible-energy regression deliberately supplies 1 J while keeping a passing peak-power
ceiling. It must fail `energy_closes` and `screen_feasible`. The lossless boundary test is an
arithmetic limit, not a claim of physically attainable efficiency.
