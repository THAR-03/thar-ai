#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== Instalasi Termux AI Coder ==="

pkg update -y
pkg install -y python git

pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
  echo "Membuat file .env kosong, isi OPENAI_API_KEY di dalamnya."
  echo 'OPENAI_API_KEY=""' > .env
  echo 'OPENAI_MODEL="gpt-4o"' >> .env
fi

chmod +x agent.py

echo ""
echo "Instalasi selesai."
echo "1. Edit file .env, isi OPENAI_API_KEY kamu."
echo "2. Jalankan dengan: python agent.py"
