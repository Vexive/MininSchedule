from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from settings.emojis import EMOJIS

class Keyboards:
    @staticmethod
    def main_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(f"{EMOJIS['start']} Добавить задачу", f"f'{EMOJIS['description']} Показать задачи")
        keyboard.add(f"{EMOJIS['delete']} Удалить задачу", f"{EMOJIS['edit']} Редактировать задачу")
        return keyboard

    @staticmethod
    def priority_keyboard(self, task_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(f"{EMOJIS['high_priority']} Высокая", callback_data=f"priority_{task_id}_high"),
            InlineKeyboardButton(f"{EMOJIS['medium_priority']} Средняя", callback_data=f"priority_{task_id}_medium"),
            InlineKeyboardButton(f"{EMOJIS['low_priority']} Низкая", callback_data=f"priority_{task_id}_low")
        )
        return keyboard

    @staticmethod
    def done_keyboard(self, task_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(f"{EMOJIS['check']} Mark as Done", callback_data=f"done_{task_id}")
        )
        return keyboard

    @staticmethod
    def show_keyboard(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("На сегодня", callback_data=""),
            InlineKeyboardButton("На завтра", callback_data=""),
            InlineKeyboardButton("На неделю", callback_data="")
        )
