import requests

URL = 'http://localhost:1234/v1/chat/completions'
HEADERS = {"Content-Type": "application/json"}


def make_promt(user_request):
    json = {
        "messages": [
            {"role": "system", "content": "Говори только на русском языке, отвечай на вопрос полностью. Будь добрым "
                                          "и приветливым."},
            {"role": "user", "content": user_request}

        ],
        "temperature": 0.9,
        "max_tokens": 50,
    }
    return json


def process_resp(response):
    if response.status_code == 200 and 'choices' in response.json():
        result = response.json()['choices'][0]['message']['content']
        return result


def ask_gpt(user_request):
    json = make_promt(user_request)
    resp = requests.post(url=URL,
                         headers=HEADERS,
                         json=json)

    if process_resp(resp) is not None:
        return process_resp(resp)
    else:
        s = 'Не удалось получить ответ от нейросети. Попробуйте позже.'
        return s
