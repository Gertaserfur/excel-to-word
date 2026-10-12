# Workflow: Mobile SMAPI discovery

**Objective:** Produce a decision-grade discovery report on modding mobile Stardew Valley and the feasibility of a mobile SMAPI.

**Inputs:** none (public web sources: Nexus Mods, GitHub, SMAPI docs/wiki, Reddit, Discord summaries, app stores, ConcernedApe/Chucklefish statements).

**Steps:**
1. Coordinator agent splits the question into independent research tracks (history, tech stack, competitors/projects, market/community, legal & platform policy, feasibility/effort).
2. One research agent per track writes cited notes to `research_notes/<title>/<track>.md`.
3. Report-writer agent synthesizes notes into `reports/<title>.md`.
4. Commit notes + report.

**Edge cases:** mobile modding info is scattered across Discord/Reddit and goes stale fast after game updates — always record game/SMAPI version and date for each claim.
