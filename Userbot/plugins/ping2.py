import os
import json
import asyncio
import psutil
# import speedtest
from speedtest import Speedtest
import random

from datetime import datetime
from gc import get_objects
from time import time
from config import CMD_HELP, log_userbot, nama_bot, owner_id
from pyrogram.raw import *
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Userbot import nlx
from Userbot.helper.tools import (Emojik, get_time, h_s, initial_ctext, zb,
                                  start_time)

__MODULES__ = "Ping2"

def help_string(org):
    return h_s(org, "help_ping2")
    
class speed:
    SpeedTest = (
        "Speedtest started at `{start}`\n"
        "Ping ➠ `{ping}` ms\n"
        "Download ➠ `{download}`\n"
        "Upload ➠ `{upload}`\n"
        "ISP ➠ __{isp}__"
    )

    NearestDC = "Country: `{}`\n" "Nearest Datacenter: `{}`\n" "This Datacenter: `{}`"

async def _(client, message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    uptime = await get_time((time() - start_time))
    delta_ping_formatted = round((end - start).microseconds / 10000, 2)
    babi = client.me.is_premium
    if babi:
        _ping = f"""
<blockquote>{pantek} : {str(delta_ping_formatted).replace('.', ',')} ms
{ngentod} : <code>{client.me.mention}</code>
{kontol} : <code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)
    else:
        _ping = f"""
<blockquote>{pantek} : {str(delta_ping_formatted).replace('.', ',')} ms
{ngentod} : <code>{client.me.mention}</code>
{kontol} : <code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)

@zb.ubot("ping1")
async def _(client, message, *args):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    uptime = await get_time((time() - start_time))
    delta_ping_formatted = round((end - start).microseconds / 10000, 2)
    xx = await message.edit("𖣐")
    await asyncio.sleep(0.3)
    await xx.edit("𖣐𖣐")
    await asyncio.sleep(0.3)
    await xx.edit("𖣐𖣐𖣐")
    await asyncio.sleep(0.3)
    await xx.edit("𖣐𖣐𖣐𖣐")
    await asyncio.sleep(0.3)
    await xx.edit("𖣐𖣐𖣐𖣐𖣐")
    await asyncio.sleep(0.3)
    await xx.edit("⚡")
    await asyncio.sleep(0.5)
    babi = client.me.is_premium
    if babi:
        _ping = f"""
<blockquote>⎆ <emoji id=5260547274957672345>🎲</emoji> ᴘɪɴɢ : {str(delta_ping_formatted).replace('.', ',')} ms
⎆ <emoji id=5235948055928262102>⭐</emoji> ᴜᴘᴛɪᴍᴇ : {uptime}
⎆ <emoji id=5204015897500469606>😢</emoji> ᴋɪɴɢ : <code>{client.me.mention}</code>
⎆ <emoji id=5194979342144260681>😂</emoji> ᴡᴀʀʀɪᴏʀ : <code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)
    else:
        _ping = f"""
<blockquote>⎆ <emoji id=5260547274957672345>🎲</emoji> ᴘɪɴɢ : {str(delta_ping_formatted).replace('.', ',')} ms
⎆ <emoji id=5235948055928262102>⭐</emoji> ᴜᴘᴛɪᴍᴇ : {uptime}
⎆ <emoji id=5204015897500469606>😢</emoji> ᴋɪɴɢ : <code>{client.me.mention}</code>
⎆ <emoji id=5194979342144260681>😂</emoji> ᴡᴀʀʀɪᴏʀ : <code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)

