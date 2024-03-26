from ...admin import auth
from pyrogram import Client, filters

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
    if not (await auth(message.from_user.id)):
        return
    
    await message.reply_text(
        text=TEXT,
        quote=True
    )