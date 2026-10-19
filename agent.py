from ollama import chat
from datetime import datetime

def get_current_time():
    """Get the current local date and time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def multiply(a: float, b: float) -> float:
    """Multiply two numbers. Use this for any multiplication instead of calculating yourself.

    Args:
        a: The first number
        b: The second number

    Returns:
        The product of a and b
    """
    return a * b

available_tools = {"get_current_time": get_current_time, "multiply": multiply,}

messages = [
    {"role": "system", "content": "You are a helpful assistant. You have tools. If a tool can answer the question, always call the tool instead of guessing."},
]

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    messages.append({"role": "user", "content": user_input})

    while True:
        response = chat(model="qwen3:8b", messages=messages, tools=[get_current_time, multiply])
        messages.append(response.message)

        if not response.message.tool_calls:
            break

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            result = available_tools[name](**args)
            print("Tool:", name, args, "->", result)
            messages.append({"role": "tool", "tool_name": name, "content": str(result)})

    print("Agent:", response.message.content)