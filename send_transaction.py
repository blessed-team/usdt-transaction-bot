import requests,random,time,pytz
from datetime import datetime

ETHERSCAN="3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI"
BSCSCAN="3JTRMXERPSTG1AY9AV1ZYD1WGRHZNEU3VI"
TRONSCAN="1dad2f3d-d4e9-4be5-a7eb-51bedf58edfe"

TG_TOKEN="8897185110:AAGZy5xqvOYe4QBslIGJLFezTU_VwZtwbiY"
TG_CHAT="-1004439708770"

NAMES=["Invoice","Alex0z","CPA-Master","0x27ox","Hawk","Mark","Rick Owens","T1m 24/7","Blessed","DIOR-h8ter","DB-legacy"]

MIN=300
MAX=1100


def rnd(x):
    return 10*(x//10)


def eth():
    try:
        p={"module":"account","action":"tokentx","contractaddress":"0xdac17f958d2ee523a2206206994597c13d831ec7","page":1,"offset":100,"sort":"desc","apikey":ETHERSCAN}
        d=requests.get("https://api.etherscan.io/api",params=p).json()
        if not isinstance(d.get("result"),list):return None
        for t in d["result"]:
            a=float(t["value"])/1e6
            if MIN<=a<=MAX:return {"n":"ERC20","a":a,"h":t["hash"],"t":int(t["timeStamp"])}
    except Exception as e:print("ETH",e)


def bsc():
    try:
        p={"module":"account","action":"tokentx","contractaddress":"0x55d398326f99059ff775485246999027b3197955","page":1,"offset":100,"sort":"desc","apikey":BSCSCAN}
        d=requests.get("https://api.bscscan.com/api",params=p).json()
        if not isinstance(d.get("result"),list):return None
        for t in d["result"]:
            a=float(t["value"])/1e18
            if MIN<=a<=MAX:return {"n":"BEP20","a":a,"h":t["hash"],"t":int(t["timeStamp"])}
    except Exception as e:print("BSC",e)


def tron():
    try:
        h={"TRON-PRO-API-KEY":TRONSCAN}
        p={"limit":200,"start":0}
        d=requests.get("https://apilist.tronscanapi.com/api/token_trc20/transfers",headers=h,params=p).json()

        for t in d.get("token_transfers",[]):
            if t.get("tokenInfo",{}).get("tokenAbbr")!="USDT":continue
            a=float(t["quant"])/1e6
            if MIN<=a<=MAX:
                return {"n":"TRC20","a":a,"h":t["transaction_id"],"t":int(t["block_ts"])/1000}

    except Exception as e:print("TRON",e)



def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            data={"chat_id":TG_CHAT,"text":msg,"parse_mode":"HTML"}
        )
    except Exception as e:print("TG",e)



def main():

    print("Запуск")

    tx=None

    for f in [eth,bsc,tron]:
        tx=f()
        if tx:break

    if not tx:
        print("Нет транзакций")
        return


    amount=rnd(tx["a"])

    worker=amount/2

    dt=datetime.fromtimestamp(
        tx["t"],
        pytz.timezone("Europe/Berlin")
    ).strftime("%H:%M:%S %d-%m-%Y")


    msg=(
        f"💲 Профит у: <b>{random.choice(NAMES)}</b>\n"
        f"┠ Сумма заноса: <b>{amount:.2f}</b> USDT <i>({tx['n']})</i>\n"
        f"┖ Доля воркера: <b>{worker:.2f}</b> USDT <i>({tx['n']})</i>\n\n"
        f"🧬 Hash:\n<code>{tx['h']}</code>\n\n"
        f"🕔 Время: {dt}"
    )


    print(msg)

    time.sleep(random.randint(60,900))

    send(msg)



if __name__=="__main__":
    main()
