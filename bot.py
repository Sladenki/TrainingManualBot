import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
import random

# Импорт переменных из файла constants
from constants import SCHEDULE_22_IB_1_1, SCHEDULE_22_IB_1_2, SCHEDULE_22_IB_1_3, NEWS_DATA, SESSION_DATA, ADDRESSES_DATA, EXTRA_SCHEDULE_DATA

# Импорт клавиатур
from keyboards import main_menu, group_menu

# Токен для бота
TOKEN = "7953725237:AAFZeMbOle0Mv1Ik_DZbmsHlOP-74teNWmY"

# Создание объектов бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройка логирования (чтобы видеть ошибки и события)
logging.basicConfig(level=logging.INFO)


# Данные о расписании
schedule_data = {
    "22-ИБ-1-1": SCHEDULE_22_IB_1_1,
    "22-ИБ-1-2": SCHEDULE_22_IB_1_2,
    "22-ИБ-1-3": SCHEDULE_22_IB_1_3,
}

news_data = NEWS_DATA
session_data = SESSION_DATA
addresses_data = ADDRESSES_DATA
extra_schedule_data = EXTRA_SCHEDULE_DATA

# New data structures for additional features
quiz_data = {
    "current_quiz": None,
    "quizzes": [
        {
            "question": "Что такое Python?",
            "options": ["Язык программирования", "Змея", "Игра", "Операционная система"],
            "correct_answer": 0
        },
        {
            "question": "Какой тип данных используется для хранения текста в Python?",
            "options": ["int", "float", "str", "bool"],
            "correct_answer": 2
        },
        {
            "question": "Какой символ используется для комментариев в Python?",
            "options": ["//", "#", "/*", "--"],
            "correct_answer": 1
        }
    ]
}

mood_data = {}  # Dictionary to store user moods

# New function for quiz system
@dp.message(lambda message: message.text == "/quiz" or message.text == "📝 Викторина")
async def start_quiz(message: types.Message):
    if quiz_data["current_quiz"] is None:
        quiz = random.choice(quiz_data["quizzes"])
        quiz_data["current_quiz"] = quiz
        
        buttons = []
        for i, option in enumerate(quiz["options"]):
            buttons.append([InlineKeyboardButton(
                text=option,
                callback_data=f"quiz_answer_{i}"
            )])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await message.answer(
            f"📝 Викторина:\n\n{quiz['question']}",
            reply_markup=keyboard
        )
    else:
        await message.answer("Дождитесь завершения текущей викторины!")

@dp.callback_query(lambda callback: callback.data.startswith("quiz_answer_"))
async def process_quiz_answer(callback: types.CallbackQuery):
    await callback.answer()
    if quiz_data["current_quiz"] is None:
        await callback.message.answer("Викторина уже завершена!")
        return
    
    answer = int(callback.data.split("_")[-1])
    quiz = quiz_data["current_quiz"]
    
    if answer == quiz["correct_answer"]:
        await callback.message.answer("✅ Правильно! Молодец!")
    else:
        await callback.message.answer(f"❌ Неправильно! Правильный ответ: {quiz['options'][quiz['correct_answer']]}")
    
    quiz_data["current_quiz"] = None
    # Добавляем кнопку для новой викторины
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Начать новую викторину",
            callback_data="new_quiz"
        )]
    ])
    await callback.message.answer("Хотите попробовать ещё раз?", reply_markup=keyboard)

@dp.callback_query(lambda callback: callback.data == "new_quiz")
async def new_quiz(callback: types.CallbackQuery):
    await callback.answer()
    await start_quiz(callback.message)

# New function for mood tracking
@dp.message(lambda message: message.text == "/mood")
async def track_mood(message: types.Message):
    moods = ["😊", "😐", "😢", "😡", "😴", "🤔"]
    buttons = []
    # Создаем кнопки по 3 в ряд
    for i in range(0, len(moods), 3):
        row = []
        for mood in moods[i:i+3]:
            row.append(InlineKeyboardButton(
                text=mood,
                callback_data=f"mood_{mood}"
            ))
        buttons.append(row)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Как ваше настроение сегодня?", reply_markup=keyboard)

@dp.callback_query(lambda callback: callback.data.startswith("mood_"))
async def process_mood(callback: types.CallbackQuery):
    await callback.answer()
    mood = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    if user_id not in mood_data:
        mood_data[user_id] = []
    
    mood_data[user_id].append({
        "mood": mood,
        "date": datetime.now()
    })
    
    await callback.message.answer(f"Спасибо за ваш ответ! {mood}")

@dp.callback_query(lambda callback: callback.data == "quiz")
async def quiz_callback(callback: types.CallbackQuery):
    await callback.answer()
    await start_quiz(callback.message)

@dp.callback_query(lambda callback: callback.data == "mood")
async def mood_callback(callback: types.CallbackQuery):
    await callback.answer()
    await track_mood(callback.message)

# Обработчик команды /start
@dp.message(lambda message: message.text == "/start")
async def start_cmd(message: types.Message):
    # Создаем большую кнопку меню
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Открыть меню")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer("Привет! Выберите действие:", reply_markup=main_menu)
    await message.answer(reply_markup=reply_keyboard)

# Обработчик нажатия на большую кнопку меню
@dp.message(lambda message: message.text == "📱 Открыть меню")
async def menu_button(message: types.Message):
    await start_cmd(message)

# Обработчик нажатия на кнопку "Расписание"
@dp.callback_query(lambda callback: callback.data == "schedule")
async def show_schedule_menu(callback: types.CallbackQuery):
    await callback.answer()  # Подтверждаем нажатие сразу
    await bot.send_message(callback.from_user.id, "Выберите группу:", reply_markup=group_menu)

# Обработчик выбора группы
@dp.callback_query(lambda callback: callback.data.startswith("group_"))
async def show_schedule(callback: types.CallbackQuery):
    await callback.answer()  # Подтверждаем нажатие
    group = callback.data.split("_")[1] # Получаем название группы из callback_data
    schedule = schedule_data.get(group, "Расписание не найдено")  # Получаем расписание
    await bot.send_message(callback.from_user.id, schedule)

@dp.callback_query(lambda callback: callback.data == "news")
async def show_news(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, news_data)

@dp.callback_query(lambda callback: callback.data == "session")
async def show_session(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, session_data)

@dp.callback_query(lambda callback: callback.data == "addresses")
async def show_addresses(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, addresses_data)

@dp.callback_query(lambda callback: callback.data == "extra_schedule")
async def show_addresses(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, extra_schedule_data)

@dp.callback_query(lambda callback: callback.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, "Выберите действие:", reply_markup=main_menu)

# Главная асинхронная функция, запускающая бота
async def main():
    # Добавляем кнопку в меню бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Открыть меню"),
        BotCommand(command="quiz", description="Пройти викторину"),
        BotCommand(command="mood", description="Отметить настроение")
    ])
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
