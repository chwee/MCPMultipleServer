# 1. Story Writer MCP Server
# We’ll start by creating the Story Writer server. This tool will take a topic and generate a short story about it, providing the result in Markdown format.

# https://dev.to/sreeni5018/building-an-ai-agent-with-mcp-model-context-protocolanthropics-and-langchain-adapters-25dc

from mcp.server.fastmcp import FastMCP, Context
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Dict, List, Union
# from langchain.schema import AIMessage, HumanMessage
from langchain_core.messages import AIMessage, HumanMessage
import os
from openai import OpenAI


from dotenv import load_dotenv
load_dotenv(override=True)


# Access env var
api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, verbose=True)
mcp = FastMCP("storywriter")

@mcp.tool()
async def write_storyt(topic: str) -> str:
    """Write a story.
    Args:
        topic: The story topic  
    Returns:
        The written story as a string
    """
    try:
        messages = [
            (
                "system",
                "You are a talented story writer. Create an engaging short story on the given topic in a maximum of 100 words. Provide the output in markdown format only.",
            ),
            ("human", f"The topic is: {topic}"),
        ]
        ai_msg = await model.ainvoke(messages)
        return ai_msg.content
    except Exception as e:
        return f"An error occurred while writing story: {e}"

if __name__ == "__main__":
  mcp.run()