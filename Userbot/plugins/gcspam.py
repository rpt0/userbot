"""
yang hapus credits pantatnya bisulan
create by: https://t.me/NorSodikin
"""

import asyncio

from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait

from Userbot.helper.database import dB
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "SpamGcast"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_spmgcs")


async def flood(client, ex):
    await asyncio.sleep(ex.value)


def extract_type_and_msg(message, is_reply_text=False):
    args = message.text.split(None, 2)

    if len(args) < 2:
        return None, None

    type = args[1]

    if is_reply_text:
        msg = (
            message.reply_to_message.text
            if message.reply_to_message
            else args[2] if len(args) > 2 else None
        )
    else:
        msg = (
            message.reply_to_message
            if message.reply_to_message
            else args[2] if len(args) > 2 else None
        )

    return type, msg


total_spam_gcast = {}


async def SpamMsg(client, message, send):
    delay = dB.get_var(client.me.id, "SPAM") or 0
    await asyncio.sleep(int(delay))
    if message.reply_to_message:
        return await send.copy(message.chat.id)
    else:
        return await client.send_message(message.chat.id, send)


async def SpamGcast(client, message, send):
    total_spam_gcast[client.me.id] = 0

    blacklist = dB.get_list_from_var(client.me.id, "BLGCAST")
    delay = dB.get_var(client.me.id, "SPAM") or 0

    async def send_message(target_chat):
        await asyncio.sleep(int(delay))
        if message.reply_to_message:
            await send.copy(target_chat)
            return
        else:
            await client.send_message(target_chat, send)
            return

    async def handle_flood_wait(client, exception, target_chat):
        # await flood(client, exception.value)
        await asyncio.sleep(exception.value)
        await send_message(target_chat)

    async for dialog in client.get_dialogs():
        if (
            dialog.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}
            and dialog.chat.id not in blacklist
        ):
            try:
                await send_message(dialog.chat.id)
                total_spam_gcast[client.me.id] += 1
            except FloodWait as e:
                await handle_flood_wait(client, e, dialog.chat.id)
                total_spam_gcast[client.me.id] += 1
            except Exception:
                pass


@zb.ubot("spamgc")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    r = await message.reply(_("proses").format(em.proses, proses_))
    count, msg = extract_type_and_msg(message)
    if not msg:
        return await r.edit(_("spm_1").format(em.gagal, message.text.split()[0]))
    try:
        count = int(count)
    except Exception as error:
        return await r.edit(_("err").format(em.gagal, error))
    for x in range(int(count)):
        await SpamMsg(client, message, msg)
    return await r.edit("{}Done.".format(em.sukses))


@zb.ubot("spamg")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    r = await message.reply(_("proses").format(em.proses, proses_))
    count, msg = extract_type_and_msg(message)
    if not msg:
        return await r.edit(_("spm_1").format(em.gagal, message.text.split()[0]))
    try:
        count = int(count)
    except Exception as error:
        return await r.edit(_("err").format(em.gagal, error))

    async def run_spam():
        spam_gcast = [SpamGcast(client, message, msg) for _ in range(int(count))]
        await asyncio.gather(*spam_gcast)

    await run_spam()
    await r.edit("{}Done.".format(em.sukses))
    del total_spam_gcast[client.me.id]
    return


@zb.ubot("setdelay")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    r = await message.reply(_("proses").format(em.proses, proses_))
    count, msg = extract_type_and_msg(message)
    if count == "none":
        dB.set_var(client.me.id, "SPAM", 0)
        return await r.edit(
            "{}Spam delay berhasil diatur menjadi none".format(em.sukses)
        )
    try:
        count = int(count)
    except Exception as error:
        return await r.edit(_("err").format(em.gagal, error))
    if not count:
        return await r.edit("{}Silahkan berikan angka delay".format(em.gagal))
    dB.set_var(client.me.id, "SPAM", count)
    return await r.edit(
        "{}Spam delay berhasil disetel ke: `{}`.".format(em.sukses, count)
    )
