import json

from openai import AzureOpenAI
from src.constants.properties import OPENAI_TOKEN, OPENAI_ENDPOINT, OPENAI_API_VERSION, GPT_MODEL

client = AzureOpenAI(
    api_key=OPENAI_TOKEN,
    azure_endpoint=OPENAI_ENDPOINT,
    api_version=OPENAI_API_VERSION
)

def get_completion(messages, tool_functions, user_id = None):
    while True:
        completion = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            tools=[{"type": "function", "function": func.openai_schema} for func in tool_functions],
            tool_choice="auto"
        )

        completion_message = completion.choices[0].message
        if completion_message.tool_calls is None:
            return completion_message.content
        else:
            messages.append(completion_message)
            for tool_call in completion_message.tool_calls:
                print(f"\033[90m🛠️ {tool_call.function.name} {tool_call.function.arguments}\033[0m")
                tool_result = execute_tool(tool_call, tool_functions, user_id)
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": json.dumps(tool_result),
                    })

def execute_tool(tool_call, funcs, user_id = None):
    func = next(iter([func for func in funcs if func.__name__ == tool_call.function.name]))

    if not func:
        return f"Error: Function {tool_call.function.name} not found. Available functions: {[func.__name__ for func in funcs]}"
    try:
        func = func(**eval(tool_call.function.arguments))
        if user_id and 'user_id' in func.run.__code__.co_varnames:
            output = func.run(user_id=user_id)
        else:
            output = func.run()
        return output
    except Exception as e:
        return "Error: " + str(e)