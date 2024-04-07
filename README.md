# Tools Bot
A telegram tools bot with more features for groups and personal use.

---

## Features

- AI: AI using Gemini API
- User/Chat Information
- QR Code Encoding and Decoding
- Translating messages
- YouTube Video Thumbnail Downloading
- Country Information
- Word Dictionary

---

## Deploy

```sh
git clone https://github.com/FayasNoushad/Tools-Bot.git
cd Tools-Bot
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
# <Create Variables appropriately>
python3 main.py
```

---

## Variables

### Required

- `API_HASH` Your API Hash from my.telegram.org
- `API_ID` Your API ID from my.telegram.org
- `BOT_TOKEN` Your bot token from @BotFather
- `DATABASE_URL` MongoDB URL
- `ADMINS` Administrators IDs seperated by whitespace

### Not Required

- `BOT_NAME` Your bot name
- `DATABASE_NAME` MongoDB Database Name
- `AUTH` Enable or Disable authentication

---

## Credits

- [Contributors](https://github.com/FayasNoushad/Gemini-Bot/graphs/contributors)
- [Pyrogram](https://github.com/pyrogram/pyrogram)

---

