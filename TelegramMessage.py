from telegram import InputMediaPhoto, InlineKeyboardButton, Bot, InlineKeyboardMarkup
from PollHandler import Poll
import os


igrrai_link = os.getenv("IGRRAI_LINK")
link_title = "Сообщение сообществу"


def get_photo_url(data):
    return data["photo"]["orig_photo"]["url"]


def get_album_link(data):
        return f'https://vk.com/album{data["owner_id"]}_{data["id"]}'


class Message:
    def __init__(self, bot: Bot, data):
        self.bot = bot
        self.date = data["date"]
        self.id = data["id"]

        self.photos = []
        self.links = []
        self.album = ""
        self.poll = None
        self.text = data["text"]

        self.get_attachments(data)

    def get_attachments(self, data):
        for attachment in data["attachments"]:
            if attachment["type"] == "photo":
                self.photos.append(InputMediaPhoto(get_photo_url(attachment)))

            if attachment["type"] == "album":
                self.album = get_album_link(attachment["album"])

            if attachment["type"] == "link":
                if attachment["link"]["url"] == igrrai_link or attachment["link"]["title"] == link_title:
                    self.links.append([InlineKeyboardButton(link_title, url=os.getenv("TELEGRAM_GROUP_LINK"))])

            if attachment["type"] == "poll":
                self.poll = Poll(attachment["poll"])

            if attachment["type"] == "video":
                pass

    async def send_to_tg(self, chat_id):
        if len(self.album) > 0:
            self.text = f"{self.text} \r\n {self.album}"

        if len(self.photos) == 1:
            reply_markup = InlineKeyboardMarkup(self.links)
            if len(self.text) > 1024:
                caption = self.text[:1024]
                remaining_text = self.text[1024:]
                await self.bot.send_photo(chat_id, self.photos[0].media, caption=caption, connect_timeout=60, read_timeout=60)
                await self.bot.send_message(chat_id, remaining_text, reply_markup=reply_markup, connect_timeout=60, read_timeout=60)
            else:
                await self.bot.send_photo(chat_id, self.photos[0].media, caption=self.text, reply_markup=reply_markup, connect_timeout=60, read_timeout=60)
        elif len(self.photos) > 1:
            if len(self.text) > 1024:
                imageUrl = self.photos[0].media
                caption = self.text[:1024]
                image = InputMediaPhoto(imageUrl, caption=caption)
                remaining_text = self.text[1024:]
                self.photos[0] = image
                await self.bot.send_media_group(chat_id, self.photos, connect_timeout=60, read_timeout=60)
                await self.bot.send_message(chat_id, remaining_text, connect_timeout=60, read_timeout=60)
            else:
                imageUrl = self.photos[0].media
                image = InputMediaPhoto(imageUrl, caption=self.text)
                self.photos[0] = image
                await self.bot.send_media_group(chat_id, self.photos, connect_timeout=60, read_timeout=60)

        if self.poll is not None:
            await self.bot.send_poll(chat_id, question=self.poll.question, options=self.poll.options, is_anonymous=True, allows_multiple_answers=self.poll.multiple_answers, connect_timeout=60, read_timeout=60)
