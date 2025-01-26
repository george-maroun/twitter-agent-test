# openai_functions.py
post_tweet_function = {
    "type": "function",
    "function": {
        "name": "post_tweet",
        "description": "Post a tweet promoting the brand.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text of the tweet to post."
                },
                "brand_name": {
                    "type": "string",
                    "description": "The name of the brand making the tweet."
                }
            },
            "required": ["content", "brand_name"],
            "additionalProperties": False
        },
        "strict": True
    }
}
