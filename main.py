import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
dp = Dispatcher()


ASTRO_API_URL = 'https://aztro.sameerkumar.website'


buttons = [
    KeyboardButton(text="aries"),
    KeyboardButton(text="taurus"),
    KeyboardButton(text="gemini"),
    KeyboardButton(text="cancer"),
    KeyboardButton(text="leo"),
    KeyboardButton(text="virgo"),
    KeyboardButton(text="libra"),
    KeyboardButton(text="scorpio"),
    KeyboardButton(text="sagittarius"),
    KeyboardButton(text="capricorn"),
    KeyboardButton(text="aquarius"),
    KeyboardButton(text="pisces")
]

# Создание клавиатуры с тремя рядами кнопок
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons[0], buttons[1], buttons[2], buttons[3]],
        [buttons[4], buttons[5], buttons[6], buttons[7]],
        [buttons[8], buttons[9], buttons[10], buttons[11]],
    ],
    resize_keyboard=True
)

@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    await message.answer("Выберите ваш знак зодиака:", reply_markup=keyboard)

def get_horoscope(zodiac_sign):
    # Пример запроса к API для получения гороскопа (замените данный URL на реальный)
    url = f'https://example.com/api/horoscope?sign={zodiac_sign}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('horoscope', "Гороскоп не найден.")
    else:
        return "Извините, гороскоп временно недоступен."

@dp.message(lambda message: message.text in [button.text for button in buttons])
async def send_horoscope(message: types.Message):
    zodiac_sign = message.text
    horoscope = get_horoscope(zodiac_sign)
    await message.answer(horoscope)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
