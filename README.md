# CryptoLab: Evolusi Kriptografi dari Klasik ke Modern

UAS Kriptografi · Nashwa Harvani Rubiantono · A11.2024.15544 · Teknik Informatika, UDINUS

Aplikasi Streamlit yang menggabungkan algoritma dari Pertemuan 2 sampai 6, ditambah notebook
`laporan.ipynb` berisi teori, rumus, gambar, dan pengujian.

## Cara menjalankan di VS Code

1. Ekstrak zip, lalu buka folder `cryptolab` di VS Code (File > Open Folder).
2. Buka terminal VS Code (Ctrl + `) dan buat lingkungan virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi:

   ```bash
   streamlit run app.py
   ```

   Browser terbuka otomatis di `http://localhost:8501`.

## Cara membuka notebook

1. Buka `laporan.ipynb` di VS Code.
2. Klik **Select Kernel** di kanan atas, lalu pilih Python dari `.venv`.
3. Pilih **Run All**. Rumus dan gambar tampil otomatis. Hasil pengujian sudah tersimpan, jadi notebook
   juga bisa langsung dibaca tanpa dijalankan ulang.

## Isi aplikasi

| Menu | Isi | Pertemuan |
|---|---|---|
| Cipher klasik | Vigenère, Beaufort, Auto-key, Playfair, lengkap dengan langkah perhitungan | 2 |
| XOR, avalanche, PRNG | Cipher XOR, avalanche pada SHA-256, LCG vs CSPRNG | 4, 5 |
| Stream cipher RC4 | RC4 dan demo bahaya two-time pad | 5 |
| AES dan mode operasi | ECB, CBC, CTR, GCM, KDF, padding, demo gambar, uji manipulasi | 5, 6 |

## Saran urutan demo (sekitar 7 menit)

1. **Cipher klasik:** enkripsi `KRIPTOGRAFI` dengan kunci `KUNCI` (hasil `ULVRBYAECNS`), lalu buka tabel langkahnya.
2. **Playfair:** tunjukkan bujursangkar 5×5 dan hasil yang sama dengan contoh di slide.
3. **Avalanche:** geser slider bit, lihat sekitar 50% bit hash ikut berubah.
4. **RC4:** tunjukkan test vector, lalu demo two-time pad (dua hasil XOR identik).
5. **AES, demo gambar:** ECB masih menampakkan gembok, CBC tampak acak. Ini momen paling berkesan.
6. **AES, uji manipulasi:** CBC lolos tanpa peringatan (1.000.000 menjadi 0.000.000), GCM menolak data.

## Struktur berkas

```
cryptolab/
├── app.py              antarmuka Streamlit
├── modules/            fungsi kriptografi (dipakai bersama oleh app dan notebook)
│   ├── klasik.py
│   ├── modern.py
│   ├── rc4.py
│   └── aes_mode.py
├── images/             diagram dan hasil demo
├── laporan.ipynb       teori, rumus, gambar, pengujian
├── requirements.txt
└── .streamlit/config.toml
```

## Masalah umum

- **`ModuleNotFoundError: No module named 'Crypto'`**: jalankan `pip install pycryptodome`.
- **Error aneh pada `Crypto.Cipher`**: paket lama bernama `crypto` mungkin terpasang.
  Jalankan `pip uninstall crypto pycrypto`, lalu `pip install pycryptodome`.
- **`streamlit` tidak dikenali**: aktifkan `.venv` terlebih dahulu, atau jalankan `python -m streamlit run app.py`.
- **Notebook tidak menemukan `modules`**: pastikan folder yang dibuka di VS Code adalah folder `cryptolab`
  (tempat `laporan.ipynb` berada).
