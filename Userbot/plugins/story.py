import os

from pyrogram.enums import StoriesPrivacyRules

from Userbot import nlx
from Userbot.helper.tools import Emojik, initial_ctext, zb

USER_PREMIUM = True


def extract_user_link(link):
    type = "t.me/c/" in link
    chat_id = (
        int("-100" + str(link.split("/")[-2])) if type else str(link.split("/")[-3])
    )
    msg_id = int(link.split("/")[-1])
    return chat_id, msg_id


async def colong_story(g, c: nlx, inf, m):
    msg = m.reply_to_message or m
    text = g.caption or ""

    if g.photo:
        media = await c.download_media(
            g.photo.file_id,
        )
        await c.send_photo(
            m.chat.id,
            media,
            caption=text,
            reply_to_message_id=msg.id,
        )
        await inf.delete()
        os.remove(media)

    elif g.video:
        media = await c.download_media(
            g.video.file_id,
        )
        thumbnail = await c.download_media(g.video.thumbs[-1]) or None
        await c.send_video(
            m.chat.id,
            video=media,
            duration=g.video.duration,
            caption=text,
            thumb=thumbnail,
            reply_to_message_id=msg.id,
        )
        await inf.delete()
        os.remove(media)
        os.remove(thumbnail)
    return


# THANKS TO MY BOROTHER
# NOR SODIKIN


def tomi_send_you_to_hell(m):
    if m.photo:
        return {"photo": m.photo.file_id}
    elif m.video:
        return {"video": m.video.file_id}
    elif m.animation:
        return {"animation": m.animation.file_id}
    else:
        return None


@zb.ubot("buatstory")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    rep = m.reply_to_message
    if len(m.command) < 2:
        return await m.reply(
            f"{em.gagal}<b>Ga gitu goblok!! kasih tujuan story dan balas ke pesan media foto, video atau animasi.</b>"
        )
    if not rep:
        return await m.reply(
            f"{em.gagal}<b>Ga gitu goblok!! Balas ke pesan media foto, video atau animasi.</b>"
        )
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    file = tomi_send_you_to_hell(rep)
    teks = rep.caption or ""
    try:
        tuju = m.text.split(None, 1)[1]
        await c.send_story(
            tuju, **file, caption=teks, privacy=StoriesPrivacyRules.PUBLIC
        )
    except Exception as e:
        print(e)
        return await pros.edit(_("err").format(em.gagal, e))
    return


@zb.ubot("cekstory")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    txt = f"{em.sukses}<b>Ini adalah list story lu jink:</b>\n\n"
    async for st in c.get_all_stories():
        st_ = await c.export_story_link("me", st.id)
        txt += f"<b>• ID Story: `{st.id}`\n Tautan Story: <a href='{st_}'>Klik Disini</a></b>"
    await m.reply(txt, disable_web_page_preview=True)
    return await pros.delete()


@zb.ubot("delstory")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    prefix = await c.get_prefix(c.me.id)
    if len(m.command) < 2:
        return await pros.edit(
            "<b>{} Ga gitu lah anj!! Kasih id story lo.\nContoh: `{}delstory` 5\n\nAtau lo bisa ketik `{}cekstory` untuk lihat id story lo!! </b>".format(
                em.gagal, " ".join(prefix[0]), " ".join(prefix[0])
            )
        )
    id_ = m.text.split(None, 1)[1]
    if not id_.isnumeric():
        return await pros.edit(
            f"{em.gagal}<b>Allahu Akbar!! dimana mana id itu angka anj!! bukan huruf atau symbol.</b>"
        )
    await c.delete_stories(story_ids=int(id_))
    return await pros.edit(f"{em.sukses}<b>Mantap story `{id_}` dihapus!!</b>")


@zb.ubot("copystory")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    rep = m.reply_to_message
    if rep:
        link = rep.text or rep.caption
    else:
        link = m.text.split(None, 1)[1]
    if not link:
        return await pros.edit(
            f"{em.gagal}<b>Dasar gublok!! kasih link lah tolol !!</b>"
        )
    if not link.startswith(("https", "t.me")):
        return await pros.edit(
            f"{em.gagal}<b>Dasar gublok!! kasih link telegram lah tolol bukan link xnxx.com!!</b>"
        )
    user, _id = extract_user_link(link)
    st = await c.get_stories(user, _id)
    await colong_story(st, c, pros, m)
    return await pros.delete()
