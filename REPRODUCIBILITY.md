# Reproducibility

Use Node 22+ and Python 3.11+. Install from the lockfile, run the Python and Node tests, then make the production build. The same seed and inputs return the same Monte Carlo summaries. Browser records can be cleared with “Run again” and never leave the device.

Research pipeline, from the repository root:

```powershell
python calibration/build_frozen_sample.py
python calibration/estimate_parameters.py
python data/vintages/build_packets.py
python research/run_research_suite.py
python -m pytest -q
node --test tests/war-room.test.mjs
pnpm run build
```

The first command retrieves ten official FRED series and rewrites the checksummed frozen sample. The research suite reproduces replay metrics, IRFs, robustness results, tournament, frontier, figures and performance measurements.

ALFRED retrieval is optional for the packaged demonstration. Set `FRED_API_KEY` from `.env.example`, call `data.providers.alfred.observations(series, cutoff)`, then attach release dates and pass records through `information_set`. Never commit keys or downloaded restricted datasets.
