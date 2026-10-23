"""CryptoLab: Evolusi Kriptografi dari Klasik ke Modern.

Aplikasi UAS Kriptografi, Teknik Informatika, Universitas Dian Nuswantoro.
Jalankan dengan:  streamlit run app.py
"""
import io

import pandas as pd
import streamlit as st
from Crypto.Random import get_random_bytes
from PIL import Image

from modules import aes_mode as aes
from modules import klasik, modern
from modules import rc4 as rc4m

NAMA = "Nashwa Harvani Rubiantono"
NIM = "A11.2024.15544"

st.set_page_config(page_title="CryptoLab", page_icon="🔐", layout="wide")


# ============================================================ Beranda
def halaman_beranda():
    st.title("CryptoLab")
    st.subheader("Evolusi kriptografi dari klasik ke modern")
    st.write(
        "CryptoLab adalah laboratorium mini untuk mencoba langsung algoritma kriptografi "
        "yang dipelajari di mata kuliah Kriptografi. Setiap modul mengikuti satu pertemuan "
        "kuliah, dan seluruhnya bisa dicoba dengan pesan, kunci, atau gambar milikmu sendiri."
    )

    st.markdown(
        """
| Modul | Isi | Pertemuan |
|---|---|---|
| Cipher klasik | Vigenère, Beaufort, Auto-key, Playfair | 2 |
| XOR dan avalanche | Cipher XOR, avalanche effect pada SHA-256, PRNG vs CSPRNG | 4 dan 5 |
| RC4 | Stream cipher dan bahaya memakai ulang keystream | 5 |
| AES dan mode operasi | ECB, CBC, CTR, GCM, padding, KDF, demo gambar, uji manipulasi | 5 dan 6 |
"""
    )

    st.markdown("#### Alur ceritanya")
    st.write(
        "1. **Cipher klasik** mengacak huruf, tetapi tetap bisa dipecahkan lewat pola statistik.  \n"
        "2. **Kriptografi modern** bekerja pada bit dan byte, dengan XOR sebagai operasi inti.  \n"
        "3. **Stream cipher** memakai keystream dari kunci pendek, tetapi keystream tidak boleh dipakai ulang.  \n"
        "4. **Block cipher AES** sangat kuat, tetapi mode operasi yang salah (ECB) tetap membocorkan pola.  \n"
        "5. **GCM** menambahkan autentikasi, sehingga data yang diubah langsung ditolak."
    )
    st.info("Pilih modul pada menu di sebelah kiri untuk mulai mencoba.")


