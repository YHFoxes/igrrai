import asyncio
import atexit
import json
import os
import sys
import time
from typing import Sequence

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

import vk_api
from telegram import Bot
from TelegramMessage import Message

module = sys.modules[__name__]
token = os.getenv("VK_TOKEN")
channel_id = os.getenv("CHANEL_ID")
telegram_token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(telegram_token)
file = "data.json"
posts = []


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Данные успешно сохранены в файл {filename}")


def load_from_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Данные успешно загружены из файла {filename}")
        return data
    else:
        empty_data = []
        save_to_json(empty_data, filename)
        return empty_data


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Я эхо-бот. Напиши мне что-нибудь, и я повторю.')


async def echo(update: Update, context: CallbackContext):
    user_message = update.message.text
    await update.message.reply_text(user_message)


async def main():
    application = Application.builder().bot(bot).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await application.start_polling()
    await application.idle()

def onExit(test):
    print(test)


async def send(messages: Sequence[Message]):
    for message in messages:
        await message.send_to_tg(channel_id)
        time.sleep(12)


if __name__ == '__main__':
    asyncio.run(main())

    """
    atexit.register(onExit, posts)
    vk_session = vk_api.VkApi(token=token)
    api = vk_session.get_api()

    posts = load_from_json(file)

    while True:
        resp = api.wall.get(domain=os.getenv("VK_DOMAIN"), count=100)
        messages = []

        for item in reversed(resp['items']):
            difference_in_seconds = time.time() - item["date"]
            difference_in_hours = difference_in_seconds / 3600
            if round(difference_in_hours) < 12 and item['id'] not in posts:
                print(f"Разница между датами: {round(difference_in_hours)} часа")
                posts.append(item['id'])
                save_to_json(posts, file)
                messages.append(Message(bot, item))

        asyncio.run(send(messages))
        time.sleep(15)
    """

