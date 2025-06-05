import re
import logging
from telegraph.aio import Telegraph
import markdown
from pyrogram import Client, filters

# Set up logging
logger = logging.getLogger(__name__)

# Telegraph and Markdown functions
async def telegraph_handler(title, html, author):
    telegraph = Telegraph()
    if len(title) >= 20:
        title = title[:20]
    await telegraph.create_account(short_name=title, author_name=author)
    response = await telegraph.create_page(
        title=title,
        html_content=html,
        author_name=author
    )
    return response['url']

async def markdown_to_html(markdown_txt):
    md = markdown.Markdown()
    html = md.convert(markdown_txt)
    return html

# Pyrogram message handler
@Client.on_message(
    (filters.forwarded | (filters.regex(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$"))
    & filters.text) & filters.private & filters.incoming
)
async def send_for_index(bot, message):
    try:
        if message.text:
            regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
            match = regex.match(message.text)
            if not match:
                logger.warning("Invalid link provided")
                return await message.reply('Invalid link')

            # Extract chat and message ID from the link
            chat = match.group(4)  # Chat ID or username
            lst_msg_id = match.group(5)  # Message ID

            # Log the indexing attempt
            print(f"Starting index_files_to_db for chat {chat}, last_msg_id={lst_msg_id}")

            # Call the indexing function (assumed to exist)
            await index_files_to_db(int(lst_msg_id), chat, message, bot)

            # Example: Convert message text to Markdown and publish to Telegraph
            if message.text:
                html_content = await markdown_to_html(message.text)
                telegraph_url = await telegraph_handler(
                    title=f"Message from {chat}",
                    html=html_content,
                    author="Telegram Bot"
                )
                await message.reply(f"Published to Telegraph: {telegraph_url}")

    except Exception as e:
        print(f"Error in index_files callback: {e}")
        await message.reply("An error occurred during processing.", show_alert=True)
