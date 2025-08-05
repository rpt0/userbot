import os

from pyrogram import enums, types

from config import bot_id, bot_username, log_pic, nama_bot
from Userbot import logger

from ..database import dB


class Emojik:
    DEFAULT_VARS = {
        "emo_ping": "🏓",
        "emo_msg": "✉️",
        "emo_proses": "⏳",
        "emo_sukses": "✅",
        "emo_gagal": "❌",
        "emo_profil": "👤",
        "emo_owner": "⭐",
        "emo_warn": "⚠️",
        "emo_block": "⛔",
        "emo_uptime": "⏰",
        "emo_robot": "⚙️",
        "emo_klip": "📎",
        "emo_net": "🌐",
        "emo_up": "⬆️",
        "emo_down": "⬇️",
        "emo_speed": "⚡️",
    }

    CUSTOM_EMOJI_IDS = {
        "emo_ping": 5258330865674494479,
        "emo_msg": 5260535596941582167,
        "emo_proses": 5427181942934088912,
        "emo_sukses": 5260416304224936047,
        "emo_gagal": 5260342697075416641,
        "emo_profil": 5258011929993026890,
        "emo_owner": 5258185631355378853,
        "emo_warn": 5260249440450520061,
        "emo_block": 5258362429389152256,
        "emo_uptime": 5258089153505009279,
        "emo_robot": 5258093637450866522,
        "emo_klip": 5260730055880876557,
        "emo_net": 5260348422266822411,
        "emo_up": 5260379144167890225,
        "emo_down": 5258514780469075716,
        "emo_speed": 5258152182150077732,
    }

    def __init__(self, client):
        self.client = client
        self.me = client.me
        self.is_premium = client.me.is_premium
        self.user_id = client.me.id
        self.mention = f"[{client.me.first_name} {client.me.last_name or ''}](tg://user?id={client.me.id})"
        self.full_name = (
            f"{self.me.first_name} {self.me.last_name if self.me.last_name else ''}"
        )

    def set_emotes(self, new_client, is_premium):
        emotes = {
            "uptime": "⏰",
            "warn": "⚠️",
            "block": "❌",
            "ping": "🏸",
            "msg": "✉️",
            "proses": "⏳",
            "gagal": "❎",
            "sukses": "✅",
            "profil": "👤",
            "owner": "⭐️",
            "robot": "⚙️",
            "klip": "📎",
            "net": "🌐",
            "up": "⬆️",
            "down": "⬇️",
            "speed": "⚡️",
        }

        emote_ids = {
            "uptime": "<emoji id=5359698274318037766>⏰</emoji>",
            "warn": "<emoji id=6008233706039284019>⚠️</emoji>",
            "block": "<emoji id=5215642288071387368>❌</emoji>",
            "ping": "<emoji id=5467537163589538076>🏸</emoji>",
            "msg": "<emoji id=5913236481220022288>✉️</emoji>",
            "proses": "<emoji id=6010111371251815589>⏳</emoji>",
            "gagal": "<emoji id=5940804914220372462>❎</emoji>",
            "sukses": "<emoji id=5940635490645449104>✅</emoji>",
            "profil": "<emoji id=5373012449597335010>👤</emoji>",
            "owner": "<emoji id=6084447187742233001>⭐️</emoji>",
            "robot": "<emoji id=5350396951407895212>⚙️</emoji>",
            "klip": "<emoji id=5972261808747057065>📎</emoji>",
            "net": "<emoji id=5224450179368767019>🌐</emoji>",
            "up": "<emoji id=5445355530111437729>⬆️</emoji>",
            "down": "<emoji id=5443127283898405358>⬇️</emoji>",
            "speed": "<emoji id=5456140674028019486>⚡️</emoji>",
        }

        emote_dict = emote_ids if is_premium else emotes

        for key, emote in emote_dict.items():
            dB.set_var(new_client.me.id, f"emo_{key}", emote)

    def initialize(self):
        me = self.client.me
        self.me = me
        self.user_id = me.id
        self.mention = f"[{me.first_name} {me.last_name or ''}](tg://user?id={me.id})"
        self.full_name = f"{me.first_name} {me.last_name or ''}"
        self.is_premium = me.is_premium
        self.load_emoji()

    def get_costum_text(self):
        me = self.client.me.id
        pong_ = dB.get_var(me, "text_ping") or "Ping"
        uptime_ = dB.get_var(me, "text_uptime") or "Uptime"
        mmg = f"<a href=tg://user?id={self.client.me.id}>{self.client.me.first_name} {self.client.me.last_name or ''}</a>"
        owner_ = dB.get_var(me, "text_owner") or f"Owner: {mmg}"
        ubot_ = dB.get_var(me, "text_ubot") or f"{nama_bot}"
        proses_ = dB.get_var(me, "text_gcast") or "Proses"
        sukses_ = dB.get_var(me, "text_sukses") or "Gcast Sukses"
        return pong_, uptime_, owner_, ubot_, proses_, sukses_

    def load_emoji(self):
        for key in self.DEFAULT_VARS:
            var = dB.get_var(self.user_id, key)

            if self.is_premium:
                default = self.CUSTOM_EMOJI_IDS.get(key)
                if isinstance(var, int):
                    setattr(self, key, var)
                else:
                    dB.set_var(self.user_id, key, default)
                    setattr(self, key, default)
            else:
                default = self.DEFAULT_VARS.get(key)
                if isinstance(var, str):
                    setattr(self, key, var)
                else:
                    dB.set_var(self.user_id, key, default)
                    setattr(self, key, default)

    def set_emoji(self, var_name, new_value):
        if var_name not in self.CUSTOM_EMOJI_IDS and var_name not in self.DEFAULT_VARS:
            raise ValueError(f"Variabel '{var_name}' tidak valid.")
        dB.set_var(self.user_id, var_name, new_value)
        setattr(
            self,
            var_name,
            str(new_value) if not isinstance(new_value, int) else new_value,
        )

    def reset_emoji(self):
        if self.is_premium:
            for key, default in self.CUSTOM_EMOJI_IDS.items():
                dB.set_var(self.user_id, key, default)
                setattr(self, key, default)
        else:
            for key, default in self.DEFAULT_VARS.items():
                dB.set_var(self.user_id, key, default)
                setattr(self, key, default)
        return f"Emoji sudah di reset ke default untuk: {self.mention}."

    def _format_emoji(self, var, fallback_emoji):
        # Tampilkan emoji hanya jika pengguna premium
        if not self.is_premium:
            return ""  # Non-premium tidak mendapatkan emoji
        if isinstance(var, int):
            return f"<emoji id={var}>{fallback_emoji}</emoji> "
        return var

    @property
    def ping(self):
        return self._format_emoji(self.emo_ping, "🏓")

    @property
    def msg(self):
        return self._format_emoji(self.emo_msg, "✉️")

    @property
    def proses(self):
        return self._format_emoji(self.emo_proses, "⏳")

    @property
    def sukses(self):
        return self._format_emoji(self.emo_sukses, "✅")

    @property
    def gagal(self):
        return self._format_emoji(self.emo_gagal, "❌")

    @property
    def profil(self):
        return self._format_emoji(self.emo_profil, "👤")

    @property
    def owner(self):
        return self._format_emoji(self.emo_owner, "⭐")

    @property
    def warn(self):
        return self._format_emoji(self.emo_warn, "⚠️")

    @property
    def block(self):
        return self._format_emoji(self.emo_block, "⛔")

    @property
    def pong(self):
        return self._format_emoji(self.emo_uptime, "⏰")

    @property
    def robot(self):
        return self._format_emoji(self.emo_robot, "⚙️")

    @property
    def klip(self):
        return self._format_emoji(self.emo_klip, "📎")

    @property
    def net(self):
        return self._format_emoji(self.emo_net, "🌐")

    @property
    def up(self):
        return self._format_emoji(self.emo_up, "⬆️")

    @property
    def down(self):
        return self._format_emoji(self.emo_down, "⬇️")

    @property
    def speed(self):
        return self._format_emoji(self.emo_speed, "⚡️")


