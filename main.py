import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api key not found")

client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="JohnAI")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    config = types.GenerateContentConfig(
        tools=[call_function.available_functions],
        system_instruction=system_prompt,
        temperature=0
    )

    for _ in range(20):
        # Step 1: call the model with the current conversation history
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=config,
        )

        if response is None:
            raise RuntimeError("failed API request")
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

        # Step 2: append every candidate the model produced so it sees its own turns next iteration
        for candidate in response.candidates:
            messages.append(candidate.content)

        # Step 3: no function calls means the model is done — print the answer and exit
        if not response.function_calls:
            print(response.text)
            return

        # Step 4: execute each requested function call and collect the result parts
        function_results = []
        for fc in response.function_calls:
            result = call_function.call_function(fc, verbose=args.verbose)
            if not result.parts:
                raise Exception(f"call_function returned Content with empty parts for '{fc.name}'")
            if result.parts[0].function_response is None:
                raise Exception(f"call_function returned no function_response for '{fc.name}'")
            if result.parts[0].function_response.response is None:
                raise Exception(f"function_response.response is None for '{fc.name}'")
            function_results.append(result.parts[0])
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")

        # Step 5: feed the tool results back so the model sees them next iteration
        messages.append(types.Content(role="user", parts=function_results))

    # Step 6: exceeded the iteration limit without a final answer
    print("Error: max iterations reached without a final response")
    sys.exit(1)
    


if __name__ == "__main__":
    main()
