import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, CHANNEL_LINK, DEVELOPER_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ─────────── Keyboards ───────────

def start_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🚀 Start Generating", callback_data="start_gen"),
        types.InlineKeyboardButton("📘 How It Works", callback_data="how")
    )
    kb.add(
        types.InlineKeyboardButton("📢 Updates", url=CHANNEL_LINK),
        types.InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_ID[1:]}")
    )
    return kb


def generate_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📝 Text → File", callback_data="text_file"),
        types.InlineKeyboardButton("🌍 Translate Text", callback_data="translate")
    )
    kb.add(
        types.InlineKeyboardButton("📚 Languages", callback_data="langs"),
        types.InlineKeyboardButton("⬅️ Back", callback_data="back")
    )
    return kb


WELCOME_TEXT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💀 <b>TEXT TO FILES GENERATOR BOT</b> 💀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👑 Welcome <b>{name}</b>

This is not a normal generator.
This is your <b>code weapon</b> ⚔️

➤ Paste text  
➤ Choose language  
➤ Get ready-to-use files  

❝ From idea to file — instantly ❞ ⚡

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# ─────────── Handlers ───────────

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    name = message.from_user.first_name
    await message.answer(
        WELCOME_TEXT.format(name=name),
        reply_markup=start_keyboard()
    )


@dp.callback_query_handler(lambda c: c.data == "start_gen")
async def start_generate(call: types.CallbackQuery):
    await call.message.edit_text(
        "🚀 <b>Select an option below</b>\n\n⚠️ This bot creates real files.",
        reply_markup=generate_keyboard()
    )


@dp.callback_query_handler(lambda c: c.data == "how")
async def how_it_works(call: types.CallbackQuery):
    await call.message.reply(
        "📘 <b>How This Bot Works</b>\n\n"
        "➤ Send your text\n"
        "➤ Select language\n"
        "➤ Get instant file\n\n"
        "No login • No limits • Free"
    )


@dp.callback_query_handler(lambda c: c.data == "langs")
async def language_list(call: types.CallbackQuery):
    await call.message.reply(
        "📚 <b>Supported Formats</b>\n\n"
        "➤ Python (.py)\n"
        "➤ HTML (.html)\n"
        "➤ JavaScript (.js)\n"
        "➤ CSS (.css)\n"
        "➤ JSON (.json)\n"
        "➤ Markdown (.md)\n"
        "➤ Text (.txt)"
    )


@dp.callback_query_handler(lambda c: c.data == "back")
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        "⬅️ Back to main menu",
        reply_markup=start_keyboard()
    )


@dp.message_handler()
async def receive_text(message: types.Message):
    await message.reply(
        "🛠 <b>Text received</b>\n\n"
        "File generation engine will be added next.\n\n"
        f"👨‍💻 Developer: <b>{DEVELOPER_ID}</b>"
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
