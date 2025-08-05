import asyncio
from time import time

from ..database import dB
from ._logs import Emojik
from ._misc import ReplyCheck

class AFK_:
    def __init__(self, client, message, reason=""):
        self.client = client
        self.message = message
        self.reason = reason
        self.emo = Emojik(self.client)
        self.emo.initialize()

    async def set_afk(self):
        db_afk = {"time": time(), "reason": self.reason}
        msg_afk = f"{self.emo.sukses} **AFK MODE!**\n Reason: {self.reason}" if self.reason else "Currently AFK!!"
        dB.set_var(self.client.me.id, "AFK", db_afk)
        try:
            ae = await self.message.reply(msg_afk, disable_web_page_preview=True)
            await asyncio.sleep(3)
            return await ae.delete()
        except:
            return

    async def get_afk(self):
        vars = dB.get_var(self.client.me.id, "AFK")
        if vars:
            afk_reason = vars.get("reason")
            afk_text = f"{self.emo.sukses} **AFK MODE!**\n **Reason:** {afk_reason}" if afk_reason else "Currently AFK!!"
            try:
                ae = await self.message.reply(afk_text, disable_web_page_preview=True)
                await asyncio.sleep(3)
                return await ae.delete()
            except:
                return

    async def unset_afk(self):
        vars = dB.get_var(self.client.me.id, "AFK")
        if vars:
            dB.remove_var(self.client.me.id, "AFK")
            afk_text = f"<b>{self.emo.sukses} Back to Online!!"
            try:
                ae = await self.message.reply(afk_text)
                await asyncio.sleep(3)
                return await ae.delete()
            except:
                return
