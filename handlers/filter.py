from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix='pressed_button_'):
    a: str
