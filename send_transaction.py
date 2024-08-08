import requests
import random
from datetime import datetime
import pytz
import time

# Жестко закодированные значения
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'  # Замените на ваш Etherscan API ключ
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'  # Замените на ваш Telegram Bot Token
TELEGRAM_CHAT_ID = '-1002133823734'  # Замените на ваш Telegram Chat ID

def get_random_usdt_transaction(api_key, min_value, max_value):
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
            print("Нет транзакций в указанном диапазоне.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка при запросе к Etherscan: {e}")
        return None

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    
    try:
        print("Отправка сообщения в Telegram...")
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Статус ответа от Telegram: {response.status_code}")
        print(f"Ответ от Telegram: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return None

def main():
    print("Запуск основной функции...")
    
    min_value = 300
    max_value = 1400

    transaction = get_random_usdt_transaction(ETHERSCAN_API_KEY, min_value, max_value)

    if transaction:
        amount_usdt = float(transaction['value']) / 10**6
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])

        utc_zone = pytz.UTC
        date_time = datetime.fromtimestamp(timestamp, utc_zone).strftime('%Y-%m-%d %H:%M:%S')

        message = (
            f"Сумма транзакции: {amount_usdt:.2f} USDT\n"
            f"Хэш транзакции: {tx_hash}\n"
            f"Дата и время: {date_time} UTC"
        )

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Не удалось отправить сообщение.")
    else:
        print("Не удалось найти подходящую транзакцию.")

    delay = random.randint(3600, 7200)
    print(f"Ожидание {delay} секунд...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
