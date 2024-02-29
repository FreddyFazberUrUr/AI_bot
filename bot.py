import telebot
import config
import logging
from gpt import GPT
from telebot import types

gpt = GPT()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
    encoding='windows-1251'
)

bot = telebot.TeleBot(token=config.token)


def collect_feedback(msg):
    with open('feedback.txt', 'w', encoding='windows-1251') as f:
        f.write(f'{msg.from_user.first_name} оставил отзыв - {msg.text}\n')
        logging.info(f'{msg.from_user.first_name} оставил отзыв.')
        bot.send_message(msg.chat.id, 'Спасибо за отзыв!')


@bot.message_handler(commands=['help'])
def help_command(msg):
    bot.send_message(msg.from_user.id, "Я - твой цифровой собеседник. Узнать обо мне подробнее можно командой "
                     "/about\n<b>Для того, чтобы пользоваться нейросетью, просто отправь свой запрос в чат.</b>\n"
                     "<i>Чтобы оставить отзыв введи команду /feedback</i>",
                     parse_mode='html')


@bot.message_handler(commands=['about'])
def about_command(msg):
    bot.send_message(msg.from_user.id, text="Рад, что ты заинтересован_а! Мое предназначение — не оставлять тебя в "
                                            "одиночестве и всячески подбадривать!"
                                            "Ссылка на гитхаб: https://github.com/FreddyFazberUrUr/AI_bot.git")


@bot.message_handler(commands=['start', 'go'])
def start(msg):
    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name} ! Я - твой цифровой собеседник. Узнать обо "
                     f"мне подробнее можно командой /about\n"
                     "Введи /help для помощи в управлении ботом.\n"
                     "Введи /feedback чтобы оставить отзыв\n"
                     "<b>Введи любой текст для того, чтобы начать разговор с нейросетью.</B>", parse_mode='html')


@bot.message_handler(commands=['feedback'])
def feedback(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    item3 = types.KeyboardButton("Неудовлетворительный ответ от нейросети")
    item2 = types.KeyboardButton("Не работают команды")
    item1 = types.KeyboardButton('Все отлично, мне понравилось!')

    markup.add(item1, item2, item3)

    bot.send_message(msg.chat.id, 'Оставьте отзыв, если вам не сложно!(можете просто написать сообщение с отзывом '
                                  'или воспользоваться вариантами под строкой ввода)\n\n<i>Убедительная просьба не '
                                  'писать всякие гадости.</i>'.format(msg.from_user, bot.get_me()), reply_markup=markup,
                     parse_mode='html')

    bot.register_next_step_handler(msg, collect_feedback)


@bot.message_handler(commands=['debug'])
def debug(msg):
    bot.send_document(msg.chat.id, open('log_file.txt'))
    bot.send_document(msg.chat.id, open('feedback.txt'))


@bot.message_handler(content_types=['text'])
def ask_gpt(msg):
    user_request = msg.text
    request_tokens = gpt.count_tokens(user_request)

    if request_tokens > gpt.MAX_TOKENS:
        bot.send_message(msg.chat.id, 'Запрос слишком длинный. Попробуйте сделать его меньше.')
        return

    if user_request.lower() != 'продолжить ответ':
        gpt.clear_history()

    else:
        logging.info('Продолжение ответа')

    json = gpt.make_promt(user_request)
    logging.debug('Промт успешно сформирован.')

    resp = gpt.send_request(json)
    logging.debug('Ответ от нейросети получен.')

    response = gpt.process_resp(resp)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    markup.add(types.KeyboardButton("Продолжить ответ"))

    if not response[0]:
        bot.send_message(msg.chat.id, 'Не удалось получить ответ от нейросети. Попробуйте позже.')

    else:
        bot.send_message(msg.chat.id, response[1], reply_markup=markup)
        logging.info('С ответом от нейросети все в порядке')


if __name__ == '__main__':
    logging.info("Бот запущен")
    bot.infinity_polling()
