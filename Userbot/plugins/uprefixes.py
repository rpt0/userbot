################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Prefixes"

USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_upref")


@zb.ubot("setprefix")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.command) < 2:
        return await xx.edit(_("upref_1").format(em.gagal, m.text.split()[0]))
    else:
        mepref = []
        for x in m.command[1:]:
            if x.lower() == "none":
                mepref.append("")
            else:
                mepref.append(x)
        try:
            c.set_prefix(c.me.id, mepref)
            dB.set_pref(c.me.id, mepref)
            parsed = " ".join(f"{x}" for x in mepref)
            return await xx.edit(_("upref_2").format(em.sukses, parsed))
        except Exception as er:
            await xx.edit(_("err").format(em.gagal, er))


# @zb.devs("batu")
async def _(c: nlx, m, _):
    return await c.send_reaction(chat_id=m.chat.id, message_id=m.id, emoji="🗿")


# @zb.devs("kiss")
async def _(c: nlx, m, _):
    return await c.send_reaction(chat_id=m.chat.id, message_id=m.id, emoji="❤️")


# @zb.devs("nangis")
async def _(c: nlx, m, _):
    return await c.send_reaction(chat_id=m.chat.id, message_id=m.id, emoji="😭")


@zb.devs("batu")
async def _(c: nlx, m, _):
    for x in nlx._ubot:
        try:
            rep = m.reply_to_message
            if rep:
                anu = rep.id
            else:
                anu = m.id
            await x.send_reaction(chat_id=m.chat.id, message_id=anu, emoji="🗿")
        except:
            continue


@zb.devs("lope")
async def _(c: nlx, m, _):
    for x in nlx._ubot:
        try:
            rep = m.reply_to_message
            if rep:
                anu = rep.id
            else:
                anu = m.id
            await x.send_reaction(chat_id=m.chat.id, message_id=anu, emoji="❤️")
        except:
            continue


@zb.devs("nangis")
async def _(c: nlx, m, _):
    for x in nlx._ubot:
        try:
            rep = m.reply_to_message
            if rep:
                anu = rep.id
            else:
                anu = m.id
            await x.send_reaction(chat_id=m.chat.id, message_id=anu, emoji="😭")
        except:
            continue


@zb.devs("menyala")
async def _(c: nlx, m, _):
    for x in nlx._ubot:
        try:
            rep = m.reply_to_message
            if rep:
                anu = rep.id
            else:
                anu = m.id
            await x.send_reaction(chat_id=m.chat.id, message_id=anu, emoji="🔥")
        except:
            continue
