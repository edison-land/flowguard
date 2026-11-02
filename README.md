# FlowGuard

[简体中文](README.zh-CN.md) · MIT · Claude Code + Codex

Review launch risks in an existing repository, following the actual code and its call relationships. Your coding agent conducts the investigation; FlowGuard provides the workflow, optional dependency adapters, evidence validation and source snapshots. **It is not an autonomous vulnerability scanner or a safety certification.**

## Install

Requires Node.js 18+ for the installer. Reviews use Python 3.9+, Git and your own skill-capable coding agent. There are no npm runtime dependencies, install hooks, telemetry or required service API keys. Your agent/model usage may have its own cost.

Install the versioned GitHub source now:

```sh
npx --package=github:edison-land/flowguard#v0.1.0 flowguard install --agent both
```

Or install the CLI persistently:

```sh
npm install -g github:edison-land/flowguard#v0.1.0
flowguard install --agent both
```

`npm install` installs the CLI; the explicit `flowguard install` command copies the skill into the selected host directories. **It never silently installs skills as a package lifecycle hook.**

| Host | User installation | Project installation |
|---|---|---|
| Codex | `~/.agents/skills/flowguard` | `<project>/.agents/skills/flowguard` |
| Claude Code | `~/.claude/skills/flowguard` | `<project>/.claude/skills/flowguard` |

```sh
flowguard install --agent codex --dry-run
flowguard install --agent claude
flowguard install --agent both --project /absolute/path/to/project
```

The installer refuses symlink paths and existing/modified installations. Identical installations made by the same version are left unchanged. To upgrade, first move the previous skill directory to a separate backup location, then install. A failure during copying may leave a partial destination for you to inspect; it is not overwritten on retry. No unrelated configuration is edited.

After installing, start a new host session if the skill is not visible. In Codex invoke `$flowguard`; in Claude Code invoke `/flowguard`. Local Claude Code installation does not install into claude.ai or Cowork cloud sessions.

### npm registry distribution

The package is prepared as `edison-flowguard`. **Registry publishing is pending maintainer authentication; use the GitHub commands above until it is published.** Once version 0.1.0 exists on npm:

```sh
npm install -g edison-flowguard@0.1.0
flowguard install --agent both
# or: npx --package=edison-flowguard@0.1.0 flowguard install --agent both
```

## Run a review

In your coding agent, use:

> Use $flowguard to review /absolute/path/to/repository for launch risks. First understand the implemented features and call relationships, then choose the investigation directions. Default to read-only: do not modify code, run project scripts, or access production. Save the report and review.json outside the repository. Record missing dependencies, hypotheses and unexamined scope.

For Claude Code use `/flowguard` instead of `$flowguard`. An installed skill is required: merely mentioning its name in an unrelated chat does not prove it loaded. The helper does not produce the investigation by itself.

No default stack, feature list or fixed investigation route is assumed. Findings record triggers, effects, source lines, full-file hashes, counterevidence, confidence and verification boundaries. Decisions remain advisory. Missing owners, deployment evidence or tests stay unknown.

For the utility commands below, use the persistent CLI installation above, or replace `flowguard` with `npx --package=github:edison-land/flowguard#v0.1.0 flowguard`.

## Optional upstream sources

FlowGuard works without them and records reduced coverage. To obtain pinned sources explicitly, **before** reviewing a target:

```sh
flowguard fetch /absolute/path/outside-target/flowguard-deps
flowguard doctor /absolute/path/outside-target/flowguard-deps
```

`fetch` downloads three full Git repositories. It runs no upstream installers or scripts. `doctor` is offline and verifies pins/hashes; `available` means source availability, **not native host execution**. The audit never silently fetches dependencies. In the review prompt provide the cache path. For instruction-only/manual installation, use `python3 /path/to/flowguard/scripts/flowguard.py` in place of the CLI. `FLOWGUARD_PYTHON` selects a different Python executable.

Sources and licenses are in [DEPENDENCIES.md](DEPENDENCIES.md), [the lock](dependencies.lock.json) and [adapters](references/adapters.md). ToB native Workflow/Task capabilities are not assumed; the documented fallback is independent analysis. ECC/Excellence may be instruction-guided, not a claim of full native plugin execution.

## Evidence utilities

Use a sanitized target checkout and an output directory outside it. Do not snapshot secret-bearing working trees.

```sh
flowguard snapshot /absolute/path/to/target > /external/output/before.json
flowguard validate /external/output/review.json /absolute/path/to/target
flowguard snapshot /absolute/path/to/target > /external/output/after.json
```

Compare the snapshots to detect final content changes. The [evidence contract](references/evidence.md) explains the version-1 review structure. Validation checks structure, citations and minimum decision constraints; it does not prove semantic correctness or runtime safety. It requires a Git target with a matching commit. Arbitrary JSON reports are not automatically compatible.

Read-only is an **agent instruction boundary, not OS isolation**. Snapshots hash regular files, including hidden files, record symlinks and reject special files. They exclude `.git` internals and cannot detect transient writes, network activity or empty-directory changes. For hostile repositories use an operator-provided read-only mount and denied network access.

## Validation and limitations

See [TEST-RESULTS.md](https://github.com/edison-land/flowguard/blob/v0.1.0/TEST-RESULTS.md) and [release checks](docs/release-validation.md). The original [single-repository trial](https://github.com/edison-land/flowguard/blob/v0.1.0/examples/comparison.md) is exploratory, sequential and not an efficacy benchmark. It does not establish recall, false-positive rate or superiority over other skills. The separate FlareMo report in the maintainer's chat was a fallback review, not a FlowGuard end-to-end test.

Development checks:

```sh
npm test
python3 -B -m unittest discover -s tests -v
npm pack --dry-run --ignore-scripts
```

[Publishing](docs/publishing.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

Original FlowGuard code and instructions are MIT. No upstream source is bundled; upstream license terms remain independent. [OpenAI skill locations](https://developers.openai.com/codex/skills#where-to-save-skills), [Claude Code skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load), [npm exec](https://docs.npmjs.com/cli/v11/commands/npm-exec/) describe the installation mechanisms. OpenAI also supports plugin distribution; this release supplies a standalone local skill and CLI.