@zb.ubot("ping2")
async def _(client, message, *args):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    uptime = await get_time((time() - start_time))
    delta_ping_formatted = round((end - start).microseconds / 10000, 2)
    xx = await message.edit("★ PING ★")
    await asyncio.sleep(0.5)
    await xx.edit("★★ PING ★★")
    await asyncio.sleep(0.5)
    await xx.edit("★★★ PING ★★★")
    await asyncio.sleep(0.5)
    await xx.edit("★★★★ PING ★★★★")
    await asyncio.sleep(0.5)
    await xx.edit("✦҈͜͡➳ PONG!")
    await asyncio.sleep(0.5)
    await xx.edit("🌩")
    await asyncio.sleep(0.5)
    babi = client.me.is_premium
    if babi:
        _ping = f"""
<blockquote><emoji id=5897929355216034070>🤩</emoji> ❃ **Ping !!**
{str(delta_ping_formatted).replace('.', ',')} ms

<emoji id=5900041834880571364>😈</emoji> ❃ **Uptime -**
{uptime}

<emoji id=5897741587835786345>🔥</emoji> **✦҈͜͡➳ Master :**
<code>{client.me.mention}</code>

<emoji id=5900145373657176313>😂</emoji> **✦҈͜͡➳ Bot :**
<code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)
    else:
        _ping = f"""
<blockquote><emoji id=5897929355216034070>🤩</emoji> ❃ **Ping !!**
{str(delta_ping_formatted).replace('.', ',')} ms

<emoji id=5900041834880571364>😈</emoji> ❃ **Uptime -**
{uptime}

<emoji id=5897741587835786345>🔥</emoji> **✦҈͜͡➳ Master :**
<code>{client.me.mention}</code>

<emoji id=5900145373657176313>😂</emoji> **✦҈͜͡➳ Bot :**
<code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)

@zb.ubot("p")
async def _(client, message, *args):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    uptime = await get_time((time() - start_time))
    delta_ping_formatted = round((end - start).microseconds / 10000, 2)
    xx = await message.edit("▩▩▩▩▩<emoji id=5474431664136407043>🚬</emoji>")
    await asyncio.sleep(0.3)
    await xx.edit("▩▩▩▩■<emoji id=5474431664136407043>🚬</emoji>")
    await asyncio.sleep(0.3)
    await xx.edit("▩▩▩■■<emoji id=5474431664136407043>🚬</emoji>")
    await asyncio.sleep(0.3)
    await xx.edit("▩▩■■■<emoji id=5474431664136407043>🚬</emoji>")
    await asyncio.sleep(0.3)
    await xx.edit("▩■■■■<emoji id=5474431664136407043>🚬</emoji>")
    await asyncio.sleep(0.3)
    await xx.edit("■■■■■<emoji id=5474431664136407043>🚬</emoji>")
    await asyncio.sleep(0.3)
    await xx.edit("<emoji id=5229011542011299168>👑</emoji>")
    await asyncio.sleep(0.5)
    babi = client.me.is_premium
    if babi:
        _ping = f"""
<blockquote>⎆<emoji id=5963085452205362622>🤯</emoji> ᴘɪɴɢ : {str(delta_ping_formatted).replace('.', ',')} ms
⎆ <emoji id=5456258235872863332>🎁</emoji> ᴜᴘᴛɪᴍᴇ : {uptime}
⎆ <emoji id=5870836972095803022>😎</emoji> ᴋɪɴɢᴢ : <code>{client.me.mention}</code>
⎆ <emoji id=5463335865235288297>🤬</emoji> ᴡᴀʀʀɪᴏʀ : <code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)
    else:
        _ping = f"""
<blockquote>⎆<emoji id=5963085452205362622>🤯</emoji> ᴘɪɴɢ : {str(delta_ping_formatted).replace('.', ',')} ms
⎆ <emoji id=5456258235872863332>🎁</emoji> ᴜᴘᴛɪᴍᴇ : {uptime}
⎆ <emoji id=5870836972095803022>😎</emoji> ᴋɪɴɢᴢ : <code>{client.me.mention}</code>
⎆ <emoji id=5463335865235288297>🤬</emoji> ᴡᴀʀʀɪᴏʀ : <code>{nama_bot}</code></blockquote>
"""
        await message.reply(_ping)
        