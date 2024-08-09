import requests
import random
from datetime import datetime
import pytz
import time
import math

# API ключи и токены
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'
TRONGRID_API_KEY = '175a5b7f-e2c2-4a3a-9bd9-bf2041feb02c'
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'
TELEGRAM_CHAT_ID = '-1002133823734'

# Адреса контрактов
ERC20_CONTRACT_ADDRESS = "0xdac17f958d2ee523a2206206994597c13d831ec7"
TRC20_CONTRACT_ADDRESS = "TF9i9VEzaayhog5EmGuq4hhYZnnDtodta3"

# Список имён
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

def get_random_usdt_transaction(api_key, contract_address, network):
    if network == "ERC20":
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": contract_address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "page": 1,
            "offset": 100,
            "apikey": api_key
        }
    elif network == "TRC20":
        url = "https://api.trongrid.io/v1/accounts/transactions"
        params = {
            "contract_address": contract_address,
            "limit": 100
        }
        headers = {"TRON-PRO-API-KEY": api_key}
    else:
        raise ValueError("Unsupported network")

    try:
        print(f"Запрос транзакций к {network}...")
        response = requests.get(url, params=params, headers=headers if network == "TRC20" else None)
        response.raise_for_status()
        transactions = response.json().get('result', []) if network == "ERC20" else response.json().get('data', [])
        print(f"Получено {len(transactions)} транзакций.")

        if network == "ERC20":
            filtered_transactions = [
                tx for tx in transactions if min_value <= float(tx['value']) / 10**6 <= max_value
            ]
        else:
            filtered_transactions = [
                tx for tx in transactions if min_value <= float(tx['amount']) / 10**6 <= max_value
            ]

        if filtered_transactions:
            return random.choice(filtered_transactions)
        else:
            print("Нет подходящих транзакций.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка при запросе транзакций: {e}")
        return None

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        print("Отправка сообщения в Telegram...")
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Сообщение отправлено. Код состояния: {response.status_code}")
        print(f"Ответ от Telegram: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return None

def main():
    print("Запуск скрипта...")
    
    min_value = 300
    max_value = 1400

    network = random.choice(["ERC20", "TRC20"])
    contract_address = ERC20_CONTRACT_ADDRESS if network == "ERC20" else TRC20_CONTRACT_ADDRESS
    transaction = get_random_usdt_transaction(ETHERSCAN_API_KEY, contract_address, network)

    if transaction:
        amount_usdt = float(transaction['value']) / 10**6 if network == "ERC20" else float(transaction['amount']) / 10**6
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp']) if network == "ERC20" else int(transaction['timestamp'])

        # Форматирование времени
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Выбор имени
        profit_name = random.choice(NAMES)
        # Расчет доли воркера
        worker_share = amount_usdt / 2

        # Формирование сообщения
        message = (
            f"<b>Профит у:</b> {profit_name}\n"
            f"<b>Сумма заноса:</b> <i>{amount_usdt:.2f} USDT ({network})</i>\n"
            f"<b>Доля воркера:</b> <i>{worker_share:.2f} USDT ({network})</i>\n\n"
            f"<b>Hash:</b> <code>{tx_hash}</code>\n"
            f"<b>Время:</b> {date_time}"
        )

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Не удалось отправить сообщение.")
    else:
        print("Не удалось получить подходящую транзакцию.")

    delay = random.randint(60, 120)
    print(f"Задержка {delay} секунд...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
