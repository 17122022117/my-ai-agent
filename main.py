import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    function_results = []

    for _ in range(20):
        response = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))

        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata is None:
            raise Exception("failed api request")
        else:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls is not None:
            for function_call in response.function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call)
                if function_call_result.parts is None:
                    raise Exception("call_function has empty .parts list")
                elif function_call_result.parts[0].function_response is None:
                    raise Exception("function_response property of first item in list of parts is None")
                elif function_call_result.parts[0].function_response.response is None:
                    raise Exception("function_response response field is None")
                else:
                    function_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(f"Response: {response.text}")
            break
        messages.append(types.Content(role="user", parts=function_results))
    else: 
        print("Maximum number of iterations reached before model final response")
        sys.exit(1)
    

if __name__ == "__main__":
    main()
