from pyrogram.errors import (PeerIdInvalid, UserAlreadyParticipant,
                             UserChannelsTooMuch)

from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Invite"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_invite")


@zb.ubot("invite|undang")
@zb.devs("sinijoin")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    mg = await m.reply_text(_("inv_1").format(em.proses))
    if len(m.command) < 2:
        await mg.edit(_("inv_2").format(em.gagal))
        return

    user_s_to_add = m.command[1]
    user_list = user_s_to_add.split(" ")
    user_id = await c.extract_user(m)

    if not user_list:
        await mg.edit(_("inv_2").format(em.gagal))
        return
    try:
        await c.add_chat_members(m.chat.id, user_list, forward_limit=100)
    except UserChannelsTooMuch:
        await mg.delete()
        return
    except PeerIdInvalid:
        await mg.edit(_("peer").format(em.gagal))
        return
    except UserAlreadyParticipant:
        await m.delete()
        return await mg.delete()
    except KeyError:
        await mg.edit(_("keyeror").format(em.gagal))
        return
    except Exception as er:
        await mg.edit(_("err").format(em.gagal, str(er)))
        return
    mention = (await c.get_users(user_id)).mention
    return await mg.edit(_("inv_3").format(em.sukses, mention, m.chat.title))


@zb.ubot("getlink|invitelink")
@zb.devs("getling")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    Nan = await m.reply_text(_("proses").format(em.proses, proses_))

    try:
        link = await c.export_chat_invite_link(m.chat.id)
        await Nan.edit(
            _("inv_4").format(em.sukses, link), disable_web_page_preview=True
        )
        return
    except Exception:
        await Nan.edit(_("inv_5").format(em.gagal))
        return
