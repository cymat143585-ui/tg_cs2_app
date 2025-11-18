from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

BOT_TOKEN = "8194199013:AAH9O-axpQHceYD3VGRsEukwoSYtGLPDqf8"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Открыть приложение", web_app=WebAppInfo(url="tg-cs2-app.vercel.app"))
    await message.answer(
        "Запускай мини-приложение!",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())