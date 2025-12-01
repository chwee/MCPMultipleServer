from mcp.server.fastmcp import FastMCP, Context
import openai
from openai import AsyncOpenAI
from typing import List
from dotenv import load_dotenv

import os
from openai import OpenAI


from dotenv import load_dotenv
load_dotenv(override=True)


# Access env var
api_key = os.getenv("OPENAI_API_KEY")

load_dotenv(override=True)


client = AsyncOpenAI(api_key =api_key)
mcp = FastMCP("image")

@mcp.tool()
async def generate_images(topic: str) -> List[str]:
    """Generate header images for a story.

    Args:
        topic: The story topic

    Returns:
        The list of image URLs
    """
    image_url_list = []
    try:
        images_response = await client.images.generate(
          prompt= f"Photorealistic image about: {topic}.",
          n= 3,
          style= "natural",
          response_format= "url",
        )
        for image in images_response.data:
          image_url_list.append(image.model_dump()["url"])
          return image_url_list
    except openai.APIConnectionError as e:
        return f"An error occurred while generating images: {e}"


if __name__ == "__main__":
  mcp.run()