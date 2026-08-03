# Pulsed Linear Motor Design Lab: one page

I separated the reusable screening question from VOLLEY's full spacecraft-deployer model:
given moving mass, stroke, thrust constant, sheet current, source voltage and ESR, what
velocity is physically reachable and can the source meet the requested peak power?

The corrected VOLLEY reference case returns **16.388 m/s at 10.533 g**. The modelled
12 mΩ bank clears the elementary maximum-power test; a representative 116 mΩ single
string does not. That is a screening result, not a cell qualification or hardware result.

The repository includes one independent desktop-stage example, source-hash verification,
unit tests, corrected result fixtures, and visible PARTIAL, superseded and open outcomes.
