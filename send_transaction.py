import requests
import random
from datetime import datetime
import pytz
import time

# Конфигурация
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'  # Telegram Bot Token
TELEGRAM_CHAT_ID = '-1002133823734'  # Telegram Chat ID
TRONGRID_API_KEY = '175a5b7f-e2c2-4a3a-9bd9-bf2041feb02c'  # TronGrid API Key
TRC20_CONTRACT_ADDRESS = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'  # USDT TRC20 Contract Address

NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

def get_random_trc20_transaction(contract_address, api_key):
    url = f"https://api.trongrid.io/v1/contracts/{contract_address}/transactions"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        transactions = response.json().get('data', [])
        if transactions:
            return random.choice(transactions)
        else:
            print("No transactions found for TRC20.")
            return None
    else:
        print("Failed to retrieve TRC20 transactions:", response.status_code, response.text)
        return None

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Message sent to Telegram: {response.status_code}")
        print(f"Response: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Failed to send message to Telegram: {e}")
        return None

def format_amount(amount):
    return f"{amount:.2f}"

def main():
    print("Starting the script...")
    
    contract_address = TRC20_CONTRACT_ADDRESS
    network = 'TRC20'

    print(f"Fetching transactions from {network}...")
    
    transaction = get_random_trc20_transaction(contract_address, TRONGRID_API_KEY)
    
    if transaction:
        amount = int(transaction['raw_data']['contract'][0]['parameter']['value']['amount']) / 10**6
        tx_hash = transaction['txID']
        timestamp = transaction['block_timestamp'] // 1000
        date_time = datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Berlin')).strftime('%H:%M:%S %d-%m-%Y')

        # Выбор имени и расчет доли воркера
        profit_name = random.choice(NAMES)
        worker_share = amount / 2

        # Формирование сообщения
        message = (
            f"🥑 Профит у: {profit_name}\n"
            f"┠ Сумма заноса: <b>{format_amount(amount)} USDT</b> <i>{network}</i>\n"
            f"┖ Доля воркера: <b>{format_amount(worker_share)} USDT</b> <i>{network}</i>\n\n"
            f"🧬 Hash: <code>{tx_hash}</code>\n"
            f"🕔 Время: {date_time}"
        )

        response = send_message(TELE
