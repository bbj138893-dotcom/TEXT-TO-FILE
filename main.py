import os
import zipfile
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from googletrans import Translator

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway ENV me dalna
CHANNEL_LINK = "https://t.me/PROFESSORXZAMINHACKER"
DEVELOPER_ID = "@SIGMAXZAMIN"
BOT_USERNAME = "@FileExecutionBot"
BOT_NAME = "TEXT TO FILES GENERATOR BOT"

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
    kb.add("🔁 Create Next File")
    kb.add("📢 Channel", "👨‍💻 Developer")
    return kb

# ================= START =================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        f"""
━━━━━━━━━━━━━━━━━━━━━━━
💀 <b>{BOT_NAME}</b> 💀
━━━━━━━━━━━━━━━━━━━━━━━

👑 Welcome <b>{message.from_user.first_name}</b>

➤ Send text  
➤ Name file  
➤ Choose format  

⚡ From idea to file — instantly
━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=main_kb()
    )

# ================= TEXT → FILE =================
@dp.message_handler(lambda m: m.text == "📝 Text → File")
async def text_to_file(message: types.Message):
    await message.answer(
        "📝 <b>Send your text</b>\n\n❝ Your content starts here ❞",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await FileState.waiting_text.set()

@dp.message_handler(state=FileState.waiting_text)
async def get_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        "📛 <b>Send file name</b>\n➤ Without extension\n➤ Example: index",
    )
    await FileState.waiting_name.set()

@dp.message_handler(state=FileState.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "🧩 <b>Choose output format</b>",
        reply_markup=format_kb()
    )
    await FileState.waiting_format.set()

@dp.message_handler(state=FileState.waiting_format)
async def make_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data["text"]
    name = data["name"]

    fmt_map = {
        "📄 TXT": ".txt",
        "🐍 PY": ".py",
        "🌐 HTML": ".html",
    }

    if message.text == "📦 ZIP":
        zip_name = f"{name}.zip"
        file_name = f"{name}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)

        with zipfile.ZipFile(zip_name, "w") as zipf:
            zipf.write(file_name)

        await message.answer_document(open(zip_name, "rb"))
        os.remove(file_name)
        os.remove(zip_name)

    elif message.text in fmt_map:
        ext = fmt_map[message.text]
        file_name = name + ext
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)

        await message.answer_document(open(file_name, "rb"))
        os.remove(file_name)
    else:
        await message.answer("❌ Select from buttons only")
        return

    await message.answer(
        f"""
🎉 <b>FILE CREATED SUCCESSFULLY</b>

🔁 Want to create another file?

👨‍💻 Developer: {DEVELOPER_ID}
🤖 Bot: {BOT_USERNAME}
""",
        reply_markup=next_kb()
    )
    await state.finish()

@dp.message_handler(lambda m: m.text == "🔁 Create Next File")
async def again(message: types.Message):
    await text_to_file(message)

# ================= TRANSLATE (FIXED) =================
@dp.message_handler(lambda m: m.text == "🌍 Translate Text")
async def tr_start(message: types.Message):
    await message.answer("🌍 Send text to translate", reply_markup=types.ReplyKeyboardRemove())
    await TranslateState.waiting_text.set()

@dp.message_handler(state=TranslateState.waiting_text)
async def tr_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🇬🇧 English", "🇵🇰 Urdu")
    kb.add("🇮🇳 Hindi", "🇷🇺 Russian")
    await message.answer("🌐 Choose target language", reply_markup=kb)
    await TranslateState.waiting_lang.set()

@dp.message_handler(state=TranslateState.waiting_lang)
async def tr_done(message: types.Message, state: FSMContext):
    lang_map = {
        "🇬🇧 English": "en",
        "🇵🇰 Urdu": "ur",
        "🇮🇳 Hindi": "hi",
        "🇷🇺 Russian": "ru"
    }
    if message.text not in lang_map:
        await message.answer("❌ Choose from buttons")
        return

    data = await state.get_data()
    result = translator.translate(data["text"], dest=lang_map[message.text])

    await message.answer(
        f"✅ <b>Translation Complete</b>\n\n📝 {result.text}",
        reply_markup=main_kb()
    )
    await state.finish()

# ================= INFO =================
@dp.message_handler(lambda m: m.text == "📢 Channel")
async def channel(message: types.Message):
    await message.answer(
        f"📢 <b>OFFICIAL CHANNEL</b>\n\n👉 Join now:\n{CHANNEL_LINK}"
    )

@dp.message_handler(lambda m: m.text == "👨‍💻 Developer")
async def dev(message: types.Message):
    await message.answer(f"👨‍💻 Developer: {DEVELOPER_ID}")

# ================= RUN =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
