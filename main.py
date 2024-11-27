import asyncio
import logging
import sys

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

#Этот обработчик получает сообщения с помощью команды `/test`, вызывет обычное меню с 2 кнопками.
@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

#Ловим нажатие кнопки(текст, который она отправляет)
@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!")

@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    # reply_markup=types.ReplyKeyboardRemove() - удаляет клавиатуру
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())



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