def del_emoji(msg):
    dia = msg.me
    dB.remove_var(dia.id, "emo_ping")
    dB.remove_var(dia.id, "emo_pong")
    dB.remove_var(dia.id, "emo_proses")
    dB.remove_var(dia.id, "emo_sukses")
    dB.remove_var(dia.id, "emo_gagal")
    dB.remove_var(dia.id, "emo_profil")
    dB.remove_var(dia.id, "emo_owner")
    dB.remove_var(dia.id, "emo_warn")
    dB.remove_var(dia.id, "emo_block")


def setting_emoji(msg):
    dia = msg.me
    ping_ = dB.get_var(dia.id, "emo_ping")
    pong_ = dB.get_var(dia.id, "emo_pong")
    proses_ = dB.get_var(dia.id, "emo_proses")
    sukses_ = dB.get_var(dia.id, "emo_sukses")
    gagal_ = dB.get_var(dia.id, "emo_gagal")
    profil_ = dB.get_var(dia.id, "emo_profil")
    alive_ = dB.get_var(dia.id, "emo_owner")
    warn_ = dB.get_var(dia.id, "emo_warn")
    block_ = dB.get_var(dia.id, "emo_block")
    ping = "🏓"
    ping_id = int("5258330865674494479")
    pong = "🥵"
    pong_id = int("5258501105293205250")
    proses = "🔄"
    proses_id = int("5427181942934088912")
    gagal = "❌"
    gagal_id = int("5260342697075416641")
    sukses = "✅"
    sukses_id = int("5260416304224936047")
    profil = "👤"
    profil_id = int("5258011929993026890")
    alive = "⭐"
    alive_id = int("5258165702707125574")
    warn = "❗"
    warn_id = int("5260249440450520061")
    block = "🚫"
    block_id = int("5258362429389152256")
    if not (ping_, pong_, proses_, sukses_, gagal_, profil_, alive_, warn_, block_):
        if dia.is_premium == True:
            dB.set_var(dia.id, "emo_ping", ping_id)

            dB.set_var(dia.id, "emo_pong", pong_id)

            dB.set_var(dia.id, "emo_proses", proses_id)

            dB.set_var(dia.id, "emo_gagal", gagal_id)

            dB.set_var(dia.id, "emo_sukses", sukses_id)

            dB.set_var(dia.id, "emo_profil", profil_id)

            dB.set_var(dia.id, "emo_owner", alive_id)

            dB.set_var(dia.id, "emo_warn", warn_id)

            dB.set_var(dia.id, "emo_block", block_id)

        elif dia.is_premium == False:
            dB.set_var(dia.id, "emo_ping", ping)

            dB.set_var(dia.id, "emo_pong", pong)

            dB.set_var(dia.id, "emo_proses", proses)

            dB.set_var(dia.id, "emo_gagal", gagal)

            dB.set_var(dia.id, "emo_sukses", sukses)

            dB.set_var(dia.id, "emo_profil", profil)

            dB.set_var(dia.id, "emo_owner", alive)

            dB.set_var(dia.id, "emo_warn", warn)

            dB.set_var(dia.id, "emo_block", block)

    else:
        pass


