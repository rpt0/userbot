################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from pyrogram.types import EmojiStatus

from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Emoji"

USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_emoji")


@zb.ubot("setemo")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    proses_, sukses_ = initial_ctext(c)[4:6]
    xx = await m.edit(_("proses").format(em.proses, proses_))
    rep = m.reply_to_message
    emoji_id = None
    prem = c.me.is_premium
    if not prem:
        return await xx.edit("{}**Your account must be premium.**".format(em.gagal))
    if rep and rep.entities:
        for entity in rep.entities:
            if entity.custom_emoji_id:
                emoji_id = entity.custom_emoji_id
                break
        else:
            await xx.edit(_("em_5").format(em.gagal, m.text.split()[0]))
            return
    else:
        await xx.edit(_("em_3").format(em.gagal))
        return

    if prem:
        if emoji_id:
            await c.set_emoji_status(EmojiStatus(custom_emoji_id=emoji_id))
            await xx.edit(_("em_25").format(em.sukses, emoji_id))
            return
        else:
            await xx.edit(_("em_5").format(em.gagal))
            return
    else:
        await xx.edit(_("em_2").format(em.gagal))
        return


@zb.ubot("emoid")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    emoji = m.reply_to_message
    if emoji.entities:
        for entot in emoji.entities:
            if entot.custom_emoji_id:
                emoid = entot.custom_emoji_id
                await xx.edit(_("em_4").format(em.sukses, emoid))
                return
            else:
                await xx.edit(_("em_3").format(em.gagal))
                return
    else:
        return await xx.edit(
            "{}<b>Please reply to premium emoji!!</b>".format(em.gagal)
        )


emoji_mapping = {
    "uptime": "emo_uptime",
    "ping": "emo_ping",
    "owner": "emo_owner",
    "proses": "emo_proses",
    "gagal": "emo_gagal",
    "sukses": "emo_sukses",
    "profil": "emo_profil",
    "warn": "emo_warn",
    "block": "emo_block",
}


@zb.ubot("emoji")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    gua = c.me.is_premium
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    jing = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.command) < 3:
        return await jing.edit(_("em_5").format(em.gagal, m.text.split()[0]))
    command, variable, value = m.command[:3]
    # emoji_id = None
    if variable.lower() in emoji_mapping:
        value_var = emoji_mapping[variable.lower()]
        if gua == True:
            if m.entities:
                for entity in m.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    dB.set_var(c.me.id, value_var, emoji_id)
                    return await jing.edit(
                        _("em_6").format(em.sukses, variable.lower(), emoji_id)
                    )

        elif gua == False:
            dB.set_var(c.me.id, value_var, value)
            await jing.edit(_("em_7").format(em.sukses, variable.lower(), value))
            return
    else:
        await jing.edit(_("em_5").format(em.gagal, m.text.split()[0]))
        return


@zb.ubot("getemo")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    return await xx.edit(
        _("em_24").format(
            em.sukses,
            em.ping,
            em.pong,
            em.proses,
            em.sukses,
            em.gagal,
            em.profil,
            em.owner,
            em.warn,
            em.block,
        )
    )


def set_pong_message(user_id, new_message):
    dB.set_var(user_id, "text_pong", new_message)
    return


def set_utime_message(user_id, new_message):
    dB.set_var(user_id, "text_uptime", new_message)
    return


def set_owner_message(user_id, new_message):
    dB.set_var(user_id, "text_owner", new_message)
    return


def set_ubot_message(user_id, new_message):
    dB.set_var(user_id, "text_ubot", new_message)
    return


def set_gcast_message(user_id, new_message):
    dB.set_var(user_id, "text_gcast", new_message)
    return


def set_sukses_message(user_id, new_message):
    dB.set_var(user_id, "text_sukses", new_message)
    return


costumtext_query = {
    "pong": set_pong_message,
    "uptime": set_utime_message,
    "owner": set_owner_message,
    "ubot": set_ubot_message,
    "proses": set_gcast_message,
    "sukses": set_sukses_message,
}


@zb.ubot("settext")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    user_id = c.me.id
    args = m.text.split(maxsplit=2)
    if len(args) >= 3:
        variable = args[1]
        new_message = c.new_arg(m)
        if variable in costumtext_query:
            costumtext_query[variable](user_id, new_message)
            return await pros.edit(_("em_8").format(em.sukses, variable))
        else:
            return await pros.edit(_("em_9").format(em.gagal))
    else:
        pref = dB.get_pref(c.me.id)
        return await pros.edit(_("em_10").format(em.gagal, pref[0]))
