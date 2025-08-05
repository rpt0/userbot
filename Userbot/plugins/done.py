import asyncio
#import datetime
from datetime import datetime
from time import time

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx
from Userbot.helper.database import dB

__MODULES__ = "Done"

def help_string(org):
    return h_s(org, "help_done")

DEFAULT_EMOJIS = {
    "BARANG": "<emoji id=5317051834639071081>💼</emoji>",
    "RUPIAH": "<emoji id=5350641884802870510>💲</emoji>",
    "WAKTU": "<emoji id=5350423812133381005>🕔</emoji>",
    "PAY": "<emoji id=5350312748574076353>💳</emoji>",
    "OWN": "<emoji id=6271365908220873700>😎</emoji>",
    "DONE": "<emoji id=5352848733488834757>✔️</emoji>",
    "THX": "<emoji id=5350740497251986696>✴️</emoji>",
    "EZ": "<emoji id=5372965329511139384>😎</emoji>",
    "LOAD": "<emoji id=5116240346656801621>❓</emoji>",
    "TOP": "<emoji id=5463071033256848094>🔝</emoji>",
    "BUYER": "<emoji id=5229045747130843073>🆔</emoji>",  
}


def get_emoji(client, alias):
    # Ambil custom emoji jika ada, jika tidak pakai default
    custom = dB.get_var(str(client.me.id), f"EMOJI_{alias}")
    return custom if custom else DEFAULT_EMOJIS.get(alias, "")


@zb.ubot("setemodone")
async def _(client, message, _):
    try:
        args = message.text.split(maxsplit=2)
        if len(args) != 3:
            await message.reply(
                f"<blockquote><b><emoji id=4918014360267260850>⛔️</emoji> Format salah!</b>\n"
                " └ Format emoji premium :   .setemodone [ALIAS] [ID EMOJI]\n"
                " └ Format emoji non premium :   .setemodone [ALIAS] [EMOJI]\n"
                " └ Alias yang didukung: BARANG, RUPIAH, WAKTU, PAY, OWN, DONE, THX, EZ, LOAD, TOP, BUYER</blockquote>"
            )
            return
        alias = args[1].upper()
        emoji = args[2]
        if alias not in DEFAULT_EMOJIS:
            await message.reply(
                f"<blockquote><b><emoji id=4918014360267260850>⛔️</emoji> Alias tidak dikenal!</b>\n"
                " └<i> Alias : BARANG, RUPIAH, WAKTU, PAY, OWN, DONE, THX, EZ, LOAD, TOP, BUYER</i></blockquote>"
            )
            return
        dB.set_var(str(client.me.id), f"EMOJI_{alias}", emoji)
        await message.reply(f"<blockquote><b><emoji id=4916036072560919511>✅</emoji>Berhasil</b><br>emoji {alias} berhasil diganti menjadi {emoji}</blockquote>")
    except Exception as e:
        await message.reply(f"Error: {e}")


@zb.ubot("adddone")
async def set_done_channel(client, message, _):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            await message.reply("<blockquote>Penggunaan: .adddone <id_channel_atau_group></blockquote>")
            return
        chan_id = args[1].strip()
        # Ambil data lama, update jadi list tanpa duplikat
        all_ids = dB.get_var(str(client.me.id), f"DONE_CHAN_{client.me.id}") or ""
        id_list = [x.strip() for x in all_ids.split(",") if x.strip()] if all_ids else []
        if chan_id not in id_list:
            id_list.append(chan_id)
            dB.set_var(str(client.me.id), f"DONE_CHAN_{client.me.id}", ",".join(id_list))
            await message.reply(f"<blockquote>ID channel/grup berhasil ditambah: <code>{chan_id}</code></blockquote>")
        else:
            await message.reply(f"<blockquote>ID channel/grup sudah ada di daftar: <code>{chan_id}</code></blockquote>")
    except Exception as e:
        await message.reply(f"Error: {e}")


