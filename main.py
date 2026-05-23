import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

# Инициализируем нашего робота-сервера
app = FastAPI(title="Pilgrim Cloud VPN API")

# База данных в оперативной памяти (для проверки работоспособности)
USERS_DB = {}

@app.get("/")
def home():
    """Главная страница проверки. Подтверждает, что код запустился в облаке."""
    return {
        "status": "online",
        "message": "VPN API успешно работает на Zeabur!",
        "author": "vselin662-ops"
    }

@app.post("/client/add", response_class=PlainTextResponse)
def add_client(username: str):
    """
    Генерирует готовые настройки VPN-подключения (конфиг) для клиента.
    Принимает имя пользователя латиницей, например: user1
    """
    if not username.isalnum():
        raise HTTPException(
            status_code=400, 
            detail="Имя пользователя должно содержать только латинские буквы и цифры!"
        )
    
    # Генерация случайных уникальных ключей шифрования
    client_private_key = f"ClientPrivKey_{uuid.uuid4().hex[:12]}="
    server_public_key = "ServerPublicKeyExample1234567890AmneziaWG="
    
    # Сборка финального текстового файла конфигурации под протокол AmneziaWG / WireGuard
    config_text = f"""[Interface]
PrivateKey = {client_private_key}
Address = 10.7.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = {server_public_key}
Endpoint = YOUR_SERVER_IP:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20
"""
    # Сохраняем пользователя в локальную память API
    USERS_DB[username] = config_text
    
    # Отдаем чистый текст настроек
    return config_text

# Автоматический подбор портов для бесплатных облачных платформ (Zeabur / Render / Docker)
if __name__ == "__main__":
    import uvicorn
    # Облако само передает номер порта через системную переменную PORT, если её нет — ставим 8080
    port_to_run = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port_to_run)
