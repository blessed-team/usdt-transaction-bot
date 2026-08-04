import requests
import random
from datetime import datetime
import pytz
import time

# Настройки API
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'  # API ключ для Etherscan (ERC20)
BSC_SCAN_API_KEY = '7C2J1YVTVAAER9TSDZHAC6WK8Z3Y5B8ABI'  # API ключ для BscScan (BEP20)
TELEGRAM_BOT_TOKEN = '8897185110:AAGZy5xqvOYe4QBslIGJLFezTU_VwZtwbiY'  # Токен для Telegram Bot
TELEGRAM_CHAT_ID = '-1004439708770'  # ID чата Telegram

# Список имен
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens", "T1m 24/7", "Blessed", "DIOR-h8ter", "DB-legacy"]

def round_up(value: float, multiple: float) -> float:
    """Округляет значение до ближайшего большего числа, кратного multiple."""
    return multiple * (value // multiple)

def get_random_erc20_transaction(api_key, min_value, max_value):
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

def get_random_bep20_transaction(api_key, min_value, max_value):
    """Получает случайную транзакцию USDT из BscScan."""
    usdt_contract_address = "0x55d398326f99059ff775485246999027b3197955"
    url = "https://api.bscscan.com/api"

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
        print("Запрос транзакций к BscScan...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        transactions = response.json().get('result', [])
        print(f"Получено {len(transactions)} транзакций.")

        filtered_transactions = [
            tx for tx in transactions if min_value <= float(tx['value']) / 10**18 <= max_value
        ]

        if filtered_transactions:
            return random.choice(filtered_transactions)
        else:
            print("Нет транзакций, соответствующих критериям.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка запроса к BscScan: {e}")
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
    max_value = 1100

    # Выбираем случайную сеть (ERC20 или BEP20)
    network_choice = random.choice(['ERC20', 'BEP20'])
    print(f"Выбранная сеть: {network_choice}")

    if network_choice == 'ERC20':
        transaction = get_random_erc20_transaction(ETHERSCAN_API_KEY, min_value, max_value)
        unit = 10**6
    else:
        transaction = get_random_bep20_transaction(BSC_SCAN_API_KEY, min_value, max_value)
        unit = 10**18

    if transaction:
        amount_usdt = float(transaction['value']) / unit
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
            f"💲 Профит у: <b>{profit_name}</b>\n"
            f"┠ Сумма заноса: <b>{rounded_amount:.2f}</b> USDT <i>({network_choice})</i>\n"
            f"┖ Доля воркера: <b>{worker_share:.2f}</b> USDT <i>({network_choice})</i>\n\n"
            
            f"🧬 Hash: <code>{tx_hash}</code>\n"
            
            f"🕔 Время: {date_time}"
        )

        # Случайная задержка перед отправкой сообщения
        delay = random.randint(60, 900)  # Задержка от 1 до 15 минут (60 до 900 секунд)
        print(f"Ожидание {delay} секунд перед отправкой сообщения...")
        time.sleep(delay)

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Не удалось отправить сообщение.")
    else:
        print("Не удалось получить подходящую транзакцию.")

if __name__ == "__main__":
    main()
