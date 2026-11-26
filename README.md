# HyperSpec-Agent

高光谱（Hyperspectral）遥感数据处理的 LLM 智能体（Agent）。

让大模型通过工具调用（function calling）自主规划并执行高光谱数据的
读取、预处理、波段运算、降维、地物分类等完整处理链路。

> 灵感与架构参考 [Earth-Agent](https://github.com/opendatalab/Earth-Agent)
> （ICLR 2026, arXiv:2509.23141）：ReAct 循环 + MCP 工具服务器 +
> OpenAI 兼容接口。区别在于我们聚焦**高光谱**（几十~几百个窄波段）场景。

## 架构

```
用户提问
   ↓
LLM Agent（ReAct 循环，langgraph create_react_agent）
   ↓ 工具调用
MCP 工具服务器（高光谱专用工具集，fastmcp / stdio）
   ↓ 读写
GeoTIFF / ENVI 格式高光谱数据（不入 git）
```

## 目录结构

```
hyperspec-agent/
├── agent/
│   └── tools/          # MCP 工具服务器（高光谱专用工具集）
├── configs/            # 模型/服务配置（模板，不含密钥）
├── scripts/            # 跑批/评测入口脚本
├── docs/               # 设计文档、工具说明书
├── data/               # 数据目录（不入 git，见 .gitignore）
└── requirements.txt    # Python 依赖（版本已实测锁定）
```

## 快速开始（占位）

```bash
conda create -n hyperspec python=3.10 -y
pip install -r requirements.txt
python scripts/run_agent.py --help
```

> ⚠️ 项目处于早期搭建阶段，工具集与评测流程开发中。

## 工具集规划

| 模块 | 计划工具 | 状态 |
|---|---|---|
| IO | 读取 ENVI/GeoTIFF、波段列表、缩略图预览 | 🚧 规划中 |
| 预处理 | 辐射定标、大气校正、坏波段剔除、噪声平滑 | 🚧 规划中 |
| 波段运算 | 波段比值/差值/NDVI 类指数、光谱曲线提取 | 🚧 规划中 |
| 降维 | PCA、MNF、波段选择 | 🚧 规划中 |
| 分类/反演 | SAM 光谱角匹配、监督分类、端元提取 | 🚧 规划中 |
| 统计 | 直方图、阈值占比、批次均值、趋势检验 | 🚧 规划中 |

## 数据说明

高光谱数据体积大，**一律不入 git**：放到 `data/`（已被 .gitignore 排除），
或用绝对路径引用服务器上的其他目录。
