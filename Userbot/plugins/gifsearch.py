import random
from pyrogram.types import InputMediaPhoto

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "GifSearch"

def help_string(org):
    return h_s(org, "help_gifsearch")


@zb.ubot("gif")
async def gif_cmd(client, message, *args):
    if len(message.command) < 2:
        return await message.reply(f"<code>{message.text}</code> [ǫᴜᴇʀʏ]")
    TM = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    try:
        x = await client.get_inline_bot_results(
            message.command[0], message.text.split(None, 1)[1]
        )
        saved = await client.send_inline_bot_result(
            client.me.id, x.query_id, x.results[random.randrange(len(x.results))].id
        )
    except:
        await message.reply("<b>❌ ɢɪꜰ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
        return await TM.delete()
    saved = await client.get_messages(client.me.id, int(saved.updates[1].message.id))
    await client.send_animation(
        message.chat.id, saved.animation.file_id, reply_to_message_id=message.id
    )
    await TM.delete()
    return await saved.delete()
