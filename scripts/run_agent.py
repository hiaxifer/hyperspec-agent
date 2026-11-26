"""最小 runner 骨架：加载 MCP 工具 → 构建 ReAct agent → 回答一个问题。

用法:
    python scripts/run_agent.py --question "读取 data/demo.hdr，列出前 10 个波段"
TODO: 实现 load_questions / 批量评测 / 对话落盘（参考 Earth-Agent scripts/run_cases.py）
"""
import argparse
import asyncio
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SYS_PROMPT = """You are a remote sensing scientist. Use tools to answer questions
about hyperspectral data analysis. Final answer format:
<Answer>Your answer</Answer>"""


async def main(question: str, config_path: str):
    from langchain_core.messages import HumanMessage
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent

    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)

    mc = cfg["models"][0]
    llm = ChatOpenAI(
        model=mc["model_name"],
        api_key=mc["api_key"],
        base_url=mc["client_args"]["base_url"],
        temperature=0.1,
        request_timeout=300,
        **({"extra_body": mc["generate_args"]} if mc.get("generate_args") else {}),
    )

    # TODO: temp_dir 改写、相对路径处理参考 Earth-Agent scripts/run_cases.py
    client = MultiServerMCPClient(cfg["mcpServers"])
    tools = await client.get_tools()
    print(f"[OK] {len(tools)} tools loaded")

    agent = create_react_agent(llm, tools)
    resp = await agent.ainvoke(
        {"messages": [HumanMessage(content=f"{SYS_PROMPT}\n\nQuestion: {question}")]},
        config={"recursion_limit": 50, "max_execution_time": 600},
    )
    for m in reversed(resp["messages"]):
        if getattr(m, "type", "") == "ai" and m.content:
            print(m.content)
            break


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--config", default=str(REPO_ROOT / "configs" / "config.example.json"))
    args = ap.parse_args()
    asyncio.run(main(args.question, args.config))
