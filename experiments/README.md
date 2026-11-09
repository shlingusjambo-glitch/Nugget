# GestaltX identity experiment

This fork preserves Nugget as a reference for its cached ProductType,
HardwareModel and HardwarePlatform spoofing. Do not run Nugget's restore
workflow on iOS 27. The companion iOS implementation uses GestaltX's
worse_query access and backup/write verification instead:
https://github.com/shlingusjambo-glitch/GestaltX/tree/experiment/siri-identity

`gestaltx-identities.json` records target device facts and their provenance.
Export the data declarations into the companion checkout with:

```sh
python3 experiments/export_gestaltx_profiles.py \
  --output ../GestaltX/GestaltX/IdentitySpoofProfiles.swift
```

This command only writes a local source file. It does not contact an Apple
account, connect to a device, or perform a restore. No Nugget application or
restore code is copied into GestaltX. The generated declarations contain
device metadata. New experiment tooling retains the Nugget fork's AGPL license.

The target identity is a hypothesis about eligibility, not a proven Expressive
Voices unlock. Neither metadata export nor a verified MobileGestalt write proves
that the model downloaded or runs. See the companion experiment guide for the
on-device test and rollback procedure.
