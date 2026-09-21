# Clean-clone reproduction

## Requirements

- Python 3.12 with NumPy, pandas, matplotlib, pytest, nbformat, and Jupyter
- Node.js 22.13 or newer
- pnpm
- Internet access to official FRED/ALFRED endpoints

No private path or API key is required for the normal R11 chain.

## Exact command chain

```powershell
pnpm install --frozen-lockfile
python scripts/fetch_official_data.py
python scripts/build_vintages.py
python calibration/build_frozen_sample.py
python calibration/estimate_parameters.py
python r10/run_r10_evaluation.py
python r11/run_uncertainty_repair.py
python scripts/build_parity_fixtures.py
python -m pytest -q
pnpm test
pnpm build
pnpm start
```

Open the local URL printed by `pnpm start`, enter the Fed 2022 scenario, lock one decision, reveal history, and advance once. Confirm that the briefing shows Headline PCE as the engine state and Headline CPI as supplementary information.

## Expected generated paths

- `data/generated/`: raw current and ALFRED vintage downloads; ignored
- `calibration/frozen/`: reconstructed raw and quarterly calibration data; ignored
- `data/scenarios/fed_2022_pce_initialization.json`: small derived release fixture
- `r10/results/` and `r11/results/`: validation evidence

Network or upstream-schema failures must stop the build. The scripts do not substitute cached or synthetic historical values.
