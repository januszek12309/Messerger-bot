import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

app = Flask(__name__)
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

# Weryfikacja webhooka
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args['hub.challenge'], 200
    return 'Verification failed', 403

# Odbieranie wiadomości
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'entry' in data:
        for entry in data['entry']:
            messaging = entry.get('messaging', [])
            for message in messaging:
                sender_id = message['sender']['id']
                message_text = message['message']['text']
                send_message(sender_id, "You said: " + message_text)
    return 'OK', 200

# Funkcja do wysyłania wiadomości
def send_message(recipient_id, message_text):
    url = f'https://graph.facebook.com/v11.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    response = requests.post(url, json={
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    })
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

if __name__ == '__main__':
    app.run(port=5000)
