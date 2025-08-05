import asyncio
import os
import time
from datetime import datetime, timedelta
from typing import Union

from pyrogram.types import Voice
from pytgcalls.types import AudioQuality, MediaStream, VideoQuality
from youtubesearchpython import VideosSearch

from Userbot import nlx

from ._formatters import convert_bytes, get_readable_time, seconds_to_min

lyrical = {}
queues = {}
demus_data = {}
streaming_data = {}
downloader = {}

plere = """<blockquote><u><b><emoji id=5260268501515377807>🎼</emoji>{} Now Playing {} <emoji id={}>🎶</emoji></b></u>

<b><emoji id=5260348422266822411>🎵</emoji> Title: {}</b>
<b><emoji id=5260652149469094137>🎤</emoji> Uploader: <u>{}</u></b>
<b><emoji id=5258258882022612173>⏲️️</emoji> Duration: <code>{}</code></b>
<b><emoji id=5260233433107407649>🖇️</emoji> Source: <a href={}>{}</a></b>
<b><emoji id=5316727448644103237>📩</emoji> Request: {}</b></blockquote>"""


def cleanup_files(*files):
    for file in files:
        if file and os.path.exists(file):
            os.remove(file)


async def cek_file_ada(
    audio: Union[bool, str] = None,
    video: Union[bool, str] = None,
):
    if audio:
        try:
            file_name = (
                audio.file_unique_id
                + "."
                + (
                    (audio.file_name.split(".")[-1])
                    if (not isinstance(audio, Voice))
                    else "ogg"
                )
            )
        except:
            file_name = audio.file_unique_id + "." + ".ogg"
        file_name = os.path.join(os.path.realpath("downloads"), file_name)
    if video:
        try:
            file_name = video.file_unique_id + "." + (video.file_name.split(".")[-1])
        except:
            file_name = video.file_unique_id + "." + "mp4"
        file_name = os.path.join(os.path.realpath("downloads"), file_name)
    return file_name


@nlx.pytgcall_close_stream()
async def clse_stream(client, update):
    chat_id = update.chat_id
    print(f"Stream ended for chat_id: {chat_id}")
    return await client.leave_call(chat_id)


async def run_stream(link, type):
    if type == "Audio":
        stream = MediaStream(
            media_path=link,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
        )

    elif type == "Video":
        stream = MediaStream(
            media_path=link,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.FHD_1080p,
        )

    return stream


def get_judul(query: str):
    search = VideosSearch(query, limit=1).result()["result"][0]
    link = f"https://youtu.be/{search['id']}"
    return link


class TeleAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.sleep = 5

    async def send_split_text(self, message, string):
        n = self.chars_limit
        out = [(string[i : i + n]) for i in range(0, len(string), n)]
        j = 0
        for x in out:
            if j <= 2:
                j += 1
                await message.reply_text(x)
        return True

    async def get_link(self, message):
        if message.chat.username:
            link = f"https://t.me/{message.chat.username}/{message.reply_to_message.id}"
        else:
            xf = str((message.chat.id))[4:]
            link = f"https://t.me/c/{xf}/{message.reply_to_message.id}"
        return link

    async def get_filename(self, file, audio: Union[bool, str] = None):
        try:
            file_name = file.file_name
            if file_name is None:
                file_name = "Telegram Audio" if audio else "Telegram Video"

        except:
            file_name = "Telegram Audio" if audio else "Telegram Video"
        return file_name

    async def get_duration(self, file):
        try:
            dur = seconds_to_min(file.duration)
        except:
            dur = "Unknown"
        return dur

    async def get_filepath(
        self,
        audio: Union[bool, str] = None,
        video: Union[bool, str] = None,
    ):
        if audio:
            try:
                file_name = (
                    audio.file_unique_id
                    + "."
                    + (
                        (audio.file_name.split(".")[-1])
                        if (not isinstance(audio, Voice))
                        else "ogg"
                    )
                )
            except:
                file_name = audio.file_unique_id + "." + ".ogg"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        if video:
            try:
                file_name = (
                    video.file_unique_id + "." + (video.file_name.split(".")[-1])
                )
            except:
                file_name = video.file_unique_id + "." + "mp4"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        return file_name

    async def download(self, c, message, mystic, fname):
        left_time = {}
        speed_counter = {}
        if os.path.exists(fname):
            return True

        async def down_load():
            async def progress(current, total):
                if current == total:
                    return
                current_time = time.time()
                start_time = speed_counter.get(message.id)
                check_time = current_time - start_time
                if datetime.now() > left_time.get(message.id):
                    percentage = current * 100 / total
                    percentage = str(round(percentage, 2))
                    speed = current / check_time
                    eta = int((total - current) / speed)
                    downloader[message.id] = eta
                    eta = get_readable_time(eta)
                    if not eta:
                        eta = "0 sec"
                    total_size = convert_bytes(total)
                    completed_size = convert_bytes(current)
                    speed = convert_bytes(speed)
                    text = f"""
**{c.me.mention} Telegram Media Downloader**

**Size:** {total_size}
**Complete:** {completed_size} 
**percentage:** {percentage[:5]}%

**Speed:** {speed}/s
**Elapsed Time:** {eta}"""
                    try:
                        await mystic.edit_text(text)
                    except:
                        pass
                    left_time[message.id] = datetime.now() + timedelta(
                        seconds=self.sleep
                    )

            speed_counter[message.id] = time.time()
            left_time[message.id] = datetime.now()

            try:
                await c.download_media(
                    message.reply_to_message,
                    file_name=fname,
                    progress=progress,
                )
                await mystic.edit_text("Succesfully Downloaded...")
                downloader.pop(message.id)
            except:
                await mystic.edit_text("Gagal mengunduh media dari telegram.")

        if len(downloader) > 10:
            timers = []
            for x in downloader:
                timers.append(downloader[x])
            try:
                low = min(timers)
                eta = get_readable_time(low)
            except:
                eta = "Unknown"
            await mystic.edit_text(
                "**kelebihan beban** dengan unduhan sekarang.\n\n**Coba Setelah:** {} (__waktu yang diharapkan__)".format(
                    eta
                )
            )
            return False

        task = asyncio.create_task(down_load())
        lyrical[mystic.id] = task
        await task
        downloaded = downloader.get(message.id)
        if downloaded:
            downloader.pop(message.id)
            return False
        verify = lyrical.get(mystic.id)
        if not verify:
            return False
        lyrical.pop(mystic.id)
        return True


Telegram = TeleAPI()
