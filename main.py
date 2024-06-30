import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('help'))
async def process_help_command(message: types.Message):
    await message.reply('Рад помочь')


@dp.message(Command('info'))
async def process_info_command(message: types.Message):
    await message.reply('Это информация о боте')


@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    await message.reply('Привет! я бот-попугайчик, буду за тобой повторять.Тебе также доступны команды /help и /info')


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
