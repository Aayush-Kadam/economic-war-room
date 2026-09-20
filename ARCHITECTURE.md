# Architecture

The browser application is a Vinext/React TypeScript site. It owns the fast interactive simulation and local Governor's Record. The reference Python engine mirrors the equations for validation and research workflows. Scenario JSON and the data registry are shared audit surfaces.

The ALFRED provider requests one explicit vintage date, attaches provenance and fails closed when the API key is absent. `information_set` validates required metadata before filtering on release date. Raw licensed data are not redistributed.

The current release is deliberately stateless on the server. A later API may expose scenarios, sessions, decisions and results using the same schemas; durable multi-user persistence is not required for the released local experience.
