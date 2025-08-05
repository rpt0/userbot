from geopy.geocoders import Nominatim
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Gps"

def help_string(org):
    return h_s(org, "help_gps")

@zb.ubot("gps|maps")
async def gps(client, message, *args):
    input_str = message.text.split(" ", 1)
    
    if len(input_str) < 2:
        return await message.reply("Mohon berikan tempat yang dicari.")
    
    input_str = input_str[1]
    await message.reply("Menemukan lokasi ini di server map...")
   
    geolocator = Nominatim(user_agent="bot")
    geoloc = geolocator.geocode(input_str)
    
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await message.reply_location(latitude=lat, longitude=lon)
    else:
        await message.reply("Saya tidak dapat menemukannya.")
