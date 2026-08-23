# Requirements Analysis Workbench 插件

简体中文 | [English](README.md)

本目录是可安装的 `requirements-analysis-workbench` 插件，包含三个技能和一个不依赖第三方包的 MCP Apps GUI：

- `analyze-requirements`：根据用户选择生成一组需求分析工件；
- `revise-requirements-module`：只修改一个现有模块，同时保留其他模块文件。
- `traceguard-audit`：审计精确证据片段、跨工件约束、变更影响、回滚和审批门槛。

可视化工作台区分引导、标准和专业模式，并为 `requirements`、`fishbone`、`context`、`use-cases`、`activity` 和 `wireframe` 六个模块分别提供勾选框。辅助文件包括作为单一事实来源的 `analysis.json`、`review-index.md`、`traceability.csv`、`traceguard.md`、`traceguard.json` 和 `manifest.json`。

当用户通过 `@` 直接调用插件并提供匹配的需求描述时，`analyze-requirements` 技能默认在分析前打开此工作台。仅打开面板不会接受界面中显示的默认值：用户必须点击 **Apply selection**，且服务端确认已保存模式与模块后，分析才会解锁。只有在请求同时给出模式和至少一个模块时，插件才接受“不打开 GUI”的明确要求；不兼容 MCP Apps 的宿主则回退为同样具有等待门禁的结构化或对话式选择。

## 确定性示例

在插件目录运行：

```powershell
python scripts/materialize_analysis.py assets/demo_analysis.json --out demo-output
python scripts/traceguard.py audit assets/demo_analysis.json --out demo-output
python -m unittest discover -s tests -v
```

生成器仅使用 Python 标准库。`project.minimum_requirements` 是可选字段，默认不设置数量门槛，因此项目、组织、行业或政策规则不会被硬编码进通用插件。

安装、发布打包、局限和许可证信息请参阅[仓库中文说明](../../README.zh-CN.md)。
