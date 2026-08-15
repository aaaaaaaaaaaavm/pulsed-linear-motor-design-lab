# Pulsed Linear Motor Design Lab: one page

I separated one reusable screening question from VOLLEY's full spacecraft-deployer model:
given moving mass, stroke, thrust constant, sheet current, force limit, source voltage and ESR,
what velocity is physically reachable, and can the source meet the requested peak power?

| | |
|---|---|
| Corrected VOLLEY detailed result | **16.029 m/s at 10.068 g** |
| Standalone constant-force screen | **16.024 m/s at 10.071 g** |
| Declared regression band | 0.01 m/s and 0.01 g |
| 12 mΩ source assumption | closes the elementary peak-power test |
| 116 mΩ representative single string | **fails** the same test |

The 0.005 m/s agreement is a software regression result. It does not validate the field,
converter, bank, winding, thermal path or mechanism.

The evidence is deliberately mixed. A1 is PARTIAL: the corrected thrust constant agrees with
the independent differential-FEM implementation to 0.03%, while two field bands remain missed.
A8 is SUPERSEDED because the retained ngspice run predates the corrected operating point. A10
FAILS for a purchasable single string. Nothing has been built or measured.

The standalone package has no runtime dependency. The higher-fidelity reference files retain
their exact tool versions, settings, hashes and VOLLEY commit identity under
`reference/volley/` and `SOURCE_MANIFEST.json`.
