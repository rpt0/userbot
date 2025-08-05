import asyncio

from pyrogram.errors import ImageProcessFailed

from config import botcax_api
from Userbot import nlx
from Userbot.helper.tools import Emojik, fetch, h_s, initial_ctext, zb

__MODULES__ = "Khodam"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_kodam")


MAX_CAPTION_LENGTH = 1024


async def gen_kdm(text):
    bahan = [
        {
            "role": "system",
            "content": "Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 2000 karakter alfabet dalam plain text serta berbahasa Indonesia.",
        },
        {
            "role": "assistant",
            "content": f"Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 2000 karakter alfabet dalam plain text serta berbahasa Indonesia.",
        },
        {"role": "user", "content": text},
    ]
    url = "https://api.botcahx.eu.org/api/search/openai-custom"
    payload = {"message": bahan, "apikey": f"{botcax_api}"}
    res = await fetch.post(url, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data["result"].replace("\n", "")
    else:
        return f"{res.text}"


"""
def gen_kdm(text):
    model = genai.GenerativeModel(
        "models/gemini-1.5-flash",
        system_instruction=(
            "Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 2000 karakter alfabet dalam plain text serta berbahasa Indonesia."
        ),
    )
    try:
        response = model.generate_content(text)
        return response.text.strip()
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"
"""


async def get_name(client, message):
    if message.reply_to_message:
        if message.reply_to_message.sender_chat:
            full_name = message.reply_to_message.sender_chat.title
        first_name = message.reply_to_message.from_user.first_name
        last_name = message.reply_to_message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
    else:
        input_text = await client.extract_user(message)
        user = await client.get_users(input_text)
        first_name = user.first_name
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}"
    return full_name


async def gen_img(c, text):
    data = {"string": f"{text}"}
    head = {"accept": "image/jpeg"}
    url = (
        f"https://api.botcahx.eu.org/api/maker/text2img?text={text}&apikey={botcax_api}"
    )
    res = await fetch.get(url, headers=head)
    image_data = res.read()
    file = f"{c.me.id}.jpg"
    with open(file, "wb") as f:
        f.write(image_data)
    return file


@zb.ubot("khodam|kodam")
async def ckdm_cmd(client: nlx, message, _):
    emo = Emojik(client)
    emo.initialize()
    nama = await get_name(client, message)
    if not nama:
        return await message.reply(_("kdm_1").format(emo.gagal))
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    pros = await message.reply(_("proses").format(emo.proses, proses_))
    try:
        deskripsi_khodam = await gen_kdm(nama)
        photo = await gen_img(client, deskripsi_khodam.replace(" ", ","))
        caption = _("kdm_2").format(
            emo.sukses, nama, deskripsi_khodam, emo.profil, client.me.mention
        )
        if len(caption) > MAX_CAPTION_LENGTH:
            caption = caption[:MAX_CAPTION_LENGTH] + "..."
        try:
            await asyncio.sleep(2)
            await pros.delete()
            return await client.send_photo(
                message.chat.id,
                photo=photo,
                caption=caption,
                reply_to_message_id=message.id,
            )
        except ImageProcessFailed:
            await asyncio.sleep(2)
            teks = _("kdm_2").format(
                emo.sukses, nama, deskripsi_khodam, emo.profil, client.me.mention
            )
            await pros.delete()
            return await message.reply(teks)

    except Exception as e:
        # return await pros.edit(_("err_1").format(emo.gagal, str(e)))
        return await pros.edit(f"{e}")
