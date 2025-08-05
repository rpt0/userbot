import re
from datetime import datetime
from html import escape
from re import compile as compilere
from re import sub
from traceback import format_exc
from typing import List

from pyrogram.enums import ChatType
from pytz import timezone
from regex import search

from ..database import dB

SMART_OPEN = "“"
SMART_CLOSE = "”"
START_CHAR = ("'", '"', SMART_OPEN)

JAKARTA_TZ = timezone("Asia/Jakarta")


async def regex_searcher(regex_string: str, string: str) -> str:
    """Search for Regex in string."""
    try:
        re_search = search(regex_string, string, timeout=6)
    except TimeoutError:
        return False
    except Exception:
        return format_exc()
        return False

    return re_search


def extract_ids_from_link(link):
    type = "t.me/c/" in link
    chat_id = (
        int("-100" + str(link.split("/")[-2])) if type else str(link.split("/")[-2])
    )
    msg_id = int(link.split("/")[-1])
    return chat_id, msg_id


async def cleanhtml(raw_html: str) -> str:
    """Clean html data."""
    cleanr = compilere("<.*?>")
    return sub(cleanr, "", raw_html)


async def escape_markdown(text: str) -> str:
    """Escape markdown data."""
    escape_chars = r"\*_`\["
    return sub(r"([%s])" % escape_chars, r"\\\1", text)


async def mention_html(name: str, user_id: int) -> str:
    """Mention user in html format."""
    name = escape(name)
    return f'<a href="tg://user?id={user_id}">{name}</a>'


async def mention_markdown(name: str, user_id: int) -> str:
    """Mention user in markdown format."""
    return f"[{(await escape_markdown(name))}](tg://user?id={user_id})"


async def clean_html(text: str) -> str:
    return (
        text.replace("<code>", "")
        .replace("</code>", "")
        .replace("<b>", "")
        .replace("</b>", "")
        .replace("<i>", "")
        .replace("</i>", "")
        .replace("<u>", "")
        .replace("</u>", "")
    )


async def clean_markdown(text: str) -> str:
    return text.replace("`", "").replace("**", "").replace("__", "")


async def remove_markdown_and_html(text: str) -> str:
    return await clean_markdown(await clean_html(text))


kode_bahasa = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Chinese": "zh-cn",
    "Czech": "cs",
    "German": "de",
    "Greek": "el",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Hindi": "hi",
    "Indonesian": "id",
    "Icelandic": "is",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Korean": "ko",
    "Latin": "la",
    "Myanmar": "my",
    "Nepali": "ne",
    "Dutch": "nl",
    "Portuguese": "pt",
    "Russian": "ru",
    "Sundanese": "su",
    "Swedish": "sv",
    "Thailand": "th",
    "Filipino": "tl",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Catalan": "ca",
    "Danish": "da",
    "Finnish": "fi",
    "Hungarian": "hu",
    "Polish": "pl",
    "Ukrainian": "uk",
    "Taiwan": "zh-tw",
}


parse_words = [
    "first",
    "last",
    "fullname",
    "id",
    "mention",
    "username",
    "chatname",
    "day",
    "date",
    "month",
    "year",
    "hour",
    "minutes",
]


async def escape_one(text: str, valids: List[str]) -> str:
    new_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] == "{":
            if idx + 1 < len(text) and text[idx + 1] == "{":
                idx += 2
                new_text += "{{{{"
                continue
            success = False
            for v in valids:
                if text[idx:].startswith("{" + v + "}"):
                    success = True
                    break
            if success:
                new_text += text[idx : idx + len(v) + 2]
                idx += len(v) + 2
                continue
            new_text += "{{"

        elif text[idx] == "}":
            if idx + 1 < len(text) and text[idx + 1] == "}":
                idx += 2
                new_text += "}}}}"
                continue
            new_text += "}}"

        else:
            new_text += text[idx]
        idx += 1

    return new_text


async def escape_gc(m, text):
    if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP, ChatType.CHANNEL]:
        escape(m.chat.title)
    else:
        escape(m.from_user.first_name)
    teks = await escape_one(text, parse_words)
    if teks:
        pass
    else:
        teks = ""
    return teks


async def escape_fil(
    m,
    text: str,
    parse_words: list,
) -> str:
    if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP, ChatType.CHANNEL]:
        chat_name = escape(m.chat.title)
    else:
        chat_name = escape(m.from_user.first_name)
    teks = await escape_one(text, parse_words)
    if teks:
        teks = teks.format(
            first=escape(m.from_user.first_name),
            last=escape(m.from_user.last_name or m.from_user.first_name),
            mention=m.from_user.mention,
            username=(
                "@" + (await escape_markdown(escape(m.from_user.username)))
                if m.from_user.username
                else m.from_user.mention
            ),
            fullname=" ".join(
                (
                    [
                        escape(m.from_user.first_name),
                        escape(m.from_user.last_name),
                    ]
                    if m.from_user.last_name
                    else [escape(m.from_user.first_name)]
                ),
            ),
            chatname=chat_name,
            id=m.from_user.id,
        )
    else:
        teks = ""

    return teks


async def escape_tag(
    c,
    ore: int,
    text: str,
    parse_words: list,
) -> str:
    orang = dB.get_userdata(ore)
    if not orang:
        return ""
    text = re.sub(r"~ \[.*?\|.*?\]", "", text)
    days_mapping = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu",
    }
    months_mapping = {
        "January": "Januari",
        "February": "Februari",
        "March": "Maret",
        "April": "April",
        "May": "Mei",
        "June": "Juni",
        "July": "Juli",
        "August": "Agustus",
        "September": "September",
        "October": "Oktober",
        "November": "November",
        "December": "Desember",
    }
    now = datetime.now(JAKARTA_TZ)
    current_time = {
        "day": days_mapping[now.strftime("%A")],
        "date": now.strftime("%d"),
        "month": months_mapping[now.strftime("%B")],
        "year": now.strftime("%Y"),
        "hour": now.strftime("%H"),
        "minutes": now.strftime("%M"),
    }
    teks = await escape_one(text, parse_words)
    if teks:
        teks = teks.format(
            first=orang["depan"],
            last=orang["belakang"],
            mention=orang["full"],
            username=orang["username"],
            fullname=orang["full"],
            id=orang["_id"],
            **current_time,
        )
    else:
        teks = ""

    return teks


async def split_quotes(text: str):
    """Split quotes in text."""
    if not any(text.startswith(char) for char in START_CHAR):
        return text.split(None, 1)
    counter = 1  # ignore first char -> is some kind of quote
    while counter < len(text):
        if text[counter] == "\\":
            counter += 1
        elif text[counter] == text[0] or (
            text[0] == SMART_OPEN and text[counter] == SMART_CLOSE
        ):
            break
        counter += 1
    else:
        return text.split(None, 1)

    # 1 to avoid starting quote, and counter is exclusive so avoids ending
    key = await remove_escapes(text[1:counter].strip())
    # index will be in range, or `else` would have been executed and returned
    rest = text[counter + 1 :].strip()
    if not key:
        key = text[0] + text[0]
    return list(filter(None, [key, rest]))


async def remove_escapes(text: str) -> str:
    """Remove the escaped from message."""
    res = ""
    is_escaped = False
    for counter in range(len(text)):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
    return res
