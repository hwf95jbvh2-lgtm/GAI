# ==========================
# check.py
# ==========================

import os
import json
import time
import hashlib
import requests
from datetime import datetime

from bs4 import BeautifulSoup

from config import (
    BOT_TOKEN,
    CHAT_ID,
    PAGE_URL,
    REQUEST_TIMEOUT,
    HEADERS,
    STATE_FILE
)

BASE_URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai"

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
        print("Telegram error:", e, flush=True)

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

    except Exception:
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

    last_error = None

    for attempt in range(3):

        try:

            response = requests.get(
                PAGE_URL,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            return response.text

        except Exception as e:

            last_error = e

            print(
                f"Попытка {attempt + 1}/3 не удалась",
                e,
                flush=True
            )

            time.sleep(5)

    raise last_error

def get_files_from_page():

    html = get_page()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    files = {}

    title = soup.find(
        string=lambda x:
        x and "Файлы для скачивания" in x
    )

    if not title:
        return files

    block = title.find_parent(
        class_="b-service-bank"
    )

    if not block:
        return files

    for link in block.find_all("a"):

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

    return files

def download_file(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    return response.content

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
            "url": info["url"],
            "description": info["description"],
            "hash": file_hash
        }

        if name not in old_state:

            changes.append(
                f"🆕 Новый файл:\n{name}"
            )

        else:

            if old_state[name]["hash"] != file_hash:

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

    return changes

def monitor()
:print(
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
        )
