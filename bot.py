import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand

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

# Обработчик команды /start
@dp.message(lambda message: message.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=main_menu)

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
    ])
    await dp.start_polling(bot) # Запускаем бота в режиме polling

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
