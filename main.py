# (c) @RoyalKrrishna

from os import link
from telethon import Button
from configs import Config
from pyrogram import Client, idle
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from plugins.tgraph import *
from helpers import *
from telethon import TelegramClient, events
import urllib.parse
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

@tbot.on(events.NewMessage(incoming=True))
async def message_handler(event):

    if event.message.post:
        return

    print("\\n")
    print("Message Received: " + event.text)
    # if event.is_channel:return
    if event.text.startswith("/"):return

    # Force Subscription
    if  not await get_user_join(event.sender_id):
        haha = await event.reply(f'''**Hey! {event.sender.first_name} 😃**

**You Have To Join Our Update Channel To Use Me ✅**

**Click Bellow Button To Join Now.👇🏻**''', buttons=Button.url('🍿Updates Channel🍿', f'https://t.me/{Config.UPDATES_CHANNEL_USERNAME}'))
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        return await haha.delete()


    print("Group: " + str(event.is_group))
    print("Channel: " + str(event.is_channel))
    args = event.text
    args = await validate_q(args)

    print("Search Query: {args}".format(args=args))
    print("\\n")

    if not args:
        return

    txt = await event.reply('**Searching For \"{}\" 🔍**'.format(event.text))

    try:
        search = []
        async for i in AsyncIter(args.split()):
            search_msg = client.iter_messages(Config.CHANNEL_ID, limit=5, search=i)
            search.append(search_msg)

        username = Config.UPDATES_CHANNEL_USERNAME
        answer = f'**Join** [@{username}](https://telegram.me/{username}) \\n\\n'

        c = 0
        buttons = [] # Initialize an empty list for buttons

        async for msg_list in AsyncIter(search):
            async for msg in msg_list:
                c += 1
                # Check if the message has media (a file)
                if msg.media:
                    file_name = ""
                    if hasattr(msg.media, 'document') and msg.media.document:
                        file_name = msg.media.document.attributes[0].file_name if msg.media.document.attributes else 'File'
                    elif hasattr(msg.media, 'video') and msg.media.video:
                         file_name = msg.media.video.attributes[0].file_name if msg.media.video.attributes else 'Video'
                    elif hasattr(msg.media, 'audio') and msg.media.audio:
                         file_name = msg.media.audio.attributes[0].file_name if msg.media.audio.attributes else 'Audio'
                    # Add more media types if needed

                    if file_name:
                        # Generate download link (assuming Telegram file ID can be used)
                        # You might need to adjust the URL format based on your bot's setup
                        download_link = f"https://t.me/{tbot.me.username}?start=file_{msg.id}" # This is an example, you might need to change this

                        # Create an inline keyboard button
                        button = InlineKeyboardButton(text=file_name, url=download_link)
                        buttons.append([button]) # Add the button to the list of buttons

                        # Add file name to the answer text
                        answer += f'\\n\\n**✅ PAGE {c}:**\\n\\n━━━━━━━━━\\n\\n**File:** {file_name}\\n\\n'

                else:
                    # Existing logic for non-file messages
                    f_text = msg.text.replace(\"*\", \"\")
                    f_text = await link_to_hyperlink(f_text)
                    answer += f'\\n\\n**✅ PAGE {c}:**\\n\\n━━━━━━━━━\\n\\n\' + \'\' + f_text.split(\"\\n\", 1)[0] + \'\' + \'\\n\\n\' + \'\' + f_text.split(\"\\n\", 2)[\
                        -1]


        finalsearch = []
        async for msg in AsyncIter(search):\
            finalsearch.append(msg)

        if c <= 0:
            answer = f'''**No Results Found For {event.text}**

**Type Only Movie Name 💬**
**Check Spelling On** [Google](http://www.google.com/search?q={event.text.replace(' ', '%20')}%20Movie) 🔍
'''

            newbutton = [Button.url('Click To Check Spelling ✅',
                                    f'http://www.google.com/search?q={event.text.replace(" ", "%20")}%20Movie')], [
                            Button.url('Click To Check Release Date 📅',
                                    f'http://www.google.com/search?q={event.text.replace(" ", "%20")}%20Movie%20Release%20Date')], [
                            Button.url('👉 Search Here 👈',
                                    f'https://amzn.to/3ykSzxC')]
            await txt.delete()
            result = await event.reply(answer, buttons=newbutton, link_preview=False)
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            await event.delete()
            return await result.delete()
        else:
            pass

        answer += f"\\n\\n**Uploaded By @{Config.UPDATES_CHANNEL_USERNAME}**"
        answer = await replace_username(answer)

        # If there are buttons (meaning files were found), send the message with buttons
        if buttons:
             message = answer
             button = buttons # Use the collected buttons
        else:
            # If no files were found, use the existing logic for Telegraph link
            html_content = await markdown_to_html(answer)
            html_content = await make_bold(html_content)
            tgraph_result = await telegraph_handler(
                html=html_content,
                title=event.text,
                author=Config.BOT_USERNAME
            )
            message = f'**Click Here 👇 For \"{event.text}\"**\\n\\n[🍿🎬 {str(event.text).upper()}\\n🍿🎬 {str(\"Click me for results\").upper()}]({tgraph_result})'
            button =  [Button.url('❓How To Open Link❓',
                                        f'https://t.me/iP_Update/8')], [\
                                Button.url('👉 Search Here 👈',
                                        f'https://amzn.to/3MmfpIu')]


        await txt.delete()
        result = await event.reply(message, buttons=button, link_preview=False)
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await event.delete()
        return await result.delete()


    except Exception as e:
        print(e)
        await txt.delete()
        result = await event.reply("**Some Error While Searching...‼️\\n\\nReport @RoyalKrrishn 🥷**")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await event.delete()
        return await result.delete()

