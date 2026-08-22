# Requirements Workbench

简体中文 | [English](README.md)

Requirements Workbench 是一个适用于 ChatGPT 和 Codex 的纯技能插件，可将软件构想、问题陈述、用户故事、会议记录或需求草稿整理为可选择、可追踪、便于评审的需求工件。

插件既为初次参与需求分析的用户提供通俗引导，也为专业分析人员保留证据、置信度、验收条件、可追踪关系和变更范围控制。它是领域无关的通用插件，项目专属约束由项目数据提供。

## 可生成的内容

用户可以选择一个或多个彼此独立的模块：

- `requirements`：原子化的功能、质量和业务需求；
- `fishbone`：问题背后的潜在原因；
- `context`：系统边界、参与者、外部系统和信息流；
- `use-cases`：参与者目标、主流程、备选流程和异常流程；
- `activity`：工作流决策、失败路径和结果；
- `wireframe`：带追踪标签、可访问的低保真 HTML 界面。

每次运行还会生成作为单一事实来源的 `analysis.json`、面向评审者的 `review-index.md`、`traceability.csv` 和带 SHA-256 文件哈希的 `manifest.json`。

## 核心特性

- 引导、标准和专业三种评审模式。
- 明确区分利益相关者证据、推断、假设、建议、冲突和待确认问题。
- 使用稳定 ID 和追踪链接连接不同工件。
- 在生成文件前执行确定性结构验证。
- 可只修订一个目标模块，并使用哈希逐字节确认其他模块未被改写。
- 对安全关键、受监管或高影响结论保留人工确认边界。
- 确定性生成器不需要 API Key、MCP Server 或第三方 Python 包。

例如，`project.minimum_requirements` 是可选字段，默认不设置数量门槛；通用插件不会强制任何组织或行业范围的最低数量要求。

## 从 GitHub 安装

请使用支持插件的当前版 ChatGPT 桌面应用或 Codex。先将本仓库添加为 marketplace 来源：

```powershell
codex plugin marketplace add yue-witness/Requirements-Workbench --ref v0.2.0
```

重启桌面应用，打开 Plugins Directory，选择 **Requirements Workbench** 来源，然后安装或启用 `requirements-workbench`。安装后请新建一个任务，使两个内置技能正确加载。

如需跟随最新 `main` 分支，可省略 `--ref v0.2.0`。

## 从 Release 包安装

从 GitHub Release 下载 `requirements-workbench-v0.2.0.zip` 并解压，然后添加解压后的 marketplace 根目录：

```powershell
codex plugin marketplace add C:\path\to\requirements-workbench-v0.2.0
```

随后重启桌面应用，并在 Plugins Directory 中安装插件。

## 使用示例

引导模式：

> 我有一个软件构想，但不熟悉需求分析。请解释可用输出，帮助我识别缺失信息，并生成需求、上下文、用例和线框图。

专业模式：

> 请用专业模式分析这些利益相关者记录。生成全部六个模块，保留原有术语，标记推断，并包含验收条件和可追踪关系。

定向修订：

> 只修订 activity 模块，加入请求被拒绝的路径。不要改写其他模块文件。

## 运行确定性示例

建议使用 Python 3.10 或更高版本。在仓库根目录运行：

```powershell
python plugins/requirements-workbench/scripts/materialize_analysis.py `
  plugins/requirements-workbench/assets/demo_analysis.json `
  --out demo-output
```

确定性生成器仅使用 Python 标准库且不会发起网络请求。由模型参与的需求分析仍在宿主 ChatGPT 或 Codex 产品中进行。

## 验证与打包

```powershell
python -m unittest discover -s plugins/requirements-workbench/tests -v
python scripts/package_release.py
```

维护者还可以运行官方 Plugin Creator 和 Skill Creator 验证器；这些外部验证器要求对应 Python 环境已安装 PyYAML。

## 仓库结构

```text
.
|-- .agents/plugins/marketplace.json
|-- plugins/requirements-workbench/
|   |-- .codex-plugin/plugin.json
|   |-- skills/
|   |-- scripts/materialize_analysis.py
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
