import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallUnionParam,
)
from prompts import system_prompt
from functions.call_function import available_functions, call_function


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

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        usage = response.usage

        if args.verbose:
            if usage is not None:
                print(f"User prompt: {args.user_prompt}\n")
                print(
                    f"Prompt tokens: {usage.prompt_tokens}\n"
                    f"Response tokens: {usage.completion_tokens}\n"
                )
            else:
                print("Token usage unavailable\n")

        message = response.choices[0].message

        if message.tool_calls:
            serialized_tool_calls: list[ChatCompletionMessageToolCallUnionParam] = []
            for tool_call in message.tool_calls:
                if tool_call.type == "function":
                    serialized_tool_calls.append(
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                    )
                else:
                    serialized_tool_calls.append(
                        {
                            "id": tool_call.id,
                            "type": "custom",
                            "custom": {
                                "name": tool_call.custom.name,
                                "input": tool_call.custom.input,
                            },
                        }
                    )

            assistant_message: ChatCompletionAssistantMessageParam = {
                "role": "assistant",
                "content": message.content,
                "tool_calls": serialized_tool_calls,
            }
            messages.append(assistant_message)

            for tool_call in message.tool_calls:
                if tool_call.type != "function":
                    raise RuntimeError(f"Unsupported tool type: {tool_call.type}")

                result_message = call_function(tool_call, verbose=args.verbose)

                if not result_message["content"]:
                    raise RuntimeError("Function call returned empty content")

                messages.append(result_message)

                if args.verbose:
                    print(f"-> {result_message['content']}")

        else:
            content = message.content or ""
            print(f"Final response:\n{content.strip()}")
            return

    print("Error: Maximum number of iterations reached without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()
    
