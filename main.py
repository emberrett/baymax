import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from baymax import Baymax
from llama_cpp import Llama


logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def main() -> None:

    load_dotenv()
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    model = os.environ["MODEL"]
    n_ctx = int(os.environ["MAX_CONTEXT"])
    chat_id = int(os.environ["TELEGRAM_CHAT_ID"])

    async def startup(self):
        await self.bot.sendMessage(chat_id, 'Baymax ready to assist.')

    llm = Llama(
        model_path=f"models/{model}",
        chat_format="llama-3",
        n_ctx=n_ctx,
        n_gpu_layers=int(os.environ["N_GPU_LAYERS"])
    )

    baymax = Baymax(chat_id, llm)

    logging.info("Model loaded")

    application = Application.builder().token(telegram_token).build()

    application.post_init = startup

    application.add_error_handler(baymax.error_handler)

    application.add_handler(handler=CommandHandler("help", baymax.help))
    application.add_handler(handler=CommandHandler("clear", baymax.clear))
    application.add_handler(handler=MessageHandler(
        filters.TEXT & ~filters.COMMAND, baymax.reply))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
