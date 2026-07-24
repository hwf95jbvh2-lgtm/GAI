# ==========================
# config.py
# ==========================

BOT_TOKEN = "8870192962:AAFAh2V8pyVAI65EEWz5JEuKbdH37IrzLlI"

CHAT_ID = "448539895"

# Страница ГИБДД
PAGE_URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"

# Интервал проверки (10 минут)
CHECK_INTERVAL = 600

# Ежедневный отчет
DAILY_REPORT_HOUR = 9
DAILY_REPORT_MINUTE = 0

REQUEST_TIMEOUT = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

STATE_FILE = "files.json"
