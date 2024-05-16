# Baymax: A locally ran, accessible-anywhere chatbot.

## 1. Clone repository
`git clone https://github.com/emberrett/baymax`

## 2. Find a model
1. Download a .gguf file from a model of your choice from [Huggingface](https://huggingface.co). [This repository](https://huggingface.co/TheBloke/Llama-2-7B-GGUF/tree/main) has a good collection of ready-to-go model files.
    
    a. [You can also prepare your own model](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#prepare-and-quantize).
2. Copy the model into the models folder
3. Enter the name of the model in `.env`


## 3. Set up Telegram bot
1. Download [Telegram](https://desktop.telegram.org/)
2. Send the following messages to @BotFather on Telegram to get your token
    1. `/start`
    2. `/newbot`
    3. `<your_bot_name>`
    4. Copy token
3. To get your Telegram chat ID:
    1. Message your new bot
    2. Open https://api.telegram.org/bot<your_token>/getUpdates in a browser
    3. Copy your chat ID

## 4. Create .env file
1. Create an `.env` file at the root directory
2. Fill it out with the following:
```
# from step 2. Can be `.bin` or `.gguf` file.
MODEL='your_model_file.bin' 

# from step 3
TELEGRAM_TOKEN=<telegram_token> 
TELEGRAM_CHAT_ID=<telegram_chat_id>

# determines how much work the GPU does running the model. -1 = all GPU, 0 = no GPU, 1+ = some GPU
# see `compose.yaml` for dedicating GPU to docker
N_GPU_LAYERS=-1 
MAX_CONTEXT=2048 # max context that can be retained for a chat 
```
## 4. Build/Run Docker image. Must have [Docker](https://docs.docker.com/engine/install/)
1. Run `docker compose up -d` from root of repo directory

Note: You can also just run the `main.py` locally without spinning up a container. Be sure to run `pip install -r requirements.txt` first.


## You are now ready to message your personal AI chatbot via Telegram.
Type `/help` for commands.

If you would like to edit the prompt the chatbot begins with, edit `prompt.txt`.
