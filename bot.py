import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7953725237:AAFZeMbOle0Mv1Ik_DZbmsHlOP-74teNWmY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Методочка по Telegram Bot")]],
    resize_keyboard=True
)

# Подменю "Подготовка рабочей среды"
setup_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Шаг 0.1: Установка Node.JS")],
        [KeyboardButton(text="Шаг 0.2: Установка IDE")],
        [KeyboardButton(text="Шаг 0.3: Создание папки проекта")],
        [KeyboardButton(text="Шаг 0.4: Использование терминала")],
        [KeyboardButton(text="Шаг 0.5: Инициализация NPM модуля")],
        [KeyboardButton(text="Шаг 0.6: Установка nodemon")],
        [KeyboardButton(text="Шаг 0.7: Установка линтера")],
        [KeyboardButton(text="Шаг 0.8: Настройка линтера")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)


@dp.message(lambda message: message.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=main_menu)


@dp.message(lambda message: message.text == "Методочка по Telegram Bot")
async def show_setup(message: types.Message):
    await message.answer("Выберите шаг:", reply_markup=setup_menu)


@dp.message(lambda message: message.text == "Назад")
async def go_back(message: types.Message):
    await message.answer("Возвращаюсь в главное меню...", reply_markup=main_menu)


@dp.message()
async def handle_steps(message: types.Message):
    steps = {
        "Шаг 0.1: Установка Node.JS": "Загрузите Node.js с официального сайта: https://nodejs.org/",
        "Шаг 0.2: Установка IDE": "Рекомендуется использовать VS Code: https://code.visualstudio.com/",
        "Шаг 0.3: Создание папки проекта": "Создайте новую папку в удобном месте и откройте её в терминале.",
        "Шаг 0.4: Использование терминала": "Откройте терминал (в VS Code: Ctrl + `) и используйте команды для работы с файлами.",
        "Шаг 0.5: Инициализация NPM модуля": "Выполните команду `npm init -y`, чтобы создать package.json.",
        "Шаг 0.6: Установка nodemon": "Введите `npm install -g nodemon` для установки nodemon.",
        "Шаг 0.7: Установка линтера": "Используйте команду `npm install eslint --save-dev`.",
        "Шаг 0.8: Настройка линтера": "Запустите `npx eslint --init` и следуйте инструкциям."
    }
    response = steps.get(message.text, "Неизвестная команда")
    await message.answer(response)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
