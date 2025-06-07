# (c) @RoyalKrrishna

import logging
import traceback
from os import getenv
from telethon import TelegramClient, Button, events
from telethon.sessions import StringSession
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from configs import Config
import asyncio
from plugins.tgraph import *
from helpers import *
import urllib.parse

# Bot and user clients
tbot = TelegramClient('mdisktelethonbot', Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)
client = TelegramClient(StringSession(Config.USER_SESSION_STRING), Config.API_ID, Config.API_HASH)

# Optional keep-alive for Render/Koyeb
if Config.REPLIT:
    from threading import Thread
    from flask import Flask, jsonify

    app = Flask('')

    @app.route('/')
    def main():
        return jsonify({"status": "running", "hosted": "Render/Koyeb", "repl": Config.REPLIT})

    def run():
        app.run(host="0.0.0.0", port=8000)

    def keep_alive():
        Thread(target=run).start()


async def get_user_join(user_id):
    if Config.FORCE_SUB == "False":
        return True
    try:
        await tbot(GetParticipantRequest(channel=int(Config.UPDATES_CHANNEL), participant=user_id))
        return True
    except UserNotParticipantError:
        return False


@tbot.on(events.NewMessage(incoming=True))
async def message_handler(event):
    if event.message.post or event.text.startswith("/"):
        return

    if not await get_user_join(event.sender_id):
        join_msg = await event.reply(
            f"**Hey! {event.sender.first_name} 😃**\n\n**You must join our update channel to use me ✅**",
            buttons=Button.url('🍿 Join Updates Channel', f'https://t.me/{Config.UPDATES_CHANNEL_USERNAME}')
        )
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        return await join_msg.delete()

    args = await validate_q(event.text)
    if not args:
        return

    txt = await event.reply(f'**Searching For "{event.text}" 🔍**')

    try:
        search = []
        async for word in AsyncIter(args.split()):
            search.append(client.iter_messages(Config.CHANNEL_ID, limit=5, search=word))

        answer = f'**Join** [@{Config.UPDATES_CHANNEL_USERNAME}](https://telegram.me/{Config.UPDATES_CHANNEL_USERNAME}) \n\n'
        c = 0

        async for msg_list in AsyncIter(search):
            async for msg in msg_list:
                c += 1
                f_text = msg.text.replace("*", "")
                f_text = await link_to_hyperlink(f_text)

                file_info = ""
                buttons = None

                if getattr(msg, "file", None):
                    file_name = getattr(msg.file, "name", "Unknown")
                    file_size = getattr(msg.file, "size", 0)

                    size_str = (
                        f"{file_size / (1024 * 1024):.2f} MB" if file_size > 1024 * 1024
                        else f"{file_size / 1024:.2f} KB" if file_size > 1024
                        else f"{file_size} B"
                    )
                    file_link = f"https://t.me/{Config.UPDATES_CHANNEL_USERNAME}/{msg.id}"

                    file_info = (
                        f"\n\n📂 **File Name:** `{file_name}`"
                        f"\n📦 **Size:** `{size_str}`"
                        f"\n🔗 [Click to Download]({file_link})"
                    )
                    buttons = [[Button.url("⬇️ Download", file_link)]]

                result_text = (
                    f'\n\n**✅ PAGE {c}:**\n\n━━━━━━━━━\n\n'
                    + f_text.split("\n", 1)[0]
                    + '\n\n'
                    + f_text.split("\n", 2)[-1]
                    + file_info
                )
                await event.reply(result_text, buttons=buttons)

        if c == 0:
            await txt.delete()
            google_query = event.text.replace(" ", "%20")
            not_found_msg = f"""**No Results Found For {event.text}**

🔍 Try searching on [Google](http://www.google.com/search?q={google_query}%20Movie)

Please type only movie name correctly.
"""
            buttons = [
                [Button.url('✅ Check Spelling', f'http://www.google.com/search?q={google_query}%20Movie')],
                [Button.url('📅 Check Release Date', f'http://www.google.com/search?q={google_query}%20Movie%20Release%20Date')],
                [Button.url('🎬 Search on Amazon', 'https://amzn.to/3ykSzxC')],
            ]
            result = await event.reply(not_found_msg, buttons=buttons, link_preview=False)
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            await event.delete()
            return await result.delete()

        await txt.delete()

    except Exception as e:
        logging.error(str(e))
        await txt.delete()
        result = await event.reply("**❌ Error while searching. Please report to @RoyalKrrishn**")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await event.delete()
        return await result.delete()


# Entry point
class Bot(Client):
    def __init__(self):
        super().__init__(
            Config.BOT_SESSION_NAME,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    def start(self):
        if Config.REPLIT:
            keep_alive()
        super().start()
        print('✅ Bot Started')

    def stop(self, *args):
        super().stop()
        print('🛑 Bot Stopped')


print("\n-------------------- Initializing Telegram Bot --------------------\n")
tg_app = Bot()
tg_app.start()

print(f"""
📦 Deployed Successfully!
👉 Join @{Config.UPDATES_CHANNEL_USERNAME}
""")

with tbot, client:
    tbot.run_until_disconnected()
    client.run_until_disconnected()
