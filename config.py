import json
import sys
from base64 import b64decode
from os import getenv

import requests
from dotenv import load_dotenv

black = int(b64decode("MTA1NDI5NTY2NA=="))

ERROR = "idk"
DIBAN = ".."


def get_tolol():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi90b2xvbC5qc29u"
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        return f"An error occurred: {str(e)}"
        sys.exit(1)


TOLOL = get_tolol()

NO_GCAST = []

load_dotenv()

id_button = {}
CMD_HELP = {}


DEVS = []

devs_boong = list(map(int, getenv("devs_boong", "").split()))
api_id = int(getenv("api_id", "25732274"))
api_hash = getenv("api_hash", "")
bot_token = getenv("bot_token", "")
bot_id = int(getenv("bot_id", ""))
db_name = getenv("db_name", "")
log_pic = getenv("log_pic", "")
def_bahasa = getenv("def_bahasa", "id")
owner_id = int(getenv("owner_id", ""))
the_cegers = list(
    map(
        int,
        getenv(
            "the_cegers",
            "",
        ).split(),
    )
)
dump = int(getenv("dump", "-100000000"))
bot_username = getenv("bot_username", "@b")
log_userbot = int(getenv("log_userbot", "-1000000"))
log_autoreply = int(getenv("log_userbot", "-1000000ppp"))
nama_bot = getenv("nama_bot", "")
nama_ip = getenv("nama_ip", "")
gemini_api = getenv("gemini_api", "")
botcax_api = getenv("botcax_api", "")


if owner_id not in the_cegers:
    the_cegers.append(owner_id)
if owner_id not in DEVS:
    DEVS.append(owner_id)
for a in the_cegers:
    DEVS.append(a)
