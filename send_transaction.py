import requests
import random
from datetime import datetime
import pytz
import time
import math

# Ваши API ключи и токены
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'  # Etherscan API ключ (для ERC20)
BSC_API_KEY = '7C2J1YVTVAAER9TSDZHAC6WK8Z3Y5B8ABI'  # BscScan API ключ (для BEP20)
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'  # Telegram Bot Token
TELEGRAM_CHAT_ID = '-1002133823734'  # Telegram Chat ID

# Названия для профита
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

# Адреса контрактов
CONTRACT_ADDRESSES = {
    "ERC20": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT ERC20
    "BEP20": "0x55d398326f99059ff775485246999027b3197955"   # USDT BEP20
}

def get_random_usdt_transaction(api_key, contract_address, network):
    url = f"https://api.{network}.com/api"

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
        print(f"Fetching transactions from {network}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        transactions = response.json().get('result', [])
        print(f"Found {len(transactions)} transactions.")

        if transactions:
            return random.choice(transactions)
        else:
            print(f"No transactions found for {network}.")
            return None

    except requests.RequestException as e:
        print(f"Error fetching transactions: {e}")
        return None

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        print("Sending message to Telegram...")
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Message sent: {response.status_code}")
        return response
    except requests.RequestException as e:
        print(f"Error sending message: {e}")
        return None

def main():
    print("Starting the script...")
    
    # Выбор случайной сети
    network = "bscscan"  # Используем BSC для BEP20
    api_key = BSC_API_KEY
    contract_address = CONTRACT_ADDRESSES["BEP20"]
    
    transaction = get_random_usdt_transaction(api_key, contract_address, network)

    if transaction:
        # Обработка и округление данных
        value = int(transaction['value']) / 10**18  # BEP20 использует 18 десятичных знаков
        amount = math.floor(value * 100) / 100  # Округление до двух знаков после запятой и вниз
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])

        # Форматирование времени
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Выбор случайного имени
        profit_name = random.choice(NAMES)
        worker_share = amount / 2

        # Формирование сообщения
        message = (
            f"💲 Профит у: <b>{profit_name}</b>\n"
            f"┠ Сумма заноса: <b>{amount:.2f}</b> USDT <i>BEP20</i>\n"
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

    delay = random.randint(30, 60)
    print(f"Sleeping for {delay} seconds...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
