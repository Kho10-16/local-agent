from ollama import chat
from datetime import datetime
from pathlib import Path
SAFE_FOLDER = Path(__file__).parent.resolve()

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

def read_file(path: str) -> str:
    """Read a text file and return its contents. Use this when the user asks about a file.

    Args:
        path: The file name or path, for example notes.txt

    Returns:
        The text inside the file, or an error message
    """
    full_path = (SAFE_FOLDER / path).resolve()

    if not full_path.is_relative_to(SAFE_FOLDER):
        return "Error: Access to this file is not allowed."

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

available_tools = {
    "get_current_time": get_current_time,
    "multiply": multiply,
    "read_file": read_file,
}

tools = [get_current_time, multiply, read_file]

messages = [
    {"role": "system", "content": "You are a helpful assistant. You have tools. If a tool can answer the question, always call the tool instead of guessing."},
]

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    messages.append({"role": "user", "content": user_input})

    while True:
        response = chat(model="qwen3:8b", messages=messages, tools=tools)
        messages.append(response.message)

        if not response.message.tool_calls:
            break

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            result = available_tools[name](**args)
            print("Tool:", name, args, "->", str(result)[:100])
            messages.append({"role": "tool", "tool_name": name, "content": str(result)})

    print("Agent:", response.message.content)