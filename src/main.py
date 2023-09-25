import asyncio

import sqlalchemy
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import yfinance as yf
from .config import TOKEN
import aiohttp

from .db import add_ticker, get_tickers, add_person, remove_ticker, initialize_db

dp = Dispatcher()


async def get_ticker(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}
    async with aiohttp.ClientSession() as session:
        async with session.get(yfinance, params=params, headers=headers) as res:
            data = await res.json()

            company_code = data['quotes'][0]['symbol']
            return company_code


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    add_person(message.from_user.id)
    await message.answer("Hello, I'm a bot that can show you the current price of a stock.")


@dp.message(Command('get'))
async def get_handler(message: Message) -> None:
    stock = message.text.split(' ')[1].upper()
    ticker = await get_ticker(stock)
    stock = yf.Ticker(ticker)
    await message.answer(
        f'The current price of {stock.info["shortName"]} ({ticker}) is {hbold(stock.info["currentPrice"])} {stock.info["currency"]}')


@dp.message(Command('save'))
async def add_ticker_handler(message: Message) -> None:
    ticker = message.text.split(' ')[1].upper()
    ticker = await get_ticker(ticker)
    add_ticker(message.from_user.id, ticker)
    await message.answer(f'{hbold(ticker)} was added to your list of tickers')


@dp.message(Command('favorites'))
async def get_tickers_handler(message: Message) -> None:
    tickers = get_tickers(message.from_user.id)
    for i in tickers:
        stock = yf.Ticker(i)
        await message.answer(
            f'The current price of {stock.info["shortName"]} ({i}) is {hbold(stock.info["currentPrice"])} {stock.info["currency"]}')


@dp.message(Command('remove'))
async def remove_ticker_handler(message: Message) -> None:
    ticker = message.text.split(' ')[1].upper()
    remove_ticker(message.from_user.id, ticker)
    await message.answer(f'{hbold(ticker)} was removed from your list of tickers')


async def main() -> None:
    initialize_db()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
