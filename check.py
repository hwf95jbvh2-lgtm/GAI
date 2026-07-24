import os
import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import unquote

from config import (
    BOT_TOKEN,
    CHAT_ID,
    PAGE_URL,
    STATE_FILE
)

def send_message(text):

    try:

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=30
        )

    except Exception as e:

        print(
            "Ошибка Telegram:",
            e,
            flush=True
        )

def load_state():

    if not os.path.exists(STATE_FILE):
        return []

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            return data.get(
                "files",
                []
            )

    except Exception as e:

        print(
            "Ошибка чтения files.json:",
            e,
            flush=True
        )

        return []

def save_state(files):

    try:

        with open(
            STATE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "files": files
                },
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception as e:

        print(
            "Ошибка сохранения files.json:",
            e,
            flush=True
        )

def get_files_from_page():

    print(
        "Открываю страницу...",
        flush=True
    )

    response = requests.get(
        PAGE_URL,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        },
        timeout=60
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    files = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if href and ".pdf" in href.lower():

            name = href.split("/")[-1]

            name = unquote(name)

            files.append(name)

    files = sorted(files)

    print(
        "Найдены файлы:",
        files,
        flush=True
    )

    return files

def check_files():

    old_files = load_state()

    new_files = get_files_from_page()

    changed = (
        set(old_files)
        !=
        set(new_files)
    )

    save_state(
        new_files
    )

    return changed

def monitor():

    print(
        "Проверка файлов...",
        flush=True
    )

    changed = check_files()

    if changed:

        send_message(
            "🚨 Попался!\n\n"
            "На сайте что-то изменилось.\n\n"
            "Пора проверить:\n"
            f"{PAGE_URL}"
        )

    else:

        print(
            "Изменений нет",
            flush=True
        )
            flush=True
        )
