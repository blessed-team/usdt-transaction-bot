import requests
import random
from datetime import datetime
import pytz
import time


# ==========================
# API KEYS
# ==========================

ETHERSCAN_API_KEY = "3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI"
BSCSCAN_API_KEY = "3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI"
TRONGRID_API_KEY = "74d034f4-09db-47b6-af19-12bc8e0aae1b"

TELEGRAM_BOT_TOKEN = "8897185110:AAGZy5xqvOYe4QBslIGJLFezTU_VwZtwbiY"
TELEGRAM_CHAT_ID = "-1004439708770"


# ==========================
# SETTINGS
# ==========================

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


MIN_VALUE = 300
MAX_VALUE = 1100


# ==========================
# HELPERS
# ==========================

def round_up(value, multiple):
    return multiple * (value // multiple)



# ==========================
# ERC20 ETHEREUM
# ==========================

def get_erc20_transaction():

    url = "https://api.etherscan.io/api"

    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "page": 1,
        "offset": 100,
        "apikey": ETHERSCAN_API_KEY
    }


    try:

        print("ETHEREUM запрос...")

        r = requests.get(url, params=params, timeout=30)

        data = r.json()


        if not isinstance(data.get("result"), list):
            print(data)
            return None


        result = []


        for tx in data["result"]:

            amount = float(tx["value"]) / 10**6

            if MIN_VALUE <= amount <= MAX_VALUE:
                result.append({

                    "network": "ERC20",
                    "amount": amount,
                    "hash": tx["hash"],
                    "time": tx["timeStamp"]

                })


        return random.choice(result) if result else None


    except Exception as e:

        print("ERC20 error:", e)
        return None




# ==========================
# BEP20 BSC
# ==========================

def get_bep20_transaction():

    url = "https://api.bscscan.com/api"


    params = {

        "module": "account",
        "action": "tokentx",
        "contractaddress": "0x55d398326f99059ff775485246999027b3197955",
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "page": 1,
        "offset": 100,
        "apikey": BSCSCAN_API_KEY

    }


    try:

        print("BSC запрос...")


        r = requests.get(url, params=params, timeout=30)

        data = r.json()


        if not isinstance(data.get("result"), list):
            print(data)
            return None


        result = []


        for tx in data["result"]:


            amount = float(tx["value"]) / 10**18


            if MIN_VALUE <= amount <= MAX_VALUE:

                result.append({

                    "network": "BEP20",
                    "amount": amount,
                    "hash": tx["hash"],
                    "time": tx["timeStamp"]

                })


        return random.choice(result) if result else None



    except Exception as e:

        print("BEP20 error:", e)
        return None





# ==========================
# TRC20 TRON
# ==========================

def get_trc20_transaction():


    # последние TRC20 переводы USDT
    url = "https://api.trongrid.io/v1/assets/TRX/transactions"


    headers = {

        "TRON-PRO-API-KEY": TRONGRID_API_KEY

    }


    try:

        print("TRON запрос...")


        # получаем последние транзакции USDT
        url = (
            "https://api.trongrid.io/v1/accounts/"
            "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj/"
            "transactions/trc20"
        )


        r = requests.get(
            url,
            headers=headers,
            timeout=30
        )


        data = r.json()


        if "data" not in data:

            print(data)
            return None



        result = []



        for tx in data["data"]:


            if tx["token_info"]["symbol"] != "USDT":
                continue


            amount = float(tx["value"]) / 10**6



            if MIN_VALUE <= amount <= MAX_VALUE:


                result.append({

                    "network": "TRC20",
                    "amount": amount,
                    "hash": tx["transaction_id"],
                    "time": int(tx["block_timestamp"]) // 1000

                })



        return random.choice(result) if result else None



    except Exception as e:

        print("TRC20 error:", e)

        return None





# ==========================
# TELEGRAM
# ==========================


def send_message(message):


    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    )


    data = {

        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"

    }


    try:

        r = requests.post(
            url,
            data=data,
            timeout=30
        )


        print(r.json())


    except Exception as e:

        print("Telegram error:", e)





# ==========================
# MAIN
# ==========================


def main():


    print("Запуск...")


    network = random.choice(
        [
            "ERC20",
            "BEP20",
            "TRC20"
        ]
    )


    print(
        "Выбрана сеть:",
        network
    )



    if network == "ERC20":

        tx = get_erc20_transaction()


    elif network == "BEP20":

        tx = get_bep20_transaction()


    else:

        tx = get_trc20_transaction()



    if not tx:

        print(
            "Подходящих транзакций нет"
        )

        return



    amount = round_up(
        tx["amount"],
        10
    )


    worker = amount / 2



    zone = pytz.timezone(
        "Europe/Berlin"
    )


    date = datetime.fromtimestamp(
        tx["time"],
        zone
    ).strftime(
        "%H:%M:%S %d-%m-%Y"
    )



    name = random.choice(
        NAMES
    )



    message = (

        f"💲 Профит у: "
        f"<b>{name}</b>\n"

        f"┠ Сумма заноса: "
        f"<b>{amount:.2f}</b> USDT "
        f"<i>({tx['network']})</i>\n"

        f"┖ Доля воркера: "
        f"<b>{worker:.2f}</b> USDT "
        f"<i>({tx['network']})</i>\n\n"

        f"🧬 Hash:\n"
        f"<code>{tx['hash']}</code>\n\n"

        f"🕔 Время: {date}"

    )



    delay = random.randint(
        60,
        900
    )


    print(
        f"Ждем {delay} секунд..."
    )


    time.sleep(delay)



    send_message(
        message
    )



if __name__ == "__main__":

    main()
