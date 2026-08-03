# Decision log

## D1: keep a screening core separate from the reference calculation

I did not disguise the full VOLLEY script as a general package. The `plmd` module contains
only the assumptions that can be stated cleanly as inputs. The committed calculation remains
under `reference/volley/` with its hashes and qualifications.

## D2: retain the failed source-impedance result

The 12 mΩ modelled bank is not a purchasable single string. The calculator exposes the
maximum-power failure instead of silently adding parallel strings or moving the requirement.

## D3: reject non-physical inputs before evaluating the result

A zero force limit used to reach `sqrt()` and fail as a programming error. That loses the
engineering cause. The public function now names non-positive or non-finite fields before any
derived quantity is computed.

## D4: identify the source by commit and by file hash

The extracted files first existed as a reviewed working tree and were therefore identified
only by hashes. VOLLEY has since committed that exact state as `aa22a06`. I retain both
identities: the commit connects the history, while SHA-256 checks the copied bytes.