@zb.ubot("listdone")
async def list_done_channel(client, message, _):
    try:
        all_ids = dB.get_var(str(client.me.id), f"DONE_CHAN_{client.me.id}") or ""
        id_list = [x.strip() for x in all_ids.split(",") if x.strip()]
        if not id_list:
            await message.reply("<blockquote>Tidak ada channel/grup yang terdaftar untuk share .donex.</blockquote>")
            return
        daftar = []
        for cid in id_list:

            try:
                ent = await client.get_chat(int(cid)) if cid.lstrip('-').isdigit() else await client.get_chat(cid)
                name = ent.title if hasattr(ent, "title") else (ent.first_name + (f" {ent.last_name}" if ent.last_name else ""))
                daftar.append(f"<b>{name}</b> <code>{cid}</code>")
            except Exception as e:
                daftar.append(f"<code>{cid}</code> <i>(tidak ditemukan/nama tidak bisa diambil)</i>")
        await message.reply("<b>Daftar channel/grup untuk share .donex:</b>\n" + "\n".join(daftar))
    except Exception as e:
        await message.reply(f"Error: {e}")

@zb.ubot("donex")
async def _(client: nlx, m, _):
    zeeb_nih = await m.reply("<emoji id=5116240346656801621>❓</emoji> Processing...")
    await asyncio.sleep(2)
    try:
        args = m.text.split(" ", 1)
        if len(args) < 2 or ',' not in args[1]:
            await m.reply_text(
                "<blockquote><b><emoji id=4918014360267260850>⛔️</emoji> Format salah !</b>\n"
                " └<i>Example Commands : .donex name item,price,payment</i></blockquote>"
            )
            return

        parts = args[1].split(",", 2)
        if len(parts) < 2:
            await m.reply_text(
                "<blockquote><b><emoji id=4918014360267260850>⛔️</emoji> Format salah !</b>\n"
                " └<i>Example Commands : .donex name item,price,payment</i></blockquote>"
            )
            return

        name_item = parts[0].strip()
        price = parts[1].strip()
        payment = parts[2].strip() if len(parts) > 2 else "Lainnya"
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        buyer_id = None
        if m.reply_to_message and getattr(m.reply_to_message, "from_user", None):
            buyer_id_full = str(m.reply_to_message.from_user.id)
            if len(buyer_id_full) > 4:
                buyer_id = buyer_id_full[:len(buyer_id_full) - 4] + "#" * 4
            else:
                buyer_id = "#" * len(buyer_id_full)
        else:
            buyer_id = None

        emoji_buyer = get_emoji(client, "BUYER")
        buyer_id_line = f"{emoji_buyer} <b>ID Pembeli:</b> <code>{buyer_id}</code>\n" if buyer_id else ""

        response = (
            f"<blockquote>{get_emoji(client,'DONE')}「 𝗣𝗘𝗠𝗕𝗔𝗬𝗔𝗥𝗔𝗡 𝗗𝗜𝗧𝗘𝗥𝗜𝗠𝗔 」 {get_emoji(client,'DONE')}\n</blockquote>"
            f"<blockquote>{get_emoji(client,'BARANG')} <b>ʙᴀʀᴀɴɢ : {name_item}</b>\n"
            f"{get_emoji(client,'RUPIAH')} <b>ɴᴏᴍɪɴᴀʟ : {price}</b>\n"
            f"{get_emoji(client,'WAKTU')} <b>ᴡᴀᴋᴛᴜ : {waktu}</b>\n"
            f"{get_emoji(client,'PAY')} <b>ᴘᴀʏᴍᴇɴᴛ : {payment}</b>\n"
            f"{buyer_id_line}</blockquote>"
            f"<blockquote>{get_emoji(client,'THX')} ᴛᴇʀɪᴍᴀᴋᴀꜱɪʜ ᴛᴇʟᴀʜ ᴏʀᴅᴇʀ\n {get_emoji(client,'LOAD')} ᴘᴇsᴀɴᴀɴ sᴇɢᴇʀᴀ ᴅɪᴘʀᴏsᴇs\n</blockquote>"
            f"<blockquote>{get_emoji(client,'OWN')} ʙʏ : <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name} {m.from_user.last_name or ''}</a></blockquote>"
        )

        replied = m.reply_to_message

        chan_ids_raw = dB.get_var(str(client.me.id), f"DONE_CHAN_{client.me.id}")
        chan_id_list = [x.strip() for x in chan_ids_raw.split(",") if x.strip()] if chan_ids_raw else []

        send_channel_error = ""
        for chan_id in chan_id_list:
            try:
                if chan_id.lstrip('-').isdigit():
                    chan_id_send = int(chan_id)
                else:
                    chan_id_send = chan_id
                if replied and getattr(replied, "photo", None):
                    photo_id = replied.photo.file_id if hasattr(replied.photo, 'file_id') else replied.photo
                    await client.send_photo(chan_id_send, photo=photo_id, caption=response)
                else:
                    await client.send_message(chan_id_send, response)
            except Exception as e:
                send_channel_error += (
                    f"\n\n<b>Gagal kirim ke <code>{chan_id}</code>!</b>\n"
                    f"<i>Pastikan bot sudah menjadi admin pada channel atau grup tujuan, dan ID sudah benar.</i>\n"
                    f"<code>{e}</code>" #@moire_mor
                )

        if replied and getattr(replied, "photo", None):
            photo_id = replied.photo.file_id if hasattr(replied.photo, 'file_id') else replied.photo
            await m.reply_photo(photo=photo_id, caption=response)
            if send_channel_error:
                await m.reply(send_channel_error)
            await zeeb_nih.delete()
            await m.delete()
        else:
            await zeeb_nih.edit(response + (send_channel_error if send_channel_error else ""))
            await m.delete()

    except Exception as e:
        await zeeb_nih.edit(f"error: {e}")

