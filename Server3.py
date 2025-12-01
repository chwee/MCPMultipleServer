from mcp.server.fastmcp import FastMCP, Context
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from googlesearch import search  
from typing import Dict, List, Union
# from langchain.schema import AIMessage, HumanMessage
from langchain_core.messages import AIMessage, HumanMessage

import os
from openai import OpenAI


from dotenv import load_dotenv
load_dotenv(override=True)


# Access env var
api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o", api_key=api_key, verbose=True)
mcp = FastMCP("storywriter")

@mcp.tool()
async def search_google(query: str) -> str:
    """Search Google for the query and return results as markdown formatted text.
    Args:
        query: The search query
    Returns:
        Search results formatted in markdown
    """
    try:
        search_results = list(search(query, num_results=5))  # Limiting to 5 results
        if not search_results:
            return "No results found."

        # Format the search results in Markdown
        markdown_results = "### Search Results:\n\n"
        for idx, result in enumerate(search_results, 1):
            markdown_results += f"**{idx}.** [{result}](<{result}>)\n"
        return markdown_results
    except Exception as e:
        return f"An error occurred while searching Google: {e}"

if __name__ == "__main__":
    mcp.run()