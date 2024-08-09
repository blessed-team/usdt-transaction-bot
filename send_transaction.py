import requests
import random
from datetime import datetime
import pytz
import time

# Конфигурация API и токенов
ETHERSCAN_API_KEY = '3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI'  # Etherscan API Key для ERC20
TRONGRID_API_KEY = '175a5b7f-e2c2-4a3a-9bd9-bf2041feb02c'  # TronGrid API Key для TRC20
TELEGRAM_BOT_TOKEN = '6482784614:AAEgqlW2JhisaGyo26WYVytrgl-8F-Nwlmk'  # Telegram Bot Token
TELEGRAM_CHAT_ID = '-1002133823734'  # Telegram Chat ID

# Контракты
ERC20_CONTRACT_ADDRESS = "0xdac17f958d2ee523a2206206994597c13d831ec7"  # USDT ERC20 контракт
TRC20_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT TRC20 контракт

# Список имен
NAMES = ["Invoice", "Alex0z", "CPA-Master", "0x27ox", "Hawk", "Mark", "Rick Owens"]

def get_random_transaction(api_key, contract_address, network):
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
        url = "https://api.trongrid.io/v1/accounts/{}/transactions".format(contract_address)
        params = {
            "only_to": True,
            "limit": 100
        }
    else:
        print("Неподдерживаемая сеть.")
        return None

    try:
        print(f"Получение транзакций из {network}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        transactions = response.json().get('result', [])
        print(f"Получено {len(transactions)} транзакций.")

        if network == "ERC20":
            filtered_transactions = [tx for tx in transactions if 300 <= float(tx['value']) / 10**6 <= 1400]
            if filtered_transactions:
                return random.choice(filtered_transactions)
            else:
                print("Нет подходящих транзакций в ERC20.")
                return None

        elif network == "TRC20":
            if transactions:
                # Фильтруем транзакции по значениям
                filtered_transactions = [tx for tx in transactions if 300 <= float(tx['amount']) / 10**6 <= 1400]
                if filtered_transactions:
                    return random.choice(filtered_transactions)
                else:
                    print("Нет подходящих транзакций в TRC20.")
                    return None
        else:
            print("Ошибка при получении транзакций.")
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
        print(f"Ответ от Telegram: {response.status_code}")
        print(f"Ответ: {response.json()}")
        return response
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return None

def round_down(amount):
    return int(amount)

def format_amount(amount):
    return f"{amount:.2f}"

def main():
    print("Запуск скрипта...")
    
    networks = ["ERC20", "TRC20"]
    network = random.choice(networks)
    contract_address = ERC20_CONTRACT_ADDRESS if network == "ERC20" else TRC20_CONTRACT_ADDRESS
    
    transaction = get_random_transaction(ETHERSCAN_API_KEY, contract_address, network)

    if transaction:
        amount = float(transaction['value']) / 10**6 if network == "ERC20" else float(transaction['amount']) / 10**6
        tx_hash = transaction['hash']
        timestamp = int(transaction['timestamp']) if network == "TRC20" else int(transaction['timeStamp'])

        # Обработка времени и даты
        europe_zone = pytz.timezone('Europe/Berlin')
        date_time = datetime.fromtimestamp(timestamp, europe_zone).strftime('%H:%M:%S %d-%m-%Y')

        # Выбор имени и расчёт доли воркера
        profit_name = random.choice(NAMES)
        amount = round_down(amount)
        worker_share = round_down(amount / 2)

        # Формирование сообщения
        message = (
            f"🥑 Профит у: {profit_name}\n"
            f"┠ Сумма заноса: <b>{format_amount(amount)} USDT</b> <i>{network}</i>\n"
            f"┖ Доля воркера: <b>{format_amount(worker_share)} USDT</b> <i>{network}</i>\n\n"
            f"🧬 Hash: <code>{tx_hash}</code>\n"
            f"🕔 Время: {date_time}"
        )

        response = send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        if response and response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Не удалось отправить сообщение.")
    else:
        print("Не удалось получить транзакцию.")

    delay = random.randint(3600, 7200)  # Интервал от 1 до 2 часов
    print(f"Ожидание {delay} секунд...")
    time.sleep(delay)

if __name__ == "__main__":
    main()
