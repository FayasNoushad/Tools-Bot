import os
import textwrap
import PIL.Image
from vars import GEMINI_API
from ..admin import auth
from pyrogram import Client, filters
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown


HELP = """
--**Gemini AI**--

**Text only:**
- Just send me question as text with /ai command
- I will reply with generated text

**Photo only:**
- Just send me photo
- Then reply /ai command to the photo
- I will reply with generated text

**Photo and Text:**
- Send me a photo
- Reply /ai command with text to the photo
- I will reply with generated text
"""

# Gemini AI Help Message
@Client.on_message(
    filters.command(
        ["aihelp", "ai_help", "geminihelp", "gemini_help", "geminiai_help", "bardhelp", "bard_help"]
    )
)
async def gemini_help(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    await message.reply_text(
        text=HELP,
        quote=True
    )


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Update the handle_message function to call the Gemini AI API
@Client.on_message(filters.command(["ai", "genai", "aitext", "gemini", "bard"]))
async def gemini_ai(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    if (message.reply_to_message) and (message.reply_to_message.photo):
        await gemini_ai_img(_, message)
    else:
        await gemini_ai_text(_, message)


# Update the handle_message function to call the Gemini AI API
@Client.on_message(filters.command(["genaitext", "aitext", "geminitext", "textai"]))
async def gemini_ai_text(_, message, text=""):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # To avoid command only messages
    if message.text.startswith("/") and (" " not in message.text) and (not message.reply_to_message) and (not message.reply_to_message.text):
        return
    
    m = await message.reply_text("Please wait...", quote=True)
    
    if text:
        query = text
    else:
        if (message.reply_to_message and (" " not in message.text)):
            query = message.reply_to_message.text
        else:
            query = message.text.split(" ", 1)[1]
    
    genai.configure(api_key=GEMINI_API)
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(query)
    except Exception as e:
        await m.edit_text("e", disable_web_page_preview=True)
        return
    
    if response.parts:
        for part in response.parts:
            result = part.text
            if len(result) < 4096:
                await message.reply_text(
                    text=result,
                    disable_web_page_preview=True,
                    quote=True
                )
            else:
                directory_path = "./downloads"
                file_path = os.path.join(directory_path, "result.md")
                with open(file_path, "w") as file:
                    file.write(result)
                await message.reply_document(
                    document=file_path,
                    quote=True
                )
                os.remove(file_path)
    else:
        result = to_markdown(response.text)
        if len(result) < 4096:
            await message.reply_text(
                text=result,
                disable_web_page_preview=True,
                quote=True
            )
        else:
            directory_path = "./downloads"
            file_path = os.path.join(directory_path, "result.md")
            with open(file_path, "w") as file:
                file.write(result)
            await message.reply_document(
                document=file_path,
                quote=True
            )
            os.remove(file_path)
    await m.delete()


@Client.on_message(filters.command(["aiimage", "genaiimage", "aiimg", "geminivision", "imgai"]))
async def gemini_ai_img(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    m = await message.reply_text("Please wait...", quote=True)
    
    image = await message.reply_to_message.download()
    img = PIL.Image.open(image)
    
    genai.configure(api_key=GEMINI_API)
    model = genai.GenerativeModel('gemini-pro-vision')
    
    try:
        if (" " in message.text):
            query = message.text.split(" ", 1)[1]
            response = model.generate_content([query, img])
        else:
            response = model.generate_content(img)
    except Exception as e:
        await m.edit_text(e, disable_web_page_preview=True)
        return
    
    results = []
    if response.parts:
        for part in response.parts:
            results.append(part.text)
    else:
        results.append(to_markdown(response.text))
    
    for result in results:
        try:
            if len(result) < 4096:
                await message.reply_text(
                    text=result,
                    disable_web_page_preview=True,
                    quote=True
                )
            else:
                directory_path = "./downloads"
                file_path = os.path.join(directory_path, "result.md")
                with open(file_path, "w") as file:
                    file.write(result)
                await message.reply_document(
                    document=file_path,
                    quote=True
                )
                os.remove(file_path)
        except:
            pass
    await m.delete()
    try:
        os.remove(image)
    except Exception as e:
        print(e)
