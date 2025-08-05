import requests
import filetype
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "RemoveBg"

def help_string(org):
    return h_s(org, "help_removebg")


def upload_media(media_path: str):
    with open(media_path, "rb") as file:
        file_data = file.read()
        ext = filetype.guess_extension(file_data) or "unknown"

    files = {"fileToUpload": (f"file.{ext}", open(media_path, "rb"))}
    data = {"reqtype": "fileupload"}
    
    response = requests.post("https://catbox.moe/user/api.php", files=files, data=data)
    
    if response.status_code == 200:
        return response.text.strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

@zb.ubot("rmbg|removebg")
async def remove_bg(client, message, *args):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("Silakan reply ke gambar yang ingin dihapus background-nya.")

    photo = await message.reply_to_message.download()
    image_url = upload_media(photo)

    if "Error" in image_url:
        return await message.reply(f"Gagal mengunggah gambar: {image_url}")

    REMOVE_BG_API = f"https://api.botcahx.eu.org/api/tools/removebg?url={image_url}&apikey=Priaindia"
    
    response = requests.get(REMOVE_BG_API)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status"):
            result_url = data["url"]["result"]
            await message.reply_photo(result_url, caption="Berhasil menghapus background!")
        else:
            await message.reply("Gagal menghapus background.")
    else:
        await message.reply(f"Error: {response.status_code}")
