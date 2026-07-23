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

def send_message(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=REQUEST_TIMEOUT
        )

    except Exception as e:
        print("Ошибка Telegram:", e, flush=True)

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

def get_files_from_page():

    response = requests.get(
        PAGE_URL,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    files = {}

    for link in soup.find_all("a"):

        url = link.get("href")

        if not url:
            continue

        if ".pdf" not in url.lower():
            continue

        if url.startswith("/"):
            url = (
                "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai"
                + url
            )

        name = url.split("/")[-1]

        files[name] = url

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

    for name, url in files.items():

        content = download_file(url)

        file_hash = get_hash(content)

        current_state[name] = {
            "url": url,
            "hash": file_hash,
            "time": datetime.now().isoformat()
        }

        if name not in old_state:

            changes.append(
                f"🆕 Новый файл:\n{name}"
            )

        elif old_state[name]["hash"] != file_hash:

            changes.append(
                f"📄 Изменен файл:\n{name}"
            )

    for old_name in old_state:

        if old_name not in current_state:

            changes.append(
                f"❌ Файл удален:\n{old_name}"
            )

    save_state(current_state)

    return changes

def monitor():

    print(
        "Проверка файлов...",
        flush=True
    )

    changes = check_files()

    if changes:

        message = (
            "⚠️ Изменения на сайте:\n\n"
            +
            "\n\n".join(changes)
        )

        send_message(message)

    else:

        print(
            "Изменений нет",
            flush=True
        )