@zb.ubot("deldone")
async def del_done_channel(client, message, _):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            await message.reply("<blockquote>Penggunaan: .deldone <id_channel_atau_group></blockquote>")
            return
        chan_id = args[1].strip()
        all_ids = dB.get_var(str(client.me.id), f"DONE_CHAN_{client.me.id}") or ""
        id_list = [x.strip() for x in all_ids.split(",") if x.strip()]
        if chan_id in id_list:
            id_list.remove(chan_id)
            dB.set_var(str(client.me.id), f"DONE_CHAN_{client.me.id}", ",".join(id_list))
            await message.reply(f"<blockquote>ID channel/grup berhasil dihapus: <code>{chan_id}</code></blockquote>")
        else:
            await message.reply(f"<blockquote>ID channel/grup tidak ditemukan: <code>{chan_id}</code></blockquote>")
    except Exception as e:
        await message.reply(f"Error: {e}")

@zb.ubot("done")
async def done_command(client, message, *args):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(2)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2 or "," not in args[1]:
            await message.reply_text("<blockquote>Penggunaan: .done name item,price,payment</blockquote>")
            return

        parts = args[1].split(",", 2)
        if len(parts) < 2:
            await message.reply_text("<blockquote>Penggunaan: .done name item,price,payment</blockquote>")
            return

        name_item = parts[0].strip()
        price = parts[1].strip()
        payment = parts[2].strip() if len(parts) > 2 else "Lainnya"
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            f"<blockquote>{get_emoji(client,'DONE')}「 𝗣𝗘𝗠𝗕𝗔𝗬𝗔𝗥𝗔𝗡 𝗗𝗜𝗧𝗘𝗥𝗜𝗠𝗔 」 {get_emoji(client,'DONE')}\n</blockquote>"
            f"<blockquote>{get_emoji(client,'BARANG')} <b>ʙᴀʀᴀɴɢ : {name_item}</b>\n"
            f"{get_emoji(client,'RUPIAH')} <b>ɴᴏᴍɪɴᴀʟ : {price}</b>\n"
            f"{get_emoji(client,'WAKTU')} <b>ᴡᴀᴋᴛᴜ : {waktu}</b>\n"
            f"{get_emoji(client,'PAY')} <b>ᴘᴀʏᴍᴇɴᴛ : {payment}</b>\n</blockquote>"
            f"<blockquote>{get_emoji(client,'THX')} ᴛᴇʀɪᴍᴀᴋᴀꜱɪʜ ᴛᴇʟᴀʜ ᴏʀᴅᴇʀ\n {get_emoji(client,'LOAD')} ᴘᴇsᴀɴᴀɴ sᴇɢᴇʀᴀ ᴅɪᴘʀᴏsᴇs\n</blockquote>"
            f"<blockquote>{get_emoji(client,'OWN')} ʙʏ : <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a></blockquote>"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")

