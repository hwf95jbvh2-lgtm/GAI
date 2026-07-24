# ==========================
# check.py
# ==========================

import os
import json
import time
import hashlib
import requests

from bs4 import BeautifulSoup

from config import (
    BOT_TOKEN,
    CHAT_ID,
    PAGE_URL,
    STATE_FILE
)

BASE_URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai"

TIMEOUT = 90

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

        return {}

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as e:

        print(
            "Ошибка чтения files.json:",
            e,
            flush=True
        )

        return {}

def save_state(data):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

def get_hash(content):

    return hashlib.sha256(content).hexdigest()

def get_page():

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
        timeout=TIMEOUT
    )

    response.raise_for_status()

    print(
        "Страница получена",
        flush=True
    )

    return response.text

def get_files_from_page():

    html = get_page()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    files = {}

    print(
        "Ищу PDF...",
        flush=True
    )

    for link in soup.find_all("a"):

        href = link.get("href")

        if not href:

            continue

        if ".pdf" not in href.lower():

            continue

        if href.startswith("/"):

            url = BASE_URL + href

        else:

            url = href

        name = href.split("/")[-1]

        description = link.text.strip()

        files[name] = {

            "url": url,

            "description": description

        }

    print(
        "Найдены файлы:",
        files,
        flush=True
    )

    return files

def download_file(url):

    print(
        "Скачивание:",
        url,
        flush=True
    )

    for attempt in range(1, 4):

        try:

            response = requests.get(

                url,

                headers={

                    "User-Agent":
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "Chrome/120 Safari/537.36"

                },

                timeout=TIMEOUT

            )

            response.raise_for_status()

            print(

                "Скачан размер:",

                len(response.content),

                "байт",

                flush=True

            )

            return response.content

        except Exception as e:

            print(

                f"Ошибка скачивания {attempt}/3:",

                e,

                flush=True

            )

            time.sleep(10)

    raise Exception(

        "Не удалось скачать файл: "

        + url

    )

def check_files():

    old_state = load_state()

    current_state = {}

    changes = []

    files = get_files_from_page()

    for name, info in files.items():

        content = download_file(

            info["url"]

        )

        file_hash = get_hash(

            content

        )

        current_state[name] = {

            "url":

            info["url"],

            "description":

            info["description"],

            "hash":

            file_hash

        }

        if name not in old_state:

            changes.append(

                f"🆕 Новый файл:\n{name
                                  "

            )

        else:

            if old_state[name].get("hash") != file_hash:

                changes.append(

                    f"📄 Изменен файл:\n{name}"

                )

            if old_state[name].get("description") != info["description"]:

                changes.append(

                    f"📝 Изменено описание:\n{name}\n\n"
                    f"Новое:\n{info['description']}"

                )

    for old_name in old_state:

        if old_name not in current_state:

            changes.append(

                f"❌ Файл удален:\n{old_name}"

            )

    save_state(

        current_state

    )

    print(

        "files.json сохранен",

        flush=True

    )

    return changes

def monitor():

    print(

        "Проверка файлов...",

        flush=True

    )

    changes = check_files()

    if changes:

        send_message(

            "⚠️ Изменения на сайте:\n\n"

            +

            "\n\n".join(changes)

        )

    else:

        print(

            "Изменений нет",

            flush=True

        )}
