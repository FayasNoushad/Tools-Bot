import os
import textwrap
import PIL.Image
from ...database import db
from ...admin import auth, add_user
from pyrogram import Client, filters
import google.generativeai as genai
from IPython.display import Markdown


def check_api(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    try:
        # for testing the API
        response = model.generate_content('Hello')
        return True
    except:
        return False


async def no_api(message):
    await message.reply_text(
        text="You didn't set your API. Please set your API.\n/help for more details.",
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
    
    # add user to database
    await add_user(message)
    
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
    
    # add user to database
    await add_user(message)
    
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
    
    api = await db.get_api(message.from_user.id)
    if not api:
        await no_api(message)
        return
    genai.configure(api_key=api)
    model = genai.GenerativeModel('gemini-pro')
    
    try:
        response = model.generate_content(query)
    except Exception as e:
        await m.edit_text(e, disable_web_page_preview=True)
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
    
    # add user to database
    await add_user(message)
    
    m = await message.reply_text("Please wait...", quote=True)
    
    image = await message.reply_to_message.download()
    img = PIL.Image.open(image)
    
    api = await db.get_api(message.from_user.id)
    if not api:
        await no_api(message)
        return
    genai.configure(api_key=api)
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
