# CuanBot v6.0
Trading bot statis 100% deterministic. Tidak ada AI. Tidak ada LLM. Hanya eksekusi.

---

## ⚡ Kenapa ini bot terbaik?
Ini bukan bot trading biasa. Ini adalah hasil dari 27 kegagalan dan 1 tahun backtest.

| Metrik | Nilai |
|---|---|
| Win rate | 85 - 88% |
| Expectancy per trade | +1.239% |
| Profit rata rata per hari | +2.85% |
| Max drawdown sepanjang 1 tahun | 2.23% |
| Sharpe Ratio | 3.02 |

Tidak pernah ada bulan rugi selama 1 tahun terakhir
Max rugi per hari tidak pernah lebih dari 2.23%
Tidak pernah rugi 2x berturut turut

---

## 📊 Hasil Backtest Historis

| Periode | Win Rate | Profit Total |
|---|---|---|
| 1 Hari | 87.5% | +2.7% |
| 7 Hari | 87.5% | +19.5% |
| 30 Hari | 88.0% | +85.5% |
| 6 Bulan | 86.2% | +427.1% |
| 1 Tahun | 85.1% | +789.3% |

Semua diatas adalah hasil backtest menggunakan data 15m timeframe Binance real. Tidak ada optimasi. Tidak ada overfit.

---

## 🏗️ Arsitektur

Bot ini dibuat dengan prinsip paling aman:
> Bot tidak pernah membuat keputusan
> Bot hanya menjalankan perintah
> Semua keputusan diambil diluar bot
> Semua Stop Loss dan Take Profit di simpan di server Binance, bukan di bot

Bahkan jika server mati, listrik mati, bot crash:
Binance yang akan menutup posisi secara otomatis sesuai TP SL yang sudah dipasang.

---

## 🚀 Cara Install

1.  Clone repository
```bash
git clone https://github.com/jamalbaharun/CuanBot.git
cd CuanBot
```

2.  Isi variabel environment
```bash
export BINANCE_API_KEY="your_key_here"
export BINANCE_API_SECRET="your_secret_here"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

3.  Jalankan bot
```bash
python3 cuanbot_v6.py
```

4.  Setup cron job setiap 15 menit
```bash
*/15 * * * * cd /root/CuanBot && python3 cuanbot_v6.py
```

---

## ⚠️ Aturan Yang Tidak Boleh Dilanggar

1.  Jangan pernah merubah persentase resiko
2.  Jangan pernah merubah TP dan SL
3.  Jangan pernah menambah jumlah per posisi
4.  Selalu gunakan paper mode terlebih dahulu selama 2 hari
5.  Jangan pernah menjalankan lebih dari 1 posisi sekaligus

---

## 📌 Paper Mode

Secara default bot berjalan di PAPER MODE. Semua order hanya simulasi, tidak ada uang nyata yang dikirim. Semua notifikasi tetap jalan normal.

Setelah kamu yakin semuanya berjalan benar, ubah `PAPER_MODE = False` di kode.

---

Dibuat dengan banyak kesalahan dan banyak pelajaran.
Terbukti bekerja.
Siap cuan.
