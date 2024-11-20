import aiosqlite
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
import DB_assets

async def check_question(correct_option, callback, current_question_index, a, quiz_data, DB_NAME):
    if a == correct_option:
      await callback.message.answer("Верно!")
      await update_question_counter(callback, quiz_data, DB_NAME)
    else:
      await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    num_win = await DB_assets.get_test_table_any_field(callback.from_user.id, DB_NAME)
    num_fail = await DB_assets.get_test_table_any_field(callback.from_user.id, DB_NAME)
    await callback.message.answer(f"Промежуточный результат: +{num_win}")

    #проверка на последний вопрос
async def last_question_check(callback, current_question_index, quiz_data, DB_NAME):
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id, quiz_data, DB_NAME)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")

        #обнуление счётчика результатов
        num_win = await DB_assets.get_test_table_any_field(callback.from_user.id, DB_NAME)
        num_fail = len(quiz_data) - num_win
        await callback.message.answer(f"Результат: +{num_win}, -{num_fail}")
        default = 0
        await DB_assets.update_test_table_any_field(callback.from_user.id, default, DB_NAME)

    # эхо выбора варианта ответа
async def chose_option_echo(callback, current_question_index, a, quiz_data):
    correct_option = quiz_data[current_question_index]['correct_option']
    chose_option = quiz_data[current_question_index]['options'][a]
    await callback.message.answer(f"Выбранный вариант: {chose_option}")
    return correct_option

async def get_question(message, user_id, quiz_data, DB_NAME):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await DB_assets.get_quiz_index(user_id, DB_NAME)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index], quiz_data)
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message, quiz_data, DB_NAME):
    user_id = message.from_user.id
    current_question_index = 0
    await DB_assets.update_quiz_index(user_id, current_question_index, DB_NAME)
    await get_question(message, user_id, quiz_data, DB_NAME)

async def update_question_counter(callback, quiz_data, DB_NAME):
    test1 = await DB_assets.get_test_table_any_field(callback.from_user.id, DB_NAME)
    test1 += 1
    await DB_assets.update_test_table_any_field(callback.from_user.id, test1, DB_NAME)


def generate_options_keyboard(answer_options, right_answer, quiz_data):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data= str(answer_options.index(option))
            )
        )
    builder.adjust(1)
    return builder.as_markup()