async def create_logs(client):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    chat_id = None
    nama = f"{nama_bot} Logs"
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.SUPERGROUP:
            if dialog.chat.title == nama:
                chat_id = dialog.chat.id
    if chat_id:
        logger.info(f"{nama} {chat_id}")
        dB.set_var(client.me.id, "NEW_LOG", chat_id)
        link = await client.export_chat_invite_link(chat_id)
        try:
            await client.add_chat_members(chat_id, bot_username)
            privileges = types.ChatPrivileges()
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=bot_id,
                privileges=privileges,
            )
        except Exception:
            pass
        return link
    else:
        des = "Jangan Keluar Dari Grup Log Ini\n\nPowered by: @ZeebSupport"
        gc = await client.create_supergroup(nama, des)
        poto = f"downloads/pp_{client.me.id}.jpg"
        await client.bash(f"wget {log_pic} -O {poto}")
        gmbr = {"video": poto} if poto.endswith(".mp4") else {"photo": poto}
        await client.set_chat_photo(gc.id, **gmbr)
        dB.set_var(client.me.id, "NEW_LOG", gc.id)
        if os.path.exists(poto):
            os.remove(poto)
        link = await client.export_chat_invite_link(gc.id)
        await client.add_chat_members(gc.id, bot_username)
        privileges = types.ChatPrivileges()
        await client.promote_chat_member(
            chat_id=gc.id,
            user_id=bot_id,
            privileges=privileges,
        )
        return link


def initial_ctext(c):
    pong_ = dB.get_var(c.me.id, "text_pong") or "Pong"
    uptime_ = dB.get_var(c.me.id, "text_uptime") or "Uptime"
    mmg = f"<a href=tg://user?id={c.me.id}>{c.me.first_name} {c.me.last_name or ''}</a>"
    owner_ = dB.get_var(c.me.id, "text_owner") or f"Owner: {mmg}"
    ubot_ = dB.get_var(c.me.id, "text_ubot") or f"{nama_bot}"
    proses_ = dB.get_var(c.me.id, "text_gcast") or "Processing..."
    sukses_ = dB.get_var(c.me.id, "text_sukses") or "Broadcast results"
    return pong_, uptime_, owner_, ubot_, proses_, sukses_
