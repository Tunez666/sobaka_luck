import os
import telebot

# получаем токен и chat_id из переменных окружения
TOKEN = os.getenv("TOKEN")
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID")

if not TOKEN:
    raise ValueError("Не задан TOKEN в переменных окружения")
if not MANAGER_CHAT_ID:
    raise ValueError("Не задан MANAGER_CHAT_ID в переменных окружения")

MANAGER_CHAT_ID = int(MANAGER_CHAT_ID)  # строку превращаем в число
bot = telebot.TeleBot(TOKEN)

# Словарь для связки сообщений пользователей и их ID
user_to_manager = {}

# Когда пишет пользователь — пересылаем менеджеру
@bot.message_handler(func=lambda m: True)
def forward_to_manager(message):
    global MANAGER_CHAT_ID
    # сохраняем ID юзера за message_id
    user_to_manager[message.message_id] = message.chat.id

    # пересылаем в группу менеджеров
    bot.forward_message(MANAGER_CHAT_ID, message.chat.id, message.message_id)

# Когда менеджер отвечает (reply в группе) — пересылаем пользователю
@bot.message_handler(content_types=['text'])
def manager_reply(message):
    if message.chat.id == MANAGER_CHAT_ID and message.reply_to_message:
        original_msg_id = message.reply_to_message.message_id
        if original_msg_id in user_to_manager:
            user_id = user_to_manager[original_msg_id]
            bot.send_message(user_id, message.text)

print("Бот запущен...")
bot.polling(none_stop=True, interval=1)
