from telegraph.aio import Telegraph
import markdown
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Your existing Telegraph and markdown functions
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

# Telegram bot handler for /publish command
async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user provided text after /publish
    if not context.args:
        await update.message.reply_text("Please provide markdown text after /publish. Example: /publish # Title\nText")
        return

    # Combine arguments into markdown text
    markdown_text = " ".join(context.args)
    
    # Extract title from the first line if it starts with '#'
    lines = markdown_text.split("\n")
    title = "Untitled"
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()  # Remove '# ' from title
        markdown_text = "\n".join(lines[1:]).strip()  # Remove title from content

    # Convert markdown to HTML
    html_content = await markdown_to_html(markdown_text)
    
    # Create Telegraph page
    author = update.effective_user.full_name or "Anonymous"
    try:
        telegraph_url = await telegraph_handler(title, html_content, author)
        await update.message.reply_text(f"Published to Telegraph: {telegraph_url}")
    except Exception as e:
        await update.message.reply_text(f"Error publishing to Telegraph: {str(e)}")

# Main function to start the bot
async def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    # Add handler for /publish command
    application.add_handler(CommandHandler("publish", publish))
    
    # Start the bot
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
