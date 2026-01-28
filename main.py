import os
import zipfile
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from googletrans import Translator

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_LINK = "https://t.me/PROFESSORXZAMINHACKER"
DEVELOPER_ID = "@SIGMAXZAMIN"
BOT_USERNAME = "@FileExecutionBot"
BOT_NAME = "TEXT TO FILES GENERATOR BOT"

# =========================================

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
translator = Translator()

# ================= STATES =================
class FileState(StatesGroup):
    waiting_text = State()
    waiting_name = State()
    waiting_format = State()

class TranslateState(StatesGroup):
    waiting_text = State()
    waiting_lang = State()

# ================= KEYBOARDS =================
def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📝 Text → File", "🌍 Translate Text")
    kb.add("📢 Channel", "👨‍💻 Developer")
    return kb

def format_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📄 TXT", "🐍 PY")
    kb.add("🌐 HTML", "📦 ZIP")
    return kb

def next_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📝 Text → File")
    kb.add("🌍 Translate Text")
    kb.add("📢 Channel", "👨‍💻 Developer")
    return kb

def lang_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("English", "Urdu")
    kb.add("Hindi", "Arabic")
    kb.add("Cancel")
    return kb

LANG_MAP = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar"
}

# ================= START =================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💀 <b>{BOT_NAME}</b> 💀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👑 Welcome <b>{message.from_user.first_name}</b>

This is not a normal generator.
This is your <b>code weapon</b> ⚔️

➤ Paste text  
➤ Name the file  
➤ Choose format  
➤ Get instant file  

❝ One idea. Unlimited files. ❞ ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=main_kb()
    )

# ================= TEXT → FILE =================
@dp.message_handler(lambda m: m.text == "📝 Text → File")
async def text_to_file(message: types.Message):
    await message.answer(
        "📥 <b>Send your text</b>\n\nThis content will be converted into a file.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await FileState.waiting_text.set()

@dp.message_handler(state=FileState.waiting_text)
async def get_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        "🧾 <b>Send file name</b>\n\n➤ Without extension\n➤ Example: index"
    )
    await FileState.waiting_name.set()

@dp.message_handler(state=FileState.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text.strip()

    if not name.replace("_", "").isalnum():
        await message.answer("❌ Invalid name\nUse only letters & numbers")
        return

    await state.update_data(name=name)
    await message.answer(
        "🧩 <b>Choose output format</b>",
        reply_markup=format_kb()
    )
    await FileState.waiting_format.set()

@dp.message_handler(state=FileState.waiting_format)
async def make_file(message: types.Message, state: FSMContext):
    formats = {
        "📄 TXT": ".txt",
        "🐍 PY": ".py",
        "🌐 HTML": ".html",
        "📦 ZIP": "zip"
    }

    if message.text not in formats:
        await message.answer("❌ Select format from buttons only")
        return

    data = await state.get_data()
    text = data["text"]
    name = data["name"]

    if message.text == "📦 ZIP":
        inner = f"{name}.txt"
        zipname = f"{name}.zip"

        with open(inner, "w", encoding="utf-8") as f:
            f.write(text)

        with zipfile.ZipFile(zipname, "w") as z:
            z.write(inner)

        await message.answer_document(open(zipname, "rb"))
        os.remove(inner)
        os.remove(zipname)

    else:
        file = name + formats[message.text]
        with open(file, "w", encoding="utf-8") as f:
            f.write(text)

        await message.answer_document(open(file, "rb"))
        os.remove(file)

    await message.answer(
        f"""
━━━━━━━━━━━━━━━━━━━━━━━
🎉 FILE CREATED SUCCESSFULLY

Your file is ready & delivered 📁  
Clean • Accurate • Ready to use  

🔁 Want to create another file?

👨‍💻 Developer: {DEVELOPER_ID}
🤖 Bot: {BOT_USERNAME}
━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=next_kb()
    )

    await state.finish()

# ================= TRANSLATE =================
@dp.message_handler(lambda m: m.text == "🌍 Translate Text")
async def translate_start(message: types.Message):
    await message.answer("✍️ Send text to translate")
    await TranslateState.waiting_text.set()

@dp.message_handler(state=TranslateState.waiting_text)
async def translate_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("🌐 Choose language", reply_markup=lang_kb())
    await TranslateState.waiting_lang.set()

@dp.message_handler(state=TranslateState.waiting_lang)
async def translate_lang(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.finish()
        await message.answer("❌ Cancelled", reply_markup=main_kb())
        return

    if message.text not in LANG_MAP:
        await message.answer("❌ Choose from buttons")
        return

    data = await state.get_data()
    result = translator.translate(data["text"], dest=LANG_MAP[message.text])

    await message.answer(
        f"✅ <b>Translation Complete</b>\n\n📘 {result.text}",
        reply_markup=main_kb()
    )
    await state.finish()

# ================= INFO =================
@dp.message_handler(lambda m: m.text == "📢 Channel")
async def channel(message: types.Message):
    await message.answer(
        f"""
📢 <b>OFFICIAL CHANNEL</b>

Updates • Features • Power tools  
Everything first — only here ⚡

👉 <a href="{CHANNEL_LINK}">Join now</a>
"""
    )

@dp.message_handler(lambda m: m.text == "👨‍💻 Developer")
async def developer(message: types.Message):
    await message.answer(f"👨‍💻 Developer: {DEVELOPER_ID}")

# ================= RUN =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
