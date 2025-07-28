import os
import asyncio
import sys
import time
import random
import string  
import base64

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant

from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION,DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, BOT_USERNAME
from helper_func import is_subscribed1, is_subscribed2, is_subscribed3, subscribed1, subscribed2, subscribed3, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user, is_admin, get_user, expire_premium_user



# Function to auto-delete messages after a delay and send confirmation
async def delete_after_delay(message: Message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass  # In case message is already deleted or something goes wrong 


@Bot.on_message(filters.command('start') & filters.private & subscribed1 & subscribed2 & subscribed3)
async def start_command(client: Bot, message: Message):
    id = message.from_user.id

    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    premium_user_data = await get_user(id)
    if premium_user_data.get("premium", True):
        await expire_premium_user(id, message)  # Expire premium if applicable


    user_data_doc = await get_user(id) 


    if "verify_" in message.text:
        _, token = message.text.split("_", 1)
        if verify_status['verify_token'] != token:
            return await message.reply("Your Token is Invalid or Expired 🥲  Try Again by Clicking /start")
        await update_verify_status(id, is_verified=True, verified_time=time.time())
        reply_markup = None if verify_status["link"] == "" else InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=verify_status["link"])]])
        return await message.reply(f"Your Token Successfully Verified and valid for : {get_exp_time(VERIFY_EXPIRE)} 😀", reply_markup=reply_markup, protect_content=False, quote=True)

    if user_data_doc.get('premium', True) or id == OWNER_ID:
        if len(message.text) > 7:
            try:
                base64_string = message.text.split(" ", 1)[1]
                string_decoded = await decode(base64_string)
                argument = string_decoded.split("-")
                
                if len(argument) == 3:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                    ids = range(start, end+1) if start <= end else list(range(start, end-1, -1))
                elif len(argument) == 2:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                else:
                    return

                temp_msg = await message.reply("Pʟᴇᴀsᴇ ᴡᴀɪᴛ...")
                try:
                    messages = await get_messages(client, ids)
                    await temp_msg.delete()
                    for msg in messages:
                        caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name) if bool(CUSTOM_CAPTION) & bool(msg.document) else ("" if not msg.caption else msg.caption.html)
                        reply_markup = None if DISABLE_CHANNEL_BUTTON else msg.reply_markup
                        
                        try:
                            copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                            await asyncio.sleep(0.5)
                            

                            # Here we call the delete_after_delay function
                            if copied_msg:
                                asyncio.create_task(delete_after_delay(copied_msg, 600))  # Delete after 10 minutes
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                            if copied_msg:
                                asyncio.create_task(delete_after_delay(copied_msg, 600))  # Delete after 10 minutes
                        except:
                            pass
                    await copied_msg.reply("<b>⚠️ Please Note :\nThis File will be Automatically Deleted after 10 Minutes. ⏳</b>")
                except:
                    await message.reply_text("Something went wrong..!")
                return
            except:
                pass
        
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("About Me", callback_data="about"),
              InlineKeyboardButton("Close", callback_data="close")]]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
    else:
        # ELSE part for non-premium users
        text = (
            f"👑 Premium Access Required❗\n\n"
"🔓 Unlock full access to videos and premium content 🔥 with just one tap!\n\n"
"🔥 To unlock Exclusive Content :-\n\n"
"1️⃣ Choose a premium plan below.\n"
"2️⃣ Enjoy unlimited access instantly!\n\n"
"✨ Upgrade now and enjoy full access to all exclusive content!"

        )

        buttons = [
            [InlineKeyboardButton("Get Premium", url="https://t.me/angelicfraud")],
            [InlineKeyboardButton("Need Help", url="https://t.me/angelicfraud")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(text, reply_markup=reply_markup)


#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Bot, message: Message):

    user_id = message.from_user.id
    # Check subscription status
    sub1 = await is_subscribed1(None, client, message)
    sub2 = await is_subscribed2(None, client, message)
    sub3 = await is_subscribed3(None, client, message)

    buttons = []
    if sub1 and not sub2 and not sub3:
        # User subscribed to 1, show buttons for 2 and 3
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub2 and not sub1 and not sub3:
        # User subscribed to 2, show buttons for 1 and 3
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink1)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub3 and not sub1 and not sub2:
        # User subscribed to 3, show buttons for 1 and 2
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink1)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
    elif not sub1 and not sub2 and not sub3:
        # User subscribed to none, show all three buttons
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink1)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub1 and sub2 and not sub3:
        # User subscribed to 1 and 2, show button for 3
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub1 and sub3 and not sub2:
        # User subscribed to 1 and 3, show button for 2
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
    elif sub2 and sub3 and not sub1:
        # User subscribed to 2 and 3, show button for 1
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink1)])
    elif sub1 and sub2 and sub3:
        # All subscriptions satisfied, no join buttons
        pass
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass


    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private)
async def get_users(client: Bot, message: Message):
    user_id = message.from_user.id
    is_user_admin = await is_admin(user_id)
    if not is_user_admin and user_id != OWNER_ID:       
        return
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.command('broadcast') & filters.private)
async def send_text(client: Bot, message: Message):
    user_id = message.from_user.id
    is_user_admin = await is_admin(user_id)
    if not is_user_admin and user_id != OWNER_ID:        
        return
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcast ho rha till then FUCK OFF </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

@Bot.on_message(filters.private & filters.command("restart") & filters.user(OWNER_ID))
async def restart_bot(b, m):
    restarting_message = await m.reply_text(f"⚡️<b><i>Restarting....</i></b>", disable_notification=True)

    # Wait for 3 seconds
    await asyncio.sleep(3)

    # Update message after the delay
    await restarting_message.edit_text("✅ <b><i>Successfully Restarted</i></b>")

    # Restart the bot
    os.execl(sys.executable, sys.executable, *sys.argv)
