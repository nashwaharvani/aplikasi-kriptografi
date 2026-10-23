"""Kriptografi modern dasar (Pertemuan 4 dan 5): XOR cipher, avalanche effect,
PRNG (LCG) versus CSPRNG."""
import hashlib
import secrets


# ---------------------------------------------------------------- XOR cipher
def xor_cipher(data: bytes, key: bytes) -> bytes:
    """C = P xor K (kunci diulang). Self-inverse: fungsi yang sama untuk dekripsi."""
    if not key:
        raise ValueError("Kunci tidak boleh kosong.")
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))


def rincian_xor(data: bytes, key: bytes, batas: int = 16):
    """Tabel XOR per byte (maksimal `batas` byte pertama)."""
    baris = []
    for i, d in enumerate(data[:batas]):
        k = key[i % len(key)]
        baris.append({
            "No": i + 1,
            "Plainteks": chr(d) if 32 <= d < 127 else "?",
            "ASCII P": d,
            "Biner P": format(d, "08b"),
            "Kunci": chr(k) if 32 <= k < 127 else "?",
            "Biner K": format(k, "08b"),
            "Hasil XOR": format(d ^ k, "08b"),
            "Hex": format(d ^ k, "02x"),
        })
    return baris


# ---------------------------------------------------------------- Avalanche
def balik_bit(data: bytes, posisi: int) -> bytes:
    """Balik satu bit. Posisi 0 = bit paling kanan (LSB) dari byte pertama."""
    if not 0 <= posisi < len(data) * 8:
        raise ValueError("Posisi bit di luar jangkauan.")
    hasil = bytearray(data)
    hasil[posisi // 8] ^= 1 << (posisi % 8)
    return bytes(hasil)


def beda_bit(a: bytes, b: bytes) -> int:
    """Jumlah bit yang berbeda antara dua barisan byte."""
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def avalanche_sha256(teks: str, posisi_bit: int = 0) -> dict:
    """Bandingkan SHA-256 dari teks asli dan teks dengan satu bit dibalik."""
    asli = teks.encode()
    ubah = balik_bit(asli, posisi_bit)
    h1 = hashlib.sha256(asli).digest()
    h2 = hashlib.sha256(ubah).digest()
    beda = beda_bit(h1, h2)
    return {
        "teks_ubah": ubah.decode("utf-8", errors="replace"),
        "hash_asli": h1.hex(),
        "hash_ubah": h2.hex(),
        "bit_beda": beda,
        "persen": beda / 256 * 100,
    }


# ---------------------------------------------------------------- PRNG vs CSPRNG
def lcg(seed: int, n: int, a: int = 1103515245, c: int = 12345, m: int = 2 ** 31) -> list:
    """PRNG klasik x_{n+1} = (a*x_n + c) mod m. Deterministik: seed sama, hasil sama."""
    x, hasil = seed, []
    for _ in range(n):
        x = (a * x + c) % m
        hasil.append(x)
    return hasil


def csprng_hex(n_byte: int = 8) -> str:
    """Bilangan acak aman secara kriptografis (entropy dari sistem operasi)."""
    return secrets.token_bytes(n_byte).hex()
