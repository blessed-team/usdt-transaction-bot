import requests
import random
from datetime import datetime
import pytz
import time

# API ключи и токены
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'  # Etherscan API ключ
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'  # Telegram Bot Token
TELEGRAM_CHAT_ID = '-1002133823734'  # Telegram Chat ID
TRONGRID_API_KEY = '175a5b7f-e2c2-4a3a-9bd9-bf2041feb02c'  # TronGrid API ключ

# Контрактные адреса
ERC20_CONTRACT_ADDRESS = "0xdac17f958d2ee523a2206206994597c13d831ec7"  # Контракт USDT ERC20
TRC20_CONTRACT_ADDRESS = "TF9i9VEzaayhog5EmGuq4hhYZnnDtodta3"  # Контракт USDT TRC20

# Имя для профита
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

def get_random_transaction(api_key, contract_address, network='ERC20'):
    if network == 'ERC20':
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
    elif network == 'TRC20':
        url = "https://api.trongrid.io/v1/accounts/{}/transactions/trc20".format(contract_address)
        params = {
            "limit": 100
        }
        headers = {
            'TRON-PRO-API-KEY': api_key
        }
    else:
        print("Неизвестная сеть.")
        return None

    try:
        print(f"Запрос транзакций к {network} API...")
        if network == 'ERC20':
            response = requests.get(url, params=params)
        elif network == 'TRC20':
            response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        transactions = response.json().get('result', [])
        print(f"Получено {len(transactions)} транзакций.")

        # Фильтруем транзакции по значению
        min_value = 300
        max_value = 1400
        filtered_transactions = [
            tx for tx in transactions if min_value <= float(tx['value']) / (10**6 if network == 'ERC20' else 10**6) <= max_value
        ]

        if filtered_transactions:
            return random.choice(filtered_transactions)
        else:
            print("Нет подходящих транзакций.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка запроса к {network} API: {e}")
        return None

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        print("Отправка сообщения в Telegram...")
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Статус ответа Telegram: {response.status_code}")
        print(f"Ответ от Telegram: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
        return None

def main():
    print("Запуск скрипта...")

    # Выбираем случайную сеть (ERC20 или TRC20)
    network = random.choice(['ERC20', 'TRC20'])
    contract_address = ERC20_CONTRACT_ADDRESS if network == 'ERC20' else TRC20_CONTRACT_ADDRESS

    transaction = get_random_transaction(ETHERSCAN_API_KEY if network == 'ERC20' else TRONGRID_API_KEY, contract_address, network)

    if transaction:
        amount = float(transaction['value']) / (10**6 if network == 'ERC20' else 10**6)
        tx_hash = transaction['hash']
        timestamp = int(transaction['timeStamp'])

        # Конвертируем время в европейский формат
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Случайное имя из списка
        profit_name = random.choice(NAMES)
        worker_share = amount / 2

        # Формируем сообщение
        message = (
            f"💲 Профит у: {profit_name}\n"
            f"┠ Сумма заноса: {amount:.2f} USDT {network}\n"
            f"┖ Доля воркера: {worker_share:.2f} USDT\n\n"
            
            f"🧬 Hash: <code>{tx_hash}</code>\n"
            f"🕔 Время: {date_time}"
        )

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Ошибка отправки сообщения.")
    else:
        print("Нет подходящих транзакций.")

    delay = random.randint(60*60, 2*60*60)  # От 1 до 2 часов
    print(f"Ожидание {delay} секунд...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
