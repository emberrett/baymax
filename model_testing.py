import json
import os
from llama_cpp import Llama


with open('model_config.json', 'r') as config_file:
    config = json.load(config_file)

llm_kwargs = config["model"]

llm = Llama(**llm_kwargs)

base_context = [{"role": "user",
                         "content": config["initial_prompt"]}]



context = base_context


user_messages = [
    "what's your name?",
    "Hi I'm Ethan",
    "What's my name?",
    "Help me write a song about birds",
    "Make the song shorter",
    "What's 2 + 2?",
    "Who won the 2011 NBA finals?"
]

for message in user_messages:
    print(f"User: {message}")
    context.append({"role": "user", "content": message})
    completion_output = llm.create_chat_completion(
        context, **config["chat_completion"])
    assistant_response = completion_output["choices"][0]["message"]["content"]
    context.append({"role": "assistant", "content": assistant_response})
    print(f"Assistant: {assistant_response}")
