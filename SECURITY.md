# Security

FlowGuard is a local agent workflow, not a security boundary. Review target source in a sanitized checkout; use a read-only mount and denied network for hostile code. Do not upload secrets or private source to issues or reports.

The installer writes only after an explicit `install` command, refuses existing/modified destinations and symlink paths, and edits no host configuration. npm package installation has no lifecycle hooks. Python utilities never run reviewed application code. `fetch` explicitly downloads pinned optional source repositories; it does not install upstream plugins or claim native execution. Agents must still treat their contents as untrusted.

Report possible vulnerabilities through GitHub's private vulnerability reporting when enabled, or request a private contact without including exploit details or secrets in a public issue. Source review and automated scans are not proof of safety. Never present a FlowGuard recommendation as deployment authorization.
