from ...database import db
from ...authorise import auth
from ...common import MORE_HELP
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton





@Client.on_message(filters.private & filters.command(["dictionary_settings", "dict_settings"]))
async def display_settings(_, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    user_id = message.from_user.id
    """
            dictionary=dict(
                phonetics=dict(
                    phonetics=True,
                    text=True,
                    audio=True
                ),
                origin=True,
                meanings=dict(
                    meanings=True,
                    part_of_speech=True,
                    definitions=True,
                    example=True,
                    synonyms=False,
                    antonyms=False
                )
            )
    """
    text = f"--**Dictionary Settings**--\n"
    buttons = []
    phonetics = await db.get_phonetics(user_id)
    text += f"\n**Phonetics:** `{'Yes' if phonetics else 'No'}`"
    buttons.append(
        [
            InlineKeyboardButton(
                f"Phonetics - {'✅' if phonetics else '❎'}",
                callback_data="dictionary-phonetics-set_phonetics")
        ]
    )
    buttons.append(
        [InlineKeyboardButton("Phonetics Settings", callback_data="dictionary-phonetics-settings")]
    )
    origin = await db.get_origin(user_id)
    text += f"\n**Origin:** `{'Yes' if origin else 'No'}`"
    buttons.append(
        [InlineKeyboardButton(f"Origin - {'✅' if origin else '❎'}", callback_data="dictionary-set_origin")]
    )
    meanings = await db.get_meanings(user_id)
    text += f"\n**Meanings:** `{'Yes' if meanings else 'No'}`"
    buttons.append(
        [InlineKeyboardButton(f"Meanings - {'✅' if meanings else '❎'}", callback_data="dictionary-set_meanings")]
    )
    buttons.append(
        [InlineKeyboardButton("Meanings Settings", callback_data="dictionary-meanings_settings")]
    )
    help_buttons = [
        InlineKeyboardButton("Dictionary Help", callback_data="dictionary-help"),
        MORE_HELP
    ]
    close_btn = [
        InlineKeyboardButton('Close ✖️', callback_data='close')
    ]
    all_buttons = []
    all_buttons.extend(buttons)
    all_buttons.append(help_buttons)
    all_buttons.append(close_btn)
    settings_buttons = InlineKeyboardMarkup(all_buttons)
    try:
        if cb:
            await message.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=settings_buttons
            )
        else:
            await message.reply_text(
                text=text,
                quote=True,
                disable_web_page_preview=True,
                reply_markup=settings_buttons
            )
    except Exception as error:
        print(error)


async def phonetics_settings(_, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    user_id = message.from_user.id
    phonetics = await db.get_phonetics(user_id)
    phonetics_text = await db.get_phonetics_text(user_id)
    phonetics_audio = await db.get_phonetics_audio(user_id)
    text = f"--**Phonetics Settings**--\n"
    text += f"\n**Phonetics:** `{'Enabled' if phonetics else 'Disabled'}`"
    text += f"\n**Phonetics Text:** `{'Yes' if phonetics_text else 'No'}`"
    text += f"\n**Phonetics Audio:** `{'Yes' if phonetics_audio else 'No'}`"
    buttons = [
        [
            InlineKeyboardButton(
                f"Text - {'✅' if phonetics_text else '❎'}",
                callback_data="dictionary-phonetics-set_phonetics_text"),
            InlineKeyboardButton(
                f"Audio - {'✅' if phonetics_audio else '❎'}",
                callback_data="dictionary-phonetics-set_phonetics_audio")
        ],
        [InlineKeyboardButton("Back to Settings", callback_data="dictionary-settings")]
    ]
    help_buttons = [
        InlineKeyboardButton("Dictionary Help", callback_data="dictionary-help"),
        MORE_HELP
    ]
    close_btn = [
        InlineKeyboardButton('Close ✖️', callback_data='close')
    ]
    all_buttons = []
    all_buttons.extend(buttons)
    all_buttons.append(help_buttons)
    all_buttons.append(close_btn)
    settings_buttons = InlineKeyboardMarkup(all_buttons)
    try:
        if cb:
            await message.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=settings_buttons
            )
        else:
            await message.reply_text(
                text=text,
                quote=True,
                disable_web_page_preview=True,
                reply_markup=settings_buttons
            )
    except Exception as error:
        print(error)