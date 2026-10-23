"""AES dan mode operasi (Pertemuan 5 dan 6): ECB, CBC, CTR, GCM, padding PKCS#7,
penurunan kunci dari password (KDF + salt), serta demo gambar dan uji manipulasi."""
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image, ImageDraw

MODE = ["ECB", "CBC", "CTR", "GCM"]
PANJANG_IV = {"ECB": 0, "CBC": 16, "CTR": 8, "GCM": 12}   # IV / nonce (byte)
PANJANG_TAG = {"ECB": 0, "CBC": 0, "CTR": 0, "GCM": 16}   # tag autentikasi (byte)
PANJANG_SALT = 16
ITERASI_KDF = 200_000


# ---------------------------------------------------------------- KDF
def turunkan_kunci(password: str, salt: bytes, panjang: int = 32) -> bytes:
    """PBKDF2-HMAC-SHA256: password (mudah diingat) -> kunci AES (acak-seperti)."""
    if not password:
        raise ValueError("Password tidak boleh kosong.")
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERASI_KDF, panjang)


# ---------------------------------------------------------------- Padding PKCS#7
def padding_pkcs7(data: bytes, ukuran: int = 16):
    """Kembalikan (data berpadding, jumlah byte padding)."""
    padded = pad(data, ukuran)
    return padded, len(padded) - len(data)


# ---------------------------------------------------------------- Enkripsi inti
def enkripsi(mode: str, plain: bytes, key: bytes) -> dict:
    """Kembalikan dict berisi iv (atau nonce), tag, dan ct."""
    if mode == "ECB":
        ct = AES.new(key, AES.MODE_ECB).encrypt(pad(plain, 16))
        return {"iv": b"", "tag": b"", "ct": ct}
    if mode == "CBC":
        iv = get_random_bytes(16)
        ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(plain, 16))
        return {"iv": iv, "tag": b"", "ct": ct}
    if mode == "CTR":
        c = AES.new(key, AES.MODE_CTR)
        ct = c.encrypt(plain)
        return {"iv": c.nonce, "tag": b"", "ct": ct}
    if mode == "GCM":
        nonce = get_random_bytes(12)
        ct, tag = AES.new(key, AES.MODE_GCM, nonce=nonce).encrypt_and_digest(plain)
        return {"iv": nonce, "tag": tag, "ct": ct}
    raise ValueError(f"Mode tidak dikenal: {mode}")


def dekripsi(mode: str, key: bytes, ct: bytes, iv: bytes = b"", tag: bytes = b"") -> bytes:
    """Dekripsi. Melempar ValueError bila padding rusak (CBC/ECB) atau tag GCM tidak cocok."""
    if mode == "ECB":
        return unpad(AES.new(key, AES.MODE_ECB).decrypt(ct), 16)
    if mode == "CBC":
        return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16)
    if mode == "CTR":
        return AES.new(key, AES.MODE_CTR, nonce=iv).decrypt(ct)
    if mode == "GCM":
        return AES.new(key, AES.MODE_GCM, nonce=iv).decrypt_and_verify(ct, tag)
    raise ValueError(f"Mode tidak dikenal: {mode}")


# ---------------------------------------------------------------- Teks + password
def bungkus(salt: bytes, h: dict) -> bytes:
    """paket = salt | iv/nonce | tag | cipherteks"""
    return salt + h["iv"] + h["tag"] + h["ct"]


def buka(mode: str, paket: bytes):
    n_iv, n_tag = PANJANG_IV[mode], PANJANG_TAG[mode]
    if len(paket) < PANJANG_SALT + n_iv + n_tag:
        raise ValueError("Paket terlalu pendek untuk mode ini. Periksa mode yang dipilih.")
    salt = paket[:PANJANG_SALT]
    iv = paket[PANJANG_SALT:PANJANG_SALT + n_iv]
    tag = paket[PANJANG_SALT + n_iv:PANJANG_SALT + n_iv + n_tag]
    ct = paket[PANJANG_SALT + n_iv + n_tag:]
    return salt, {"iv": iv, "tag": tag, "ct": ct}


