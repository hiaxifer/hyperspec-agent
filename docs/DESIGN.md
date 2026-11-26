# 设计文档（起点）

## 1. 目标

构建一个面向高光谱遥感数据的 LLM agent：

- 输入：自然语言的科学问题（如"这景 AVIRIS 数据里 ROI-A 的光谱与 ROI-B 相似度如何？")
- 输出：数据驱动的答案（数值/类别/结论），全程可追溯（每步工具调用落盘）
- 评测：参考 Earth-Bench 的思路——过程分（工具链是否正确）+ 结果分（答案对错）

## 2. 技术选型（沿用 Earth-Agent 已验证的组合）

| 组件 | 选型 | 理由 |
|---|---|---|
| Agent 框架 | langgraph `create_react_agent` | Earth-Agent 同款，ReAct 循环稳定 |
| 工具服务 | MCP（fastmcp, stdio） | 工具即 Python 函数 + docstring，schema 自动生成 |
| 模型接口 | OpenAI 兼容（ChatOpenAI） | 本地 vLLM / 云端 API 通吃 |
| 数据栈 | spectral + rasterio + numpy | ENVI/GeoTIFF 高光谱事实标准 |

已知坑（见根 README 与 Earth-Agent 项目经验）：
`pydantic` 锁 2.11.x、`langgraph` 锁 0.x、Qwen3.5 系必须 `enable_thinking: false`。

## 3. 高光谱 vs 多光谱的工具差异（本项目存在的理由）

- 波段数：几十~几百个窄波段 → 需要波段选择/降维工具（PCA/MNF）
- 光谱曲线是核心对象 → 需要曲线提取、光谱库比对、SAM 光谱角匹配
- 坏波段/噪声波段常见 → 预处理工具链必须有
- ENVI 格式（.hdr + .img）为主 → IO 层优先支持 ENVI

## 4. 里程碑

- [ ] M1：io_tools + 一个最小可跑通的单工具 agent（本仓库 README 的快速开始）
- [ ] M2：5 类工具 server 全部就位，自然语言问数的端到端 demo
- [ ] M3：小型评测集（自建 10-20 题，含 GT 工具链）+ 过程分评测脚本
- [ ] M4：对照实验：不同模型（本地 Qwen3.5-9B / 云端 API）在同一评测集上的表现
