from ...authorise import auth
from ...common import MORE_HELP_ONLY
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
async def country_help(_, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if cb:
        await message.message.edit_text(
            text=TEXT,
            disable_web_page_preview=True,
            reply_markup=MORE_HELP_ONLY
        )
    else:
        await message.reply_text(
            text=TEXT,
            quote=True,
            disable_web_page_preview=True,
            reply_markup=MORE_HELP_ONLY
        )