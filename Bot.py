import os
import yt_dlp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "BOT"8439251072:AAHWbHzMwqL-TjV3_yz-hSsp37Teh1KWuy0"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("🎵 Qo‘shiq nomini yozing.\nMen 3 ta variant chiqaraman.")

@dp.message_handler()
async def search(msg: types.Message):
    query = msg.text

    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch3:{query}", download=False)

    kb = InlineKeyboardMarkup()
    for i, entry in enumerate(info['entries']):
        title = entry['title'][:40]
        kb.add(
            InlineKeyboardButton(
                text=f"{i+1}️⃣ {title}",
                callback_data=f"dl|{entry['id']}"
            )
        )

    await msg.answer("👇 Variantni tanlang:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("dl"))
async def download(call: types.CallbackQuery):
    video_id = call.data.split("|")[1]

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=True)
        filename = ydl.prepare_filename(info)

    await call.message.answer_audio(
        open(filename, 'rb'),
        title=info['title'],
        performer=info.get('uploader', 'Unknown')
    )

    os.remove(filename)
    await call.answer("🎶 Yuklab bo‘ldi!")

executor.start_polling(dp)
