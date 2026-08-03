# Change log / audit record

I record changes here by cause and consequence. Read this with `docs/PROVENANCE.md` and
`OPEN_PROBLEMS.md`; a version number is not evidence that the hardware exists.

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
