import requests
import os
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Xnxx"

def help_string(org):
    return h_s(org, "help_xnxx")


@zb.ubot("xnxx")
async def random_bokep(client, message, *args):
    try:
        query = message.text.split()[1:]
        if not query:
            await message.reply("🚩 Gunakan format: `.xnxx [kata kunci]`\n\nContoh: `.xnxx japanese teacher` atau `.xnxx school girl cute`")
            return
        search_query = " ".join(query[:4])
        
        status_msg = await message.reply(f"🔍 Mencari video untuk: **{search_query}**...")

        api_url = f"https://api.botcahx.eu.org/api/search/xnxx?query={search_query}&apikey=Biyy"
        
        response = requests.get(api_url)
        response.raise_for_status()
        api = response.json()

        results = api.get('result', [])
        if not results:
            await status_msg.edit(f"🚩 Tidak ditemukan hasil untuk: **{search_query}**")
            return

        data = results[0]

        capt = f"""
<blockquote>乂 Hasil Pencarian: {search_query}
◦ Title : {data.get('title', 'N/A')}
◦ Views : {data.get('views', 'N/A')}
◦ Quality : {data.get('quality', 'N/A')}
◦ Duration : {data.get('duration', 'N/A')}
◦ **[🔗 Link ]({data.get('link', 'N/A')})</blockquote>
"""

        await status_msg.edit(f"📥 Mengunduh video dari: **{data.get('title', 'N/A')}**...")

        dl_url = f"https://api.botcahx.eu.org/api/download/xnxxdl?url={data['link']}&apikey=Biyy"
        dl_response = requests.get(dl_url)
        dl_response.raise_for_status()
        dl_data = dl_response.json()
        video_url = dl_data.get('result', {}).get('url')

        if not video_url:
            await status_msg.edit("🚩 Gagal mendapatkan URL video.")
            return

        video_path = "video.mp4"

        await status_msg.edit("📥 Sedang mengunduh video, harap tunggu...")
        with requests.get(video_url, stream=True) as vid_res:
            vid_res.raise_for_status()
            with open(video_path, "wb") as f:
                for chunk in vid_res.iter_content(chunk_size=8192):
                    f.write(chunk)

        await status_msg.edit("📤 Mengunggah video ke Telegram...")
        
        await client.send_video(message.chat.id, video_path, caption=capt)
        os.remove(video_path)

        await status_msg.delete()

    except requests.exceptions.RequestException as e:
        await message.reply(f"🚩 Terjadi Kesalahan Saat Mengakses API: {str(e)}")
    except Exception as e:
        await message.reply(f"🚩 Terjadi Kesalahan: {str(e)}")
        
