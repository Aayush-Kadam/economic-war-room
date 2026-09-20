# Scenario schema

Each JSON scenario defines: stable `id`; country and central bank; historical or synthetic mode; date range and ordered decision dates; information cutoff for every meeting; allowed instruments and basis-point options; initial state; shock process/timeline; source-series IDs; mandate weights; Monte Carlo path count and seed; and mandatory counterfactual disclaimer.

Historical action records are immutable and stored separately from player decisions. A player record contains scenario ID, seed, date, cutoff/vintage, starting state, action, communication, memo, simulation digest and reveal status. Engines consume the common schema; optional country extensions add FX, reserves, fiscal dominance or lower-bound tools without forcing them into every scenario.
