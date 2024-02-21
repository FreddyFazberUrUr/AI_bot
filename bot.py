import telebot
import config
import logging
import gpt

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = telebot.TeleBot(token=config.token)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.from_user.id, "Я - твой цифровой собеседник. Узнать обо мне подробнее можно командой "
                     "/about\n<b>Для того, чтобы пользоваться нейросетью, просто отправь свой запрос в чат.</b>",
                     parse_mode='html')


@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.from_user.id, text="Рад, что ты заинтересован_а! Мое предназначение — не оставлять тебя в "
                                                "одиночестве и всячески подбадривать!")


@bot.message_handler(commands=['start', 'go'])
def start(msg):
    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name} ! Я - твой цифровой собеседник. Узнать обо "
                     f"мне подробнее можно командой /about\n"
                     "Введи /help для помощи в управлении ботом.\n"
                     "Введи любой текст для того, чтобы начать разговор с нейросетью.")


@bot.message_handler(commands=['debug'])
def debug(msg):
    bot.send_message(msg.chat.id, 'Файл с логами')


@bot.message_handler(content_types=['text'])
def ask_gpt(msg):
    bot.send_message(msg.chat.id, gpt.ask_gpt(msg.text))


if __name__ == '__main__':
    bot.infinity_polling()
