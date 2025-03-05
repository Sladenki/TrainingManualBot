import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7953725237:AAFZeMbOle0Mv1Ik_DZbmsHlOP-74teNWmY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Главное меню
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Расписание", callback_data="schedule")],
    [InlineKeyboardButton(text="📰 Новости", callback_data="news")],
    [InlineKeyboardButton(text="📝 Сессия", callback_data="session")],
    [InlineKeyboardButton(text="📍 Адреса", callback_data="addresses")],
])

# Меню выбора группы
group_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="22-ИБ-1-1", callback_data="group_22-ИБ-1-1")],
    [InlineKeyboardButton(text="22-ИБ-1-2", callback_data="group_22-ИБ-1-2")],
    [InlineKeyboardButton(text="22-ИБ-1-3", callback_data="group_22-ИБ-1-3")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_main")],
])

# Моковые данные для расписания, новостей, сессии и адресов
schedule_data = {
    "22-ИБ-1-1": "Расписание для группы 22-ИБ-1-1:\nПонедельник: Математика\nВторник: Программирование\nСреда: Английский",
    "22-ИБ-1-2": "Расписание для группы 22-ИБ-1-2:\nПонедельник: Физика\nВторник: История\nСреда: Химия",
    "22-ИБ-1-3": "Расписание для группы 22-ИБ-1-3:\nПонедельник: Информатика\nВторник: Экономика\nСреда: Философия",
}
news_data = """
Последние новости КГТУ:
1. В университете прошла конференция по IT.
2. Открыта регистрация на олимпиаду по программированию.
3. В библиотеку поступили новые книги по искусственному интеллекту.
"""
session_data = "Даты сессий:\nЗимняя сессия: 15-30 января\nЛетняя сессия: 1-15 июня"
addresses_data = """
Контактные данные КГТУ:
Адрес: ул. Иванова, 10
Телефон: +7 (123) 456-78-90
Email: info@kgtu.ru
"""

# Словарь для хранения текущего состояния пользователя
user_states = {}


@dp.message(lambda message: message.text == "/start")
async def start_cmd(message: types.Message):
    user_states[message.from_user.id] = "main_menu"
    await message.answer("Привет! Выберите действие:", reply_markup=main_menu)


@dp.callback_query(lambda callback: callback.data == "schedule")
async def show_schedule_menu(callback: types.CallbackQuery):
    user_states[callback.from_user.id] = "schedule_menu"
    await callback.message.edit_text("Выберите группу:", reply_markup=group_menu)


@dp.callback_query(lambda callback: callback.data.startswith("group_"))
async def show_schedule(callback: types.CallbackQuery):
    group = callback.data.split("_")[1]
    schedule = schedule_data.get(group, "Расписание не найдено")
    user_states[callback.from_user.id] = f"schedule_{group}"
    await callback.message.edit_text(schedule, reply_markup=group_menu)


@dp.callback_query(lambda callback: callback.data == "news")
async def show_news(callback: types.CallbackQuery):
    if user_states.get(callback.from_user.id) == "news":
        return  # Предотвращение повторного нажатия
    user_states[callback.from_user.id] = "news"
    await callback.message.edit_text(news_data, reply_markup=main_menu)


@dp.callback_query(lambda callback: callback.data == "session")
async def show_session(callback: types.CallbackQuery):
    if user_states.get(callback.from_user.id) == "session":
        return  # Предотвращение повторного нажатия
    user_states[callback.from_user.id] = "session"
    await callback.message.edit_text(session_data, reply_markup=main_menu)


@dp.callback_query(lambda callback: callback.data == "addresses")
async def show_addresses(callback: types.CallbackQuery):
    if user_states.get(callback.from_user.id) == "addresses":
        return  # Предотвращение повторного нажатия
    user_states[callback.from_user.id] = "addresses"
    await callback.message.edit_text(addresses_data, reply_markup=main_menu)


@dp.callback_query(lambda callback: callback.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    user_states[callback.from_user.id] = "main_menu"
    await callback.message.edit_text("Выберите действие:", reply_markup=main_menu)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())