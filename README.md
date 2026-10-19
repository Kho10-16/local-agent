# Local AI Agent

A simple AI agent that runs fully on my own PC using Ollama and Qwen3 (8B).
It chats in the terminal, remembers the conversation, and decides by itself when to use tools.

## Features
- Runs locally on GPU (no cloud, no API key)
- Tool calling: `get_current_time`
- Conversation memory
- Agent loop: model → tool → result → answer

## How to run
1. Install [Ollama](https://ollama.com) and pull the model:
```
   ollama pull qwen3:8b
```
2. Install dependencies:
```
   pip install -r requirements.txt
```
3. Start the agent:
```
   python agent.py
```
   Type `exit` to quit.