def enkripsi_teks(mode: str, teks: str, password: str, bits: int = 256) -> dict:
    salt = get_random_bytes(PANJANG_SALT)
    key = turunkan_kunci(password, salt, bits // 8)
    h = enkripsi(mode, teks.encode(), key)
    return {"paket": bungkus(salt, h), "salt": salt, "key": key, **h}


def dekripsi_teks(mode: str, paket_hex: str, password: str, bits: int = 256) -> str:
    try:
        paket = bytes.fromhex("".join(paket_hex.split()))
    except ValueError:
        raise ValueError("Paket harus berupa teks heksadesimal (0-9, a-f).")
    salt, h = buka(mode, paket)
    key = turunkan_kunci(password, salt, bits // 8)
    return dekripsi(mode, key, h["ct"], h["iv"], h["tag"]).decode("utf-8", errors="replace")


# ---------------------------------------------------------------- Demo gambar
def gambar_contoh(ukuran=(240, 240)) -> Image.Image:
    """Logo gembok sederhana dengan area warna rata, supaya pola ECB terlihat jelas."""
    w, h = ukuran
    img = Image.new("RGB", ukuran, (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.ellipse([w * 0.12, h * 0.12, w * 0.88, h * 0.88], fill=(27, 79, 138))
    d.arc([w * 0.32, h * 0.18, w * 0.68, h * 0.55], 180, 360, fill=(255, 255, 255), width=int(w * 0.05))
    d.rectangle([w * 0.28, h * 0.42, w * 0.72, h * 0.72], fill=(245, 170, 30))
    d.ellipse([w * 0.46, h * 0.50, w * 0.54, h * 0.58], fill=(27, 79, 138))
    d.rectangle([w * 0.485, h * 0.55, w * 0.515, h * 0.65], fill=(27, 79, 138))
    return img


def enkripsi_gambar(img: Image.Image, mode: str, key: bytes) -> Image.Image:
    """Enkripsi byte piksel RGB lalu bentuk kembali menjadi gambar (untuk visualisasi)."""
    img = img.convert("RGB")
    data = img.tobytes()
    buf = data + bytes((-len(data)) % 16)       # nol-padding khusus demo visual
    if mode == "ECB":
        ct = AES.new(key, AES.MODE_ECB).encrypt(buf)
    elif mode == "CBC":
        ct = AES.new(key, AES.MODE_CBC, get_random_bytes(16)).encrypt(buf)
    elif mode == "CTR":
        ct = AES.new(key, AES.MODE_CTR).encrypt(data)
    elif mode == "GCM":
        ct = AES.new(key, AES.MODE_GCM, nonce=get_random_bytes(12)).encrypt(data)
    else:
        raise ValueError(f"Mode tidak dikenal: {mode}")
    return Image.frombytes("RGB", img.size, ct[:len(data)])


# ---------------------------------------------------------------- Uji manipulasi
def uji_manipulasi(mode: str, plain: bytes, key: bytes, posisi: int = 0) -> dict:
    """Balik satu bit pada cipherteks, lalu coba dekripsi.
    CBC mendekripsi 'berhasil' tetapi hasilnya rusak; GCM menolaknya."""
    h = enkripsi(mode, plain, key)
    ct = bytearray(h["ct"])
    posisi = max(0, min(posisi, len(ct) - 1))
    ct[posisi] ^= 0x01
    try:
        hasil = dekripsi(mode, key, bytes(ct), h["iv"], h["tag"])
        return {"terdeteksi": False, "hasil": hasil.decode("utf-8", errors="replace"), "pesan": "Dekripsi berhasil tanpa peringatan."}
    except ValueError as e:
        return {"terdeteksi": True, "hasil": "", "pesan": f"Ditolak: {e}"}
