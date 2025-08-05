from pyrogram import Client, filters
from pyrogram.errors import (
    UsernameNotOccupied,
    UserNotParticipant,
    PeerIdInvalid
)

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "GetPP"

def help_string(org):
    return h_s(org, "help_getpp")


@zb.ubot("getpp|getprofile")
async def get_profile_pic(client, message, *args):
    target = None

    if message.reply_to_message:
        target = message.reply_to_message.from_user.id

    elif len(message.command) > 1:
        target = message.command[1]

    else:
        target = message.chat.id
        
    if not target:
        return await message.reply_text("**__Gunakan `/getpp @username`, reply user, atau kirim `.getpp` di grup/channel untuk ambil PP.__**")

    try:
        async for photo in client.get_chat_photos(target, limit=1):  # Ambil 1 foto terbaru
            await client.send_photo(
                message.chat.id,
                photo=photo.file_id,
                caption="<pre>Done✅</pre>"
            )
            return

        await message.reply_text("**__User/grup tidak memiliki foto profil__**.")

    except (UsernameNotOccupied, UserNotParticipant, PeerIdInvalid):
        await message.reply_text("**__Akun atau grup tidak ditemukan.__**")
    except Exception as e:
        await message.reply_text(f"**__Terjadi kesalahan: {str(e)}__**")
