import aiohttp
import requests
from bs4 import BeautifulSoup
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Alkitab"

def help_string(org):
    return h_s(org, "help_alkitab")


@zb.ubot("alkitab")
async def search_alkitab(client, message, *args):
    text = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
    if not text:
        await message.reply("<b>uhm.. teksnya mana?</b>\n<blockquote><b>contoh: .alkitab kejadian</b></blockquote>")
        return

    url = f"https://alkitab.me/search?q={text}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }
    
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    result = []
    for div in soup.find_all('div', class_='vw'):
        p_tag = div.find('p')
        if p_tag:
            teks = p_tag.get_text(strip=True)
            link = div.find('a')['href']
            title = div.find('a').get_text(strip=True)
            result.append({'teks': teks, 'link': link, 'title': title})

    caption = "────────".join(
        f"""
<blockquote><b>{v['title']}
{v['teks']}</b></blockquote>
""" for v in result)
    
    await message.reply(caption if caption else "Tidak ada hasil yang ditemukan.")
