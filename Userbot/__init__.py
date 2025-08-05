#
import uvloop

uvloop.install()

import asyncio
import importlib
import logging
import os
import re
import shlex
import subprocess
import sys
import asyncio
from datetime import datetime

from pyrogram.errors import FloodWait
from aiohttp import ClientSession
from pyrogram import Client, enums, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import (CallbackQueryHandler, DeletedMessagesHandler,
                               DisconnectHandler, EditedMessageHandler,
                               MessageHandler)
from pyromod import listen
from pytgcalls import PyTgCalls
from pytgcalls import filters as flip
from pytz import timezone

from config import (CMD_HELP, DEVS, NO_GCAST, api_hash, api_id, bot_id,
                    bot_token, bot_username, botcax_api, db_name, def_bahasa,
                    devs_boong, dump, gemini_api, id_button, log_pic,
                    log_userbot, nama_bot, nama_ip, owner_id, the_cegers)
from Userbot.helper.database import dB
from Userbot.plugins import ALL_MODULES

aiohttpsession = ClientSession()

list_error = []


class JakartaFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        jakarta_tz = timezone("Asia/Jakarta")
        return dt.astimezone(jakarta_tz)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()


class ConnectionHandler(logging.Handler):
    def emit(self, record):
        if any(error_type in record.getMessage() for error_type in ["OSError"]):
            subprocess.run(["pkill", "-f", "gunicorn"])
            os.execl(sys.executable, sys.executable, "-m", "Userbot")
            # pass


logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)
logging.getLogger("hydrogram").setLevel(logging.WARNING)
logging.getLogger("hydrogram.client").setLevel(logging.WARNING)
logging.getLogger("hydrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("hydrogram.session.session").setLevel(logging.CRITICAL)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = JakartaFormatter(
    "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
connection_handler = ConnectionHandler()
logger.addHandler(connection_handler)
logger.addHandler(stream_handler)


class BaseBot(Client):
    _prefix = {}
    _translate = {}
    _ubot = []
    _my_peer = {}
    _my_id = []
    _langs = {}
    _logger = {}

    _seles_ids = []
    status_background = {}
    _putaran = {}

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def parse_date(self, date_str: str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except (ValueError, TypeError):
            return None

    async def broadcaster(
        self,
        client,
        user_id: int,
        message_ids: dict,
        chat_ids: list,
        blacklist: list,
        delay_per_chat: float,
        delay_between_intervals: float,
        max_loops: int,
        auto_off_time: datetime
    ):
        if not message_ids:
            return
        try:
            await client.send_message(
                message_ids["chat_id"],
                f"<blockquote><b><emoji id=4915853119839011973>⚠️</emoji> Terdeteksi bot melakukan restart.\n<emoji id=5350490470025816976>🚀</emoji> Auto Start Broadcast.</b>\n └<i> Menunggu {int(delay_between_intervals)} menit untuk mengirim pesan</i></blockquote>",
                reply_to_message_id=message_ids["message_id"]
            )
        except Exception as e:
            print(f"<blockquote><i><emoji id=4918014360267260850>⛔️</emoji> Gagal mengirim pesan awal: {e}</i></blockquote>")
        await asyncio.sleep(int(delay_between_intervals) * 60)

        putaran = dB.get_var(user_id, 'INTERVAL_COUNT') or 0
        while putaran < max_loops:
            if not dB.get_var(user_id, "ENABLED") or not client.status_background.get(user_id):                
                self.status_background[user_id] = False
                try:
                    await client.send_message(
                        message_ids["chat_id"],
                        "<blockquote><i><emoji id=5350740982583301822>🗑</emoji> Menghapus data message_ids dari database</blockquote></i>",
                        reply_to_message_id=message_ids["message_id"]
                    )
                finally:
                    dB.set_var(user_id, "MESSAGE_IDS", {})
                    dB.set_var(user_id, "INTERVAL_COUNT", 0)
                break

            if auto_off_time and datetime.now() > auto_off_time:
                dB.set_var(user_id, "ENABLED", False)
                self.status_background[user_id] = False
                try:
                    await client.send_message(
                        message_ids["chat_id"],
                        "<blockquote><b><emoji id=5350423812133381005>🕔</emoji> Waktu yang ditentukan telah dilampaui</b>.\n  └<i> Menghentikan Broadcast jaseb.</blockquote></i>",
                        reply_to_message_id=message_ids["message_id"]
                    )
                finally:
                    dB.set_var(user_id, "MESSAGE_IDS", {})
                    dB.set_var(user_id, "INTERVAL_COUNT", 0)
                break

            try:
                original_msg = await client.get_messages(
                    message_ids["chat_id"],
                    message_ids["message_id"]
                )
            except Exception as e:
                print(f"<blockquote><i><emoji id=4918014360267260850>⛔️</emoji> Gagal mengambil pesan asli: {e}</blockquote></i>")
                break

            success_count = 0
            fail_count = 0

            for chat_id in chat_ids:
                if not dB.get_var(user_id, "ENABLED") or not client.status_background.get(user_id):
                    client.status_background[user_id] = False
                    dB.set_var(user_id, "MESSAGE_IDS", {})
                    break                  
                if chat_id in blacklist:
                    continue
                try:
                    await original_msg.forward(chat_id)
                    success_count += 1
                    await asyncio.sleep(delay_per_chat)
                except FloodWait as fw:
                    print(f"<blockquote><i><emoji id=5350381992036820471>🛡</emoji> FloodWait terdeteksi di chat {chat_id}, menunggu {fw.value} detik...</blockquote></i>")
                    await asyncio.sleep(fw.value)
                except Exception as e:
                    print(f"Gagal mengirim ke {chat_id}: {e}")
                    fail_count += 1

            putaran += 1
            dB.set_var(user_id, "INTERVAL_COUNT", putaran)
            report = f"""<blockquote><b><emoji id=5350404703823883106>⭐️</emoji> Hasil Broadcast <emoji id=5350404703823883106>⭐️</emoji></b></blockquote>
<blockquote>╭─❖ Ringkasan
├ <emoji id=5317059204802952215>🖱️</emoji> Status: Selesai
├ <emoji id=5317059204802952215>🖱️</emoji> Berhasil : {success_count} grup
├ <emoji id=5317059204802952215>🖱️</emoji> Gagal : {fail_count} grup
├ <emoji id=5317059204802952215>🖱️</emoji> Delay : {delay_per_chat}s/grup
├ <emoji id=5317059204802952215>🖱️</emoji> Interval delay : {delay_between_intervals}m
├ <emoji id=5317059204802952215>🖱️</emoji> Interval ke : {putaran}
├ <emoji id=5317059204802952215>🖱️</emoji> Auto-off : {dB.get_var(user_id, 'AUTO-OFF')}
└ <emoji id=5317059204802952215>🖱️</emoji> TimeNow Server : {datetime.now().strftime('%d/%m/%Y')}</blockquote>
"""
            try:
                await client.send_message(message_ids["chat_id"], report)
            except Exception as e:
                print(f"Gagal mengirim laporan: {e}")
            await asyncio.sleep(int(delay_between_intervals) * 60)

    async def loop_restart(self):
        for client in self._ubot:
            user_id = client.me.id

            if not dB.get_var(user_id, "ENABLED"):
                continue

            message_ids = dB.get_var(user_id, "MESSAGE_IDS") or {}
            if not message_ids:
                continue

            self.status_background[user_id] = True

            try:
                chat_ids = await client.get_chats_dialog("group")
            except Exception as e:
                print(f"<blockquote><i><emoji id=4918014360267260850>⛔️</emoji> Gagal mendapatkan daftar grup untuk user {user_id}: {e}</blockquote></i>")
                continue

            blacklist = dB.get_list_from_var(user_id, "BLGCAST")
            delay_per_chat = float(dB.get_var(user_id, "DELAY_GCAST") or 0.5)
            delay_between_intervals = float(dB.get_var(user_id, "DELAY_PER_SEND") or 0.5)
            auto_off_time = self.parse_date(dB.get_var(user_id, "AUTO-OFF") or "")
            max_loops = int(dB.get_var(user_id, "MAX_LOOP") or 999_999_999)

            asyncio.create_task(
                self.broadcaster(
                    client, user_id, message_ids, chat_ids, blacklist,
                    delay_per_chat, delay_between_intervals, max_loops, auto_off_time
                )
        )

    async def get_chats_dialog(self, query):
        chat_types = {
            "global": [ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP],
            "all": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE],
            "group": [ChatType.GROUP, ChatType.SUPERGROUP],
            "bot": [ChatType.BOT],
            "usbot": [ChatType.PRIVATE, ChatType.BOT],
            "private": [ChatType.PRIVATE],
            "channel": [ChatType.CHANNEL],
        }

        if query not in chat_types:
            return []

        valid_chat_types = chat_types[query]
        chat_ids = []

        try:
            async for dialog in self.get_dialogs():
                try:
                    chat = dialog.chat
                    if chat and chat.type in valid_chat_types:
                        chat_ids.append(chat.id)
                except Exception:
                    continue
        except Exception:
            pass

        return chat_ids

    def get_langs(self, user_id):
        return self._langs.get(user_id, def_bahasa)

    def set_langs(self, user_id, kode):
        self._langs[user_id] = kode

    def get_logger(self, user_id):
        return self._logger.get(user_id, None)

    def set_logger(self, user_id, grup):
        self._logger[user_id] = grup

    def get_mention(self, me, logs=False, no_tag=False):
        name = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
        link = f"tg://user?id={me.id}"
        return (
            f"{me.id}|{name}"
            if logs
            else name if no_tag else f"<a href={link}>{name}</a>"
        )

    def set_prefix(self, user, prefix):
        self._prefix[user] = prefix

    def get_prefix(self, user):
        return self._prefix.get(user, [".", ",", "?", "+", "!"])

    def get_m(self, m):
        msg = (
            m.reply_to_message
            if m.reply_to_message
            else "" if len(m.command) < 2 else " ".join(m.command[1:])
        )
        return msg

    def get_text(self, m):
        if m.reply_to_message:
            if len(m.command) < 2:
                text = m.reply_to_message.text or m.reply_to_message.caption
            else:
                text = (
                    (m.reply_to_message.text or m.reply_to_message.caption)
                    + "\n\n"
                    + m.text.split(None, 1)[1]
                )
        else:
            if len(m.command) < 2:
                text = ""
            else:
                text = m.text.split(None, 1)[1]
        return text

    async def bash(self, cmd):
        try:
            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            err = stderr.decode().strip()
            out = stdout.decode().strip()
            return out, err
        except NotImplementedError:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            stdout, stderr = process.communicate()
            err = stderr.decode().strip()
            out = stdout.decode().strip()
            return out, err

    async def run_cmd(self, cmd):
        args = shlex.split(cmd)
        try:
            process = await asyncio.create_subprocess_exec(
                *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return (
                stdout.decode("utf-8", "replace").strip(),
                stderr.decode("utf-8", "replace").strip(),
                process.returncode,
                process.pid,
            )
        except NotImplementedError:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            stdout, stderr = process.communicate()
            return (
                stdout.decode("utf-8", "replace").strip(),
                stderr.decode("utf-8", "replace").strip(),
                process.returncode,
                process.pid,
            )

    async def aexec(self, code, c, m):
        exec(
            "async def __aexec(c, m): "
            + "\n chat = m.chat"
            + "\n r = m.reply_to_message"
            + "\n c = c"
            + "\n m = m"
            + "\n p = print"
            + "".join(f"\n {l_}" for l_ in code.split("\n"))
        )
        return await locals()["__aexec"](c, m)

    async def shell_exec(self, code, treat=True):
        process = await asyncio.create_subprocess_shell(
            code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )

        stdout = (await process.communicate())[0]
        if treat:
            stdout = stdout.decode().strip()
        return stdout, process

    def get_arg(self, m):
        if m.reply_to_message and len(m.command) < 2:
            msg = m.reply_to_message.text or m.reply_to_message.caption
            if not msg:
                return ""
            msg = msg.encode().decode("UTF-8")
            msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
            return msg
        elif len(m.command) > 1:
            return " ".join(m.command[1:])
        else:
            return ""

    def new_arg(self, m):
        if m.reply_to_message and len(m.command) < 3:
            msg = m.reply_to_message.text or m.reply_to_message.caption
            if not msg:
                return ""
            msg = msg.encode().decode("UTF-8")
            msg = msg.replace(" ", "", 2) if msg[2] == " " else msg
            return msg
        elif len(m.command) > 2:
            return " ".join(m.command[2:])
        else:
            return ""

    async def extract_userid(self, m, t):
        def is_int(t):
            try:
                int(t)
            except ValueError:
                return False
            return True

        text = t.strip()

        if is_int(text):
            return int(text)

        entities = m.entities
        entity = entities[1 if m.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            return (await self.get_users(text)).id
        if entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id
        return None

    async def extract_user_and_reason(self, m, s=False):
        args = m.text.strip().split()
        text = m.text
        rg = None
        reason = None
        if m.reply_to_message:
            reply = m.reply_to_message
            if not reply.from_user:
                if reply.sender_chat and reply.sender_chat != m.chat.id and s:
                    id_ = reply.sender_chat.id
                else:
                    return None, None
            else:
                id_ = reply.from_user.id

            if len(args) < 2:
                reason = None
            else:
                reason = text.split(None, 1)[1]
            return id_, reason

        if len(args) == 2:
            rg = text.split(None, 1)[1]
            return await self.extract_userid(m, rg), None

        if len(args) > 2:
            rg, reason = text.split(None, 2)[1:]
            return await self.extract_userid(m, rg), reason

        return rg, reason

    async def extract_user(self, m):
        return (await self.extract_user_and_reason(m))[0]


class Userbot(BaseBot):
    __module__ = "pyrogram.client"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_id = api_id
        self.api_hash = api_hash
        self.device_model = nama_ip
        self.sleep_threshold = 30
        self.max_concurrent_transmissions = 10
        self.in_memory = True
        self.call_py = PyTgCalls(self, cache_duration=50)

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_edited_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(EditedMessageHandler(func, filters), group)
            return func

        return decorator

    def on_disconnect(self):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(DisconnectHandler(func))
            return func

        return decorator

    def on_deleted_messages(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(DeletedMessagesHandler(func, filters), group)
            return func

        return decorator

    def pytgcall_close_stream(self):
        def decorator(func):
            for ub in self._ubot:
                ub.call_py.on_update(flip.stream_end)(func)
            return func

        return decorator

    def user_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, client, message):
            if message.text:
                text = message.text.strip().encode("utf-8").decode("utf-8")
                username = client.me.username or ""
                prefixes = self.get_prefix(client.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix) :]

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        message.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)

    async def start(self):
        await super().start()
        if not self.call_py._is_running:
            await self.call_py.start()
        handler = dB.get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = [".", ",", "?", "+", "!"]
        defbahasa = dB.get_var(self.me.id, "bahasa")
        if defbahasa:
            self._langs[self.me.id] = defbahasa
        else:
            self._langs[self.me.id] = def_bahasa
        self._logger[self.me.id] = "me"
        self._translate[self.me.id] = {"negara": "id"}
        full = f"<a href=tg://user?id={self.me.id}>{self.me.first_name} {self.me.last_name or ''}</a>"
        dB.add_userdata(
            self.me.id,
            self.me.first_name,
            self.me.last_name,
            self.me.username,
            self.me.mention,
            full,
            self.me.id,
        )
        self._ubot.append(self)
        self._my_id.append(self.me.id)
        
        # Start cleanup task for augcsast if this is the first userbot
        if len(self._ubot) == 1:
            try:
                from Userbot.plugins.augcsast import cleanup_old_locks
                asyncio.create_task(cleanup_old_locks())
                logger.info("Started autogcast cleanup task")
            except ImportError:
                pass
        
        logger.info(f"Starting Userbot {self.me.id}|@{self.me.username}")


class Bot(BaseBot):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

    async def load_seles(self):
        seles = dB.get_list_from_var(self.me.id, "seller", "user")
        prem = dB.get_list_from_var(self.me.id, "PREM", "USERS")
        if owner_id not in DEVS:
            DEVS.append(owner_id)
        if owner_id not in the_cegers:
            the_cegers.append(owner_id)
        for p in the_cegers:
            if p not in seles:
                dB.add_to_var(self.me.id, "seller", p, "user")
            if p not in prem:
                dB.add_to_var(self.me.id, "PREM", p, "USERS")

    async def start(self):
        await super().start()
        logger.info("🔄 Importing Modules")
        for modul in ALL_MODULES:
            imported_module = importlib.import_module(f"Userbot.plugins.{modul}")
            module_name = (
                getattr(imported_module, "__MODULES__", "").replace(" ", "_").lower()
            )
            if module_name:
                CMD_HELP[module_name] = imported_module
        logger.info("✅ Successed Import All Plugins")
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention
        txt = "🔥**Userbot berhasil diaktifkan**🔥\n"
        txt += f"✅ **Total Pengguna: {len(nlx._ubot)}**"
        msg = f"<blockquote>{txt}</blockquote>"
        dB.set_var(bot_id, "total_users", len(nlx._ubot))
        logger.info(f"🔥 {self.username} Bot Started 🔥")
        return await self.send_message(owner_id, msg)


bot = Bot(
    name="bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    in_memory=True,
    workdir="./Userbot/",
    plugins=dict(root="Userbot.assistant"),
)
nlx = Userbot(name="kn")
