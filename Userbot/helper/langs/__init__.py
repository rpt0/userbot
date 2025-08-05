import os
import sys
from typing import Dict, List

import yaml

from Userbot import logger, nlx

from ..database import dB

languages = {}
languages_present = {}


def get_string(key: str, lang: str = "en"):
    if key in languages[lang]:
        return languages[lang][key]
    else:
        return languages["en"].get(key, key)


def get_string2(lang: str, string: str) -> str:
    try:
        return languages[lang][string]
    except KeyError:
        return languages["en"].get(string)


for filename in os.listdir(r"./Userbot/helper/langs/strings/"):
    language_name = filename[:-4]
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./Userbot/helper/langs/strings/en.yml", encoding="utf8")
        )
        languages_present["en"] = languages["en"]["name"]
    if filename.endswith(".yml"):

        if language_name == "en":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./Userbot/helper/langs/strings/" + filename, encoding="utf8")
        )
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except:
        logger.error("There is some issue with the language file inside bot.")
        exit()
