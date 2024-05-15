# Download a model from [huggingface](https://huggingface.co/)

Huggingface doesn't make it very clear how exactly to "download models". You will need to follow these steps:


# Find a model
1. Download a .gguf file from a model of your choice from [Huggingface](https://huggingface.co). [This repository](https://huggingface.co/TheBloke/Llama-2-7B-GGUF/tree/main) has a good collection ready model files.
    a. [You can also prepare your own model](C:\\Users\\berre\\Downloads\\llama-2-7b.Q2_K.gguf).
2. Paste the path of the model file in `.env`

# Set up Telegram bot
1. Download Telegram
2. Send the following messages to @BotFather on Telegram to get your token
    1. `/start`
    2. `/newbot`
    3. `<your_bot_name>`
    4. Copy token
3. Paste the token into `.env`
3. To get your Telegram chat ID:
    1. Message your new bot
    2. Open https://api.telegram.org/bot<your_token>/getUpdates in a browser
    3. Copy your chat ID
3. Paste chat ID into `.env`