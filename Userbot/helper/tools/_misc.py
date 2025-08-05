import asyncio
import functools
import glob
import math
import multiprocessing
import os
import random
import time
from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Union

from yt_dlp import YoutubeDL

max_workers = multiprocessing.cpu_count() * 5
exc_ = ThreadPoolExecutor(max_workers=max_workers)


from pyrogram.errors import FloodWait, MessageNotModified

# part of https://github.com/DevsExpo/FridayUserbot


def ReplyCheck(m):
    reply_id = None
    if m.reply_to_message:
        reply_id = m.reply_to_message.id
    elif not m.from_user:
        reply_id = m.id
    return reply_id


def humanbytes(size):
    """Convert Bytes To Bytes So That Human Can Read It"""
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Time Formatter"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


async def progress(current, total, message, start, type_of_ps, file_name=None):
    """Progress Bar For Showing Progress While Uploading / Downloading File - Normal"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def run_in_exc(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(exc_, lambda: f(*args, **kwargs))

    return wrapper


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


def cookies():
    folder_path = f"{os.getcwd()}/cookies"
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return f"""cookies/{str(cookie_txt_file).split("/")[-1]}"""


def get_ytdl_options(
    ytdl_opts: Union[str, dict, list], commandline: bool = True
) -> Union[str, dict, list]:
    token_data = os.getenv("TOKEN_DATA")

    if isinstance(ytdl_opts, list):
        if token_data:
            ytdl_opts += [
                "--username" if commandline else "username",
                "oauth2",
                "--password" if commandline else "password",
                "''",
            ]
        else:
            ytdl_opts += ["--cookies" if commandline else "cookiefile", cookies()]

    elif isinstance(ytdl_opts, str):
        if token_data:
            ytdl_opts += (
                "--username oauth2 --password '' "
                if commandline
                else "username oauth2 password '' "
            )
        else:
            ytdl_opts += (
                f"--cookies {cookies()}" if commandline else f"cookiefile {cookies()}"
            )

    elif isinstance(ytdl_opts, dict):
        if token_data:
            ytdl_opts.update({"username": "oauth2", "password": ""})
        else:
            ytdl_opts["cookiefile"] = cookies()

    return ytdl_opts


async def YoutubeDownload(url, as_video=False, as_url=False):
    if as_video:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    else:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    data_ytp = "<blockquote><b>💡 Informasi {}</b>\n\n<b>🏷 Nama:</ʙ> {}<b>\n<b>🧭 Durasi:</b> {}\n<b>👀 Dilihat:</b> {}\n<b>📢 Channel:</b> {}\n<b>🔗 Tautan:</b> <a href={}>Youtube</a>\n\n<b>⚡ Download By:</b> {}</blockquote>"
    ydl_opts = get_ytdl_options(ydl_opts, False)
    ydl = YoutubeDL(ydl_opts)
    ytdl_data = await run_sync(ydl.extract_info, url, download=True)
    file_name = ydl.prepare_filename(ytdl_data)
    videoid = ytdl_data["id"]
    title = ytdl_data["title"]
    url = f"https://youtu.be/{videoid}"
    duration = ytdl_data["duration"]
    channel = ytdl_data["uploader"]
    views = f"{ytdl_data['view_count']:,}".replace(",", ".")
    thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    return file_name, title, url, duration, views, channel, thumb, data_ytp


"""


async def YoutubeDownload(url, as_video=False, as_url=False):
    url = f"https://api.botcahx.eu.org/api/dowloader/yt?url={url}&apikey={botcax_api}"
    response = await get(url)
    if response["status"] == True:
        if as_video:
            data = response["result"]
            title = data["title"]
            thumb = data["thumb"]
            url = data["source"]
            duration = data["duration"]
            bahan = data["mp3"]
        else:
            data = response["result"]
            title = data["title"]
            thumb = data["thumb"]
            url = data["source"]
            duration = data["duration"]
            bahan = data["mp4"]
    else:
        return f"{response['status']}"
    file_name = wget.download(bahan)
    data_ytp = "<blockquote><b>💡 Informasi {}</b>\n\n<b>🏷 Nama:</ʙ> {}</b>\n<b>🧭 Durasi:</b> {}\n<b>🔗 Tautan:</b> <a href={}>Youtube</a>\n\n<b>⚡ Download By:</b> {}</blockquote>"

    return file_name, title, url, int(duration), thumb, data_ytp
"""


def get_file_size(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)


async def BokepDownload(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
        "nocheckcertificate": True,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
    }
    ydl = YoutubeDL(ydl_opts)
    ytdl_data = await run_sync(ydl.extract_info, url, download=True)
    file_name = ydl.prepare_filename(ytdl_data)
    full_title = ytdl_data["title"]
    file_size = get_file_size(file_name)
    if file_size > 1000:
        os.remove(file_name)
        return None, f"File terlalu besar untuk diunduh. Ukuran: {file_size:.2f} MiB"

    return file_name, full_title


"""
async def BokepDownload(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
        "nocheckcertificate": True,
        "geo_bypass": True,
    }
    ydl = YoutubeDL(ydl_opts)
    ytdl_data = await run_sync(ydl.extract_info, url, download=True)
    file_name = ydl.prepare_filename(ytdl_data)
    full_title = ytdl_data["title"]
    return file_name, full_title
"""
