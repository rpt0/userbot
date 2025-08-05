import requests

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Tiktok"

def help_string(org):
    return h_s(org, "help_tiktok")
@zb.ubot("tt")
async def tiktok_handler(client, message, *args):
    if len(message.command) < 2:
        await message.reply("linknya mana?")
        return

    url = message.command[1]
    proses_message = await message.reply("```\nprosess...```")

    try:
        response = requests.get(f"https://api.diioffc.web.id/api/download/tiktok?url={url}")
        data = response.json()

        if "images" in data["result"]:
            for img_url in data["result"]["images"]:
                await client.send_photo(message.chat.id, img_url)
        else:
            video_url = data["result"]["play"]
            video_caption = data["result"]["title"]
            await client.send_video(message.chat.id, video_url, caption=f"```\ndone ᣃ࿈ ᴜsᴇʀʙᴏᴛ-ᴠɪᴘ ࿈ᣄ```")

            audio_url = data["result"]["music_info"]["play"]
            audio_title = data["result"]["music_info"]["title"]
            audio_author = data["result"]["music_info"]["author"]
            audio_cover = data["result"]["music_info"]["cover"]

            await client.send_audio(
                message.chat.id,
                audio_url,
                title=audio_title,
                performer=audio_author,
                thumb=audio_cover
            )

        await proses_message.delete()

    except Exception as e:
        await proses_message.delete()
        await message.reply(f"Error \n{e}")
