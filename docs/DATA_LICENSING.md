# Data licensing and redistribution

The public package distributes code, series metadata, transformations, manifests, hashes, model outputs, and a small derived PCE initialization fixture. It does not distribute downloaded raw observations or the reconstructed calibration CSV.

| Source | Series | Status | Public-package treatment |
|---|---|---|---|
| U.S. Bureau of Economic Analysis via FRED/ALFRED | PCEPI, PCEPILFE, GDPC1 | derived-only | Retrieve at install; retain only small derived initialization and metrics with attribution |
| U.S. Bureau of Labor Statistics via FRED/ALFRED | UNRATE | retrieve-at-install | No raw observations bundled |
| Federal Reserve / Chicago Fed via FRED | FEDFUNDS, NFCI, TOTALSL | retrieve-at-install | No raw observations bundled |
| Congressional Budget Office via FRED | GDPPOT | retrieve-at-install | No raw observations bundled |
| University of Michigan via FRED | MICH | unresolved for redistribution | No raw or reconstructed calibration data bundled |
| U.S. Energy Information Administration via FRED | DCOILWTICO | retrieve-at-install | No raw observations bundled |

BEA states that its website information is generally public domain unless noted otherwise and requests attribution. FRED requires users to inspect each series' copyright tag and source terms. Because provider terms can change and FRED content can include third-party restrictions, this repository applies the conservative retrieve-at-install strategy to every raw series.

Official retrieval writes only to ignored paths: `data/generated/` and `calibration/frozen/`. Users are responsible for complying with current source terms. Nothing in the MIT software license grants rights to third-party data.
