from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
from llama_cpp import Llama
from dotenv import load_dotenv
import os
from functools import lru_cache
import html
import traceback
import json
import re


@lru_cache
def get_llm():
    load_dotenv()
    model = os.environ["MODEL"]
    n_ctx = int(os.environ["MAX_CONTEXT"])
    return Llama(
        model_path=f"models/{model}",
        chat_format="llama-3",
        n_ctx=n_ctx,
        n_gpu_layers=int(os.environ["N_GPU_LAYERS"])
    )


@lru_cache
def get_chat_id():
    load_dotenv()
    return int(os.environ["TELEGRAM_CHAT_ID"])


async def startup(self):
    await self.bot.sendMessage(get_chat_id(), 'Baymax ready to assist.')


def set_system_context():
    global chat_context
    with open("prompt.txt", "r") as prompt:
        prompt = prompt.read().replace('\n', '')
        chat_context = [{"role": "system",
                         "content": prompt}]


def auth(func):
    def wrapper(*args, **kwargs):
        if args[0].message.chat_id != get_chat_id():
            return unauthorized(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper


async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Unauthorized.")


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
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("/clear will clear chat context. This may be helpful if the bot is running too slowly")


@auth
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Clearing chat context...")
    set_system_context()
    await update.message.reply_text("Chat context cleared.")


@auth
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("User requested ")
    chat_context.append({"role": "user", "content": update.message.text})
    llm = get_llm()
    output = llm.create_chat_completion(chat_context, max_tokens=128)
    content = output["choices"][0]["message"]["content"]
    chat_context.append({"role": "assistant", "content": content})
    await update.message.reply_text(content)
