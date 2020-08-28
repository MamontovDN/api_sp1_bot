import os
import requests
import telegram
import time
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PRACTICUM_URL = os.getenv("Yandex_Practicum_url")


def parse_homework_status(homework):
    homework_name = homework["homework_name"]
    homework_status = homework["status"]
    if homework_name is None or homework_status is None:
        return "неверный ответ сервера"
    if homework_status == "rejected":
        verdict = "К сожалению в работе нашлись ошибки."
    else:
        verdict = "Ревьюеру всё понравилось, " \
                  "можно приступать к следующему уроку."
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    url = PRACTICUM_URL
    params = {"from_date": current_timestamp}
    headers = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}
    homework_statuses = requests.get(url,
                                     headers=headers,
                                     params=params
                                     )
    return homework_statuses.json()


def send_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    return bot.send_message(CHAT_ID, message)


def main():
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get("homeworks"):
                send_message(parse_homework_status(
                    new_homework.get("homeworks")[0])
                )
            current_timestamp = new_homework.get("current_date")
            time.sleep(700)

        except Exception as e:
            print(f"Бот упал с ошибкой: {e}")
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()
