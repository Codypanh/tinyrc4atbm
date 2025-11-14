# tiny_rc4_logic.py
# Phiên bản Tiny RC4: S-box 0..15 (N=16), nhưng mã hóa trên byte ASCII 0..255

def ksa_tiny(key):
    """Key Scheduling Algorithm - khởi tạo và trộn S-box"""
    N = 16
    S = list(range(N))
    j = 0
    for i in range(N):
        j = (j + S[i] + key[i % len(key)]) % N
        S[i], S[j] = S[j], S[i]
    return S

def prga_tiny(S, n_bytes):
    """Pseudo-Random Generation Algorithm - sinh keystream mod 16"""
    N = 16
    i = j = 0
    keystream = []
    for _ in range(n_bytes):
        i = (i + 1) % N
        j = (j + S[i]) % N
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % N]   # K nằm trong 0..15
        keystream.append(K)
    return keystream

def encrypt_tiny_rc4(plaintext_nums, key):
    """
    plaintext_nums: list số 0..255 (ord(c) từ chuỗi)
    key: list số 0..15
    """
    S = ksa_tiny(key)
    keystream = prga_tiny(S, len(plaintext_nums))
    # XOR byte 0..255 với keystream 0..15 → vẫn 0..255, không mod 16 nữa
    cipher = [p ^ k for p, k in zip(plaintext_nums, keystream)]
    return cipher, keystream

def decrypt_tiny_rc4(ciphertext_nums, key):
    """Giải mã: XOR lại với cùng keystream"""
    S = ksa_tiny(key)
    keystream = prga_tiny(S, len(ciphertext_nums))
    plain = [c ^ k for c, k in zip(ciphertext_nums, keystream)]
    return plain
