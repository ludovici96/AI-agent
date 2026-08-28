import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from prompts import system_prompt
from functions.call_function import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("api key is not loaded")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system", 
            "content": system_prompt
         },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        #temperature=0,
        tools=available_functions,
    )
    
    usage = response.usage
    if args.verbose:
        if usage is not None:
            print(f"User prompt: {args.user_prompt}\n")
            print(f"Prompt tokens: {usage.prompt_tokens}\n"
                f"Response tokens: {usage.completion_tokens}\n"
                )
        else:
            print("Token usage unavailable\n")

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")

    else:
        print(f"response: {response.choices[0].message.content.strip()}")


if __name__ == "__main__":
    main()
    
