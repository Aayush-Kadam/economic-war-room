# Reproducibility

Use Node 22+ and Python 3.11+. Install from the lockfile, run the Python and Node tests, then make the production build. The same seed and inputs return the same Monte Carlo summaries. Browser records can be cleared with “Run again” and never leave the device.

ALFRED retrieval is optional for the packaged demonstration. Set `FRED_API_KEY` from `.env.example`, call `data.providers.alfred.observations(series, cutoff)`, then attach release dates and pass records through `information_set`. Never commit keys or downloaded restricted datasets.
