import telebot
import config
import logging
from gpt import GPT

gpt = GPT()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
    encoding='windows-1251'
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
                                                "одиночестве и всячески подбадривать!"
                                                "Ссылка на гитхаб: https://github.com/FreddyFazberUrUr/AI_bot.git")


@bot.message_handler(commands=['start', 'go'])
def start(msg):
    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name} ! Я - твой цифровой собеседник. Узнать обо "
                     f"мне подробнее можно командой /about\n"
                     "Введи /help для помощи в управлении ботом.\n"
                     "<b>Введи любой текст для того, чтобы начать разговор с нейросетью.</B>", parse_mode='html')


@bot.message_handler(commands=['debug'])
def debug(msg):
    bot.send_document(msg.chat.id, open('log_file.txt'))


@bot.message_handler(content_types=['text'])
def ask_gpt(msg):
    user_request = msg.text
    request_tokens = gpt.count_tokens(user_request)

    if request_tokens > gpt.MAX_TOKENS:
        bot.send_message(msg.chat.id, 'Запрос слишком длинный. Попробуйте сделать его меньше.')
        return

    if user_request.lower() != 'продолжи':
        gpt.clear_history()

    json = gpt.make_promt(user_request)
    logging.debug('Промт успешно сформирован.')

    resp = gpt.send_request(json)
    logging.debug('Ответ от нейросети получен.')

    response = gpt.process_resp(resp)
    logging.info('С ответом от нейросети все в порядке')

    if not response[0]:
        bot.send_message(msg.chat.id, 'Не удалось получить ответ от нейросети. Попробуйте позже.')
    else:
        bot.send_message(msg.chat.id, response[1])
        logging.info('С ответом от нейросети все в порядке')


if __name__ == '__main__':
    logging.info("Бот запущен")
    bot.infinity_polling()
