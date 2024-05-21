import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from utils import set_system_context, help, reply, clear, get_llm, error_handler, startup


load_dotenv()

telegram_token = os.environ["TELEGRAM_TOKEN"]


logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def main() -> None:

    set_system_context()
    get_llm()
    logging.info("Model loaded")

    application = Application.builder().token(telegram_token).build()

    application.post_init = startup

    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, reply))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
