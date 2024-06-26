import os
from dotenv import load_dotenv

load_dotenv()

# For Bot
BOT_NAME = os.environ.get("BOT_NAME", "Tools-Bot")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

# Authorisation and Administrators
AUTH = bool(os.environ.get("AUTH", True))
ADMINS = set(int(x) for x in os.environ.get("ADMINS", "").split())

# Database (MongoDB)
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Tools-Bot")
