import asyncio
import logging
import sys
from pars import *
from aiogram import Bot, Dispatcher, html, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import token_telegram

# Все обработчики должны быть прикреплены к Маршрутизатору (или Диспетчеру)
dp = Dispatcher()

#Этот обработчик получает сообщения с помощью команды `/start`.
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    #Создание кнопок
    kb = [
        [
            types.KeyboardButton(text="Лига Европы. Сегодня"),
            types.KeyboardButton(text="Лига Европы. Все матчи")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите вариант"
    )
    #вывод текста и кнопок после ввода /start
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Выбери вариант!", reply_markup=keyboard)

#Этот обработчик получает сообщения с помощью команды `/games`, вызывет обычное меню с 2 кнопками.
@dp.message(F.text, Command("games"))
async def any_message(message: Message):
    kb = [
        [
            types.KeyboardButton(text="Лига Европы. Сегодня"),
            types.KeyboardButton(text="Лига Европы. Все матчи")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите вариант"
    )
    await message.answer("Выберите вариант!", reply_markup=keyboard)

#Ловим нажатие кнопки(текст, который она отправляет)
@dp.message(F.text.lower() == "лига европы. сегодня")
async def europe_today(message: types.Message):
    #вывод сегодняшних матчей
    start = pars()
    matches = start.main()
    today = start.today_matches(matches)
    if len(today) == 0:
        await message.reply(f"Сегодня матчей нет!")
    else:
        await message.reply(f"{today}")

@dp.message(F.text.lower() == "лига европы. все матчи")
async def europe_all(message: types.Message):
    #вывод всех матчей
    start = pars()
    matches = start.main()
    for i in matches:
        # reply_markup=types.ReplyKeyboardRemove() - удаляет клавиатуру
        await message.reply(f"{i[0]}\n{i[1]}\n{i[3]}\n{i[4]}")




#эхо-ответчик
# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")
#




async def main() -> None:
    bot = Bot(token=token_telegram, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

