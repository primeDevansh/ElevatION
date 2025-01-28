from openai import OpenAI
import os
 
def call_llm(messages):
    client = OpenAI(
        base_url="https://api-inference.huggingface.co/v1/",
        api_key="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"
    )
 
    completion = client.chat.completions.create(
        model="microsoft/Phi-3.5-mini-instruct",
        messages=messages,
        max_tokens=500
    )
 
    return completion.choices[0].message.content
 