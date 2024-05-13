from llama_cpp import Llama
import os
from dotenv import load_dotenv

load_dotenv()

model_path = os.environ["MODEL_PATH"]
gpu_layers = int(os.environ["N_GPU_LAYERS"])

if 'nt' not in os.name:
    # if running in container
    if os.path.exists('/.dockerenv'):
        model_path = 'models' + '/' + os.path.basename('model_path')
    else:
        # ensure the path matches unix standard
        model_path =  os.path.abspath(model_path)

llm = Llama(
    model_path=model_path,
    chat_format="llama-3",
    n_gpu_layers=gpu_layers
)

prompt = input("Prompt: ")
messages = [{"role": "system", "content": "You are a virtual assistant who responds with helpful answers."}]
while prompt.lower() != 'clear':
    messages.append({"role": "user", "content": prompt})
    output = llm.create_chat_completion(messages, max_tokens=128)
    content = output["choices"][0]["message"]["content"]
    print(content)
    messages.append({"role": "assistant", "content": content})
    prompt = input("Prompt: ")
    print(messages)

