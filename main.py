import sys
import time
import random

import asyncio
import logging

from os import getenv

from redis.asyncio import Redis

from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties

TOKEN = getenv("BOT_TOKEN")
REDIS_HOST = getenv("REDIS_HOST")

dp = Dispatcher()
db = Redis(host=REDIS_HOST, port=6379, db=0)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("dick"))
async def dick(message: Message):
    if not db.hexists(message.from_user.id, "time"):
        db.hset(message.from_user.id, "time", 0)
        db.hset(message.from_user.id, "size", 0)

    db.hset(message.from_user.id, "name", message.from_user.full_name)

    size = int(db.hget(message.from_user.id, "size").decode("utf-8"))
    current_time = db.hget(message.from_user.id, "time").decode("utf-8");

    if time.time() - float(current_time) > 3600 * 24:
        new_size = random.randint(0, 10)
        size += new_size
        db.hset(message.from_user.id, "size", y)
        db.hset(message.from_user.id, "time", time.time())
        await message.answer(f"{message.from_user.full_name}, твой писюн вырос на {new_size} см.\nТеперь он равен {size} см.\nСледующая попытка завтра!")
    else:
        await message.answer(f"{message.from_user.full_name}, ты уже играл.\nСейчас он равен {size} см.\nСледующая попытка завтра!")

@dp.message(Command("top"))
async def top(message: Message):
    x = ""
    i = 1
    for key in db.scan_iter():
        x += f"{db.hget(key, "name").decode("utf-8")} - {db.hget(key, "size").decode("utf-8")} см.\n"
        i += 1
    await message.answer(x)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
