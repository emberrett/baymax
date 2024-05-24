from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
from llama_cpp import Llama
import html
import traceback
import json
import re


class Baymax():
    def __init__(
            self,
            chat_id: int,
            model: Llama,
    ):
        self.chat_id = chat_id
        self.model = model
        self.context: list[dict]
        self.system_prompt: str
        self.set_system_context()

    def set_system_context(self):
        with open("prompt.txt", "r") as prompt:
            prompt = prompt.read().replace('\n', '')
            self.context = [{"role": "system",
                            "content": prompt}]

    def get_chat_id(self):
        return self.get_chat_id

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
        self.set_system_context()
        await update.message.reply_text("Chat context cleared.")

    @auth
    async def reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info("User requested ")
        self.context.append({"role": "user", "content": update.message.text})
        output = self.model.create_chat_completion(self.context, temperature=0.5, repeat_penalty=1.2, top_p=0.95)
        content = output["choices"][0]["message"]["content"]
        self.context.append({"role": "assistant", "content": content})
        await update.message.reply_text(content)
