# Decision log

## D1: keep a screening core separate from the reference calculation

I did not disguise the full VOLLEY script as a general package. The `plmd` module contains
only the assumptions that can be stated cleanly as inputs. The original calculation remains
under `reference/volley/` with its hashes and qualifications.

## D2: retain the failed source-impedance result

The 12 mΩ modelled bank is not a purchasable single string. The calculator exposes the
maximum-power failure instead of silently adding parallel strings or moving the requirement.
