from telegraph.aio import Telegraph
from telegraph.utils import markdown_to_html
import asyncio

telegraph = Telegraph()
TOKEN = None

async def init_telegraph():
    global TOKEN
    await telegraph.create_account(short_name='KeshavBot')
    TOKEN = telegraph.access_token

async def create_tgraph_post(md_txt, title="KeshavBot Post"):
    html_content = await markdown_to_html(md_txt)
    response = await telegraph.create_page(
        title=title,
        html_content=html_content,
        author_name="KeshavBot"
    )
    return f"https://telegra.ph/{response['path']}"

# Example usage
if __name__ == "__main__":
    async def main():
        md_txt = "**Welcome to KeshavBot!**\n\nThis is a sample markdown."
        await init_telegraph()
        link = await create_tgraph_post(md_txt)
        print("Telegraph Link:", link)

    asyncio.run(main())
from plugins.tgraph import create_tgraph_post

@Client.on_message(filters.command("tgraph"))
async def handle_tgraph(client, message):
    md_txt = "**Batch Link Summary**\n\nTotal Files: `10`"
    link = await create_tgraph_post(md_txt, title="Batch Summary")
    await message.reply_text(f"✅ [View Post]({link})", disable_web_page_preview=True)
