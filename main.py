# tiny_rc4_display.py
from tiny_rc4_logic  import encrypt_tiny_rc4, decrypt_tiny_rc4

def to_hex(data):
    """Chuyển danh sách số thành chuỗi hex (viết hoa, liền nhau)"""
    return ''.join(format(x, '02X') for x in data)

def main():
    # Nhập khóa: cho phép nhập 4123 hoặc 4 1 2 3
    raw_key = input("Nhập khóa (4 số từ 0-15, ví dụ 4123 hoặc 4 1 2 3): ").strip()

    # Nếu người dùng gõ không có khoảng trắng (vd '4123')
    if ' ' not in raw_key:
        parts = list(raw_key)  # '4123' -> ['4','1','2','3']
    else:
        parts = raw_key.split()  # '4 1 2 3' -> ['4','1','2','3']

    try:
        key = [int(x) % 16 for x in parts]
    except ValueError:
        print("Khóa không hợp lệ, dùng khóa mặc định [1,2,3,4]")
        key = [1, 2, 3, 4]

    # Đảm bảo đúng 4 phần tử
    if len(key) < 4:
        key = (key + [0, 0, 0, 0])[:4]
    elif len(key) > 4:
        key = key[:4]

    mode = input("Hãy lựa chọn:\n1. Mã hóa (Encrypt)\n2. Giải mã (Decrypt)\nChọn: ").strip()

    if mode == '1':
        # MÃ HÓA
        plaintext = input("Nhập văn bản cần mã hóa: ")
        plaintext_nums = [ord(c) for c in plaintext]

        print("\n=== TINY RC4 ENCRYPT ===")
        print("Plaintext (ASCII):", plaintext_nums)

        cipher_nums, keystream = encrypt_tiny_rc4(plaintext_nums, key)

        cipher_text = ''.join(chr(x) for x in cipher_nums)

        print("[+] Keystream (0-15):", keystream)
        print("[+] Cipher (bytes):", cipher_nums)
        print("[+] Cipher (as text, có thể có ký tự lạ):", repr(cipher_text))
        print("[+] Cipher (HEX):", to_hex(cipher_nums))
        print("\n=> Hãy copy chuỗi cipher (as text) này để dùng cho bước giải mã cùng key.")

    elif mode == '2':
        # GIẢI MÃ
        cipher_input = input("Nhập cipher (chuỗi ký tự đã mã hóa): ")
        cipher_nums = [ord(c) for c in cipher_input]

        print("\n=== TINY RC4 DECRYPT ===")
        print("Cipher (ASCII codes):", cipher_nums)

        plain_nums = decrypt_tiny_rc4(cipher_nums, key)
        plain_text = ''.join(chr(x) for x in plain_nums)

        print("[+] Decrypted (bytes):", plain_nums)
        print("[+] Decrypted (text):", plain_text)

    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
