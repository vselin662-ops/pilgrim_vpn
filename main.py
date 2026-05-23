from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

# Создаем приложение (нашего робота)
app = FastAPI()

# Это главная страница. Если зайти на нее, она скажет, что всё работает
@app.get("/")
def home():
    return {"сообщение": "Ура! Наш VPN робот успешно запущен!"}

# Это секретная команда. Она будет создавать настройки для подключения к VPN
@app.post("/get-vpn")
def get_vpn_config():
    # Робот генерирует текст настроек (конфиг)
    config_text = """[Interface]
PrivateKey = пример_секретного_ключа_12345
Address = 10.7.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = пример_ключа_сервера_67890
Endpoint = 127.0.0.1:51820
AllowedIPs = 0.0.0.0/0"""
    
    return PlainTextResponse(config_text)
