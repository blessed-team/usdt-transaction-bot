import os
import requests
import random
from datetime import datetime
import time

def get_random_usdt_transaction(api_key, min_value, max_value):
    # Адрес контракта USDT на Ethereum
    usdt_contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    
    # URL для получения последних транзакций токена
    url = "https://api.etherscan.io/api"

    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": usdt_contract_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "page": 1,
        "offset": 100,  # Количество транзакций на странице (до 1000)
        "apikey": api_key
    }

    response = requests.get(url, params=params)
    transactions = response.json().get('result', [])

    # Фильтрация транзакций по диапазону суммы
    filtered_transactions = [
        tx for tx in transactions if min_value <= float(tx['value']) / 10**6 <= max_value
    ]

    if filtered_transactions:
        # Возвращаем случайную транзакцию из отфильтрованных
        return random.choice(filtered_transactions)
    return None

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    return response

def main():
    api_key = os.getenv('ETHERSCAN_API_KEY')
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Укажите диапазон в USDT
    min_value = 300
    max_value = 1400

    transaction = get_random_usdt_transaction(api_key, min_value, max_value)

    if transaction:
        amount_usdt = float(transaction['value']) / 10**6
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])
        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        message = (
            f"Сумма транзакции: {amount_usdt:.2f} USDT\n"
            f"Хэш транзакции: {tx_hash}\n"
            f"Дата и время: {date_time} UTC"
        )
        
        response = send_message(token, chat_id, message)
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print("Failed to send message.")
    else:
        print("No transactions found in the specified range.")

if __name__ == "__main__":
    while True:
        main()
        # Случайная задержка от 1 до 2 часов
        delay = random.randint(3600, 7200)
        time.sleep(delay)
