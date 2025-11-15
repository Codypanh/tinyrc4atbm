📘 README – TinyRC4 Web & CLI Demo
🔒 TinyRC4 – Demo mã hóa/giải mã (Web + CLI)

Dự án gồm 4 file chính:

tiny_rc4_logic.py — Thuật toán TinyRC4 (KSA + PRGA + encrypt + decrypt)

api.py — Chạy server Flask để mã hóa/giải mã qua giao diện web

index.html — Giao diện web demo

main.py — Chạy TinyRC4 dạng CLI (dùng trong terminal)

🚀 Cách chạy dự án
1️⃣ Cài thư viện cần thiết
pip install flask

2️⃣ Chạy phiên bản Web (Flask + HTML)

File cần chạy: api.py

python api.py


Nếu chạy thành công, terminal sẽ báo:

 * Running on http://127.0.0.1:5000


👉 Mở trình duyệt và truy cập:

http://127.0.0.1:5000


Giao diện web có thể:

Mã hóa văn bản → trả về HEX + ký tự Latin-1 + keystream

Giải mã văn bản (nhập Hex hoặc ký tự Latin-1)

3️⃣ Chạy phiên bản CLI (terminal)

File cần chạy: main.py

python main.py


CLI hỗ trợ:

Nhập khóa dạng 4 1 2 3 hoặc 4123

Chọn:
1 → Mã hóa
2 → Giải mã

Hiển thị: plaintext / cipher / hex / keystream

4️⃣ Cấu trúc thư mục
project/
│── api.py
│── main.py
│── tiny_rc4_logic.py
└── index.html


Lưu ý: api.py sử dụng index.html thông qua Flask (template_folder='.').

📝 Ghi chú

TinyRC4 trong dự án này dùng S-box 0..15 (N=16) nhưng mã hóa trên byte ASCII 0–255.

Khi giải mã cần cùng key và cùng thuật toán.

Giao diện web hỗ trợ cả HEX và ký tự Latin-1 để giữ đúng mapping byte-ký tự.
