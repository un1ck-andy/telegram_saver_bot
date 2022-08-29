import telebot
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)


@bot.message_handler(content_types=["text"])
def get_user_text(message):
    filename = "INBOX.txt"
    message_time = message.json["date"]
    message_time = datetime.utcfromtimestamp(message_time)
    message_time = message_time.strftime("%Y-%m-%d %H:%M:%S")
    if "forward_date" in message.json:
        forward_time = message.json["forward_date"]
        forward_time = datetime.utcfromtimestamp(forward_time)
        forward_time = forward_time.strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        if "forward_date" in message.json:
            f.write(f'{message_time} FROM {forward_time}\n {message.json["text"]}\n')
        else:
            f.write(f'{message_time}\n {message.json["text"]}\n')
    bot.send_message(message.chat.id, "Saved")


if __name__ == "__main__":
    bot.polling(none_stop=True)
