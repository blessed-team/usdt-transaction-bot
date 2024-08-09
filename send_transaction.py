import requests
import random
from datetime import datetime
import pytz
import time

# API ключи и ID
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'
TRONGRID_API_KEY = '175a5b7f-e2c2-4a3a-9bd9-bf2041feb02c'
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'
TELEGRAM_CHAT_ID = '-1002133823734'

# Адреса контрактов
CONTRACT_ADDRESSES = {
    "ERC20": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT ERC20
    "TRC20": "TXoQyHBbKjyz7x4Yx9F4DpqiyuEwFj8jKw"  # Пример адреса USDT TRC20
}

NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

def get_random_transaction(api_key, network, min_value, max_value):
    if network == "ERC20":
        contract_address = CONTRACT_ADDRESSES["ERC20"]
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
        contract_address = CONTRACT_ADDRESSES["TRC20"]
        url = f"https://api.trongrid.io/v1/accounts/{contract_address}/transactions/trc20"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "limit": 100,
            "only_confirmed": True
        }
    else:
        raise ValueError("Unsupported network")

    try:
        print(f"Запрос транзакций к {network} API...")
        response = requests.get(url, params=params, headers=headers if network == "TRC20" else None)
        response.raise_for_status()
        transactions = response.json().get('data', [])
        print(f"Получено {len(transactions)} транзакций.")

        filtered_transactions = [
            tx for tx in transactions if min_value <= float(tx['value']) / 10**6 <= max_value
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
        print(f"Статус ответа от Telegram: {response.status_code}")
        print(f"Ответ от Telegram: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return None

def main():
    print("Запуск скрипта...")

    network = random.choice(["ERC20", "TRC20"])  # Случайный выбор сети
    min_value = 300
    max_value = 1400

    transaction = get_random_transaction(ETHERSCAN_API_KEY, network, min_value, max_value)

    if transaction:
        amount_usdt = float(transaction['value']) / 10**6
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])

        # Установить временную зону Europe/Berlin
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Выбрать имя из списка
        profit_name = random.choice(NAMES)
        worker_share = amount_usdt / 2

        # Создать сообщение
        message = (
            f"💲 Профит у: {profit_name}\n"
            f"┠ Сумма заноса: {amount_usdt:.2f} USDT {network}\n"
            f"┖ Доля воркера: {worker_share:.2f} USDT\n\n"

            f"🧬 Hash: <code>{tx_hash}</code>\n"
            f"🕔 Время: {date_time}"
        )

        # Отправить сообщение
        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Не удалось отправить сообщение.")
    else:
        print("Не удалось получить транзакцию.")

    delay = random.randint(3600, 7200)  # Задержка от 1 до 2 часов
    print(f"Ожидание {delay} секунд...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
