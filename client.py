import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import AIMessage, HumanMessage

import os
from openai import OpenAI


from dotenv import load_dotenv
load_dotenv(override=True)


# Access env var
api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o" , api_key= api_key)

python_path = sys.executable

async def main():
    client = MultiServerMCPClient()

    # Connect to each MCP server
    await client.connect_to_server(
        "storywriter",
        command=python_path,
        args=["write_blog.py"],
        encoding_error_handler="ignore",
    )
    await client.connect_to_server(
        "imagegenerator",
        command=python_path,
        args=["image.py"],
        encoding_error_handler="ignore",
    )
    await client.connect_to_server(
        "googlesearch",
        command=python_path,
        args=["google_search.py"],
        encoding_error_handler="ignore",
    )

    # Load all tools from all connected servers
    tools = await client.get_tools()

    # Create the agent
    agent = create_react_agent(model, tools, debug=True)

    # Call the agent
    review_requested = await agent.ainvoke(
        input={"messages": "Write story about lord krishna and arjuna and generate images for it and also search in google for it"},
        debug=True
    )

    parsed_data = parse_ai_messages(review_requested)
    for ai_message in parsed_data:
        print(ai_message)

    print("Story written successfully")

if __name__ == "__main__":
    asyncio.run(main())