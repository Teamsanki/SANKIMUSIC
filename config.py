import os
from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_SESSION = os.getenv("USER_SESSION")


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

TELEGRAPH_PHOTO = os.getenv("TELEGRAPH_PHOTO")
OWNER_LINK = os.getenv("OWNER_LINK")
SUPPORT_LINK = os.getenv("SUPPORT_LINK")
LOGGER_GROUP_ID = int(os.getenv("LOGGER_GROUP_ID"))
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
