import os
import json
import asyncio
import psutil
import random
import requests
import re
import platform
import subprocess
import sys
import traceback
import aiohttp
import filetype
import wget
import math
from io import BytesIO, StringIO
import psutil
from pyrogram.enums import UserStatus
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import get_event_loop
from gc import get_objects
from pyrogram.raw import *
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncio import sleep
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from bs4 import BeautifulSoup
from io import BytesIO
from pyrogram.errors.exceptions import *
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from httpx import AsyncClient, Timeout
################################################################
import random
################################################################
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping

from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (Emojik, get_time, h_s, initial_ctext, zb,
                                  start_time)


__MODULES__ = "Ping"


def help_string(org):
    return h_s(org, "help_pingst")



@zb.ubot("ping")
@zb.devs("mping")
@zb.deve("mping")
async def ping_(c, m, _):
    em = Emojik(c)
    em.initialize()
    start = datetime.now()
    await c.invoke(Ping(ping_id=0))
    end = datetime.now()
    upnya = await get_time((time() - start_time))
    duration = round((end - start).microseconds / 100000, 2)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    _ping = f"""
<blockquote><b>{em.ping}{pong_}:</b> <u>{duration}ms</u>
<b>{em.pong}{uptime_}:</b> <u>{upnya}</u>
<b>{em.owner}{owner_}</b></blockquote>"""
    return await m.reply(_ping)


@zb.devs("teston")
@zb.deve("teston")
async def ping_(c, m, _):
    em = Emojik(c)
    em.initialize()
    start = datetime.now()
    await c.invoke(Ping(ping_id=0))
    end = datetime.now()
    duration = round((end - start).microseconds / 100000, 2)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    _ping = f"""
<b>{em.ping}{pong_}:</b> <u>{duration}ms</u>
<b>{em.owner}{owner_}</b>
<blockquote>ᴜsᴇʀʙᴏᴛ ᴏɴ ʙᴀɴɢ tin</blockquote>
<blockquote><b>@Boyszzzz</b></blockquote>"""
    return await m.reply(_ping)



def add_absen(c, text):
    auto_text = dB.get_var(c.me.id, "TEXT_ABSEN") or []
    auto_text.append(text)
    dB.set_var(c.me.id, "TEXT_ABSEN", auto_text)


@zb.deve("absen")
@zb.devs("absen")
async def _(c: nlx, message, _):
    txt = dB.get_var(c.me.id, "TEXT_ABSEN")
    if len(message.command) == 1:
        if not txt:
            return
        try:
            psn = random.choice(txt)
            return await message.reply(psn)
        except:
            pass
    else:
        command, variable = message.command[:2]
        if variable.lower() == "text":
            for x in nlx._ubot:
                value = " ".join(message.command[2:])
                add_absen(x, value)

        else:
            return
