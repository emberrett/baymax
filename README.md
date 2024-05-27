# Baymax: A locally ran, accessible-anywhere chatbot.

## 1. Clone repository
`git clone https://github.com/emberrett/baymax`

## 2. Find a model
1. Download a .gguf file from a model of your choice from [Huggingface](https://huggingface.co). [This repository](https://huggingface.co/TheBloke/Llama-2-7B-GGUF/tree/main) has a good collection of ready-to-go model files. I suggest using `llama-2-7b.Q4_K_M.gguf`.
    
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
2. Type `MODEL='your_model_file.bin'` into the `.env` file 

## 5. Create `.config` file
1. This file contains your telegram info and will determine how your model will run. See `example_config.config` for reference.

See [llama-cpp-python](https://llama-cpp-python.readthedocs.io/en/latest/api-reference/) docs for more info on model and chat completion args.

## 4. Build/Run Docker image. Must have [Docker](https://docs.docker.com/engine/install/)
1. Run `docker compose up -d` from root of repo directory

Note: You can also just run the `main.py` locally without spinning up a container. Be sure to run `pip install -r requirements.txt` first.


## You are now ready to message your personal AI chatbot via Telegram.
Type `/help` for commands.

For running container with Nvidia GPU access on Windows, see [this guide](https://saturncloud.io/blog/how-to-use-gpu-from-a-docker-container-a-guide-for-data-scientists-and-software-engineers/)