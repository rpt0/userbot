import asyncio
import random

from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Tagall"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_tagall")


berenti = False


def random_emoji():
    emojis = "🍦 🎈 🎸 🌼 🌳 🚀 🎩 📷 💡 🏄‍♂️ 🎹 🚲 🍕 🌟 🎨 📚 🚁 🎮 🍔 🍉 🎉 🎵 🌸 🌈 🏝️ 🌞 🎢 🚗 🎭 🍩 🎲 📱 🏖️ 🛸 🧩 🚢 🎠 🏰 🎯 🥳 🎰 🛒 🧸 🛺 🧊 🛷 🦩 🎡 🎣 🏹 🧁 🥨 🎻 🎺 🥁 🛹".split(
        " "
    )
    return random.choice(emojis)


@zb.ubot("tagall|all")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    global berenti
    chat_id = m.chat.id
    admins = False
    berenti = True
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    progres = await m.reply(_("proses").format(em.proses, proses_))

    try:
        administrator = []
        async for admin in c.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            if not berenti:
                break
            administrator.append(admin)
        await c.get_chat_member(chat_id, m.from_user.id)
        admins = administrator
    except Exception as e:
        return await m.reply(_("err").format(em.gagal, str(e)))

    if not admins:
        await m.reply(_("ment_1").format(em.gagal))
        return

    if not m.reply_to_message and len(m.command) < 2:
        await m.reply(_("ment_2").format(em.gagal))
        return

    send = c.get_arg(m)
    text = " ".join(m.command[1:])
    mention_texts = []
    members = c.get_chat_members(chat_id)
    berenti = True
    count = 0

    async for member in members:
        if not berenti:
            break
        if not member.user.is_bot and member.status != "user_status_empty":
            mention_texts.append(f"[{random_emoji()}](tg://user?id={member.user.id})")
            count += 1
            if len(mention_texts) == 4:
                mention_text = f"{send}\n\n"
                mention_text += " ".join(mention_texts)
                try:
                    await c.send_message(chat_id, mention_text)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await c.send_message(chat_id, mention_text)
                await asyncio.sleep(2.5)
                mention_texts = []

    if mention_texts:
        repl_text = c.get_arg(m)
        if repl_text:
            repl_text += "\n\n" + "\n".join(mention_texts)
        else:
            repl_text = " ".join(mention_texts)
        try:
            await c.send_message(chat_id, repl_text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await c.send_message(chat_id, repl_text)
        await asyncio.sleep(2.5)

    berenti = False
    await progres.delete()
    await m.reply(_("ment_5").format(em.sukses, count))
    return


@zb.ubot("stoptag")
async def stop_tagall(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    global berenti
    if not berenti:
        await m.reply(_("ment_3").format(em.gagal))
        return

    berenti = False
    return await m.reply(_("ment_4").format(em.sukses))
