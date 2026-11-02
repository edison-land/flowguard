# FlowGuard

[English](README.md) · MIT · 支持 Claude Code 与 Codex

对已有仓库做上线风险审查。先理解真实功能与调用关系，再按证据选择调查方向。调查由你的 coding agent 完成；FlowGuard 提供工作流、可选依赖适配、证据校验与前后快照。**它不是自动漏洞扫描器，也不能证明项目安全。**

## 安装

安装器需要 Node.js 18+；审查辅助工具需要 Python 3.9+、Git 和支持 Skill 的 coding agent。npm 包没有运行时第三方依赖、安装钩子或遥测，也不要求额外 API Key。你的模型或 Agent 服务可能收费。

先从公开 GitHub 的固定版本安装：

```sh
npx --package=github:edison-land/flowguard#v0.1.0 flowguard install --agent both
```

或者保留命令行工具：

```sh
npm install -g github:edison-land/flowguard#v0.1.0
flowguard install --agent both
```

`npm install` 下载 CLI；第二条显式命令才把 skill 放到 Agent 识别目录，不在包安装时偷偷改配置。

| Agent | 用户级目录 | 项目级目录 |
|---|---|---|
| Codex | `~/.agents/skills/flowguard` | `<项目>/.agents/skills/flowguard` |
| Claude Code | `~/.claude/skills/flowguard` | `<项目>/.claude/skills/flowguard` |

```sh
flowguard install --agent codex --dry-run
flowguard install --agent claude
flowguard install --agent both --project /项目绝对路径
```

相同版本、内容未改的安装可重复执行。其他已有目录、被修改的安装、符号链接路径会被拒绝，不会覆盖你的内容。升级前先将旧 skill 目录移到独立备份位置再安装；中途失败可能留下供检查的部分目录，重试不会覆盖它。不会改动其他 Agent 配置。

安装后若看不到 skill，请开启新会话。Codex 使用 `$flowguard`，Claude Code 使用 `/flowguard`。本地安装不代表已经装进 claude.ai 或 Cowork 云会话。

### npm 官方仓库

包名准备为 `edison-flowguard`。**维护者尚未完成 npm 登录发布；发布前使用上面的 GitHub 安装方式。** npm 上出现 0.1.0 后可用：

```sh
npm install -g edison-flowguard@0.1.0
flowguard install --agent both
# 或：npx --package=edison-flowguard@0.1.0 flowguard install --agent both
```

## 使用

在支持 Skill 的 coding agent 新会话中输入（Claude Code 把 `$flowguard` 改为 `/flowguard`）：

> 使用 $flowguard 审查 /项目绝对路径 的上线风险。先根据实际代码理解功能和调用关系，再动态决定调查方向，不预设项目具备哪些功能。默认只读，不修改代码，不运行项目脚本，不访问生产服务。将中文报告和 review.json 保存到项目仓库外，区分阻断问题、待验证假设与未检查范围，并给出修复优先级和下一步验证方式。

仅在聊天里提到名称，不代表 Skill 已成功加载。辅助脚本不能独立生成审查结论。负责人、日期、完成测试等未知项如实保留，不编造上线批准。

下文工具命令需先全局安装 CLI；若只做了单次 npx 安装，可将 `flowguard` 替换为 `npx --package=github:edison-land/flowguard#v0.1.0 flowguard`。

## 可选上游依赖

无依赖也能审查，但会明确记录降级。确需增强时，在审查前显式下载，并把缓存路径告诉 Agent：

```sh
flowguard fetch /仓库外绝对路径/flowguard-deps
flowguard doctor /仓库外绝对路径/flowguard-deps
```

`fetch` 下载三个完整 Git 仓库，不运行上游安装器或脚本。`doctor` 离线校验固定 commit 和哈希；源码可用不代表原生工作流可执行。审查过程不自动下载依赖。手动安装不使用 CLI 时，可将 `flowguard` 替换为 `python3 /skill路径/scripts/flowguard.py`；`FLOWGUARD_PYTHON` 可指定 Python 可执行文件。

依赖版本、授权和适配限制见 [DEPENDENCIES.md](DEPENDENCIES.md)、[锁文件](dependencies.lock.json)、[适配说明](references/adapters.md)。ToB 原生 Workflow/Task 不可用时明确 fallback；ECC 与 Excellence 的指令辅助模式不冒充完整原生运行。上游源码不打包进本项目。

## 输出与边界

[证据格式](references/evidence.md)约定 `review.json` 的版本 1 结构：目标、适配器、调查问题轨迹、覆盖范围、缺口、发现与建议结论。证据包含行号、整文件哈希、触发条件、影响、反证、置信度和验证边界。不要把任意 JSON 报告直接当作符合该格式。

```sh
flowguard snapshot /项目绝对路径 > /仓库外/before.json
flowguard validate /仓库外/review.json /项目绝对路径
flowguard snapshot /项目绝对路径 > /仓库外/after.json
```

目标需有 Git commit。快照对普通文件计算哈希、记录符号链接并拒绝特殊文件；包含隐藏文件，因此只对已脱敏、不含密钥的源码副本运行。快照不记录 `.git` 内部，不证明没有短暂写入或网络活动，也不覆盖空目录变化。只读是 Agent 行为约束，不是系统隔离；不可信项目需要操作者提供只读挂载与断网环境。

## 验证与贡献

[原型测试记录](https://github.com/edison-land/flowguard/blob/v0.1.0/TEST-RESULTS.md)、[首版发布检查](docs/release-validation.md)、[单仓库试用对比](https://github.com/edison-land/flowguard/blob/v0.1.0/examples/comparison.md)。试用是单样本顺序实验，不能证明召回率、误报率或普遍优势。维护者聊天中另做的 FlareMo 报告是降级审查，不能算这份 Skill 的完整试运行。

```sh
npm test
python3 -B -m unittest discover -s tests -v
npm pack --dry-run --ignore-scripts
```

[发布流程](docs/publishing.md) · [安全说明](SECURITY.md) · [贡献方式](CONTRIBUTING.md)

原创文件 MIT；上游依赖保留各自许可。安装目录依据 [OpenAI 文档](https://developers.openai.com/codex/skills#where-to-save-skills)与 [Claude Code 文档](https://code.claude.com/docs/en/skills#choose-where-skills-load)。本版交付本地 Skill 与 CLI，没有宣称已发布为 OpenAI/Claude 插件市场产品。
