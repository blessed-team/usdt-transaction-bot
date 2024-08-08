import requests

def send_test_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Статус ответа от Telegram: {response.status_code}")
        print(f"Ответ от Telegram: {response.json()}")
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")

# Замените эти значения на ваши реальные
bot_token = 'YOUR_BOT_TOKEN'
channel_id = '-1002133823734'  # ID вашего канала
message = 'Hello World'

send_test_message(bot_token, channel_id, message)
