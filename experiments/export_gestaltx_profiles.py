#!/usr/bin/env python3
"""Export factual target identities for GestaltX; never connects to an iPhone.

SPDX-License-Identifier: AGPL-3.0-only
The generated Swift contains device metadata and declarations, not Nugget's
application or restore implementation.
"""
import argparse
import json
from pathlib import Path
import re


def generate(path):
    manifest = json.loads(path.read_text())
    if manifest.get("schemaVersion") != 1 or not manifest.get("profiles"):
        raise ValueError("Unsupported or empty identity manifest")
    rows = []
    identifiers = set()
    for profile in manifest["profiles"]:
        if set(profile) != {"id", "name", "product", "board", "platform"}:
            raise ValueError("Unexpected profile fields")
        if profile["id"] in identifiers:
            raise ValueError("Duplicate profile ID")
        identifiers.add(profile["id"])
        for key, pattern in [("id", r"[a-z0-9]+"), ("name", r"iPhone [0-9]+ Pro"),
                             ("product", r"iPhone[0-9]+,[0-9]+"),
                             ("board", r"[A-Z][0-9]+[a-z]*AP"), ("platform", r"t[0-9]+")]:
            if not isinstance(profile[key], str) or not re.fullmatch(pattern, profile[key]):
                raise ValueError("Invalid " + key)
        fields = ", ".join(f"{key}: {json.dumps(profile[key])}" for key in ["id", "name", "product", "board", "platform"])
        rows.append("        Profile(" + fields + ")")
    return ("// Device facts exported from the Nugget fork's experiments/gestaltx-identities.json.\n"
            "// See docs/IDENTITY_EXPERIMENT.md for provenance and limitations.\n"
            "extension IdentitySpoof {\n    static let profiles: [Profile] = [\n"
            + ",\n".join(rows) + "\n    ]\n}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("gestaltx-identities.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(generate(args.manifest))
    print("Exported identity metadata to", args.output)
