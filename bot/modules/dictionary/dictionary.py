import requests
from ...database import db
from pyrogram import Client, filters


async def dictionary(word, id):
    word = requests.utils.quote(word)
    api = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    response = requests.get(api)
    data = response.json()
    if True:#try:
        details = "--**Word Details**--\n"
        
        for i in data:
            details += "\n**Word:** " + i["word"] + "\n"
            
            # Pronunciations
            if ("phonetics" in i) and (len(i["phonetics"]) > 0) and (await db.get_phonetics(id)):
                details += "\n**Pronunciation{}".format("s:**\n" if (len(i["phonetics"])>1) else ":**")
                for phonetic in i["phonetics"]:
                    phonetics_text_settings = await db.get_phonetics_text(id)
                    phonetics_audio_settings = await db.get_phonetics_audio(id)
                    if ("text" in phonetic) and (phonetics_text_settings):
                        if ("audio" in phonetic) and (phonetic["audio"] != "") and (phonetics_audio_settings):
                            details += f"- [{phonetic['text']}]({phonetic['audio']})"
                        else:
                            details += f"- {phonetic['text']}"
                    elif ("audio" in phonetic) and (phonetic["audio"] != "") and (phonetics_audio_settings):
                        details += f"- {phonetic['audio']}"
                    details += "\n"
            
            # Meanings
            if ("meanings" in i) and (len(i["meanings"]) > 0) and (await db.get_meanings(id)):
                for meaning in i["meanings"]:
                    details += "\n"
                    if (await db.get_part_of_speech(id)):
                        details += "**Part of Speech:** " + meaning["partOfSpeech"] + "\n"
                    # Definitions
                    if ("definitions" in meaning) and (await db.get_definitions(id)):
                        for definition in meaning["definitions"]:
                            details += f"- Definition: `{definition['definition']}`\n"
                            if ("example" in definition) and (await db.get_example(id)):
                                details += f"  Example: `{definition['example']}`\n"
                            if ("synonyms" in definition) and (len(definition['synonyms']) > 0)  and (await db.get_synonyms(id)):
                                details += f"  Synonyms: `{', '.join(definition['synonyms'])}`\n"
                            if ("antonyms" in definition) and (len(definition['antonyms']) > 0) and (await db.get_antonyms(id)):
                                details += f"  Antonyms: `{', '.join(definition['antonyms'])}`\n"
        
    #except:
    #    details = "No details found for the word."
    return details


@Client.on_message(filters.command(["dict", "dictionary", "word"]))
async def send_dictionary_details(_, message):
    m = await message.reply_text(
        text="Searching...",
        quote=True
    )
    if (len(message.text.split(" ")) == 1):
        if (message.reply_to_message) and (message.reply_to_message.text):
            word = message.reply_to_message.text
        else:
            await m.edit_text(
                text="Reply to a text message containing the word.",
                disable_web_page_preview=True
            )
            return
    else:
        word = message.text.split(" ", 1)[1]
    details = await dictionary(word, message.from_user.id)
    await m.edit_text(
        text=details,
        disable_web_page_preview=True
    )
