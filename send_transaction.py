import requests
import random
from datetime import datetime
import pytz
import time

# Настройки API
ETHERSCAN_API_KEY = "3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI"


TELEGRAM_BOT_TOKEN = "8897185110:AAGZy5xqvOYe4QBslIGJLFezTU_VwZtwbiY"
TELEGRAM_CHAT_ID = "-1004439708770"

# Список имен
NAMES = [
    "Invoice",
    "Alex0z",
    "CPA-Master",
    "0x27ox",
    "Hawk",
    "Mark",
    "Rick Owens",
    "T1m 24/7",
    "Blessed",
    "DIOR-h8ter",
    "DB-legacy"
]


def round_up(value: float, multiple: float) -> float:
    return multiple * (value // multiple)


def get_random_erc20_transaction(api_key, min_value, max_value):

    usdt_contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"

    url = "https://api.etherscan.io/v2/api"

    params = {
        "chainid": 1,
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

        print("Запрос транзакций к Etherscan V2...")

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        data = response.json()

        print(data)


        if not isinstance(data.get("result"), list):
            print("Ошибка API:")
            return None


        filtered=[]


        for tx in data["result"]:

            try:

                amount=float(tx["value"])/10**6

                if min_value <= amount <= max_value:
                    filtered.append(tx)

            except:
                continue


        print(
            "Подходящих транзакций:",
            len(filtered)
        )


        if filtered:
            return random.choice(filtered)


        return None


    except Exception as e:

        print(
            "Etherscan error:",
            e
        )

        return None


def send_message(token, chat_id, message):
    """Отправка сообщения в Telegram."""

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        print("Отправка сообщения в Telegram...")

        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()

        print(f"Статус Telegram: {response.status_code}")
        print(response.json())

        return response

    except Exception as e:
        print(f"Ошибка Telegram: {e}")
        return None


network_choice = "ERC20"

print(f"Выбранная сеть: {network_choice}")

transaction = get_random_erc20_transaction(
    ETHERSCAN_API_KEY,
    min_value,
    max_value
)

unit = 10**6

    if not transaction:
        print("Не удалось получить подходящую транзакцию.")
        return

    amount_usdt = float(transaction["value"]) / unit
    tx_hash = transaction["hash"]
    timestamp = int(transaction["timeStamp"])

    europe_zone = pytz.timezone("Europe/Berlin")

    date_time = datetime.fromtimestamp(
        timestamp,
        europe_zone
    ).strftime("%H:%M:%S %d-%m-%Y")

    profit_name = random.choice(NAMES)

    rounded_amount = round_up(amount_usdt, 10)
    worker_share = rounded_amount / 2

    message = (
        f"💲 Профит у: <b>{profit_name}</b>\n"
        f"┠ Сумма заноса: <b>{rounded_amount:.2f}</b> USDT <i>({network_choice})</i>\n"
        f"┖ Доля воркера: <b>{worker_share:.2f}</b> USDT <i>({network_choice})</i>\n\n"
        f"🧬 Hash: <code>{tx_hash}</code>\n"
        f"🕔 Время: {date_time}"
    )

    delay = random.randint(60, 900)

    print(f"Ожидание {delay} секунд...")

    time.sleep(delay)

    response = send_message(
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_CHAT_ID,
        message
    )

    if response and response.status_code == 200:
        print("Сообщение успешно отправлено.")
    else:
        print("Не удалось отправить сообщение.")


if __name__ == "__main__":
    main()
