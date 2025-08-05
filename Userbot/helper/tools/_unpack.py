from base64 import urlsafe_b64decode
from struct import error as StructError
from struct import unpack

from attrify import Attrify as Atr


def unpackInlineMessage(inline_message_id: str):
    try:
        decoded_data = urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4)
        )
        if len(decoded_data) != 20:
            return None
        dc_id, message_id, chat_id, query_id = unpack("<iiiq", decoded_data)
        temp = {
            "dc_id": dc_id,
            "message_id": message_id,
            "chat_id": int(str(chat_id).replace("-1", "-1001")),
            "query_id": query_id,
            "inline_message_id": inline_message_id,
        }
        return Atr(temp)

    except (StructError, ValueError):
        return None


def unpacked4(inline_message_id: str):
    dc_id, message_id, chat_id, query_id = unpack(
        "<iiiq",
        urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4),
        ),
    )
    if str(chat_id).startswith("-"):
        chat = int(str(chat_id).replace("-", "-100"))
    else:
        chat = int(str(chat_id))
    if str(query_id).startswith("-"):
        nquery = int(str(query_id).replace("-", ""))

    else:
        nquery = int(str(query_id))

    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": chat,
        "query_id": nquery,
        "inline_message_id": inline_message_id,
    }
    return Atr(temp)


def unpacked2(inline_message_id: str):
    dc_id, message_id, chat_id, query_id = unpack(
        "<iiiq",
        urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4),
        ),
    )
    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": int(str(chat_id).replace("-", "-100")),
        "query_id": query_id,
        "inline_message_id": inline_message_id,
    }
    return Atr(temp)


async def unpacked3(inline_message_id: str):
    decoded_data = urlsafe_b64decode(
        inline_message_id + "=" * (len(inline_message_id) % 4)
    )

    if len(decoded_data) != 20:
        raise ValueError("Invalid inline_message_id length for get_message_data")

    dc_id, message_id, chat_id, query_id = unpack("<iiiq", decoded_data)

    chat_id = int(str(chat_id).replace("-1", "-1001"))

    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": chat_id,
        "query_id": query_id,
        "inline_message_id": inline_message_id,
    }

    return Atr(temp)
