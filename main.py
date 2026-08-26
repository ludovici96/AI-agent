import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import argparse

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
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
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

    print(f"response: {response.choices[0].message.content.strip()}")
    #print(repr(response.choices[0].message.content))


if __name__ == "__main__":
    main()
    
