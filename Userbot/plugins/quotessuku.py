import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "QuotesSuku"

def help_string(org):
    return h_s(org, "help_quotessuku")

@zb.ubot("qjawa")
async def chat_gpt(client, message, *args):
    try:
       prs = await message.reply_text(f"<emoji id=4943239162758169437>🤩</emoji> Menjawab....")
       response = requests.get(f'https://api.botcahx.eu.org/api/random/quotesjawa?apikey=Biyy')

       try:
          if "quotes" in response.json():
             x = response.json()["quotes"]                  
             await prs.edit(
                 f"<blockquote>{x}</blockquote>"
                 )

          else:
               await message.reply_text("No 'results' key found in the response.")
       except KeyError:
            await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")

@zb.ubot("qminang")
async def chat_gpt(client, message, *args):
    try:
       prs = await message.reply_text(f"<emoji id=4943239162758169437>🤩</emoji> Menjawab....")
       response = requests.get(f'https://api.botcahx.eu.org/api/random/minangkabau?apikey=Biyy')

       try:
          if "hasl" in response.json():
             x = response.json()["hasl"]                  
             await prs.edit(
                 f"<blockquote>{x}</blockquote>"
                 )

          else:
               await message.reply_text("No 'results' key found in the response.")
       except KeyError:
            await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")

@zb.ubot("qsunda")
async def chat_gpt(client, message, *args):
    try:
       prs = await message.reply_text(f"<emoji id=4943239162758169437>🤩</emoji> Menjawab....")
       response = requests.get(f'https://api.botcahx.eu.org/api/random/sunda?apikey=Biyy')

       try:
          if "hasl" in response.json():
             x = response.json()["hasl"]                  
             await prs.edit(
                 f"<blockquote>{x}</blockquote>"
                 )

          else:
               await message.reply_text("No 'results' key found in the response.")
       except KeyError:
            await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")

@zb.ubot("qbatak")
async def chat_gpt(client, message, *args):
    try:
       prs = await message.reply_text(f"<emoji id=4943239162758169437>🤩</emoji> Menjawab....")
       response = requests.get(f'https://api.botcahx.eu.org/api/random/batak?apikey=Biyy')

       try:
          if "hasl" in response.json():
             x = response.json()["hasl"]                  
             await prs.edit(
                 f"<blockquote>{x}</blockquote>"
                 )

          else:
               await message.reply_text("No 'results' key found in the response.")
       except KeyError:
            await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")
