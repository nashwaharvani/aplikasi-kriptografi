"""Stream cipher RC4 (Pertemuan 5): KSA + PRGA, serta demo bahaya reuse keystream."""


def rc4(key: bytes, data: bytes) -> bytes:
    """RC4 berbasis XOR, jadi fungsi yang sama dipakai untuk enkripsi dan dekripsi."""
    if not key:
        raise ValueError("Kunci tidak boleh kosong.")
    # KSA (Key Scheduling Algorithm)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    # PRGA (Pseudo-Random Generation Algorithm)
    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        out.append(byte ^ k)
    return bytes(out)


def keystream(key: bytes, n: int) -> bytes:
    """Keystream = hasil RC4 atas barisan nol (0 xor k = k)."""
    return rc4(key, bytes(n))


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def demo_two_time_pad(key: bytes, pesan1: bytes, pesan2: bytes) -> dict:
    """Dua pesan dienkripsi dengan kunci yang sama. XOR kedua cipherteks
    sama dengan XOR kedua plainteks, sehingga keystream 'habis terbuang'."""
    n = min(len(pesan1), len(pesan2))
    c1 = rc4(key, pesan1[:n])
    c2 = rc4(key, pesan2[:n])
    xor_c = xor_bytes(c1, c2)
    xor_p = xor_bytes(pesan1[:n], pesan2[:n])
    return {"c1": c1, "c2": c2, "xor_cipher": xor_c, "xor_plain": xor_p, "sama": xor_c == xor_p}


# Test vector dari slide Pertemuan 5
TEST_KEY = b"Key"
TEST_PLAIN = b"Plaintext"
TEST_CIPHER_HEX = "bbf316e8d940af0ad3"
