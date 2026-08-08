from flask import Flask, request
import requests
import re

app = Flask(__name__)

def start_session():
    requests.post(url='http://localhost:8000/api/sessions', headers={'accept': 'application/json', 'X-Api-Key': 'yoursecretkey', 'Content-Type': 'application/json'}, json={'name': 'default'})
    requests.post(url='http://localhost:8000/api/sessions/default/start', headers={'accept': 'application/json', 'X-Api-Key': 'yoursecretkey'})

def send_message(chat_id, text):
    """
    Send message to chat_id.
    :param chat_id: Phone number + "@c.us" suffix - 1231231231@c.us
    :param text: Message for the recipient
    """
    # Send a text back via WhatsApp HTTP API
    response = requests.post(
        "http://localhost:8000/api/sendText",
        json={
            "chatId": chat_id,
            "text": text,
            "session": "default",
        },
        headers={
            'X-Api-Key': 'yoursecretkey',
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
    )
    return response.status_code

def send_prompt_ollama(prompt):
    json_data = {
            'model': 'qwen2.5:1.5b',
            'prompt': prompt,
            'system': 'Ты ИИ которая отвечает с юмором в два - три предложения используя эмодзи в ответе.',
            'stream': False
    }
    response = requests.post(url='http://localhost:11434/api/generate', json=json_data) 
    json_response = response.json()
    return json_response['response']

@app.route('/whatsapp', methods=['POST'])
def receive_prompt():
    response = request.get_json()
    body = response['payload']['body']
    chat = response['payload']['from']
    if 'Арман' or 'арман' in body:
        print('"Arman" Detected!')
        body = re.sub(r'[Аа]рман', '', body)
        response = send_prompt_ollama(body)
        status = send_message(chat, response)
        return '', 200
    print('"Arman" Not Detected!')
    return '', 200

if __name__ == '__main__':
    start_session()
    app.run(host='0.0.0.0', port=5000, debug=True)
