from config import def_bahasa, owner_id
from Userbot import nlx

from ..database import dB
from ..langs import get_string, get_string2


def h_s(org: int, string: str) -> str:
    try:
        lang = nlx.get_langs(org)
        return get_string2(lang, string)
    except:
        return get_string2(def_bahasa, string)


def language(mystic):
    async def wrapper(client, message, **kwargs):
        kon = dB.get_var(client.me.id, "menten")
        if kon and message.from_user.id != owner_id:
            return await message.reply(
                "<b>Bot sedang dalam proses Update.\n\nSilahkan tunggu info dari Owner.</b>"
            )
        try:
            language = nlx.get_langs(client.me.id)
            _ = lambda key: get_string(key, language)
        except:
            language = get_string("en")
            _ = lambda key: get_string(key, language)
        return await mystic(client, message, _)

    return wrapper


def languageCB(mystic):
    async def wrapper(client, cq, **kwargs):
        kon = dB.get_var(client.me.id, "menten")
        if kon and cq.from_user.id != owner_id:
            return await cq.answer(
                "<b>Bot sedang dalam proses Update.\n\nSilahkan tunggu info dari Owner.</b>",
                True,
            )
        try:
            language = nlx.get_langs(cq.from_user.id)
            _ = lambda key: get_string(key, language)
        except:
            language = "en"
            _ = lambda key: get_string(key, language)
        return await mystic(client, cq, _)

    return wrapper


def languageIQ(mystic):
    async def wrapper(client, cq, **kwargs):
        try:
            language = nlx.get_langs(cq.from_user.id)
            _ = lambda key: get_string(key, language)
        except:
            language = "en"
            _ = lambda key: get_string(key, language)
        return await mystic(client, cq, _)

    return wrapper


def LanguageStart(mystic):
    async def wrapper(client, message, **kwargs):

        try:
            language = nlx.get_langs(client.me.id)
            _ = lambda key: get_string(key, language)
        except:
            language = get_string("en")
            _ = lambda key: get_string(key, language)
        return await mystic(client, message, _)

    return wrapper
