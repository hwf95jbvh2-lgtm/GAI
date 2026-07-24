import time
import traceback

from config import CHECK_INTERVAL
from check import monitor, send_message

def main():

    send_message(
        "🟢 На месте.\n\n"
        "Начинаю наблюдение.\n"
        "Если PDF зашевелятся, я сообщу."
    )

    while True:

        try:

            monitor()

        except Exception:

            error = traceback.format_exc()

            send_message(
                "❌ Что-то пошло не так.\n\n"
                f"{error}"
            )

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
