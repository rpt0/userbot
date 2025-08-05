import requests
import random
import wget
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "QuotesAnime"

def help_string(org):
    return h_s(org, "help_quotesanime")

def get_random_quotes(query):
    API_URL = "https://api.siputzx.my.id/api/r/quotesanime"
    params = {
        "type": "quotesanime",
        "count": 0
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") and "data" in data:
            quote_list = data["data"]
            if quote_list:
                hasil = random.choice(quote_list)
                return (
                    f"<blockquote><b><emoji id=6206162931663508973>💜</emoji><emoji id=6204012166660494973>💜</emoji> Karakter : **{hasil['karakter']}**\n"
                    f"<emoji id=6204141080103884640>🩶</emoji><emoji id=6204020391522866140>🩶</emoji> Anime : {hasil['anime']}\n</b></blockquote>"
                    f"<blockquote><b><emoji id=6206155965226554117>💙</emoji><emoji id=6206278032492074356>💙</emoji> Quotes : {hasil['quotes']}\n</b></blockquote>"
                    f"<blockquote><b><emoji id=6203954029983175918>🩵</emoji><emoji id=6206191192548315925>🩵</emoji> Link 🔗 [Sumber]({hasil['link']})</b></blockquote>"
                )  
                
        return "<blockquote><b><emoji id=5215204871422093648>❌</emoji> Tidak ditemukan quotes yang sesuai.</b></blockquote>"

    except requests.exceptions.Timeout:
        return "<blockquote><b><emoji id=5454415424319931791>⌛️</emoji> Permintaan waktu habis. Coba lagi nanti.</b></blockquote>"
    except requests.exceptions.RequestException as e:
        return f"<blockquote><b><emoji id=5213205860498549992>⚠️</emoji> Terjadi kesalahan saat mengambil quotes: {e}</b></blockquote>"

@zb.ubot("qanime")
async def quotes_handler(client, message, *args):
    query = " ".join(message.command[1:])
    await message.reply("<blockquote><b><i><emoji id=4967797089971995307>🔍</emoji> Sedang mencari quote...</i></b></blockquote>")

    quotes_text = get_random_quotes(query)

    await message.reply(quotes_text, disable_web_page_preview=True)
