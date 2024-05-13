from llama_cpp import Llama
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
import logging

load_dotenv()

model_path = os.environ["MODEL_PATH"]
telegram_token = os.environ["TELEGRAM_TOKEN"]
gpu_layers = int(os.environ["N_GPU_LAYERS"])
chat_id = int(os.environ["TELEGRAM_CHAT_ID"])
in_container = os.path.exists('/.dockerenv')

if 'nt' not in os.name:
    if in_container:
        model_path = 'models' + '/' + os.path.basename('model_path')
    else:
        # ensure the path matches unix standard
        model_path = os.path.abspath(model_path)

llm = Llama(
    model_path=model_path,
    chat_format="llama-3",
    n_gpu_layers=gpu_layers
)


logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    await update.message.reply_text(update.message.text)


def main() -> None:

    def reset_chat_context():
        global chat_context
        chat_context = [{"role": "system",
                         "content": "You are a virtual assistant who responds with helpful answers."}]

    reset_chat_context()

    application = Application.builder().token(telegram_token).build()

    async def confirm_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message.chat_id == chat_id:
            pass
        else:
            await update.message.reply_text("Unauthorized.")

    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("/clear will clear chat context. This may be helpful if the bot is running too slowly")

    async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info("Clearing chat context...")
        reset_chat_context()
        await update.message.reply_text("Chat context cleared.")

    async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info("User requested ")
        chat_context.append({"role": "user", "content": update.message.text})
        output = llm.create_chat_completion(chat_context, max_tokens=128)
        content = output["choices"][0]["message"]["content"]
        chat_context.append({"role": "assistant", "content": content})
        await update.message.reply_text(content)

    application.add_handler(MessageHandler(None, confirm_chat_id))

    application.add_handler(CommandHandler("help", help))

    application.add_handler(CommandHandler("clear", clear))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, reply))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    main()
