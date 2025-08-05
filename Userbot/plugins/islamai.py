import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "IslamAi"

def help_string(org):
    return h_s(org, "help_islamai")

@zb.ubot("islamai")
async def chat_gpt(client, message, *args):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji>mohon gunakan format\ncontoh : .islamai asal usul al-quran"
            )
        else:
            prs = await message.reply_text(f"<emoji id=4943239162758169437>🤩</emoji>Menjawab....")
            hai = message.text.split(' ', 1)[1]
            response = requests.get(f'https://vapis.my.id/api/islamai?q={hai}')

            try:
                if "result" in response.json():
                    x = response.json()["result"]                  
                    await prs.edit(
                      f"<blockquote>{x}</blockquote>"
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")
      
