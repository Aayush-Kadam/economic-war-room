# Project charter

## Purpose and audience

Economic War Room teaches monetary policy as sequential choice under incomplete information, uncertain lags and competing objectives. It is intended for students, researchers, policymakers, technical reviewers and recruiters who want an inspectable model rather than an arcade score.

## User loop

At each dated meeting the user receives only released information, reviews a staff brief, chooses a rate and communication stance, records a memo, locks the choice, then sees the historical action. Lagged choices propagate to the next decision. Completion yields a chronological Governor's Record and separated observed/modelled paths.

## Scientific positioning

The system is a calibrated semi-structural counterfactual laboratory. Simulations are conditional on equations, calibration and shock distributions. They are not observed history, forecasts, proof of causality or rankings of named policymakers.

## Historical realism rule

Normal play admits an observation only when `release_date <= decision_cutoff`. Revised values require a matching vintage. Any post-cutoff record is a failing test. Hindsight mode, when added, must be visibly separate.

## Non-goals and constraints

The project does not predict markets, provide investment advice, infer exact counterfactual history, hide model uncertainty or use an LLM for numerical output. Player memos stay on-device. Country extensions require country-specific mechanisms and evidence.
