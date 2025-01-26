# main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from data import brand_info, tweet_history
from twitter_mock import post_tweet
from openai_functions import post_tweet_function
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize the client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Tweet(BaseModel):
    author: str
    content: str
    timestamp: str
    engagement: int

@app.post("/generate_tweet")
def generate_tweet():
    """
    Endpoint that triggers the AI to decide if and how to post a tweet.
    """
    # 1. Prepare context messages for the AI.
    system_message = {
        "role": "developer",
        "content": [
            {
                "type": "text",
                "text": (
                    "You are an AI agent that promotes a given brand on Twitter. "
                    "You have access to the brand information and past tweet history. "
                    "Write a short promotional tweet."
                )
            }
        ]
    }

    context_messages = [
        {
            "role": "developer", 
            "content": [{"type": "text", "text": f"Brand Info: {brand_info}"}]
        },
        {
            "role": "developer", 
            "content": [{"type": "text", "text": f"Tweet History: {tweet_history}"}]
        }
    ]

    # 2. Call OpenAI ChatCompletion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message] + context_messages,
    )

    # 3. Return the generated tweet
    return {
        "status": "success",
        "tweet": response.choices[0].message.content
    }


# # main.py
# import os
# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# from dotenv import load_dotenv

# from data import brand_info, tweet_history
# from twitter_mock import post_tweet
# from openai_functions import post_tweet_function
# from openai import OpenAI

# # Load environment variables from .env file
# load_dotenv()

# app = FastAPI()

# # Initialize the client with API key from environment variable
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# class Tweet(BaseModel):
#     author: str
#     content: str
#     timestamp: str
#     engagement: int

# @app.post("/generate_tweet")
# def generate_tweet():
#     """
#     Endpoint that triggers the AI to decide if and how to post a tweet.
#     """
#     # 1. Prepare context messages for the AI.
#     system_message = {
#         "role": "developer",  # Changed from "system" to "developer"
#         "content": [
#             {
#                 "type": "text",
#                 "text": (
#                     "You are an AI agent that promotes a given brand on Twitter. "
#                     "You have access to the brand information and past tweet history. "
#                     "Write a short promotional tweet if it seems beneficial."
#                 )
#             }
#         ]
#     }

#     context_messages = [
#         {
#             "role": "developer", 
#             "content": [{"type": "text", "text": f"Brand Info: {brand_info}"}]
#         },
#         {
#             "role": "developer", 
#             "content": [{"type": "text", "text": f"Tweet History: {tweet_history}"}]
#         }
#     ]

#     # 2. Call OpenAI ChatCompletion with function calling
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[system_message] + context_messages,
#         tools=[post_tweet_function],  # Changed from functions to tools
#         tool_choice="auto",  # Changed from function_call to tool_choice
#     )

#     # 3. Check if the model called the function
#     message = response.choices[0].message

#     # If there's a tool call, parse its arguments
#     if message.tool_calls:  # Changed from function_call to tool_calls
#         tool_call = message.tool_calls[0]  # Get the first tool call

#         if tool_call.function.name == "post_tweet":
#             # The arguments are returned as a JSON string, so parse them
#             import json
#             args = json.loads(tool_call.function.arguments)
#             tweet_content = args.get("content")
#             tweet_brand_name = args.get("brand_name")

#             # 4. Call the mock Twitter function
#             post_tweet(content=tweet_content, brand_name=tweet_brand_name)

#             return {
#                 "status": "Function called",
#                 "function_name": tool_call.function.name,
#                 "arguments": args
#             }
#     else:
#         # If the model didn't call the function, just return the assistant's message
#         return {
#             "status": "No tweet posted",
#             "assistant_message": message.get("content", "")
#         }
