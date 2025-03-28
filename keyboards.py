from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Расписание", callback_data="schedule")],
    [InlineKeyboardButton(text="📰 Новости", callback_data="news")],
    [InlineKeyboardButton(text="📝 Сессия", callback_data="session")],
    [InlineKeyboardButton(text="📍 Адреса", callback_data="addresses")],
    [InlineKeyboardButton(text="🤔 Внеучебное расписание", callback_data="extra_schedule")],
])

# Меню выбора группы
group_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="22-ИБ-1-1", callback_data="group_22-ИБ-1-1")],
    [InlineKeyboardButton(text="22-ИБ-1-2", callback_data="group_22-ИБ-1-2")],
    [InlineKeyboardButton(text="22-ИБ-1-3", callback_data="group_22-ИБ-1-3")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")],
])
