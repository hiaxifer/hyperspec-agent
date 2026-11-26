# 工具服务器（MCP Server）目录

每个 `.py` 文件是一个独立的 MCP 服务器（基于 fastmcp，stdio 传输），
启动后把本文件的函数以工具 schema 的形式暴露给 LLM。

## 写工具的约定（参考 Earth-Agent 的做法）

1. 工具 = 一个带完整 docstring 的函数：**模型的全部"使用说明"就是 docstring**，
   要写清参数含义、单位、返回值格式，并给 Example。
2. 工具尽量原子化、可组合（如：单波段统计、波段比值、阈值占比各一个工具），
   复杂处理链让 LLM 自己编排。
3. 输出文件统一写到 `--temp_dir` 指定的目录（启动参数），返回完整绝对路径。
4. 工具返回错误时返回可读的错误字符串（不抛异常崩溃），让模型有机会自我纠正。

## TODO

- [ ] `io_tools.py`：ENVI/GeoTIFF 读取、波段列表、光谱曲线提取、缩略图
- [ ] `preprocess_tools.py`：坏波段剔除、辐射定标、噪声平滑
- [ ] `bandmath_tools.py`：波段比值/差值、光谱指数
- [ ] `dimred_tools.py`：PCA / MNF / 波段选择
- [ ] `classify_tools.py`：SAM 光谱角匹配、监督分类
- [ ] `stats_tools.py`：直方图、阈值占比、批次统计
