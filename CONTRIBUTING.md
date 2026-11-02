# Contributing

Keep investigation evidence-led and stack-independent. Distinguish source observations, untested runtime effects and executed reproductions. Preserve read-only defaults and host compatibility. Add no telemetry, automatic dependency downloads or install hooks.

For code changes run `npm test` and `python3 -B -m unittest discover -s tests -v`. Check the npm tarball with `npm pack --dry-run --ignore-scripts`; do not include caches, bytecode, secrets, upstream source or private target reports. New installer tests must use temporary destinations, never a contributor's actual agent directories. Document what was executed and what remains unverified.

Dependency updates require an explicit pin/hash/license review. Do not add upstream skill text to the MIT package without resolving its own license obligations. Send focused pull requests with a concrete before/after case and validation results.
