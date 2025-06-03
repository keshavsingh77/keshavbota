from TeamTeleRoid.database import db
from configs import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Client.on_callback_query()
async def button(bot, cmd: CallbackQuery):
        cb_data = cmd.data
        if "About_msg" in cb_data:
            await cmd.message.edit(
            text=Config.ABOUT_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Our Channel", url="https://t.me/FYM_Update"),
                        InlineKeyboardButton("Our Group", url="https://t.me/iPopcornMovieGroup")
                    ],
                    [
                        InlineKeyboardButton("Developer", url="https://t.me/RoyalKrrishna"),
                        InlineKeyboardButton("Home", callback_data="gohome")
                    ]
                ]
            ),
            parse_mode="html"
        )
        elif "Help_msg" in cb_data:
            await cmd.message.edit(
            text=Config.ABOUT_HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("About", callback_data="About_msg"),
                        InlineKeyboardButton("Our Channel", url="https://t.me/FYM_Update")
                    ], 
                                        [
                        InlineKeyboardButton("Owner", url="https://t.me/RoyalKrrishna"),
                        InlineKeyboardButton("Home", callback_data="gohome")
                    ]
                ]
            ),
            parse_mode="html"
        )
        elif "gohome" in cb_data:
            await cmd.message.edit(
            text=Config.HOME_TEXT.format(cmd.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                                        [
                        InlineKeyboardButton("Help", callback_data="Help_msg"),
                        InlineKeyboardButton("About", callback_data="About_msg")
                    ],
                    [
                        InlineKeyboardButton("Support", url="https://t.me/RoyalKrrishna"),
                        InlineKeyboardButton("Channel", url="https://t.me/FYM_Update")
                    ]
                ]
            ),
            parse_mode="html"
        )

        elif "remove_api" in cb_data:
            _, group_id = cb_data.split("#")
            await db.remove_user_api(int(group_id))
            await cmd.message.edit("Deleted Successfully")
            return
        elif "cancel_removeapi" in cb_data:
            await cmd.message.delete()

