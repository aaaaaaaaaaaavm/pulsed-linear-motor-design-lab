# Contributing

I treat numerical outputs as engineering claims, not decoration. A change to `plmd` should
state units, identify the assumption it changes and include a limiting case or rejection-path
test. Do not replace an unfavourable result by moving a tolerance after the run.

Commit subjects should describe the engineering consequence. “Reject non-physical force
inputs” is useful later; “update core.py” is not.

The files under `reference/volley/` are retained from VOLLEY commit `aa22a06`. Change them only
by selecting a later reviewed VOLLEY commit, copying its exact blobs and regenerating
`SOURCE_MANIFEST.json`. A changed hash without that chain is a provenance break.

Before proposing a release, run:

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```
