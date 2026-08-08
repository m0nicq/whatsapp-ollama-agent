# WhatsApp AI Assistant
## Description
A WhatsApp bot that responds using Ollama's LLM AI. It listens for incoming messages via WAHA and sends them to Ollama to generate a response.

## Getting Started
### Installing
```
git clone https://github.com/m0nicq/whatsapp-ollama-agent
ollama pull qwen2.5:3b
ollama run qwen2.5:3b
docker compose -f waha/docker-compose.yaml up
pip3 install -r requirements.txt
python3 app.py
After running python3 app.py, scan the QR code.
```
