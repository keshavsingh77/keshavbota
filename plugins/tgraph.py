nano /keshavbotA/plugins/tgraph.py
file_id, ref = unpack_new_file_id(post.document.file_id)

# Generate Markdown content
md_txt = f"**Batch Link Summary**\n\nTotal Files: `{og_msg}`\n"
for file in outlist[:20]:  # Limit preview to 20 files
    name = file.get("title", "No Name")
    size = file.get("size", 0)
    size_mb = round(size / (1024 * 1024), 2)
    md_txt += f"\n📁 **{name}** - `{size_mb} MB`"

# Convert to HTML for Telegraph
html = await markdown_to_html(md_txt)

# Create Telegraph link
try:
    t_url = await telegraph_handler(
        f"Batch by {message.from_user.first_name}",
        html,
        author=message.from_user.first_name
    )
    await sts.edit(
        f"Here is your link:\n📎 [Telegram Start Link](https://t.me/{temp.U_NAME}?start=BATCH-{file_id})\n"
        f"📝 [Telegraph Summary]({t_url})\n\nContains `{og_msg}` files."
    )
except Exception as e:
    await sts.edit(
        f"Batch link:\nhttps://t.me/{temp.U_NAME}?start=BATCH-{file_id}\n\nTelegraph failed: `{e}`"
    )
