import requests
import random
from datetime import datetime
import pytz
import time

# Настройки API
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'  # API ключ для Etherscan
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'  # Токен для Telegram Bot
TELEGRAM_CHAT_ID = '-1002133823734'  # ID чата Telegram

# Список имен
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

def round_up(value: float, multiple: float) -> float:
    """Округляет значение до ближайшего большего числа, кратного multiple."""
    return multiple * (value // multiple)

def get_random_usdt_transaction(api_key, min_value, max_value):
    """Получает случайную транзакцию USDT из Etherscan."""
    usdt_contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    url = "https://api.etherscan.io/api"

    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": usdt_contract_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "page": 1,
        "offset": 100,
        "apikey": api_key
    }

    try:
        print("Запрос транзакций к Etherscan...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        transactions = response.json().get('result', [])
        print(f"Получено {len(transactions)} транзакций.")

        filtered_transactions = [
            tx for tx in transactions if min_value <= float(tx['value']) / 10**6 <= max_value
        ]

        if filtered_transactions:
            return random.choice(filtered_transactions)
        else:
            print("Нет транзакций, соответствующих критериям.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка запроса к Etherscan: {e}")
        return None

def send_message(token, chat_id, message):
    """Отправляет сообщение в Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        print("Отправка сообщения в Telegram...")
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Сообщение отправлено в Telegram: {response.status_code}")
        print(f"Ответ Telegram: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
        return None

def main():
    print("Запуск скрипта...")
    
    min_value = 300
    max_value = 1400

    transaction = get_random_usdt_transaction(ETHERSCAN_API_KEY, min_value, max_value)

    if transaction:
        amount_usdt = float(transaction['value']) / 10**6
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])

        # Форматирование даты и времени в европейском формате
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Выбираем случайное имя из списка
        profit_name = random.choice(NAMES)

        # Округление суммы до ближайшего большего числа, кратного 10
        rounded_amount = round_up(amount_usdt, 10)
        worker_share = rounded_amount / 2

        # Формирование сообщения
        message = (
            f"💲 Профит у: {profit_name}\n"
            f"┠ Сумма заноса: {rounded_amount:.2f} USDT\n"
            f"┖ Доля воркера: {worker_share:.2f} USDT\n\n"
            
            f"🧬 Hash: <code>{tx_hash}</code>\n"
            f"🕔 Время: {date_time}"
        )

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Не удалось отправить сообщение.")
    else:
        print("Не удалось получить подходящую транзакцию.")

    # Случайная задержка перед следующим запуском
    delay = random.randint(3600, 7200)  # Задержка от 15 до 30 минут
    print(f"Ожидание {delay} секунд до следующего запуска...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
