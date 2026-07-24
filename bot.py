import time
import traceback

from config import CHECK_INTERVAL
from check import monitor, send_message


HEARTBEAT_INTERVAL = 60


def main():

    send_message(
        "🟢 На месте.\n\n"
        "Начинаю наблюдение.\n"
        "Если PDF зашевелятся, я сообщу."
    )

    last_heartbeat = 0

    while True:

        try:

            monitor()

            if time.time() - last.heartbeat >= HEARTBEAT_INTERVAL:

            
                send_message(
                    "💚 Всё спокойно.\n\n"
                    "Я на посту и продолжаю следить за файлами."
                )

                last_heartbeat = time_time ()


        except Exception:

            error = traceback.format_exc()

            send_message(
                "❌ Что-то пошло не так.\n\n"
                f"{error}"
            )


        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
