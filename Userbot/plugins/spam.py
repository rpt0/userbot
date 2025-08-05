################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import asyncio

from pyrogram.errors import FloodWait, SlowmodeWait, UserBannedInChannel

from config import NO_GCAST, the_cegers
from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, zb

dispam = []

berenti = False

__MODULES__ = "Spam"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_spam")


@zb.ubot("spam")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    global berenti
    if m.chat.id in NO_GCAST:
        return await m.reply("ANAK KONTOL MALAH MAU SPAM DIGC SUPPORT GOBLOK")
    reply = m.reply_to_message
    berenti = True

    if reply:
        try:
            count_message = int(m.command[1])
            for i in range(count_message):
                if not berenti:
                    break
                await reply.copy(m.chat.id)
                await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await reply.copy(m.chat.id)
            await asyncio.sleep(0.1)
        except Exception as error:
            return await m.reply(str(error))
    else:
        if len(m.command) < 2:
            return await m.reply(_("spm_1").format(em.gagal, m.text.split()[0]))
        else:
            try:
                count_message = int(m.command[1])
                for i in range(count_message):
                    if not berenti:
                        break
                    await m.reply(
                        m.text.split(None, 2)[2],
                    )
                    await asyncio.sleep(0.1)
            except UserBannedInChannel:
                return await m.reply(_("lim_er").format(em.gagal))
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await m.reply(
                    m.text.split(None, 2)[2],
                )
                await asyncio.sleep(0.1)
            except Exception as error:
                return await m.reply(str(error))
    berenti = False
    return await m.delete()


@zb.ubot("dspam")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    global berenti

    reply = m.reply_to_message
    if m.chat.id in NO_GCAST:

        return await m.reply("ANAK KONTOL MALAH MAU SPAM DIGC SUPPORT GOBLOK")
    berenti = True
    if reply:
        try:
            count_message = int(m.command[1])
            count_delay = int(m.command[2])
        except Exception as error:
            return await m.reply(str(error))
        for i in range(count_message):
            if not berenti:
                break
            try:
                await reply.copy(m.chat.id)
                await asyncio.sleep(count_delay)
            except UserBannedInChannel:
                return await m.reply(_("lim_er").format(em.gagal))
            except SlowmodeWait as e:
                await asyncio.sleep(e.value)
                await reply.copy(m.chat.id)
                await asyncio.sleep(count_delay)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await reply.copy(m.chat.id)
                await asyncio.sleep(count_delay)
    else:
        if len(m.command) < 4:
            return await m.reply(_("spm_2").format(em.gagal, m.text.split()[0]))
        else:
            try:
                count_message = int(m.command[1])
                count_delay = int(m.command[2])
            except Exception as error:
                return await m.reply(str(error))
            for i in range(count_message):
                if not berenti:
                    break
                try:
                    await m.reply(m.text.split(None, 3)[3])
                    await asyncio.sleep(count_delay)
                except UserBannedInChannel:
                    return await m.reply(_("lim_er").format(em.gagal))
                except SlowmodeWait as e:
                    await asyncio.sleep(e.value)
                    await m.reply(m.text.split(None, 3)[3])
                    await asyncio.sleep(count_delay)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await m.reply(m.text.split(None, 3)[3])
                    await asyncio.sleep(count_delay)
    berenti = False
    return await m.delete()


@zb.ubot("cspam")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    global berenti
    if not berenti:
        return await m.reply(_("spm_3").format(em.gagal))
    berenti = False
    return await m.reply(_("spm_4").format(em.sukses))


@zb.ubot("dspamfw")
async def _(c: nlx, message, _):
    em = Emojik(c)
    em.initialize()

    if message.chat.id in NO_GCAST:
        for x in the_cegers:
            if c.me.id == x:
                continue
            else:
                return await message.reply(
                    "ANAK KONTOL MALAH MAU SPAM DIGC SUPPORT GOBLOK"
                )

    proses = await message.reply("{}Done!!".format(em.proses))
    # berenti = True

    try:
        la, count_str, delay_str, link = message.text.split(maxsplit=3)
        count = int(count_str)
        delay = int(delay_str)
    except ValueError:
        return await proses.edit(_("spm_5").format(em.gagal, message.text.split()[0]))

    chat_id, message_id = link.split("/")[-2:]

    try:
        chat_id = int(chat_id)
    except ValueError:
        pass

    message_id = int(message_id)

    for la in range(count):
        try:

            await c.get_messages(chat_id, message_id)
            await c.forward_messages(message.chat.id, chat_id, message_ids=message_id)
            await asyncio.sleep(delay)
        except UserBannedInChannel:
            return await message.reply(_("lim_er").format(em.gagal))
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await c.forward_messages(message.chat.id, chat_id, message_ids=message_id)
            await asyncio.sleep(delay)
        except SlowmodeWait:
            continue
        except Exception as e:
            if (
                "CHAT_SEND_PHOTOS_FORBIDDEN" in str(e)
                or "CHAT_SEND_MEDIA_FORBIDDEN" in str(e)
                or "USER_RESTRICTED" in str(e)
            ):
                await message.reply(_("spm_6").format(em.gagal))
            else:
                await proses.reply(_("err").format(em.gagal, e))
            break

    await message.delete()
    return await proses.delete()
