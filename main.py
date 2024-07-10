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


API_URL = "https://aztro.sameerkumar.website"

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
    await message.answer("Привет, я бот-гороскоп. Выберите Ваш знак зодиака:", reply_markup=keyboard)


def get_horoscope(zodiac_sign):
    try:
        params = {"sign": zodiac_sign, "day": "today"}
        response = requests.post(API_URL, params=params)

        if response.status_code != 200:
            logging.error(f'Error fetching horoscope: {response.status_code} {response.reason}')
            return "Извините, гороскоп временно недоступен."

        data = response.json()
        horoscope = data.get('description', 'Гороскоп не найден.')
        logging.info(f'Received horoscope: {horoscope}')
        return horoscope
    except Exception as e:
        logging.error(f'Error fetching horoscope: {e}')
        return "Извините, гороскоп временно недоступен."


@dp.message(lambda message: message.text in [button.text for button in buttons])
async def send_horoscope(message: types.Message):
    zodiac_sign = message.text.lower()
    logging.info(f'Requested horoscope for: {zodiac_sign}')
    horoscope = get_horoscope(zodiac_sign)
    await message.answer(horoscope)


async def main():
    await dp.start_polling(bot)

asyncio.run(main())

