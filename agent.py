#!/usr/bin/env python3
"""
Termux AI Coder — asisten coding CLI sederhana berbasis OpenAI API.

Perintah dalam chat:
  /read <path>          -> masukkan isi file ke konteks obrolan
  /write <path>         -> simpan code block terakhir dari AI ke file (minta konfirmasi)
  /run <perintah shell> -> jalankan perintah shell (minta konfirmasi)
  /clear                -> reset riwayat obrolan
  /exit                 -> keluar
"""

import os
import re
import sys
import subprocess
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Paket 'openai' belum terpasang. Jalankan: pip install -r requirements.txt")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")

if not API_KEY:
    print("OPENAI_API_KEY belum diset. Isi file .env atau export manual:")
    print('  export OPENAI_API_KEY="sk-..."')
    sys.exit(1)

client = OpenAI(api_key=API_KEY)

SYSTEM_PROMPT = (
    "Kamu adalah asisten AI untuk membantu coding di terminal (Termux/Android). "
    "Jawab ringkas, berikan kode dalam code block markdown. "
    "Ikuti kebijakan penggunaan OpenAI yang berlaku; jangan membantu aktivitas ilegal atau berbahaya."
)

history = [{"role": "system", "content": SYSTEM_PROMPT}]
last_code_block = None


def extract_last_code_block(text: str):
    blocks = re.findall(r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```", text, re.DOTALL)
    return blocks[-1] if blocks else None


def cmd_read(path: str):
    p = Path(path).expanduser()
    if not p.is_file():
        print(f"File tidak ditemukan: {path}")
        return
    content = p.read_text(errors="replace")
    history.append({
        "role": "user",
        "content": f"Isi file {path}:\n```\n{content}\n```"
    })
    print(f"[ok] Isi {path} ditambahkan ke konteks obrolan.")


def cmd_write(path: str):
    global last_code_block
    if not last_code_block:
        print("Tidak ada code block dari AI untuk disimpan. Minta AI generate kode dulu.")
        return
    p = Path(path).expanduser()
    print(f"Akan menulis {len(last_code_block)} karakter ke {p}")
    confirm = input("Lanjutkan? (y/N): ").strip().lower()
    if confirm != "y":
        print("Dibatalkan.")
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(last_code_block)
    print(f"[ok] Tersimpan ke {path}")


def cmd_run(shell_cmd: str):
    print(f"Perintah: {shell_cmd}")
    confirm = input("Jalankan perintah ini? (y/N): ").strip().lower()
    if confirm != "y":
        print("Dibatalkan.")
        return
    result = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("[stderr]", result.stderr)


def chat(user_input: str):
    global last_code_block
    history.append({"role": "user", "content": user_input})
    resp = client.chat.completions.create(
        model=MODEL,
        messages=history,
    )
    reply = resp.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    code = extract_last_code_block(reply)
    if code:
        last_code_block = code
    print(f"\n{reply}\n")


def main():
    print("=== Termux AI Coder ===")
    print(f"Model: {MODEL}")
    print("Ketik pesan biasa untuk chat, atau /read /write /run /clear /exit\n")

    while True:
        try:
            line = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar.")
            break

        if not line:
            continue
        if line == "/exit":
            break
        if line == "/clear":
            history[:] = history[:1]
            print("[ok] Riwayat obrolan direset.")
            continue
        if line.startswith("/read "):
            cmd_read(line[len("/read "):].strip())
            continue
        if line.startswith("/write "):
            cmd_write(line[len("/write "):].strip())
            continue
        if line.startswith("/run "):
            cmd_run(line[len("/run "):].strip())
            continue

        chat(line)


if __name__ == "__main__":
    main()
