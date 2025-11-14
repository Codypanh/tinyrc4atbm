import json
from flask import Flask, request, jsonify, render_template
# Import logic đã sửa của bạn (file tiny_rc4_logic.py)
from tiny_rc4_logic import encrypt_tiny_rc4, decrypt_tiny_rc4

app = Flask(__name__, template_folder='.') # Dùng thư mục hiện tại cho HTML

# --- Các hàm xử lý dữ liệu ---

def parse_key(key_str):
    """Phân tích key string (vd: "1 2 3 4") thành list số."""
    try:
        parts = key_str.strip().split()
        if not parts: # Nếu chuỗi rỗng
            raise ValueError("Key rỗng")
        key = [int(x) % 16 for x in parts]
    except ValueError:
        print("Khóa không hợp lệ, dùng khóa mặc định [1, 2, 3, 4]")
        key = [1, 2, 3, 4]
    
    if len(key) < 4:
        key = (key + [0, 0, 0, 0])[:4]
    elif len(key) > 4:
        key = key[:4]
    return key

def bytes_to_hex(byte_list):
    """Chuyển list các byte (số 0-255) thành chuỗi Hex"""
    return "".join(format(b, '02X') for b in byte_list)

def hex_to_bytes(hex_str):
    """Chuyển chuỗi Hex thành list các byte. Sẽ báo lỗi nếu không phải Hex."""
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    # Thêm kiểm tra: Chỉ cho phép các ký tự Hex
    if not all(c in '0123456789abcdefABCDEF' for c in hex_str):
        raise ValueError("Dữ liệu nhập vào không phải là chuỗi Hex hợp lệ")
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

# --- Các tuyến API ---

@app.route('/')
def index():
    """Phục vụ file HTML giao diện chính"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def api_process():
    """API chính xử lý cả mã hóa và giải mã"""
    try:
        data = request.json
        mode = data.get('mode')
        key_str = data.get('key', '1 2 3 4')
        text = data.get('text', '')

        key = parse_key(key_str)
        
        if mode == 'encrypt':
            # plaintext: chuỗi ký tự; convert -> list số (0-255) via ord (1-1 mapping)
            plaintext_bytes = [ord(c) for c in text]

            cipher_bytes, keystream = encrypt_tiny_rc4(plaintext_bytes, key)

            result_hex = bytes_to_hex(cipher_bytes)
            # Chuỗi ký tự 1-1 với bytes (dùng latin-1 để map 0-255 -> 1 ký tự)
            try:
                result_chars = bytes(cipher_bytes).decode('latin-1')
            except Exception:
                result_chars = ''.join(chr(b) for b in cipher_bytes)

            return jsonify({
                'success': True,
                'result_hex': result_hex,
                'result_chars': result_chars,
                'keystream': keystream,
                'note': 'Kết quả trả về cả Hex và chuỗi ký tự (latin-1).'
            })

        elif mode == 'decrypt':
            # Hỗ trợ nhập ciphertext là Hex (VD: "4F2A...") hoặc là chuỗi ký tự (raw chars)
            ciphertext_input = text or ''
            ciphertext_input = ciphertext_input.strip()

            # Nếu có vẻ là hex (chỉ chứa ký tự hex) thì parse thành byte list,
            # ngược lại coi đó là chuỗi ký tự (một ký tự -> một byte bằng ord())
            ciphertext_bytes = None
            if ciphertext_input and all(c in '0123456789abcdefABCDEF' for c in ciphertext_input):
                # Nếu độ dài lẻ thì hex_to_bytes sẽ pad bên trong
                try:
                    ciphertext_bytes = hex_to_bytes(ciphertext_input)
                except ValueError as e:
                    return jsonify({'success': False, 'error': str(e)}), 400
            else:
                # treat as raw characters
                ciphertext_bytes = [ord(c) for c in text]

            plain_bytes = decrypt_tiny_rc4(ciphertext_bytes, key)

            # Trả về chuỗi ký tự (latin-1) để giữ mapping 1-1 với bytes
            try:
                result_text = bytes(plain_bytes).decode('latin-1')
            except Exception:
                result_text = ''.join(chr(b) for b in plain_bytes)

            return jsonify({
                'success': True,
                'result_text': result_text,
                'result_bytes': plain_bytes,
                'note': 'Kết quả là văn bản (latin-1) và danh sách byte'
            })
        else:
            return jsonify({'success': False, 'error': 'Chế độ không hợp lệ'}), 400

    except Exception as e:
        # Bắt các lỗi chung khác
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
