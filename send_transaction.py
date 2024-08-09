import requests
import random
from datetime import datetime
import pytz
import time
import math

# Ваши API ключи и токены
BSC_API_KEY = '7C2J1YVTVAAER9TSDZHAC6WK8Z3Y5B8ABI'  # BscScan API ключ (для BEP20)
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'  # Telegram Bot Token
TELEGRAM_CHAT_ID = '-1002133823734'  # Telegram Chat ID

# Адрес контракта BEP20
CONTRACT_ADDRESS = "0x55d398326f99059ff775485246999027b3197955"  # USDT BEP20

# Имя воркера
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

def round_down(value: float, decimal_places: int) -> float:
    """Округляет число до ближайшего меньшего числа с заданным количеством знаков после запятой."""
    factor = 10 ** decimal_places
    return math.floor(value * factor) / factor

def get_random_usdt_transaction(api_key, contract_address, min_value, max_value):
    """Получает случайную транзакцию USDT с BscScan."""
    url = "https://api.bscscan.com/api"

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

    try:
        print("Fetching transactions from BscScan...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        transactions = response.json().get('result', [])
        print(f"Found {len(transactions)} transactions.")

        filtered_transactions = [
            tx for tx in transactions if min_value <= float(tx['value']) / 10**18 <= max_value
        ]

        if filtered_transactions:
            return random.choice(filtered_transactions)
        else:
            print("No transactions found with the specified value range.")
            return None

    except requests.RequestException as e:
        print(f"Error fetching transactions from BscScan: {e}")
        return None

def send_message(token, chat_id, message):
    """Отправляет сообщение в Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        print("Sending message to Telegram...")
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Message sent to Telegram: {response.status_code}")
        print(f"Response from Telegram: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        return None

def main():
    print("Starting the script...")
    
    min_value = 300
    max_value = 1400

    transaction = get_random_usdt_transaction(BSC_API_KEY, CONTRACT_ADDRESS, min_value, max_value)

    if transaction:
        amount_usdt = float(transaction['value']) / 10**18  # BEP20 использует 18 десятичных знаков
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])

        # Форматирование времени
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Выбор случайного имени
        profit_name = random.choice(NAMES)

        # Округление суммы
        rounded_amount = round_down(amount_usdt, 2)
        worker_share = rounded_amount / 2

        # Формирование сообщения
        message = (
            f"🥑 Профит у: <b>{profit_name}</b>\n"
            f"┠ Сумма заноса: <b>{rounded_amount:.2f}</b> USDT <i>BEP20</i>\n"
            f"┖ Доля воркера: <b>{worker_share:.2f}</b> USDT <i>BEP20</i>\n\n"
            f"🧬 Hash: <code>{tx_hash}</code>\n"
            f"🕔 Время: {date_time}"
        )

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Message sent successfully.")
        else:
            print("Failed to send message.")
    else:
        print("No transaction data found.")

    # Задержка перед следующим запуском
    delay = random.randint(3600, 7200)  # От 1 до 2 часов
    print(f"Sleeping for {delay} seconds...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
