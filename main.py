import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api key not found")

client = genai.Client(api_key=api_key)


def main():
    
    parser = argparse.ArgumentParser(description="JohnAI")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )


    if response is None:
        raise RuntimeError("failed API request")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)
    


if __name__ == "__main__":
    main()
