# Data and licensing audit

The frozen calibration inputs are ten FRED/ALFRED series accompanied by source identifiers, observation windows, and checksums. FRED series remain subject to the source agencies' terms; repository inclusion is for reproducible research and does not transfer third-party rights. No API key or retrieved credential is committed.

Before public redistribution, maintainers must verify each upstream series' current notes and source-agency reuse terms, retain attribution, and avoid implying Federal Reserve endorsement. This audit is a release checklist, not legal advice.

## R10 release decision

`NOT CLEARED FOR PUBLIC REDISTRIBUTION.` The repository still bundles raw observations and the series-by-series source-agency permissions have not been confirmed. Until that review is complete, either obtain clearance or remove bundled raw observations and reproduce them through documented retrieval scripts. Derived metrics may also require source-specific attribution review.
