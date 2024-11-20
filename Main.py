import nest_asyncio
nest_asyncio.apply()

import aiosqlite
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
import DB_assets
import quiz_engine
import json
from pathlib import Path

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '7934850098:AAEO4Gdt7vgVQ8NLrAQXs4WrjOuJHxvL3Us'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()
# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'

# Структура квиза
path = Path('pages.json')
quiz_data = json.loads(path.read_text(encoding='utf-8'))

async def quiz_core(callback: types.CallbackQuery, a, quiz_data, DB_NAME):
    current_question_index = await DB_assets.get_quiz_index(callback.from_user.id, DB_NAME)
    # эхо выбора варианта ответа
    correct_option = await quiz_engine.chose_option_echo(callback, current_question_index, a, quiz_data)
    await quiz_engine.check_question(correct_option, callback, current_question_index, a, quiz_data, DB_NAME)
    current_question_index = await DB_assets.update_quiz_number(callback, DB_NAME)
    await quiz_engine.last_question_check(callback, current_question_index, quiz_data, DB_NAME)

@dp.callback_query(F.data == '0')
async def any_answer(callback: types.CallbackQuery):
    a = 0
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await quiz_core(callback, a, quiz_data, DB_NAME)
               
@dp.callback_query(F.data == '1')
async def any_answer(callback: types.CallbackQuery):
    a = 1
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await quiz_core(callback, a, quiz_data, DB_NAME)

@dp.callback_query(F.data == '2')
async def any_answer(callback: types.CallbackQuery):
    a = 2
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await quiz_core(callback, a, quiz_data, DB_NAME)

@dp.callback_query(F.data == '3')
async def any_answer(callback: types.CallbackQuery):
    a = 3
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await quiz_core(callback, a, quiz_data, DB_NAME)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await quiz_engine.new_quiz(message, quiz_data, DB_NAME)

# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await DB_assets.create_table(DB_NAME)
    await DB_assets.create_test_table(DB_NAME)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())