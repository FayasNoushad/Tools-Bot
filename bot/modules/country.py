import urllib
from ..admin import auth
from countryinfo import CountryInfo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TEXT = """
--**Country Information**--

- Just send me /countryinfo with a country name
- Then I will check and send you the informations

**Informations :-**
Name, Native Name, Capital, Population, Region, Sub Region, \
Top Level Domains, Calling Codes, Currencies, Residence, \
Timezone, Wikipedia, Google

Example: /countryinfo India"""


# Country information help message
@Client.on_message(
    filters.command(
        [
            "countryinfo_help", "country_info_help", "country_help",
            "countryinfohelp", "country_infohelp", "countryhelp"
        ]
    )
)
async def country_help(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    await message.reply_text(
        text=TEXT,
        quote=True
    )


@Client.on_message(
    filters.command(["countryinfo", "country_info", "country"])
)
async def country_info(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    try:
        if (" " in message.text):
            country = CountryInfo(message.text.split(" ", 1)[1])
        else:
            if (message.reply_to_message) and (message.reply_to_message.text):
                country = CountryInfo(message.reply_to_message.text)
    except KeyError:
        await message.reply_text(
            text="Key error.\nCan you check the name again."
        )
        return
    name_parts = country.name().split()
    updated_name_parts = []
    for i in name_parts:
        updated_name_parts.append(i.capitalize())
    country_name = " ".join(updated_name_parts)
    google_url = "https://www.google.com/search?q="+urllib.parse.quote(country_name)
    info = f"""**Country Information**

Name : `{country_name}`
Native Name : `{country.native_name()}`
Capital : `{country.capital()}`
Population : `{country.population()}`
Region : `{country.region()}`
Sub Region : `{country.subregion()}`
Top Level Domains : `{country.tld()}`
Calling Codes : `{country.calling_codes()}`
Currencies : `{country.currencies()}`
Residence : `{country.demonym()}`
Timezone : `{country.timezones()}`"""
    
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Wikipedia', url=country.wiki()),
                InlineKeyboardButton('Google', url=google_url)

            ]
        ]
    )
    
    try:
        await message.reply_text(
            text=info,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
    except Exception as error:
        print(error)
