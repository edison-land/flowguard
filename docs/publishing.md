# Publishing

## GitHub

The source repository is `edison-land/flowguard`. Version 0.1.0 is an initial experimental release, not a security certification. Keep original license and dependency attribution. Review the staged file list before pushing and tag the tested commit `v0.1.0`.

## npm

Prepared name: `edison-flowguard`. Name availability is only a point-in-time check, not a reservation. Publishing requires an npm account authorized to publish that name; GitHub authentication does not authenticate npm.

Run from the repository:

```sh
npm test
python3 -B -m unittest discover -s tests -v
npm pack --dry-run --ignore-scripts
npm publish --dry-run --ignore-scripts
npm login --registry=https://registry.npmjs.org/
npm publish --access public --ignore-scripts
```

Complete browser/2FA authorization locally; never put registry tokens or one-time passwords in source or chat. After a successful publish, verify `npm view edison-flowguard@0.1.0 version`, test the published tarball in a temporary prefix, and replace both READMEs' pending-registry notice with the verified registry install instructions. No automatic publishing workflow is configured.

The npm `files` allowlist includes only CLI, skill instructions, metadata, references, helper, dependency lock and license/documentation. The tarball excludes tests, historical trial outputs, caches and upstream checkouts. There are no lifecycle install hooks and no runtime npm dependencies.
