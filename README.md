# Телеграмм бот с ИИ
_Бот, состоящий из 2 модулей и файла config.py_
## Инструкция к применению
1. Скопировать репозиторий в вашу папку с проектом. Проверить наличие файлов requirements.txt, bot.py, gpt.py, config.py.
2. Написать комманду pip install -r requirements.txt в терминале.
3. Открыть файл config.py и вставить свой токен в переменную token.
4. Запустить локальный сервер в LM Studio
5. Запустить файл bot.py.

# Файл bot.py 
bot.py - это основной файл программы, который получает и отправляет сообщения в телеграмме.

### Функция start(msg)
Данная функция реагирует на комманду /start и отправляет приветственное сообщение и инструкцию по использованию ботом.

### Функция ask_gpt(msg)
Данная функция реагирует на любой текст, обрабатывает его с помощью функций файла gpt.py и отправляет пользователю ответ от нейросети.

### Функция help_command(msg)
Данная функция реагирует на комманду /help и отправляет сообщение с краткой инструкцией по использованию ботом.

### Функция about_command(msg)
Данная функция реагирует на комманду /about и отправляет сообщение с информацией о боте.

# Файл gpt.py, класс GPT
Класс GPT отправляет post-запросы на локальный сервер и сохраняет или удаляет историю запросов.

### Функция count_tokens(prompt)
Данная функция считает кол-во токенов в промте для нейросети.
Возращает - кол-во токенов.

### Функция make_promt(self, user_request)
Данная функция вставляет сообщение от пользователя(user_reguest) в словарь json.
Возращяет - словарь json.

### Функция send_request(self, json)
Отправляет post-запрос на локальный сервер.
Возвращает - ответ нейросети.

### Функция process_resp(self, response) -> [bool, str]
Проверяет ответ нейросети.
Возвращает(если ошибка) - текст и код ошибки.
Возвращает(если нет ошибки) - ответ нейросети.

