# Dependency inspection — 2026-10-30

Fetched remote default-branch HEADs using git clone --depth 1. No upstream installers executed. SHA-pinned checkouts stay in work/upstream; no upstream content is vendored into the distributable.

| Dependency | Commit | License / entry |
|---|---|---|
| [trailofbits](https://github.com/trailofbits/skills) | `2be6433b39e009cd2b6fd3be1895f6b1faa5af9a` | [CC-BY-SA-4.0](https://github.com/trailofbits/skills/blob/2be6433b39e009cd2b6fd3be1895f6b1faa5af9a/LICENSE); [SKILL.md](https://github.com/trailofbits/skills/blob/2be6433b39e009cd2b6fd3be1895f6b1faa5af9a/plugins/audit-context-building/skills/audit-context-building/SKILL.md) |
| [ecc](https://github.com/affaan-m/ECC) | `b38be6a7f6350964d59328b52f0624e1d1d552d1` | [MIT](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/LICENSE); [SKILL.md](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/skills/production-audit/SKILL.md) |
| [excellence](https://github.com/magnus919/agent-skills) | `bf2d2423043715515df309eea8f7c2565a1eee3b` | [MIT](https://github.com/magnus919/agent-skills/blob/bf2d2423043715515df309eea8f7c2565a1eee3b/LICENSE.md); [SKILL.md](https://github.com/magnus919/agent-skills/blob/bf2d2423043715515df309eea8f7c2565a1eee3b/production-excellence/SKILL.md) |

## Installation and runtime findings

See references/adapters.md for native install commands, Codex execution modes, optional dependencies and safety overrides. Inspection included ToB SKILL, README, workflow and file inventory; ECC SKILL and root LICENSE; Excellence SKILL, AGENTS, manifest, gate and evidence references and root LICENSE.md. Locked markdown/JS/YAML hashes cover supporting resources and sibling skill entries. No proprietary service is required by the three selected entries.

ToB is CC-BY-SA-4.0, not MIT. ECC and Excellence are MIT with author notices. Licensing conclusions describe repository files, not legal certification. Recheck nested third-party licenses before redistributing any full dependency checkout. Native harness compatibility is not implied by successful fetch/doctor.

Excellence gate documentation has a real policy conflict: general Exception requirements exclude owner-only approval while the low-risk applicability table permits self-approval. FlowGuard does not synthesize a waiver; unresolved authority conflicts are Escalation.

## Reproduction

Use the full commits in dependencies.lock.json. fetch clones repositories and detaches these commits, without running checkout hooks, target packages or upstream scripts. New fetches may require network access. doctor is offline. Fetch failure leaves partial cache visible and reports error; it never means dependency availability.

ECC 当前 README 提供完整安装方式 `npx ecc-universal@2.2.3 install --guided`，以及 Codex 的 `--harness codex --dry-run`。FlowGuard 不执行这些命令，避免全局插件、hooks 或不相关能力进入此次审查。Excellence 的 SKILL.md 声明无运行时/API key 依赖；这里使用完整独立仓库保留 sibling skills，无需通用自动安装器。上述为已检查的官方安装说明，未做完整安装端到端验收。

Final lock limits hashes to the selected plugins, referenced optional ECC skills, Excellence specialists and license files (258 resources), while retaining full independent checkouts to preserve relative resources. Git probes have a 15-second timeout and degrade on timeout.