# ============================================================ Cipher klasik
def halaman_klasik():
    st.header("Cipher klasik")
    st.caption("Pertemuan 2 · hanya huruf A-Z yang diproses, karakter lain dibuang otomatis")
    tab_shift, tab_pf = st.tabs(["Vigenère, Beaufort, Auto-key", "Playfair"])

    # ---------- Vigenère / Beaufort / Auto-key
    with tab_shift:
        jenis = st.selectbox("Jenis cipher", ["Vigenère", "Beaufort", "Auto-key Vigenère"])
        proses = st.radio("Proses", ["Enkripsi", "Dekripsi"], horizontal=True, key="proses_shift")
        pesan = st.text_area("Pesan", "KRIPTOGRAFI", key="pesan_shift")
        kunci = st.text_input("Kunci", "KUNCI", key="kunci_shift")
        dek = proses == "Dekripsi"

        if jenis == "Vigenère":
            st.latex(r"c_i = (p_i + k_i) \bmod 26 \qquad p_i = (c_i - k_i) \bmod 26")
            fungsi = klasik.vigenere
        elif jenis == "Beaufort":
            st.latex(r"c_i = (k_i - p_i) \bmod 26")
            st.caption("Beaufort bersifat self-reciprocal: rumus yang sama dipakai untuk enkripsi dan dekripsi.")
            fungsi = klasik.beaufort
        else:
            st.latex(r"\text{kunci} = \text{kunci awal} + \text{plainteks} \qquad c_i = (p_i + k_i) \bmod 26")
            fungsi = klasik.autokey

        try:
            hasil = fungsi(pesan, kunci, dek)
        except ValueError as e:
            st.error(str(e))
        else:
            st.markdown("**Hasil**")
            st.code(hasil, language=None)
            st.download_button("Unduh hasil (.txt)", hasil, file_name="hasil_klasik.txt")
            with st.expander("Lihat langkah perhitungan"):
                st.dataframe(
                    pd.DataFrame(klasik.rincian_shift(jenis, pesan, kunci, hasil, dek)),
                    hide_index=True,
                )
            if jenis == "Vigenère":
                with st.expander("Lihat tabula recta (tabel Vigenère)"):
                    huruf, tabel = klasik.tabula_recta()
                    st.caption("Baris = huruf kunci, kolom = huruf plainteks, isi sel = huruf cipherteks.")
                    st.dataframe(pd.DataFrame(tabel, index=huruf, columns=huruf))

    # ---------- Playfair
    with tab_pf:
        proses = st.radio("Proses", ["Enkripsi", "Dekripsi"], horizontal=True, key="proses_pf")
        pesan = st.text_area("Pesan", "GOODBROOMSSWEEPCLEAN", key="pesan_pf")
        kunci = st.text_input("Kunci", "JALAN NAKULA SEBELAS", key="kunci_pf")
        dek = proses == "Dekripsi"
        st.caption(
            "Aturan: huruf J pada kunci dibuang dan pada pesan diganti I. Pasangan huruf kembar disisipi Z, "
            "dan pesan berhuruf ganjil digenapkan dengan Z."
        )
        try:
            hasil = klasik.playfair(pesan, kunci, dek)
        except ValueError as e:
            st.error(str(e))
        else:
            m = klasik.matriks_playfair(kunci)
            st.markdown("**Bujursangkar kunci 5×5**")
            st.dataframe(
                pd.DataFrame([m[i * 5:(i + 1) * 5] for i in range(5)], columns=[1, 2, 3, 4, 5]),
                hide_index=True,
            )
            st.markdown("**Pesan dibagi menjadi bigram**")
            st.code(" ".join(klasik.pasangan_playfair(pesan, dek)), language=None)
            st.markdown("**Hasil**")
            st.code(klasik.bagi_pasangan(hasil), language=None)
            st.download_button("Unduh hasil (.txt)", hasil, file_name="hasil_playfair.txt")


# ============================================================ XOR, avalanche, PRNG
def halaman_modern():
    st.header("XOR, avalanche, dan pembangkitan kunci")
    st.caption("Pertemuan 4 dan 5 · kriptografi bekerja pada bit dan byte, bukan huruf")
    tab_xor, tab_av, tab_rng = st.tabs(["Cipher XOR", "Avalanche effect", "PRNG vs CSPRNG"])

    with tab_xor:
        st.latex(r"C = P \oplus K \qquad P = C \oplus K \qquad A \oplus B \oplus B = A")
        pesan = st.text_input("Plainteks", "KRIPTOGRAFI", key="xor_p")
        kunci = st.text_input("Kunci (diulang bila lebih pendek)", "KUNCI", key="xor_k")
        try:
            enc = modern.xor_cipher(pesan.encode(), kunci.encode())
        except ValueError as e:
            st.error(str(e))
        else:
            st.markdown("**Cipherteks (hex)**")
            st.code(enc.hex(), language=None)
            dec = modern.xor_cipher(enc, kunci.encode())
            st.success(f"XOR sekali lagi dengan kunci yang sama mengembalikan: {dec.decode(errors='replace')}")
            with st.expander("Lihat XOR per byte (16 byte pertama)"):
                st.dataframe(pd.DataFrame(modern.rincian_xor(pesan.encode(), kunci.encode())), hide_index=True)
            st.caption("Cipher XOR dengan kunci pendek tidak aman karena kunci berulang. Ia hanya fondasi untuk stream cipher.")

    with tab_av:
        st.write("Ubah satu bit pada pesan, lalu lihat berapa bit hash SHA-256 yang ikut berubah. Idealnya sekitar 50%.")
        pesan = st.text_input("Pesan", "Kriptografi123456", key="av_p")
        if not pesan:
            st.error("Pesan tidak boleh kosong.")
        else:
            posisi = st.slider("Bit yang dibalik (0 = bit paling kanan pada byte pertama)", 0, len(pesan.encode()) * 8 - 1, 0)
            r = modern.avalanche_sha256(pesan, posisi)
            st.markdown(f"Pesan setelah satu bit dibalik: `{r['teks_ubah']}`")
            st.markdown("**SHA-256 asli**")
            st.code(r["hash_asli"], language=None)
            st.markdown("**SHA-256 setelah diubah**")
            st.code(r["hash_ubah"], language=None)
            c1, c2 = st.columns(2)
            c1.metric("Bit yang berbeda", f"{r['bit_beda']} dari 256")
            c2.metric("Persentase", f"{r['persen']:.1f}%")
            st.progress(min(r["persen"] / 100, 1.0))

    with tab_rng:
        st.write(
            "PRNG biasa bersifat deterministik: seed yang sama selalu menghasilkan urutan yang sama, "
            "sehingga tidak boleh dipakai untuk kunci. CSPRNG mengambil entropy dari sistem operasi."
        )
        st.latex(r"x_{n+1} = (a \cdot x_n + c) \bmod m")
        seed = st.number_input("Seed LCG", min_value=0, value=42, step=1)
        n = st.slider("Jumlah angka", 1, 10, 3)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**LCG (PRNG), dipanggil dua kali**")
            st.code(f"{modern.lcg(int(seed), n)}\n{modern.lcg(int(seed), n)}", language=None)
            st.warning("Kedua baris identik, jadi mudah ditebak.")
        with c2:
            st.markdown("**secrets (CSPRNG), dipanggil dua kali**")
            st.code(f"{modern.csprng_hex()}\n{modern.csprng_hex()}", language=None)
            st.success("Setiap panggilan menghasilkan nilai baru.")


