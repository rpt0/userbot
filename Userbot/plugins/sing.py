from pyrogram.errors import MessageTooLong

from config import botcax_api
from Userbot.helper.tools import Emojik, get, h_s, initial_ctext, zb, paste

__MODULES__ = "Lyrics"


def help_string(org):
    return h_s(org, "help_sing")


@zb.ubot("chord")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    prs = await message.reply_text(_("proses").format(em.proses, proses_))
    rep = message.reply_to_message
    if len(message.command) < 2 and not rep:
        return await prs.edit(
            f"{em.gagal}**Silahkan berikan judul lagu atau balas ke pesan teks.!!**"
        )
    arg = client.get_arg(message).replace(" ", "+")
    url = f"https://api.botcahx.eu.org/api/search/chord?song={arg}&apikey={botcax_api}"
    respon = await get(url)
    if respon["status"] == True:
        data = respon["result"]
        kunci = data["chord"]

        msg = f"{em.sukses}<blockquote>**Judul: {arg.replace('+', ' ')}\nChord:**\n\n{kunci}</blockquote>"
        try:
            return await prs.edit(msg)
        except MessageTooLong:
            await prs.delete()
            konten = str(msg)
            link = await paste(konten)
            return await message.reply(
                f"{em.sukses}**[Klik Disini]({link}) Untuk Melihat Chord.**",
                disable_web_page_preview=True,
            )
    else:
        return await prs.edit(f"**{em.gagal}Maaf!! Sepertinya server sedang error!**")


@zb.ubot("lirik")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    prs = await message.reply_text(_("proses").format(em.proses, proses_))
    rep = message.reply_to_message
    if len(message.command) < 2 and not rep:
        return await prs.edit(
            f"{em.gagal}**Silahkan berikan judul lagu atau balas ke pesan teks.!!**"
        )
    arg = client.get_arg(message).replace(" ", "+")
    url = f"https://api.botcahx.eu.org/api/search/lirik?lirik={arg}&apikey={botcax_api}"
    respon = await get(url)
    if respon["status"] == True:
        data = respon["result"]
        judul = f"{arg.replace('+', ' ')}" or data["title"]
        lirik = data["lyrics"]
        artis = data["artist"]
        msg = f"{em.sukses}<blockquote>**Judul: {judul}\n\Artist: {artis}\nLirik:**\n\n{lirik}</blockquote>"
        try:
            return await prs.edit(msg)
        except MessageTooLong:
            await prs.delete()
            konten = str(msg)
            link = await paste(konten)
            return await message.reply(
                f"{em.sukses}**[Klik Disini]({link}) Untuk Melihat Chord.**",
                disable_web_page_preview=True,
            )
    else:
        return await prs.edit(f"**{em.gagal}Maaf!! Sepertinya server sedang error!**")
