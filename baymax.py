from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
from llama_cpp import Llama
import html
import traceback
import json
import re
import json
from telegram.ext import Application, CommandHandler, MessageHandler, filters


class Baymax():
    def __init__(
            self,
            intial_prompt: str,
            chat_id: str,
            token: str,
            llm_kwargs: dict,
            chat_completion_kwargs: dict
    ):
        logging.basicConfig(level=logging.INFO)
        self.chat: list[dict]
        self.intial_prompt = intial_prompt
        # passed to Llama object
        self.llm_kwargs = llm_kwargs
        # passed to Llama.create_chat_completion method
        self.chat_completion_kwargs = chat_completion_kwargs
        self.reset_system_context()
        self.chat_id = chat_id if type(chat_id) is int else int(chat_id)
        self.token = token
        self.llm = self.get_llm()
        self.application = Application.builder().token(self.token).build()
        self.set_application_args()

    def __call__(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def startup(self, *args):
        await self.application.bot.sendMessage(self.chat_id, 'Baymax ready to assist.')

    def set_application_args(self):
        self.application.post_init = self.startup

        self.application.add_error_handler(self.error_handler)

        self.application.add_handler(
            handler=CommandHandler("help", self.help))
        self.application.add_handler(
            handler=CommandHandler("clear", self.clear))
        self.application.add_handler(handler=MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.reply))

    def get_llm(self) -> Llama:
        logging.info("Initializing model...")
        return Llama(
            **self.llm_kwargs
        )

    def reset_system_context(self):
        logging.info("Restoring chat to system prompt.")
        self.chat = [{"role": "system",
                      "content": self.intial_prompt}]

    def auth(func):
        def wrapper(self, *args, **kwargs):
            if args[0].message.chat_id != self.chat_id:
                return self.unauthorized(*args, **kwargs)
            else:
                return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Unauthorized.")

    @staticmethod
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.error("Exception while handling an update:",
                      exc_info=context.error)

        if bool(re.search('Requested tokens \(\d+\) exceed context window of \d+', str(context.error))):
            await update.message.reply_text("Context exceeded. Clear with /clear")
        else:
            tb_list = traceback.format_exception(
                None, context.error, context.error.__traceback__)
            tb_string = "".join(tb_list)

            update_str = update.to_dict() if isinstance(update, Update) else str(update)
            message = (
                "An exception was raised while handling an update\n"
                f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
                "</pre>\n\n"
                f"<pre>{html.escape(tb_string)}</pre>"
            )

            await update.message.reply_text(message, parse_mode=ParseMode.HTML)

    @auth
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("/clear will clear chat context. This may be helpful if the bot is running too slowly")

    @auth
    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info("Clearing chat context...")
        self.reset_system_context()
        await update.message.reply_text("Chat context cleared.")

    @auth
    async def reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info(f"User: {update.message.text}")
        self.chat.append({"role": "user", "content": update.message.text})
        completion_output = self.llm.create_chat_completion(
            self.chat, **self.chat_completion_kwargs)
        assistant_response = completion_output["choices"][0]["message"]["content"]
        self.chat.append({"role": "assistant", "content": assistant_response})
        logging.info(f"Assistant: {assistant_response}")
        await update.message.reply_text(assistant_response)
