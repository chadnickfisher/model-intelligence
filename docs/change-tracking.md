# Current records and change tracking

Canonical records retain public sources, inspection dates, conditions, contradictions and uncertainty. [Concise changes](../changelog/changes.yaml) describe material product updates; Git retains previous versions. [Current checksums](../data/record-integrity.yaml) detect uncaptured changes without duplicating values.

The public repository contains accepted product records and reusable software. Local operating instructions and temporary research work are excluded. Git preserves previous public versions; removing a file from the current tree does not remove its history.

After editing canonical records, run:

```sh
python tools/capture_changes.py --observed-at YYYY-MM-DD --reason "Material change and why" --evidence src-...
python tools/render.py
python tools/validate.py
```

Automated tests and CI protect the product and remain tracked. Rendering and product validation need no local research archive.
