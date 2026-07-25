# done-means-done

**Your AI coding agent says "done." This skill makes it prove it.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-agent%20skill-orange)](https://code.claude.com/docs/en/skills)
[![Plain Markdown](https://img.shields.io/badge/format-plain%20Markdown-blue)](done-means-done/SKILL.md)

An [agent skill](https://code.claude.com/docs/en/skills) for [Claude Code](https://claude.com/claude-code) that closes the execution-discipline gap in AI coding agents. No more "I fixed it" without a test that actually ran. No more stopping to ask you about a variable name. No more surprise refactor bundled into a two-line bug fix.

## The problem

You hand a task to an AI agent and get one of these back:

- **"All tests pass."** No test was ever run. The claim came from reading the code.
- **"Done!"** followed by *"Next, I could also…"* — the turn ended on a promise, not a result.
- **"Which naming convention would you prefer?"** …for a private helper nobody will ever see.
- A three-line bug fix that arrives wrapped in two hundred lines of cleanup you never asked for.

None of this is a capability problem. Every current model can run its own tests, reach for a search tool, and name a variable unaided. They just won't unless told. **This skill is that telling.**

## Install

Claude Code, user-wide:

```sh
git clone https://github.com/unclecatvn/done-means-done.git
cp -r done-means-done/done-means-done ~/.claude/skills/
```

It triggers by itself on multi-step action tasks — build, fix, analyze, convert, merge. To force it in a session, type `/done-means-done`.

**Want it on for everything?** Skills only load when the task matches their description, and small one-step tasks often match nothing. For full coverage, add one line to your project's `CLAUDE.md`:

```
For every action task, follow the done-means-done skill.
```

**Not using Claude Code?** [`SKILL.md`](done-means-done/SKILL.md) is plain Markdown with no tool-specific syntax. Paste the body into any agent's system prompt — Cursor rules, Codex `AGENTS.md`, a custom harness — and it works the same.

## What it enforces

| # | Rule | In one line |
|---|------|-------------|
| 1 | **Classify intent** | A described problem gets an assessment, not an unrequested fix. Assigned work gets carried to completion. |
| 2 | **Look it up first** | Read the file before editing it. Anything a tool can answer isn't a question for you. |
| 3 | **Calibrated autonomy** | Small calls get made and noted. Only destructive or scope-changing actions stop and ask. |
| 4 | **No check run, not done** | Non-trivial logic leaves one runnable piece of evidence, executed before "done" is said. |
| 5 | **Evidence-grounded reports** | Every claim traced to a real tool result. Failures stated plainly, with the output. |
| 6 | **Stay in scope** | Do the job assigned. No drive-by refactors. |

## Does it actually work?

Benchmarked with the [skill-creator](https://github.com/anthropics/skills) eval loop on Claude Opus 4.8, 3 tasks × with/without the skill, graded by an independent grader against 12 objective assertions:

| Metric | With skill | Without | Delta |
|---|---|---|---|
| Assertion pass rate | **92%** (11/12) | 75% (9/12) | **+17 pts** |
| Time per task | 215s | 130s | +85s |
| Tokens per task | ~35.4k | ~32.0k | +10% |

The entire edge came from verification. The with-skill runs left runnable test artifacts and before/after evidence behind. The baseline runs *claimed* verification in prose but preserved nothing anyone could re-run.

**Read that table honestly:** 1 iteration, 1 run per config. It is directional, not a proof. The eval set is in this repo precisely so you can re-run it and disagree — see below.

## Design principle

Every rule is written as **goal + constraint + reason**, never as a bare `MUST` or `ALWAYS`. That matters when one skill has to run across model tiers:

- Models with weaker discipline comply with the stated rule.
- Stronger models generalize from the *reason* instead of being boxed in — Anthropic's own migration guidance notes that over-prescriptive prompts **reduce** output quality on frontier models.

If you fork this, keep that style. Explain the why; don't stack imperatives.

## Evals

[`done-means-done/evals/evals.json`](done-means-done/evals/evals.json) holds the three benchmark tasks with 12 graded expectations:

1. **A build task** — merge three revenue CSVs, sorted, with a computed column. Tests: does it decide the small things itself and leave a self-check that runs?
2. **A bug fix** — a seeded return-order bug in [`inventory.py`](done-means-done/evals/files/inventory.py). Tests: read-before-edit, fail-before/pass-after evidence, and no refactoring of the untouched functions sitting right next to it.
3. **A question, not a request** — *"why is the orders API so slow?"* Tests: does it deliver an assessment and stop, or does it start editing files nobody asked it to edit?

Run them through skill-creator's eval loop to benchmark any change before you adopt it.

## Contributing

Issues and PRs welcome — especially eval results that contradict the table above. If you have a failure mode this skill doesn't catch, open an issue with the transcript.

## License

MIT
