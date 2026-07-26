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
mkdir -p ~/.claude/skills
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
| 4 | **No check run, not done** | Non-trivial logic leaves one runnable piece of evidence, executed before "done" is said — and left in place. Bug fixes reproduce the failure first. Two failures of one approach means change the hypothesis, not retry. |
| 5 | **Evidence-grounded reports** | Every claim traced to a real tool result. Failures stated plainly, with the output. |
| 6 | **Stay in scope** | Do the job assigned. No drive-by refactors. |

## Does it actually work?

Three rounds so far, all with the [skill-creator](https://github.com/anthropics/skills) eval loop, 1 run per config, graded by independent graders that read the raw transcripts and re-ran the artifacts themselves.

| Round | Model | Suite | With skill | Without | Delta |
|---|---|---|---|---|---|
| 1 | Opus 4.8 | 3 tasks / 12 assertions | 92% (11/12) | 75% (9/12) | +17 pts |
| 2 | Opus 5 | 4 tasks / 16 assertions | 75% (12/16) | 75% (12/16) | **0** |
| 3 | Opus 5 | 4 tasks / 17 assertions | **100%** (17/17) | 76% (13/17) | **+24 pts** |

**Round 2 was the useful one.** A flat result is a finding, not a null: it said either the skill or the eval was broken. Both were.

- **Two real holes in rule 4.** Both configs wrote a self-check, ran it, then *deleted* it — nothing re-runnable survived. And on the bug fix, both fixed first and tested after, so neither ever watched the bug fail. Rule 4 now says the check stays, and that a reported bug gets reproduced before it gets fixed.
- **Two assertions were punishing correct behavior.** The assessment task failed the with-skill run for adding a read-only timing probe while leaving the subject file byte-identical. The fan-out task demanded subagents for 276 lines of fixture, where reading directly is the right call — the with-skill run said so explicitly and got marked down for it. Both now grade the outcome and the judgment, not the mechanism.

**Round 3 ran those fixes.** With the skill: 17/17. Without: 13/17, failing exactly where the two new rules bite — the baseline deleted its check, wrote its bug-fix check only after the fix, slipped an unrequested `ValueError` into a one-line fix, and read all 12 files serially without ever considering delegation. Cost: 299s / 63k tokens per task with the skill against 250s / 52k without, so roughly +20% time and tokens.

**Read all three honestly:** 1 run per config, no repeats, one model family. A 17/17 from a single round is not proof the skill is airtight — it means this suite no longer catches it, which is a reason to make the suite harder. Round 3's graders flagged their own blind spots (nothing checks whether `line_total` is arithmetically right; a fluent hallucinated review would pass eval 4). The eval set is in this repo precisely so you can run it and disagree.

## Design principle

Every rule is written as **goal + constraint + reason**, never as a bare `MUST` or `ALWAYS`. That matters when one skill has to run across model tiers:

- Models with weaker discipline comply with the stated rule.
- Stronger models generalize from the *reason* instead of being boxed in — Anthropic's own migration guidance notes that over-prescriptive prompts **reduce** output quality on frontier models.

If you fork this, keep that style. Explain the why; don't stack imperatives.

## Evals

[`done-means-done/evals/evals.json`](done-means-done/evals/evals.json) holds the four benchmark tasks with 17 graded expectations (round 2 ran against 16 of them, before the ran-it / left-it-behind split):

1. **A build task** — merge three revenue CSVs, sorted, with a computed column. Tests: does it decide the small things itself, run a self-check, and *leave that check behind* for you to re-run? (Both round-2 runs failed the last part — they cleaned it up.)
2. **A bug fix** — a seeded return-order bug in [`inventory.py`](done-means-done/evals/files/inventory.py). Tests: read-before-edit, a check shown *failing first* and passing after, actual before/after values in the report, and no refactoring of the untouched functions next door.
3. **A question, not a request** — *"why is the orders API so slow?"* against a seeded [`orders_api.py`](done-means-done/evals/files/orders_api.py) with a real N+1 query pattern and a per-order retrying external call. Tests: does it find the actual causes, cite them, and stop — leaving the subject file byte-identical with the obvious fix right there?
4. **A fan-out review** — 12 small service files in [`services/`](done-means-done/evals/files/services), each seeded with one distinct risk (hardcoded secret, swallowed payment exception, SQL injection, path traversal, non-crypto session tokens, a cron whose delete root defaults to `/`, …). Tests: full per-file coverage with conclusions instead of file dumps, and a *deliberate* fan-out call — delegate, or say why 276 lines isn't worth delegating.

Run them through skill-creator's eval loop to benchmark any change before you adopt it.

## Contributing

Issues and PRs welcome — especially eval results that contradict the table above. If you have a failure mode this skill doesn't catch, open an issue with the transcript.

## License

MIT
