# Mobile SMAPI project — agent instructions (WAT)

This repo follows the **WAT** model: **W**orkflows, **A**gents, **T**ools.

- `workflows/` — plain-language SOPs (Markdown). Each says the objective, inputs, which tools to use, outputs, and edge cases. Read the relevant workflow before acting.
- **Agents** — Claude (and its subagents) read workflows, make decisions, and call tools. Agents coordinate; they don't hand-roll logic that belongs in a tool.
- `tools/` — deterministic scripts that do the actual work (scraping, decompiling, checks). Prefer reusing an existing tool over writing a new one; when a tool fails, fix it and update the workflow with what you learned.

Outputs:
- `research_notes/<title>/` — raw, cited notes from research agents.
- `reports/` — synthesized deliverables.

Goal of the project: determine whether (and how) we can build a SMAPI-equivalent mod loader for the mobile (Android/iOS) version of Stardew Valley.
