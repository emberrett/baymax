# Download a model from [huggingface](https://huggingface.co/)

Huggingface doesn't make it very clear how exactly to "download models". You will need to follow these steps:

1. Create a [huggingface token](https://huggingface.co/settings/tokens). 
2. Install git lfs: `git lfs install`
3. Run `git lfs clone <URL for model repo>`

    a. When prompted, login with your huggingface username and token from step 1


# Set up Telegram bot
1. Download Telegram
2. Send the following messages to @BotFather on Telegram to get your token
    1. `/start`
    2. `/newbot`
    3. `<your_bot_name>`
3. To get your Telegram chat ID:
    1. Message your new bot
    2. Open https://api.telegram.org/bot<your_token>/getUpdates in a browser
    3. Copy your chat ID
3. Paste token into your `.env` file