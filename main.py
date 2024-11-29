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
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

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
async def with_puree(message: types.Message):
    start = pars()
    matches = start.main()
    today = start.today_matches(matches)

    await message.reply(f"{today}")

@dp.message(F.text.lower() == "лига европы. все матчи")
async def without_puree(message: types.Message):
    start = pars()
    matches = start.main()
    #выводим 10 первых игр
    # reply_markup=types.ReplyKeyboardRemove() - удаляет клавиатуру
    await message.reply(f"{matches[0:10]}", reply_markup=types.ReplyKeyboardRemove())



#эхо-ответчик
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")





async def main() -> None:
    bot = Bot(token=token_telegram, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

