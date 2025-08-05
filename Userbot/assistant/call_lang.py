from pyrogram.helpers import kb
from pyrogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove)

from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.langs import languages_present
from Userbot.helper.tools import zb


def st_lang(_):
    language_buttons = [
        [KeyboardButton(text=languages_present[i]) for i in languages_present]
    ]
    control_buttons = [[KeyboardButton("🏠 Menu Utama"), KeyboardButton("❌ Tutup")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=language_buttons + control_buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard


# @zb.bots("langs")
#
async def atur_bahasa(c, m, _):
    msg = _("asst_4")
    ke = st_lang(_)
    meki = nlx.get_langs(m.from_user.id)
    for a in languages_present:
        if a == meki:
            return await m.reply(msg.format(languages_present[a]), reply_markup=ke)


@zb.regex(r"^(❌ Tutup|🇺🇸 English|🇲🇨 Indonesia)")
async def _(c, m, _):
    keyber = kb([[("⬅️ Kembali")]], resize_keyboard=True, one_time_keyboard=True)
    if m.text == "❌ Tutup":
        return await cb_ttup(c, m, _)
    elif m.text == "🇺🇸 English":
        langauge = "en"
        old = nlx.get_langs(m.from_user.id)
        if str(old) == str(langauge):
            return await m.reply(_("lang_4"), reply_markup=keyber)
        try:
            nlx.set_langs(m.from_user.id, langauge)
            dB.set_var(m.from_user.id, "bahasa", langauge)
            return await m.reply(_("lang_2"), reply_markup=keyber)
        except Exception:
            return await m.reply(_("lang_3"), reply_markup=keyber)

    elif m.text == "🇲🇨 Indonesia":
        langauge = "id"
        old = nlx.get_langs(m.from_user.id)
        if str(old) == str(langauge):
            return await m.reply(_("lang_4"), reply_markup=keyber)
        try:
            nlx.set_langs(m.from_user.id, langauge)
            dB.set_var(m.from_user.id, "bahasa", langauge)
            return await m.reply(_("lang_2"), reply_markup=keyber)
        except Exception:
            return await m.reply(_("lang_3"), reply_markup=keyber)
    elif m.text == "🇲🇨 Toxic":
        langauge = "toxic"
        old = nlx.get_langs(m.from_user.id)
        if str(old) == str(langauge):
            return await m.reply(_("lang_4"), reply_markup=keyber)
        try:
            nlx.set_langs(m.from_user.id, langauge)
            dB.set_var(m.from_user.id, "bahasa", langauge)
            return await m.reply(_("lang_2"), reply_markup=keyber)
        except Exception:
            return await m.reply(_("lang_3"), reply_markup=keyber)
    elif m.text == "🏴‍☠️ Jawa":
        langauge = "jawa"
        old = nlx.get_langs(m.from_user.id)
        if str(old) == str(langauge):
            return await m.reply(_("lang_4"), reply_markup=keyber)
        try:
            nlx.set_langs(m.from_user.id, langauge)
            dB.set_var(m.from_user.id, "bahasa", langauge)
            return await m.reply(_("lang_2"), reply_markup=keyber)
        except Exception:
            return await m.reply(_("lang_3"), reply_markup=keyber)


async def cb_ttup(c, m, _):
    return await m.reply("Tutup keyboard", reply_markup=ReplyKeyboardRemove())
