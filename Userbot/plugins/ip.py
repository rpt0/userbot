from base64 import b64decode as kc
from random import choice

import requests
from pyrogram import filters

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "IP"

def help_string(org):
    return h_s(org, "help_ip")

@zb.ubot("ip")
async def hacker_lacak_target(client, message, *args):
    apikey = kc("M0QwN0UyRUFBRjU1OTQwQUY0NDczNEMzRjJBQzdDMUE=").decode("utf-8")
    ran = await message.reply_text("<code>🌐 Processing...</code>")
    ipddres = message.text.split(None, 1)[1] if len(message.command) != 1 else None
    if not ipddres:
        await ran.edit_text(
            "Example: <code>+ipaddress your ip address here : 199.482.xxx</code>"
        )
        return

    if not apikey:
        await ran.edit_text("⛔ Missing apikey ip location")
        return

    location_link = "https"
    location_api = "api.ip2location.io"
    location_key = f"key={apikey}"
    location_search = f"ip={ipddres}"
    location_param = (
        f"{location_link}://{location_api}/?{location_key}&{location_search}"
    )
    response = requests.get(location_param)
    if response.status_code == 200:
        data_location = response.json()
        try:
            location_ip = data_location["ip"]
            location_code = data_location["country_code"]
            location_name = data_location["country_name"]
            location_region = data_location["region_name"]
            location_city = data_location["city_name"]
            location_zip = data_location["zip_code"]
            location_zone = data_location["time_zone"]
            location_card = data_location["as"]
        except Exception as e:
            await ran.edit_text(f"Error request {e}")
            return
        if (
            location_ip
            and location_code
            and location_name
            and location_region
            and location_city
            and location_zip
            and location_zone
            and location_card
        ):
            location_target = f"""
<blockquote>ᚗ IP address:</b> {location_ip}
ᚗ Country code  : {location_code}
ᚗ Country name : {location_name}
ᚗ Region name  : {location_region}
ᚗ City name     : {location_city}
ᚗ Zip code      : {location_zip}
ᚗ Time Zone    : {location_zone}
ᚗ Data card     : {location_card}</blockquote>
"""
            await ran.edit_text(location_target)
        else:
            await ran.edit_text("⛔ Not data ip address")
    else:
        await ran.edit_text(
            "⛔ Sorry, there was an error processing your request. Please try again later"
        )
