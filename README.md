# rigorous-execution

A [Claude Code agent skill](https://code.claude.com/docs/en/skills) that closes the execution-discipline gap between top-tier models and everything below them.

## Why this exists

There is a measurable behavioral gap between Anthropic's top-tier model (Claude Fable 5) and other models (Claude Opus 4.8 and below). The top tier naturally does four things the others tend to skip:

1. **Verifies its own work** before reporting done — leaves a runnable check and runs it.
2. **Reaches for powerful tools** (search, parallel subagents, memory) when depth is needed, instead of hesitating.
3. **Decides small things itself** instead of stopping to ask, while still asking for destructive or scope-changing actions.
4. **Reports only what it has evidence for** — grounded in actual tool results, failures stated plainly.

The other models are fully *capable* of all four and follow instructions very well — they just won't do these things unless told. This skill is that telling.

## Design principle

Every rule in the skill is written as **goal + constraint + reason**, never as a bare `MUST`/`ALWAYS`. This matters for running one skill across model tiers:

- Weaker-discipline models comply with the rule.
- Stronger models generalize from the reason instead of being over-constrained — Anthropic's own migration guidance notes that over-prescriptive prompts *reduce* output quality on Fable 5.

If you fork this skill, keep that style: explain the why, don't stack imperatives.

## What's inside

`rigorous-execution/SKILL.md` — six sections:

| # | Section | One-liner |
|---|---------|-----------|
| 1 | Classify intent | Problem descriptions get an assessment, not an unrequested fix; assigned work gets carried to completion |
| 2 | Context | Read before editing; look it up with tools before asking; explicit thresholds for search / subagents / memory |
| 3 | Autonomy | Decide small things and note the choice; ask only for destructive or scope-changing actions; end-of-turn gate against unfinished promises |
| 4 | Verification | Non-trivial logic leaves one runnable piece of evidence, executed before declaring done |
| 5 | Reporting | Every claim checked against a tool result; outcome first; the final message stands alone |
| 6 | Scope | Do the job that was assigned — no drive-by refactors |

## Measured effect

Benchmarked with the [skill-creator](https://github.com/anthropics/skills) eval loop on **Claude Opus 4.8** (the tier the skill targets), 3 tasks × with/without skill, graded against objective assertions:

| Metric | With skill | Without skill | Delta |
|---|---|---|---|
| Assertion pass rate | 92% (11/12) | 75% (9/12) | **+17 pts** |
| Time per task | 215s | 130s | +85s |
| Tokens per task | ~35.4k | ~32.0k | +10% |

The entire edge came from verification discipline: the with-skill runs left runnable test artifacts and before/after evidence; the baseline runs claimed verification in prose but preserved nothing that could be re-run. Small sample (1 iteration, 1 run per config) — treat as directional.

## Install

**Claude Code** — copy the skill folder into your user skills directory:

```sh
git clone https://github.com/unclecatvn/rigorous-execution-skill.git
cp -r rigorous-execution-skill/rigorous-execution ~/.claude/skills/
```

The skill triggers automatically on multi-step action tasks (build, fix, analyze, convert…). To force it in a session: `/rigorous-execution`.

**Always-on**: skills only load when the task matches the description, and simple one-step tasks often don't trigger any skill. For 100% coverage, add one line to your project's `CLAUDE.md`:

```
For every action task, follow the rigorous-execution skill.
```

## Evals

`rigorous-execution/evals/evals.json` holds three test prompts with expected behavior (a CSV-merge build task, a seeded inventory bug fix, and a "why is this slow?" question that must produce an assessment *without* an unrequested fix). Run them through skill-creator's eval loop to benchmark changes before adopting them.

## License

MIT