# ============================================================ RC4
def halaman_rc4():
    st.header("Stream cipher RC4")
    st.caption("Pertemuan 5 · keystream dibangkitkan dari kunci (KSA lalu PRGA), kemudian di-XOR dengan pesan")
    st.latex(r"C = P \oplus \text{keystream} \qquad P = C \oplus \text{keystream}")

    st.subheader("Enkripsi dan dekripsi")
    pesan = st.text_input("Plainteks", "Plaintext", key="rc4_p")
    kunci = st.text_input("Kunci", "Key", key="rc4_k")
    try:
        enc = rc4m.rc4(kunci.encode(), pesan.encode())
    except ValueError as e:
        st.error(str(e))
    else:
        st.markdown("**Cipherteks (hex)**")
        st.code(enc.hex(), language=None)
        st.success(f"Dekripsi (RC4 dijalankan lagi): {rc4m.rc4(kunci.encode(), enc).decode(errors='replace')}")
        if kunci == "Key" and pesan == "Plaintext":
            ok = enc.hex() == rc4m.TEST_CIPHER_HEX
            st.caption(f"Cocok dengan test vector di slide ({rc4m.TEST_CIPHER_HEX}): {'ya' if ok else 'tidak'}")

    st.divider()
    st.subheader("Bahaya memakai ulang keystream")
    st.write(
        "Jika kunci yang sama dipakai untuk dua pesan, XOR kedua cipherteks sama dengan XOR kedua plainteks. "
        "Keystream hilang dari persamaan, dan penyerang bisa menganalisis pola bahasa (serangan two-time pad)."
    )
    p1 = st.text_input("Pesan 1", "TRANSFER SERATUS JUTA", key="rc4_p1")
    p2 = st.text_input("Pesan 2", "TRANSFER SATU MILYAR!", key="rc4_p2")
    kk = st.text_input("Kunci yang sama untuk keduanya", "rahasia", key="rc4_kk")
    try:
        t = rc4m.demo_two_time_pad(kk.encode(), p1.encode(), p2.encode())
    except ValueError as e:
        st.error(str(e))
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Cipherteks 1 ⊕ Cipherteks 2**")
            st.code(t["xor_cipher"].hex(), language=None)
        with c2:
            st.markdown("**Plainteks 1 ⊕ Plainteks 2**")
            st.code(t["xor_plain"].hex(), language=None)
        if t["sama"]:
            st.error("Keduanya identik. Keystream bocor, dan inilah alasan nonce harus selalu berbeda.")
        st.caption("Bila panjang kedua pesan berbeda, hanya bagian yang sama panjang yang dibandingkan.")


