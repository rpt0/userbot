import asyncio
import sys
import traceback
from functools import wraps

from pyrogram import enums, filters
from pyrogram.errors import (ChatSendPlainForbidden, ChatWriteForbidden,
                             FloodWait, MessageIdInvalid, SlowmodeWait)

from config import DEVS, bot_id, devs_boong, dump, owner_id, the_cegers
from Userbot import bot, nlx

from ..database import dB
from ..langs import get_string

"""
    CREDITS BY @NORSODIKIN
    NGAKU-NGAKU 7 TURUNAN LU BOOL NYA MELEDAK
"""

user_last_command_time = {}


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args):
        try:
            try:
                langs = nlx.get_langs(client.me.id)
                _ = lambda key: get_string(key, langs)
            except:
                langs = get_string("toxic")
                _ = lambda key: get_string(key, langs)
            return await func(client, message, *args)
        except Exception as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_feedback = split_limits(
                "❌**ERROR BANGSAT @ZEEBFLY** | `{}` | `{}`\n\n<pre>{}</pre>\n\n<pre>{}</pre>\n".format(
                    (0 if not client.me else client.get_mention(client.me, logs=True)),
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await bot.send_message(dump, x)
            raise err

    return capture


def caperr_cq(func):
    @wraps(func)
    async def capture(client, cq, *args):
        try:
            try:
                langs = nlx.get_langs(cq.from_user.id)
                _ = lambda key: get_string(key, langs)
            except:
                langs = get_string("toxic")
                _ = lambda key: get_string(key, langs)
            return await func(client, cq, *args)
        except Exception as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_feedback = split_limits(
                "❌**ERROR BANGSAT @ZEEBFLY** | `{}`\n\n<pre>{}</pre>".format(
                    (
                        0
                        if not cq.from_user
                        else bot.get_mention(cq.from_user, logs=True)
                    ),
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await bot.send_message(dump, x)
            raise err

    return capture


def caperr_iq(func):
    @wraps(func)
    async def capture(client, iq, *args):
        try:
            try:
                langs = nlx.get_langs(iq.from_user.id)
                _ = lambda key: get_string(key, langs)
            except:
                langs = get_string("toxic")
                _ = lambda key: get_string(key, langs)
            return await func(client, iq, *args)
        except Exception as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_feedback = split_limits(
                "❌**ERROR BANGSAT @ZEEBFLY** | `{}`\n\n<pre>{}</pre>".format(
                    (
                        0
                        if not iq.from_user
                        else bot.get_mention(iq.from_user, logs=True)
                    ),
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await bot.send_message(dump, x)
            raise err

    return capture


async def if_sudo(_, client, message):
    sudo_users = dB.get_list_from_var(client.me.id, "sudoers", "userid")
    is_user = message.from_user if message.from_user else message.sender_chat
    is_self = bool(
        message.from_user
        and message.from_user.is_self
        or getattr(message, "outgoing", False)
    )
    return is_user.id in sudo_users or is_self


async def filter_is_deleted(_, __, m):
    if m.sender_chat:
        return
    return bool(m.from_user and m.from_user.status == enums.UserStatus.LONG_AGO)


class human:
    me = filters.me
    pv = filters.private
    dev = filters.user(DEVS) & ~filters.me
    deev = filters.user(devs_boong) & ~filters.me
    cegs = filters.user(the_cegers) & ~filters.me
    cegers = filters.user(the_cegers) & filters.me


class zb:
    @staticmethod
    def devs(command, filter=human.dev):
        def wrapper(func):
            @nlx.on_message(filters.command(command, "") & filter)
            @capture_err
            async def wrapped_func(client, message, *args):
                try:
                    langs = nlx.get_langs(client.me.id)
                    _ = lambda key: get_string(key, langs)
                except:
                    langs = get_string("toxic")
                    _ = lambda key: get_string(key, langs)
                return await func(client, message, _)

            return wrapped_func

        return wrapper

    @staticmethod
    def deve(command, filter=human.deev):
        def wrapper(func):

            @nlx.on_message(filters.command(command, "^") & filter)
            @capture_err
            async def wrapped_func(client, message, *args):
                try:
                    langs = nlx.get_langs(client.me.id)
                    _ = lambda key: get_string(key, langs)
                except:
                    langs = get_string("toxic")
                    _ = lambda key: get_string(key, langs)
                return await func(client, message, _)

            return wrapped_func

        return wrapper

    @staticmethod
    def cegers(command, filter=human.cegs):
        def wrapper(func):

            @nlx.on_message(filters.command(command, "") & filter)
            @capture_err
            async def wrapped_func(client, message, *args):
                try:
                    langs = nlx.get_langs(client.me.id)
                    _ = lambda key: get_string(key, langs)
                except:
                    langs = get_string("toxic")
                    _ = lambda key: get_string(key, langs)
                return await func(client, message, _)

            return wrapped_func

        return wrapper

    @staticmethod
    def reconnect():
        def wrapper(func):
            @nlx.on_disconnect()
            async def wrapped_func(client):
                return await func(client)

            return wrapped_func

        return wrapper

    @staticmethod
    def ubot(command, filter=None):
        if filter is None:
            filter = filters.create(if_sudo)

        def wrapper(func):
            @nlx.on_message(nlx.user_prefix(command) & filter)
            @capture_err
            async def wrapped_func(client, message, *args):
                try:
                    try:
                        langs = nlx.get_langs(client.me.id)
                        _ = lambda key: get_string(key, langs)
                    except:
                        langs = get_string("toxic")
                        _ = lambda key: get_string(key, langs)
                    cmd = message.command[0].lower()
                    if cmd not in ["top", "eval", "sh", "trash", "reboot", "update"]:
                        top = dB.get_var(bot_id, cmd, "MODULES")
                        get = int(top) + 1 if top else 1
                        try:
                            dB.set_var(bot_id, cmd, get, "MODULES")
                        except:
                            pass
                    return await func(client, message, _)
                except (SlowmodeWait, FloodWait) as e:
                    await asyncio.sleep(e.value)
                    return await func(client, message, _)
                except ChatWriteForbidden:
                    return
                except ChatSendPlainForbidden:
                    return
                except MessageIdInvalid:
                    return

            return wrapped_func

        return wrapper

    @staticmethod
    def bots(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            @capture_err
            async def wrapped_func(client, message, *args):
                try:
                    try:
                        langs = nlx.get_langs(message.from_user.id)
                        _ = lambda key: get_string(key, langs)
                    except:
                        langs = get_string("toxic")
                        _ = lambda key: get_string(key, langs)
                    return await func(client, message, _)
                except MessageIdInvalid:
                    pass
                # return await func(client, message, _)

            return wrapped_func

        return wrapper

    @staticmethod
    def inline():
        def wrapper(func):
            @bot.on_inline_query()
            @caperr_iq
            async def wrapped_func(client, iq, *args):
                try:
                    langs = nlx.get_langs(iq.from_user.id)
                    _ = lambda key: get_string(key, langs)
                except:
                    langs = get_string("toxic")
                    _ = lambda key: get_string(key, langs)
                return await func(client, iq, _)

            return wrapped_func

        return wrapper

    @staticmethod
    def callback(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            @caperr_cq
            async def wrapped_func(client, cq, *args):
                try:
                    try:
                        langs = nlx.get_langs(cq.from_user.id)
                        _ = lambda key: get_string(key, langs)
                    except:
                        langs = get_string("toxic")
                        _ = lambda key: get_string(key, langs)
                    return await func(client, cq, _)
                except MessageIdInvalid:
                    pass

            return wrapped_func

        return wrapper

    @staticmethod
    def regex(pattern, filter=False):
        def wrapper(func):
            message_filters = (
                filters.regex(pattern) & filter if filter else filters.regex(pattern)
            )

            @bot.on_message(message_filters)
            @capture_err
            async def wrapped_func(client, message, *args):
                try:
                    langs = nlx.get_langs(message.from_user.id)
                    _ = lambda key: get_string(key, langs)
                except:
                    langs = get_string("toxic")
                    _ = lambda key: get_string(key, langs)
                return await func(client, message, _)

            return wrapped_func

        return wrapper

    @staticmethod
    def is_log(func):
        async def function(client, message, _):
            logs = dB.get_var(client.me.id, "NEW_LOG")
            if logs:
                if message.chat.id != int(logs):
                    return
            else:
                pass
            return await func(client, message, _)

        return function

    @staticmethod
    def nocmd(result, nlx):
        query_mapping = {
            "AFK": {
                "query": (
                    (filters.mentioned | filters.private)
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                ),
                "group": 2,
            },
            "REP_BLOCK": {
                "query": (
                    (filters.mentioned | filters.private)
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                    & filters.create(filter_is_deleted)
                ),
                "group": 4,
            },
            "PMPERMIT": {
                "query": (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.service
                ),
                "group": 1,
            },
            "LOGS_GROUP": {
                "query": (
                    filters.mentioned
                    & filters.incoming
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.me
                )
                | (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.service
                ),
                "group": 3,
            },
            "REPLY": {
                "query": (filters.reply & filters.me),
                "group": 5,
            },
        }
        result_query = query_mapping.get(result)

        def wrapper(func):
            if result_query:

                async def wrapped_func(client, message, *args):
                    try:
                        try:
                            langs = nlx.get_langs(client.me.id)
                            _ = lambda key: get_string(key, langs)
                        except:
                            langs = get_string("toxic")
                            _ = lambda key: get_string(key, langs)
                        return await func(client, message, _)
                    except (SlowmodeWait, FloodWait) as e:
                        await asyncio.sleep(e.value)
                        return await func(client, message, _)
                    except ChatWriteForbidden:
                        pass
                    except ChatSendPlainForbidden:
                        pass
                    except MessageIdInvalid:
                        pass

                nlx.on_message(result_query["query"], group=int(result_query["group"]))(
                    wrapped_func
                )

                return wrapped_func
            else:
                return func

        return wrapper

    @staticmethod
    def menten(func):
        async def function(client, message, *args):
            kon = dB.get_var(client.me.id, "menten")
            if kon and message.from_user.id != owner_id:
                return await message.reply(
                    "<b>Bot sedang dalam proses Update.\n\nSilahkan tunggu info dari Owner.</b>"
                )
            try:
                langs = nlx.get_langs(message.from_user.id)
                _ = lambda key: get_string(key, langs)
            except:
                langs = get_string("toxic")
                _ = lambda key: get_string(key, langs)
            return await func(client, message, _)

        return function

    @staticmethod
    def thecegers(func):
        async def function(client, message, *args):
            if not message.from_user:
                return
            kon = message.from_user.id
            if kon not in the_cegers:
                return
            try:
                langs = nlx.get_langs(message.from_user.id)
                _ = lambda key: get_string(key, langs)
            except:
                langs = get_string("toxic")
                _ = lambda key: get_string(key, langs)
            return await func(client, message, _)

        return function

    @staticmethod
    def edited():
        def wrapper(func):
            @nlx.on_edited_message(
                (
                    filters.mentioned
                    & filters.incoming
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.me
                )
                | (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.service
                )
            )
            async def wrapped_func(client, message):

                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def deleted():
        def wrapper(func):
            @nlx.on_deleted_messages()
            async def wrapped_func(client, message):
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def seller(func):
        async def function(client, message, *args):
            kon = message.from_user.id
            seles = dB.get_list_from_var(bot_id, "seller", "user")
            if kon not in seles:
                return
            try:
                langs = nlx.get_langs(message.from_user.id)
                _ = lambda key: get_string(key, langs)
            except:
                langs = get_string("toxic")
                _ = lambda key: get_string(key, langs)
            return await func(client, message, _)

        return function


def org_kontol(func):
    async def function(c, m, *args):
        kon = m.from_user.id
        blus = dB.get_list_from_var(c.me.id, "BLUSER")
        if kon in blus:
            return
        try:
            langs = nlx.get_langs(c.me.id)
            _ = lambda key: get_string(key, langs)
        except:
            langs = get_string("toxic")
            _ = lambda key: get_string(key, langs)
        return await func(c, m, _)

    return function
