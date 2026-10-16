# Change log / audit record

## 16 October 2026

Separate total moving-energy and peak-power feasibility; retain failed hypothetical speeds explicitly.

I record changes here by cause and consequence. Read this with `docs/PROVENANCE.md` and
`OPEN_PROBLEMS.md`; a version number is not evidence that the hardware exists.

## 0.1.3 — move the reference case to VOLLEY's corrected operating point

- VOLLEY applied a depth-resolved thrust constant on 2026-08-13 and the reference case here
  still carried the superseded one. **K_t 11.025833 → 10.538611 N per kA/m**, commanded force
  **1389.255 → 1327.865 N**, electrical input **2850.895 → 2782.391 J**.
- **The regression band holds at the new point.** The standalone constant-force screen returns
  **16.024 m/s and 10.071 g** against VOLLEY's **16.029 and 10.068** — a **0.005 m/s** difference
  inside the declared 0.01 m/s and 0.01 g bands, against 0.003 m/s at the old point. **The band
  was not widened**, and the agreement is a software regression result rather than evidence about
  any physical quantity.
- The regression test asserts the corrected figures. README and SUMMARY quote them.
- `reference/volley/` is unchanged. It is a dated snapshot of the VOLLEY state it was taken from
  and is not re-vendored here; the case file is what this repository screens against.

## 0.1.2 — hash the committed source state consistently

- Recomputed the source manifest from the retained blobs in VOLLEY commit `aa22a06`, not
  from platform-specific working-tree line endings.
- Made repository verification hash committed blobs while separately rejecting any retained
  source file that differs from the current commit. A source archive normalizes text line endings
  before hashing because no Git metadata is present; binary files remain byte-exact.
- Kept every model result and evidence class unchanged. This is a provenance portability fix,
  not new motor evidence.

## 0.1.1 — reconcile the extraction with committed VOLLEY

- Replaced the provisional working-tree provenance with VOLLEY commit `aa22a06`. Every retained
  source file was checked byte-for-byte against that commit before the manifest moved.
- Put the standalone and detailed reference results next to each other. Their 0.003 m/s
  difference is inside the pre-existing 0.01 m/s regression band.
- Added explicit rejection of non-positive thrust, force-limit, voltage and peak-power inputs.
  A square root failing later is not an engineering verdict.
- Expanded the source comments and failure-path tests so the reason for each guard remains
  beside the code.
- Kept A1 PARTIAL, A8 SUPERSEDED and A10 FAIL visible. No evidence class changed.

## 0.1.0 — initial public baseline

- Extracted the constant-force screening question from the corrected VOLLEY calculation.
- Added a standalone interface, a non-VOLLEY case, tests and repository verification.
- Retained the original numerical sources, failed checks, partial checks and unresolved risks.
