"""Cipher klasik (Pertemuan 2): Vigenère, Beaufort, Auto-key Vigenère, Playfair.

Semua fungsi hanya memahami huruf A-Z. Karakter lain (spasi, angka, tanda baca)
dibuang oleh `bersihkan()` sebelum diproses.
"""
import re

A = 65  # kode ASCII huruf 'A'


def bersihkan(teks: str) -> str:
    """Huruf besar saja, buang semua karakter selain A-Z."""
    return re.sub(r"[^A-Z]", "", teks.upper())


def _cek(teks: str, kunci: str) -> None:
    if not kunci:
        raise ValueError("Kunci harus berisi minimal satu huruf A-Z.")
    if not teks:
        raise ValueError("Pesan harus berisi minimal satu huruf A-Z.")


# ---------------------------------------------------------------- Vigenère
def vigenere(teks: str, kunci: str, dekripsi: bool = False) -> str:
    """c_i = (p_i + k_i) mod 26  |  p_i = (c_i - k_i) mod 26"""
    teks, kunci = bersihkan(teks), bersihkan(kunci)
    _cek(teks, kunci)
    arah = -1 if dekripsi else 1
    return "".join(
        chr((ord(c) - A + arah * (ord(kunci[i % len(kunci)]) - A)) % 26 + A)
        for i, c in enumerate(teks)
    )


# ---------------------------------------------------------------- Beaufort
def beaufort(teks: str, kunci: str, dekripsi: bool = False) -> str:
    """c_i = (k_i - p_i) mod 26. Bersifat self-reciprocal: rumus yang sama
    dipakai untuk enkripsi dan dekripsi (parameter `dekripsi` hanya formalitas)."""
    teks, kunci = bersihkan(teks), bersihkan(kunci)
    _cek(teks, kunci)
    return "".join(
        chr((ord(kunci[i % len(kunci)]) - ord(c)) % 26 + A)
        for i, c in enumerate(teks)
    )


# ---------------------------------------------------------------- Auto-key
def autokey(teks: str, kunci: str, dekripsi: bool = False) -> str:
    """Kunci awal disambung dengan plainteks itu sendiri."""
    teks, kunci = bersihkan(teks), bersihkan(kunci)
    _cek(teks, kunci)
    aliran = list(kunci)
    hasil = []
    for i, c in enumerate(teks):
        k = ord(aliran[i]) - A
        v = ord(c) - A
        if dekripsi:
            p = chr((v - k) % 26 + A)
            hasil.append(p)
            aliran.append(p)  # plainteks hasil dekripsi menjadi kunci berikutnya
        else:
            hasil.append(chr((v + k) % 26 + A))
            aliran.append(c)
    return "".join(hasil)


def rincian_shift(jenis: str, teks: str, kunci: str, hasil: str, dekripsi: bool = False):
    """Tabel langkah per huruf untuk Vigenère / Beaufort / Auto-key."""
    teks, kunci = bersihkan(teks), bersihkan(kunci)
    n = len(teks)
    if jenis == "Auto-key Vigenère":
        plain = hasil if dekripsi else teks
        aliran = (kunci + plain)[:n]
    else:
        aliran = (kunci * (n // len(kunci) + 1))[:n]
    return [
        {
            "No": i + 1,
            "Huruf": teks[i],
            "Kunci": aliran[i],
            "Angka huruf": ord(teks[i]) - A,
            "Angka kunci": ord(aliran[i]) - A,
            "Hasil": hasil[i],
        }
        for i in range(n)
    ]


def tabula_recta():
    """Tabel Vigenère 26x26: baris = huruf kunci, kolom = huruf plainteks."""
    huruf = [chr(A + i) for i in range(26)]
    return huruf, [[chr((r + c) % 26 + A) for c in range(26)] for r in range(26)]


# ---------------------------------------------------------------- Playfair
def matriks_playfair(kunci: str) -> list:
    """Bujursangkar 5x5 (25 huruf, tanpa J). Huruf J pada kunci dibuang."""
    kunci = bersihkan(kunci).replace("J", "")
    urut = []
    for c in kunci + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in urut:
            urut.append(c)
    return urut


def pasangan_playfair(teks: str, dekripsi: bool = False) -> list:
    """Bagi teks menjadi bigram. Pada enkripsi: J diganti I, pasangan kembar
    disisipi Z, dan jumlah huruf ganjil digenapkan dengan Z."""
    teks = bersihkan(teks).replace("J", "I")
    if dekripsi:
        if len(teks) % 2:
            raise ValueError("Cipherteks Playfair harus berjumlah huruf genap.")
        return [teks[i:i + 2] for i in range(0, len(teks), 2)]
    pasangan, i = [], 0
    while i < len(teks):
        a = teks[i]
        b = teks[i + 1] if i + 1 < len(teks) else "Z"
        if a == b:
            b = "Z"
            i += 1
        else:
            i += 2
        pasangan.append(a + b)
    return pasangan


def playfair(teks: str, kunci: str, dekripsi: bool = False) -> str:
    if not bersihkan(kunci):
        raise ValueError("Kunci harus berisi minimal satu huruf A-Z.")
    if not bersihkan(teks):
        raise ValueError("Pesan harus berisi minimal satu huruf A-Z.")
    m = matriks_playfair(kunci)
    arah = -1 if dekripsi else 1
    hasil = []
    for a, b in pasangan_playfair(teks, dekripsi):
        r1, c1 = divmod(m.index(a), 5)
        r2, c2 = divmod(m.index(b), 5)
        if r1 == r2:                      # satu baris -> geser ke kanan
            c1, c2 = (c1 + arah) % 5, (c2 + arah) % 5
        elif c1 == c2:                    # satu kolom -> geser ke bawah
            r1, r2 = (r1 + arah) % 5, (r2 + arah) % 5
        else:                             # persegi panjang -> tukar kolom
            c1, c2 = c2, c1
        hasil.append(m[r1 * 5 + c1] + m[r2 * 5 + c2])
    return "".join(hasil)


def bagi_pasangan(teks: str) -> str:
    """'ABCD' -> 'AB CD' agar mudah dibaca."""
    return " ".join(teks[i:i + 2] for i in range(0, len(teks), 2))
