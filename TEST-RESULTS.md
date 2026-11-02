# 实际验证记录 — 2026-10-30

- `python3 -m unittest discover -s tests -v`：13/13 通过；原始输出见 examples/unit-tests.log。
- skill-creator `quick_validate.py`：Skill is valid。系统 Python 缺 PyYAML，使用工作区独立 venv 安装 PyYAML==6.0.3 后验证；FlowGuard 运行本身仅依赖标准库。
- doctor：三项已获取的依赖 commit 与锁定资源哈希校验通过。available 表示源码可用，runtime 明确 not-probed。
- `validate examples/review.json TARGET`：VALID；Python 优化模式 `-O` 同样 VALID，关键约束不依赖可禁用的 assert。
- 真实仓库前后 39 文件快照一致，Git status 干净；见 examples/snapshot-check.json 和 combined-before/after.json。未执行目标包安装、构建、测试、OAuth、支付、数据库或线上操作。
- 缺失依赖、路径越界、证据哈希变化、错误行号、符号链接、未知负责人/高风险 Go、缺少 waiver、嵌套记录不完整均有拒绝/降级测试。

## 复现

在 FlowGuard 文件夹内运行标准库测试。重新获取目标到仓库外部（仅下载，不运行其内容）：

```sh
git clone https://github.com/dcccrypto/ai-saas-starter.git /external/cache/flowguard-trial-target
git -C /external/cache/flowguard-trial-target checkout --detach af3d199c848a405ac221524d09e12b3adcaa0968
python3 scripts/flowguard.py validate examples/review.json /external/cache/flowguard-trial-target
```

上游依赖复现：`python3 scripts/flowguard.py fetch /external/cache/flowguard-deps`，再运行 doctor。脚本会获取锁定 commit，已有目录不覆盖；已有错误缓存须由操作者选择新目录或修复。依赖源代码/资源通过校验不代表宿主原生能力已验证。仓库原始 installers 已检查文档但未执行，fetch 不安装插件或 hooks。

## 仍需验证

ToB 原生宿主的实际 Workflow/Task 执行；全新 Codex 会话全局安装/触发；三个官方完整安装器；更多仓库、等预算盲测；身份/SDK 假设的离线替身与隔离集成；恢复/成本/容量证据。fetch 全量远程下载路径采用 git 标准流程，本次使用直接 clone 取得同样锁定 checkout 做 doctor 验证，未再重复下载全部仓库验证 fetch 命令。只读边界是指令约束，非系统级防写或断网保证。

最后重复校验出现本机 Git 探测超时：最初三项都已验证成功（combined-doctor.json），最后 dependency-check.json 中 Excellence 被安全降级为 unavailable，而非继续假设可用。已为 Git 探测加 15 秒超时，避免审查卡死；后续重新校验记录单独保留。该超时不影响已经保存的源码审查结果，但再次使用前需重跑 doctor。
