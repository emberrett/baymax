from telegram import Update
from telegram.ext import ContextTypes
import logging
from llama_cpp import Llama
from dotenv import load_dotenv
import os
from functools import cache


@cache
def get_llm():
    load_dotenv()
    model = os.environ["MODEL"]
    return Llama(
        model_path=os.path(f"./{model}"),
        chat_format="llama-3",
        n_gpu_layers=int(os.environ["N_GPU_LAYERS"])
    )


@cache
def get_chat_id():
    load_dotenv()
    return int(os.environ["TELEGRAM_CHAT_ID"])


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
