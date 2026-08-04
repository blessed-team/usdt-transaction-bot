import requests
import random
from datetime import datetime
import pytz
import time


ETHERSCAN_API_KEY = "3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI"

TELEGRAM_BOT_TOKEN = "8897185110:AAGZy5xqvOYe4QBslIGJLFezTU_VwZtwbiY"
TELEGRAM_CHAT_ID = "-1004439708770"


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


def round_up(value, multiple):
    return multiple * (value // multiple)



def get_random_erc20_transaction(api_key, min_value, max_value):

    usdt_contract = "0xdac17f958d2ee523a2206206994597c13d831ec7"

    url = "https://api.etherscan.io/v2/api"


    params = {
        "chainid": 1,
        "module": "account",
        "action": "tokentx",
        "contractaddress": usdt_contract,
        "page": 1,
        "offset": 100,
        "sort": "desc",
        "apikey": api_key
    }


    try:

        print("Запрос транзакций Etherscan V2...")


        response = requests.get(
            url,
            params=params,
            timeout=30
        )


        data = response.json()


        print(data)


        if not isinstance(data.get("result"), list):

            print("Ошибка API")
            return None



        filtered = []


        for tx in data["result"]:

            try:

                amount = float(tx["value"]) / 10**6


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
            "Ошибка Etherscan:",
            e
        )

        return None




def send_message(token, chat_id, message):

    url = f"https://api.telegram.org/bot{token}/sendMessage"


    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }


    try:

        print("Отправка сообщения Telegram...")


        response = requests.post(
            url,
            data=data,
            timeout=30
        )


        print(response.json())


        return response



    except Exception as e:

        print(
            "Ошибка Telegram:",
            e
        )

        return None




def main():

    print("Запуск скрипта...")


    min_value = 300
    max_value = 1100


    network = "ERC20"


    print(
        f"Выбрана сеть: {network}"
    )


    transaction = get_random_erc20_transaction(
        ETHERSCAN_API_KEY,
        min_value,
        max_value
    )


    if not transaction:

        print(
            "Не удалось получить подходящую транзакцию."
        )

        return



    amount = float(transaction["value"]) / 10**6


    tx_hash = transaction["hash"]


    timestamp = int(transaction["timeStamp"])



    zone = pytz.timezone(
        "Europe/Berlin"
    )


    date_time = datetime.fromtimestamp(
        timestamp,
        zone
    ).strftime(
        "%H:%M:%S %d-%m-%Y"
    )



    name = random.choice(NAMES)



    rounded = round_up(
        amount,
        10
    )


    worker = rounded / 2



    message = (
        f"💲 Профит у: <b>{name}</b>\n"
        f"┠ Сумма заноса: <b>{rounded:.2f}</b> USDT <i>({network})</i>\n"
        f"┖ Доля воркера: <b>{worker:.2f}</b> USDT <i>({network})</i>\n\n"
        f"🧬 Hash:\n<code>{tx_hash}</code>\n\n"
        f"🕔 Время: {date_time}"
    )



    delay = random.randint(
        60,
        900
    )


    print(
        f"Ожидание {delay} секунд..."
    )


    time.sleep(delay)



    response = send_message(
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_CHAT_ID,
        message
    )



    if response and response.status_code == 200:

        print(
            "Сообщение отправлено"
        )

    else:

        print(
            "Ошибка отправки"
        )



if __name__ == "__main__":

    main()
