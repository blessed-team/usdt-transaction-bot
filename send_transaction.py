import os
import requests
import random
from datetime import datetime
import pytz
import time

# Константы и настройки
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'
TELEGRAM_CHAT_ID = '-1002133823734'
TRON_API_KEY = '175a5b7f-e2c2-4a3a-9bd9-bf2041feb02c'  # Замените на ваш ключ API для Tron
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

# Файл для хранения времени последнего запуска
LAST_RUN_FILE = 'last_run.txt'

def get_last_run_time():
    """Возвращает время последнего запуска из файла."""
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as f:
            return float(f.read().strip())
    return 0

def update_last_run_time():
    """Обновляет время последнего запуска в файле."""
    with open(LAST_RUN_FILE, 'w') as f:
        f.write(str(time.time()))

# Функция для получения случайной транзакции ERC20
def get_random_usdt_transaction_erc20(api_key, min_value, max_value):
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
            print("Нет транзакций в заданном диапазоне.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка при запросе к Etherscan: {e}")
        return None

# Функция для получения случайной транзакции TRC20
def get_random_usdt_transaction_trc20(api_key, min_value, max_value):
    url = "https://api.trongrid.io/v1/accounts/TADDRESS/transactions/trc20"

    headers = {
        "TRON-PRO-API-KEY": api_key
    }

    try:
        print("Запрос транзакций к Tron...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        transactions = response.json().get('data', [])
        print(f"Получено {len(transactions)} транзакций.")

        filtered_transactions = [
            tx for tx in transactions if min_value <= float(tx['value']) <= max_value
        ]

        if filtered_transactions:
            return random.choice(filtered_transactions)
        else:
            print("Нет транзакций в заданном диапазоне.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка при запросе к Tron: {e}")
        return None

# Функция для отправки сообщения в Telegram
def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        print("Отправка сообщения в Telegram...")
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Статус отправки в Telegram: {response.status_code}")
        print(f"Ответ от Telegram: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return None

def main():
    print("Запуск процесса транзакций...")

    # Проверяем время последнего запуска
    last_run = get_last_run_time()
    current_time = time.time()

    # Интервал между запусками в секундах (от 1 до 2 часов)
    min_interval = 3600
    max_interval = 7200

    if current_time - last_run < min_interval:
        print("Интервал времени не достигнут. Пропуск выполнения.")
        return

    min_value = 300
    max_value = 1400

    # Выбираем случайную сеть для транзакции
    network = random.choice(["ERC20", "TRC20"])

    if network == "ERC20":
        transaction = get_random_usdt_transaction_erc20(ETHERSCAN_API_KEY, min_value, max_value)
    else:
        transaction = get_random_usdt_transaction_trc20(TRON_API_KEY, min_value, max_value)

    if transaction:
        # Определяем сумму и другие параметры
        amount_usdt = float(transaction['value']) / (10**6 if network == "ERC20" else 1)
        amount_usdt = (amount_usdt // 10) * 10  # Округляем до ближайшего десятка вниз
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])

        # Устанавливаем временную зону
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Случайное имя
        profit_name = random.choice(NAMES)
        worker_share = amount_usdt / 2

        # Создаем сообщение
        message = (
            f"💲 Профит у: {profit_name}\n"
            f"┠ Сумма заноса: {amount_usdt:.2f} USDT {network}\n"
            f"┖ Доля воркера: {worker_share:.2f} USDT\n\n"
            
            f"🧬 Hash: <code>{tx_hash}</code>\n"
            f"🕔 Время: {date_time}"
        )

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
            update_last_run_time()
        else:
            print("Ошибка при отправке сообщения.")
    else:
        print("Не удалось получить данные транзакции.")

if __name__ == "__main__":
    main()