@zb.ubot("proses")
async def proses_command(client, message, *args):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(2)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2 or "," not in args[1]:
            await message.reply_text("<blockquote>Penggunaan: .proses nameitem, status</blockquote>")
            return

        parts = args[1].split(",", 1)
        if len(parts) < 1:
            await message.reply_text("<blockquote>Penggunaan: .proses nameitem, status</blockquote>")
            return

        name_item = parts[0].strip()
        status = parts[1].strip()
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            f"<blockquote>{get_emoji(client,'EZ')}「 𝗣𝗥𝗢𝗦𝗘𝗦 𝗢𝗥𝗗𝗘𝗥 」 {get_emoji(client,'EZ')}\n</blockquote>"
            f"<blockquote>{get_emoji(client,'BARANG')} <b>ʙᴀʀᴀɴɢ : {name_item}</b>\n"
            f"{get_emoji(client,'WAKTU')} <b>ᴡᴀᴋᴛᴜ : {waktu}</b>\n"
            f"{get_emoji(client,'EZ')} <b>sᴛᴀᴛᴜs : {status}</b>\n</blockquote>"
            f"<blockquote>{get_emoji(client,'OWN')} ʙʏ : <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a></blockquote>"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")

@zb.ubot("donep")
async def donep_command(client, message, *args):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(2)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2 or "," not in args[1]:
            await message.reply_text("<blockquote>Penggunaan: .donep nameitem, status</blockquote>")
            return

        parts = args[1].split(",", 1)
        if len(parts) < 1:
            await message.reply_text("<blockquote>Penggunaan: .donep nameitem, status</blockquote>")
            return

        name_item = parts[0].strip()
        status = parts[1].strip()
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            f"<blockquote>{get_emoji(client,'EZ')}「 𝗣𝗥𝗢𝗦𝗘𝗦 𝗧𝗥𝗔𝗡𝗦𝗔𝗞𝗦𝗜 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 」 {get_emoji(client,'EZ')}\n</blockquote>"
            f"<blockquote>{get_emoji(client,'BARANG')} <b>ʙᴀʀᴀɴɢ : {name_item}</b>\n"
            f"{get_emoji(client,'WAKTU')} <b>ᴡᴀᴋᴛᴜ : {waktu}</b>\n"
            f"{get_emoji(client,'EZ')} <b>sᴛᴀᴛᴜs : {status}</b>\n</blockquote>"
            f"<blockquote>{get_emoji(client,'THX')} ᴛᴇʀɪᴍᴀᴋᴀꜱɪʜ ᴛᴇʟᴀʜ ᴏʀᴅᴇʀ\n {get_emoji(client,'TOP')} ᴘʀᴏsᴇs ᴘᴇsᴀɴᴀɴ ᴛᴇʟᴀʜ sᴇʟᴇsᴀɪ\n</blockquote>"
            f"<blockquote>{get_emoji(client,'OWN')} ʙʏ : <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a></blockquote>"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")
