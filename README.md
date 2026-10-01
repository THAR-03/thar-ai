# Termux AI Coder

Asisten AI coding CLI sederhana untuk Termux (Android), menggunakan OpenAI API.
Bisa chat, baca file project, tulis/edit file, dan menjalankan perintah shell (dengan konfirmasi).

## 1. Upload ke GitHub kamu sendiri

Di komputer / Termux:

```bash
cd termux-ai-coder
git init
git add .
git commit -m "init: termux ai coder"
git branch -M main
git remote add origin https://github.com/USERNAME/termux-ai-coder.git
git push -u origin main
```

Ganti `USERNAME` dengan username GitHub kamu, dan buat dulu repo kosong bernama
`termux-ai-coder` di github.com.

## 2. Instal di Termux (dari GitHub)

```bash
pkg install -y git
git clone https://github.com/USERNAME/termux-ai-coder.git
cd termux-ai-coder
bash install.sh
```

## 3. Isi API key

Edit file `.env` (dibuat otomatis oleh `install.sh`):

```
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"
OPENAI_MODEL="gpt-4o"
```

Dapatkan API key di https://platform.openai.com/api-keys

## 4. Jalankan

```bash
python agent.py
```

## Perintah dalam chat

| Perintah                | Fungsi                                               |
|-------------------------|-------------------------------------------------------|
| `/read <path>`          | Masukkan isi file ke konteks obrolan                  |
| `/write <path>`         | Simpan code block terakhir dari AI ke file (konfirmasi dulu) |
| `/run <perintah shell>` | Jalankan perintah shell (konfirmasi dulu)             |
| `/clear`                | Reset riwayat obrolan                                 |
| `/exit`                 | Keluar                                                |

## Catatan keamanan

- `/write` dan `/run` selalu minta konfirmasi `y` sebelum eksekusi — jangan hapus
  konfirmasi ini kalau kamu modifikasi scriptnya, supaya tidak ada perintah/file
  yang berubah tanpa sepengetahuanmu.
- Simpan `.env` hanya di perangkat sendiri; jangan commit API key ke GitHub
  (`.gitignore` sudah menangani ini).
- Tool ini memanggil API OpenAI apa adanya, sehingga tetap mengikuti kebijakan
  penggunaan OpenAI (tidak ada mode "tanpa batasan").
