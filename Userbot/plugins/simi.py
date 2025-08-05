import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Simi"

def help_string(org):
    return h_s(org, "help_simi")


@zb.ubot("simi")
async def chat_gpt(client, message, *args):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji>mohon gunakan format\ncontoh : .simi query"
            )
        else:
            prs = await message.reply_text(f"<emoji id=5319230516929502602>🔍</emoji>menjawab....")
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://api.botcahx.eu.org/api/search/simsimi?query={a}&apikey=Biyy')

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
