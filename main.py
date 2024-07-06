import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


ASTRO_API_URL = 'https://aztro.sameerkumar.website'


zodiac_signs = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

builder = ReplyKeyboardBuilder()
for sign in zodiac_signs:
    builder.add(types.KeyboardButton(text=sign.capitalize()))
zodiac_keyboard = builder.as_markup(resize_keyboard=True)


def fetch_horoscope(sign: str) -> str:
    logging.info(f"Fetching horoscope for: {sign}")
    response = requests.post(ASTRO_API_URL, params={'sign': sign, 'day': 'today'})
    logging.info(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        json_response = response.json()
        logging.info(f"Response JSON: {json_response}")
        return json_response.get("description", "Предсказание не найдено.")
    else:
        logging.error(f"Failed to fetch horoscope: {response.text}")
        return "Не удалось получить предсказание."


@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    await message.reply("Привет! Выберите ваш знак зодиака:", reply_markup=zodiac_keyboard)


@dp.message(Command('help'))
async def process_help_command(message: types.Message):
    await message.reply('Рад помочь')


@dp.message(Command('info'))
async def process_info_command(message: types.Message):
    await message.reply('Это информация о боте')


@dp.message(lambda message: message.text.lower() in zodiac_signs)
async def send_horoscope(message: types.Message):
    zodiac_sign = message.text.lower()
    horoscope = fetch_horoscope(zodiac_sign)
    await message.answer(f"Ваш гороскоп на сегодня для {zodiac_sign.capitalize()}:\n\n{horoscope}")


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
