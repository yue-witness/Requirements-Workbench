# Requirements Analysis Workbench

简体中文 | [English](README.md)

Requirements Analysis Workbench 是一个适用于 ChatGPT 和 Codex 的插件，可将软件构想、问题陈述、用户故事、会议记录或需求草稿整理为可选择、可追踪、便于评审的需求工件。插件包含三个技能、确定性 Python 工具和 MCP Apps 可视化配置面板。

插件既为初次参与需求分析的用户提供通俗引导，也为专业分析人员保留证据、置信度、验收条件、可追踪关系和变更范围控制。它是领域无关的通用插件，项目专属约束由项目数据提供。

## 可生成的内容

用户可以选择一个或多个彼此独立的模块：

- `requirements`：原子化的功能、质量和业务需求；
- `fishbone`：问题背后的潜在原因；
- `context`：系统边界、参与者、外部系统和信息流；
- `use-cases`：参与者目标、主流程、备选流程和异常流程；
- `activity`：工作流决策、失败路径和结果；
- `wireframe`：带追踪标签、可访问的低保真 HTML 界面。

每次运行还会生成作为单一事实来源的 `analysis.json`、面向评审者的 `review-index.md`、`traceability.csv`、`traceguard.md`、`traceguard.json` 和带 SHA-256 文件哈希的 `manifest.json`。

## 核心特性

- 当用户通过 `@` 直接调用插件并提供匹配的需求描述时，默认打开可视化工作台，让用户确认评审模式和输出模块。仅打开面板不会接受界面中显示的默认值；用户应用有效选择前，工作流保持阻塞。只有在已提供模式和至少一个模块时，用户才可明确要求不打开 GUI；不支持 MCP Apps 的宿主则在对话中提供同样具有等待门禁的选项。
- 可视化的引导、标准和专业三种模式选择器。
- 六个输出模块分别提供独立勾选框。
- 明确区分利益相关者证据、推断、假设、建议、冲突和待确认问题。
- 使用稳定 ID 和追踪链接连接不同工件。
- 在生成文件前执行确定性结构验证。
- 可只修订一个目标模块，并使用哈希逐字节确认其他模块未被改写。
- TraceGuard 检查精确来源片段、参与者与上下文、活动与线框图追踪、术语一致性，并输出机器可读结果。
- 共享变更先生成影响预览，由评审者选择传播、本地覆盖或取消。
- 定向修订保留回滚快照；配置为高影响的事项在具名审批前保持 abstain 状态。
- 确定性生成器和本地 MCP Server 均不需要 API Key 或第三方 Python 包。

例如，`project.minimum_requirements` 是可选字段，默认不设置数量门槛；通用插件不会强制任何组织或行业范围的最低数量要求。

## 从 GitHub 安装

请使用支持插件的当前版 ChatGPT 桌面应用或 Codex。先将本仓库添加为 marketplace 来源：

```powershell
codex plugin marketplace add yue-witness/Requirements-Workbench --ref v0.3.2
```

重启桌面应用，打开 Plugins Directory，选择 **Requirements Analysis Workbench** 来源，然后安装或启用 `requirements-analysis-workbench`。安装后请新建一个任务，使三个内置技能和 MCP 工具正确加载。

如需跟随最新 `main` 分支，可省略 `--ref v0.3.2`。

## 从 Release 包安装

从 GitHub Release 下载 `requirements-analysis-workbench-v0.3.2.zip` 并解压，然后添加解压后的 marketplace 根目录：

```powershell
codex plugin marketplace add C:\path\to\requirements-analysis-workbench-v0.3.2
```

随后重启桌面应用，并在 Plugins Directory 中安装插件。

## 使用示例

引导模式：

> 我有一个软件构想，但不熟悉需求分析。请解释可用输出，帮助我识别缺失信息，并生成需求、上下文、用例和线框图。

可视化配置：

> 打开可视化需求工作台，让我选择模式并分别开关各个模块。

直接通过 `@` 调用插件并提供匹配的需求描述时，也会默认打开工作台：

> @Requirements Analysis Workbench 请分析这个预约系统的利益相关者记录。

专业模式：

> 请用专业模式分析这些利益相关者记录。生成全部六个模块，保留原有术语，标记推断，并包含验收条件和可追踪关系。

定向修订：

> 只修订 activity 模块，加入请求被拒绝的路径。不要改写其他模块文件。

TraceGuard 影响预览：

> 预览修改 FR-01 会影响哪些模块，在我确认前不要传播变更。

## 运行确定性示例

建议使用 Python 3.10 或更高版本。在仓库根目录运行：

```powershell
python plugins/requirements-analysis-workbench/scripts/materialize_analysis.py `
  plugins/requirements-analysis-workbench/assets/demo_analysis.json `
  --out demo-output

python plugins/requirements-analysis-workbench/scripts/traceguard.py audit `
  plugins/requirements-analysis-workbench/assets/demo_analysis.json `
  --out demo-output
```

确定性生成器仅使用 Python 标准库且不会发起网络请求。由模型参与的需求分析仍在宿主 ChatGPT 或 Codex 产品中进行。

## 验证与打包

```powershell
python -m unittest discover -s plugins/requirements-analysis-workbench/tests -v
python scripts/package_release.py
```

维护者还可以运行官方 Plugin Creator 和 Skill Creator 验证器；这些外部验证器要求对应 Python 环境已安装 PyYAML。

## 仓库结构

```text
.
|-- .agents/plugins/marketplace.json
|-- plugins/requirements-analysis-workbench/
|   |-- .codex-plugin/plugin.json
|   |-- .mcp.json
|   |-- mcp/server.py
|   |-- ui/workbench.html
|   |-- skills/
|   |-- scripts/
|   |-- assets/
|   |-- examples/requestbridge-demo/
|   `-- tests/
|-- scripts/package_release.py
|-- CHANGELOG.md
`-- LICENSE
```

## 局限与隐私

输出是结构化初稿，不是形式化验证，也不能替代利益相关者确认以及领域、安全、隐私、法律或监管评审。向任何模型提交材料前应先检查内容、尽量减少个人或敏感数据，并由有责任的人员决定高影响事项。

## 许可证

[MIT](LICENSE)
