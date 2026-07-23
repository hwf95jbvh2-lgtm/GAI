# ==========================
# bot.py
# ==========================

import time
import traceback
from datetime import datetime

from check import monitor, send_message
from config import CHECK_INTERVAL

def main():

    send_message(
        "🚀 Бот мониторинга файлов ГИБДД запущен.\n"
        "✅ Система работает."
    )

    last_report = None

    while True:

        try:

            monitor()

            now = datetime.now()

            # ежедневный отчет примерно раз в сутки
            if now.hour == 9 and last_report != now.date():

                send_message(
                    "✅ Все работает.\n\n"
                    "Бот продолжает мониторинг файлов ГИБДД."
                )

                last_report = now.date()

        except Exception:

            error = traceback.format_exc()

            send_message(
                "❌ Ошибка в работе системы:\n\n"
                + error[:3000]
            )

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
