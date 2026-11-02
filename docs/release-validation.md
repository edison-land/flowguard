# 0.1.0 发布检查（2026-10-30）

## 已执行

- Node 安装器测试：8/8 通过。用户级目录映射、双端完整安装、dry-run 无写入、重复安装不变、已有/修改目录拒绝、符号链接拒绝、npm 风格命令软链、错误参数均覆盖。文件写入只在临时目录。
- Python 工具测试：15/15 通过，包含新增的无效快照目标与特殊文件拒绝；无审查目标代码被执行。
- skill-creator quick_validate：通过。默认 Python 缺 PyYAML，改用原型已有的独立验证环境完成校验；运行时仍只需 Python 标准库。
- npm 包 allowlist 已检查，包含完整 Skill/lock/refs/helper/元数据/CLI 与文档；不含上游源码、试用报告、测试、缓存或 Python 字节码。
- 将实际生成的 npm tarball 安装到临时 prefix，命令软链可执行，双端项目级安装成功；doctor 对空缓存正确标记三项依赖缺失。没有写入本机真实 Agent skill 目录。
- 从公开 GitHub 的 `v0.1.0` 通过 `npm exec --package=github:edison-land/flowguard#v0.1.0` 下载并运行安装器，在临时项目中生成两端完整 Skill 目录，退出码 0。
- npm publish dry-run 仅检查打包，不上传。实际 npm registry 发布尚未完成，当前认证缺失。
- 对准备公开的文本检索本地绝对路径与常见密钥模式，未发现应带出的本机用户路径或凭据。此项不是完整历史秘密扫描。

## 人工安全复核

使用 audit-skill-safety 的只读扫描及人工复核。扫描初始结果为 BLOCK；规则把以下否定/引用误识别为高危：禁止静默跟随 latest、不能静默选择冲突规则、安装目录文档，以及依赖锁中的 AGENTS.md 路径。它们不是实际绕过指令。

人工检查了脚本子进程参数、网络与写入边界：审查工具仅有显式 fetch 的 Git 下载，禁用 checkout hooks；npm 安装无 lifecycle hooks；安装目录由显式命令选择、拒绝覆盖与符号链接。不读取凭据、不上传项目源码，不运行上游或被审查项目的代码。

人工结论：ALLOW_WITH_GUARDRAILS，适合以实验版发布。必须保留只读默认、独立缓存、缺失能力降级和不可信目标的操作系统隔离要求。包的安装测试属于已授权的包开发验证，与对目标应用的默认只读审查分开。

## 未验证

- 新 Claude Code/Codex 会话的真实发现和模型审查质量；目录符合当前官方文档，但实际触发不能由文件复制测试替代。
- Windows/Linux 的端到端安装，ToB 原生运行，完整 fetch 网络路径，所有上游原生宿主。
- 当前新打包版本在多个真实仓库上的等预算独立盲测、召回率与误报率。
- npm registry 的最终发布与发布后下载校验。

原型已有的单仓库记录保留在 examples/ 与 TEST-RESULTS.md，其范围和局限保持原文。FlareMo 降级报告没有被加入 examples，也不作为本 Skill 完整执行的证据。
