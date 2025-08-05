import aiohttp
from bs4 import BeautifulSoup
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Wikipedia"

def help_string(org):
    return h_s(org, "help_wikipedia")


async def wikipedia(query):
    try:
        url = f"https://id.wikipedia.org/wiki/{query}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return {'status': response.status, 'Pesan': 'Tidak Ditemukan'}
                page_content = await response.text()
                soup = BeautifulSoup(page_content, 'html.parser')          
                title = soup.find(id="firstHeading").get_text().strip()    
                thumb_tag = soup.select_one('#mw-content-text .mw-parser-output > div:nth-child(1) > table img')
                thumb = "https:" + thumb_tag['src'] if thumb_tag else "https://k.top4top.io/p_2121ug8or0.png"
                
                paragraphs = soup.select('#mw-content-text .mw-parser-output > p')
                content = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                
                return {
                    'status': response.status,
                    'result': {
                        'judul': title,
                        'thumb': thumb,
                        'isi': content
                    }
                }
    except Exception as e:
        return {'status': 404, 'Pesan': str(e)}


@zb.ubot("wiki|wikipedia")
async def wiki_handler(client, message, *args):
    text = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else None
    if not text:
        await message.reply_text('<b><i>contoh : .wiki israel</i></b>')
        return
            
    res = await wikipedia(text)    
    if res['status'] == 200:
        result = res['result']
        caption = f"""
<b>Judul:</b> {result['judul']}

<b>Penjelasan:</b>
{result['isi']}
"""

        if len(caption) > 1024:
            caption = caption[:1000] + '...'

        await client.send_photo(
            message.chat.id,
            photo= f"https://itzpire.com/file/540429176594.jpg",
            caption=caption
        )
    else:
        await message.reply_text('<b><i>Tidak Ditemukan</i></b>')
