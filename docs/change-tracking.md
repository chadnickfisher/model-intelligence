# Current records and change tracking

Canonical records retain public sources, inspection dates, conditions, contradictions and uncertainty. [Concise changes](../changelog/changes.yaml) describe material product updates; Git retains previous versions. [Current checksums](../data/record-integrity.yaml) detect uncaptured changes without duplicating values.

Detailed research packets, assignments, timings and review reports belong under ignored `.local/` or outside the repository. Validate those packets with the bounded research tools before changing product records. They are not app data or published documentation. Older artifacts remain recoverable from their Git versions.

After editing canonical records, run:

```sh
python tools/capture_changes.py --observed-at YYYY-MM-DD --reason "Material change and why" --evidence src-...
python tools/render.py
python tools/validate.py
```

Automated tests and CI protect the product and remain tracked. Rendering and product validation need no local research archive.