# ============================================================ AES
def _pesan_gagal(mode: str, e: Exception) -> str:
    if mode == "GCM":
        return "Autentikasi gagal: password salah atau data sudah diubah."
    if mode in ("CBC", "ECB"):
        return "Padding tidak valid: kemungkinan password atau mode yang dipilih salah."
    return f"Dekripsi gagal: {e}"


def halaman_aes():
    st.header("AES dan mode operasi")
    st.caption("Pertemuan 5 dan 6 · AES hanya mengenkripsi satu blok 16 byte; mode operasi menentukan cara mengolah pesan panjang")
    tab_teks, tab_img, tab_pad, tab_uji = st.tabs(
        ["Enkripsi teks", "Demo gambar: ECB vs CBC", "Padding PKCS#7", "Uji manipulasi: CBC vs GCM"]
    )

    # ---------- Enkripsi teks
    with tab_teks:
        c1, c2, c3 = st.columns(3)
        mode = c1.selectbox("Mode", aes.MODE, index=3)
        bits = c2.radio("Panjang kunci", [128, 256], index=1, horizontal=True)
        password = c3.text_input("Password", "rahasia123")
        st.caption("Kunci AES diturunkan dari password dengan PBKDF2 dan salt acak (KDF), lalu IV atau nonce dibangkitkan dengan CSPRNG.")
        if mode == "ECB":
            st.warning("ECB membuat blok plainteks yang sama menghasilkan blok cipherteks yang sama. Lihat tab demo gambar.")

        kiri, kanan = st.columns(2)
        with kiri:
            st.subheader("Enkripsi")
            pesan = st.text_area("Plainteks", "Pesan rahasia CryptoLab", key="aes_pesan")
            if st.button("Enkripsi", type="primary"):
                try:
                    r = aes.enkripsi_teks(mode, pesan, password, bits)
                except ValueError as e:
                    st.error(str(e))
                else:
                    st.session_state["aes_paket_in"] = r["paket"].hex()
                    st.session_state["aes_rincian"] = {
                        "Salt": r["salt"].hex(),
                        "IV / nonce": r["iv"].hex() or "(tidak dipakai)",
                        "Tag autentikasi": r["tag"].hex() or "(tidak ada)",
                        "Cipherteks": r["ct"].hex(),
                        "Kunci turunan": r["key"].hex(),
                    }
            rincian = st.session_state.get("aes_rincian")
            if rincian:
                st.dataframe(pd.DataFrame(rincian.items(), columns=["Komponen", "Nilai (hex)"]), hide_index=True)
        with kanan:
            st.subheader("Dekripsi")
            paket_hex = st.text_area("Paket terenkripsi (hex: salt, IV/nonce, tag, cipherteks)", key="aes_paket_in")
            if st.button("Dekripsi"):
                try:
                    hasil = aes.dekripsi_teks(mode, paket_hex, password, bits)
                except ValueError as e:
                    st.error(_pesan_gagal(mode, e))
                else:
                    st.success(f"Hasil dekripsi: {hasil}")

    # ---------- Demo gambar
    with tab_img:
        st.write(
            "Gambar dienkripsi byte per byte pada piksel RGB-nya. Pada ECB, area warna yang sama menghasilkan "
            "blok cipherteks yang sama, sehingga bentuk gambar masih terlihat."
        )
        c1, c2 = st.columns(2)
        sumber = c1.radio("Sumber gambar", ["Gambar contoh", "Upload gambar"], horizontal=True)
        pembanding = c2.selectbox("Bandingkan ECB dengan", ["CBC", "CTR", "GCM"])
        img = None
        if sumber == "Upload gambar":
            file = st.file_uploader("Pilih gambar", type=["png", "jpg", "jpeg"])
            if file:
                img = Image.open(file).convert("RGB")
                img.thumbnail((256, 256))
            else:
                st.info("Belum ada gambar. Gambar dengan area warna polos, seperti logo, menunjukkan kebocoran pola paling jelas.")
        else:
            img = aes.gambar_contoh()
        if img is not None:
            st.session_state.setdefault("kunci_gambar", get_random_bytes(16))
            kunci = st.session_state["kunci_gambar"]
            img_ecb = aes.enkripsi_gambar(img, "ECB", kunci)
            img_lain = aes.enkripsi_gambar(img, pembanding, kunci)
            k1, k2, k3 = st.columns(3)
            k1.image(img, caption="Gambar asli")
            k2.image(img_ecb, caption="AES-ECB (pola bocor)")
            k3.image(img_lain, caption=f"AES-{pembanding} (tampak acak)")
            buf = io.BytesIO()
            img_ecb.save(buf, format="PNG")
            st.download_button("Unduh hasil ECB (.png)", buf.getvalue(), file_name="hasil_ecb.png", mime="image/png")

    # ---------- Padding
    with tab_pad:
        st.write(
            "Blok terakhir digenapkan ke 16 byte. Aturan PKCS#7: tambahkan sebanyak N byte yang masing-masing bernilai N. "
            "Jika pesan sudah pas kelipatan 16, tetap ditambahkan satu blok penuh."
        )
        teks = st.text_input("Plainteks", "KRIPTOGRAFI", key="pad_p")
        data = teks.encode()
        padded, n = aes.padding_pkcs7(data)
        st.markdown(f"Panjang asli **{len(data)} byte**, padding **{n} byte** bernilai `0x{n:02x}`, total **{len(padded)} byte**.")
        st.markdown("**Hex setelah padding (per blok 16 byte)**")
        st.code("\n".join(padded[i:i + 16].hex(" ") for i in range(0, len(padded), 16)), language=None)
        st.caption("Coba teks sepanjang tepat 16 karakter untuk melihat satu blok padding penuh.")

    # ---------- Uji manipulasi
    with tab_uji:
        st.write(
            "Penyerang membalik satu bit pada cipherteks tanpa mengetahui kunci. "
            "CBC tidak punya autentikasi, sehingga perubahan lolos tanpa peringatan. GCM menolaknya lewat tag."
        )
        pesan = st.text_input("Pesan", "Uang ditransfer 1.000.000 rupiah ke rekening Budi Santoso", key="uji_p")
        if not pesan:
            st.error("Pesan tidak boleh kosong.")
        else:
            posisi = st.slider("Posisi byte cipherteks yang diubah", 0, max(len(pesan.encode()) - 1, 1), 0)
            st.session_state.setdefault("kunci_uji", get_random_bytes(32))
            kunci = st.session_state["kunci_uji"]
            kiri, kanan = st.columns(2)
            with kiri:
                st.subheader("AES-CBC")
                r = aes.uji_manipulasi("CBC", pesan.encode(), kunci, posisi)
                if r["terdeteksi"]:
                    st.error(r["pesan"])
                else:
                    st.warning("Perubahan tidak terdeteksi. Hasil dekripsi rusak tanpa peringatan:")
                    st.code(r["hasil"], language=None)
            with kanan:
                st.subheader("AES-GCM")
                r = aes.uji_manipulasi("GCM", pesan.encode(), kunci, posisi)
                if r["terdeteksi"]:
                    st.success("Manipulasi terdeteksi dan data ditolak.")
                    st.caption(r["pesan"])
                else:
                    st.code(r["hasil"], language=None)
            st.caption("Pada posisi 0, CBC merusak blok pertama dan mengubah satu karakter yang bisa diprediksi di blok kedua (bit-flipping attack).")


# ============================================================ Navigasi
HALAMAN = {
    "Beranda": halaman_beranda,
    "Cipher klasik": halaman_klasik,
    "XOR, avalanche, PRNG": halaman_modern,
    "Stream cipher RC4": halaman_rc4,
    "AES dan mode operasi": halaman_aes,
}

with st.sidebar:
    st.markdown("### CryptoLab")
    pilihan = st.radio("Modul", list(HALAMAN), label_visibility="collapsed")
    st.divider()
    st.caption(f"{NAMA}  \n{NIM}  \nTeknik Informatika, UDINUS")

HALAMAN[pilihan]()
