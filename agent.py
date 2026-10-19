from ollama import chat
from datetime import datetime

def get_current_time():
    """Get the current local date and time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

available_tools = {"get_current_time": get_current_time}

messages = [
    {"role": "system", "content": "You are a helpful assistant. You have tools. If a tool can answer the question, always call the tool instead of guessing."},
]

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    messages.append({"role": "user", "content": user_input})

    while True:
        response = chat(model="qwen3:8b", messages=messages, tools=[get_current_time])
        messages.append(response.message)

        if not response.message.tool_calls:
            break

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            result = available_tools[name](**args)
            print("Tool result:", result)
            messages.append({"role": "tool", "tool_name": name, "content": result})

    print("Answer:", response.message.content)