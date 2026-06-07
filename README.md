<div align="center">

# 🚀 ToolDktcVKU

### VKU Course Registration CLI Tool

Công cụ dòng lệnh hỗ trợ thao tác đăng ký tín chỉ VKU nhanh, gọn và dễ sử dụng.

<br>

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Tool-00B894?style=for-the-badge&logo=windowsterminal&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-6C5CE7?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-v7.0-FF7675?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Ready-2ECC71?style=for-the-badge)

<br>

**Quét môn • Quét lớp • Nhập Môn:Lớp • Hẹn giờ Snipe • Bắn thẳng bằng ID**

</div>

---

## 📌 Giới thiệu

**ToolDktcVKU** là một công cụ CLI viết bằng Python, hỗ trợ sinh viên thao tác nhanh hơn với hệ thống đăng ký tín chỉ VKU.

Tool sử dụng Cookie đăng nhập hợp lệ của chính người dùng để gửi request đến hệ thống đào tạo, từ đó hỗ trợ:

- Lấy danh sách môn học đang mở đăng ký.
- Lấy danh sách lớp học phần của từng môn.
- Tìm đúng lớp học phần theo tên.
- Đăng ký lớp học phần.
- Hẹn giờ đăng ký tự động.
- Chạy trực tiếp bằng lệnh terminal sau khi cài đặt.

> Dự án phục vụ mục đích học tập, nghiên cứu HTTP request, HTML parsing và tự động hóa thao tác cá nhân.

---

## ✨ Tính năng nổi bật

| Tính năng | Mô tả |
|---|---|
| 🔍 Quét môn học | Tải danh sách môn đang mở đăng ký |
| 📚 Quét lớp học phần | Xem các lớp của từng môn |
| 🎯 Nhập `Môn:Lớp` | Tự tìm đúng `hocphan_id` và `idlop` |
| ⏰ Hẹn giờ Snipe | Chờ đến giờ mở đăng ký rồi tự chạy |
| ⚡ Bắn thẳng bằng ID | Đăng ký nhanh khi đã biết ID |
| 🐞 Debug mode | Xem HTTP status và phản hồi server |
| 🧩 CLI package | Cài bằng `pip` và chạy bằng lệnh `vku-tool` |

---

## 🛠️ Yêu cầu hệ thống

Cần cài đặt:

- Python `3.9+`
- Git
- Internet ổn định
- Cookie đăng nhập hợp lệ từ hệ thống đào tạo VKU

Kiểm tra Python:

```bash
py --version
```

Hoặc:

```bash
python --version
```

---

## 📦 Cài đặt

### Cài trực tiếp từ GitHub

Trên Windows, khuyến nghị dùng:

```bash
py -m pip install git+https://github.com/LeSyBach/ToolDktcVKU.git
```

Trên Linux/macOS hoặc máy đã cấu hình Python chuẩn:

```bash
pip install git+https://github.com/LeSyBach/ToolDktcVKU.git
```

---

## ▶️ Chạy tool

Sau khi cài đặt, chạy:

```bash
vku-tool
```

Chạy chế độ debug:

```bash
vku-tool --debug
```

Nếu terminal chưa nhận lệnh `vku-tool`, thử:

```bash
py -m vku_tool.cli
```

Hoặc đóng terminal rồi mở lại.

---

## 🔄 Cập nhật phiên bản mới

```bash
py -m pip install --upgrade git+https://github.com/LeSyBach/ToolDktcVKU.git
```

---

## 🗑️ Gỡ cài đặt

```bash
py -m pip uninstall tooldktcvku -y
```

---

## 🧑‍💻 Cài đặt để phát triển local

Clone repo:

```bash
git clone https://github.com/LeSyBach/ToolDktcVKU.git
cd ToolDktcVKU
```

Cài dạng editable:

```bash
py -m pip install -e .
```

Chạy tool:

```bash
vku-tool
```

Khi sửa code trong `vku_tool/cli.py`, chỉ cần chạy lại `vku-tool`, không cần cài lại.

---

## 📁 Cấu trúc thư mục khuyến nghị

```text
ToolDktcVKU/
│
├── README.md
├── pyproject.toml
├── .gitignore
│
└── vku_tool/
    ├── __init__.py
    └── cli.py
```

| File/Thư mục | Mục đích |
|---|---|
| `README.md` | Tài liệu hướng dẫn sử dụng |
| `pyproject.toml` | Cấu hình package để cài bằng `pip` |
| `.gitignore` | Bỏ qua file rác/cache |
| `vku_tool/__init__.py` | Đánh dấu Python package |
| `vku_tool/cli.py` | Code chính của tool |

---

## ⚙️ Cấu hình lệnh CLI

Trong file `pyproject.toml`, phần quan trọng là:

```toml
[project.scripts]
vku-tool = "vku_tool.cli:main"
```

Trong đó:

- `vku-tool` là lệnh gõ trong terminal.
- `vku_tool.cli:main` là đường dẫn đến hàm `main()` trong code.

Muốn đổi tên lệnh, sửa bên trái dấu `=`.

Ví dụ đổi thành `dktc`:

```toml
[project.scripts]
dktc = "vku_tool.cli:main"
```

Cài lại:

```bash
py -m pip install -e .
```

Chạy:

```bash
dktc
```

---

## 🔐 Cách lấy Cookie

Tool cần 2 giá trị:

```text
XSRF-TOKEN
laravel_session
```

### Các bước lấy Cookie

1. Đăng nhập vào hệ thống đào tạo VKU bằng trình duyệt.
2. Nhấn `F12` để mở Developer Tools.
3. Chọn tab `Network`.
4. Tải lại trang hoặc bấm vào một request bất kỳ của hệ thống.
5. Chọn request thuộc domain:

```text
daotao.vku.udn.vn
```

6. Vào tab `Headers`.
7. Tìm phần `Cookie`.
8. Copy giá trị:
   - `XSRF-TOKEN`
   - `laravel_session`

Khi chạy tool, chương trình sẽ yêu cầu nhập hai giá trị này.

---

## 🧭 Hướng dẫn sử dụng

Sau khi chạy:

```bash
vku-tool
```

Tool sẽ hiển thị menu:

```text
01. Quét môn học
02. Quét lớp học phần
03. Nhập cặp MÔN:LỚP
04. Hẹn giờ Snipe
05. Bắn thẳng bằng ID
00. Thoát
```

---

## 01 — Quét môn học

Dùng để tải danh sách môn học đang mở đăng ký và chọn môn muốn đăng ký.

Ví dụ nhập:

```text
1,3,5
```

Hoặc chọn toàn bộ:

```text
all
```

---

## 02 — Quét lớp học phần

Dùng để chọn một môn, sau đó xem danh sách lớp học phần của môn đó.

Tool có thể hiển thị:

- Tên lớp học phần.
- ID lớp.
- Sĩ số.
- Lịch học nếu có.

---

## 03 — Nhập cặp `Môn:Lớp`

Đây là chế độ khuyến nghị khi đã biết rõ lớp cần đăng ký.

### Cú pháp

```text
Tên môn : Tên lớp học phần
```

### Ví dụ một lớp

```text
Lập trình Web : Lập trình Web (1)
```

### Ví dụ nhiều lớp

```text
Lập trình Web : Lập trình Web (1), Cơ sở dữ liệu : Cơ sở dữ liệu (2)
```

### Luồng xử lý

```text
Tìm môn
→ Lấy hocphan_id
→ Quét lớp học phần
→ Tìm lớp khớp tên
→ Lấy idlop
→ Gửi request đăng ký
```

---

## 04 — Hẹn giờ Snipe

Dùng để treo tool trước giờ mở đăng ký.

Ví dụ:

```text
Giờ mở đăng ký: 07:00:00
Ngày: 2026-06-10
Khởi động sớm: 1
```

Có thể chọn chế độ nhập sẵn cặp `Môn:Lớp` để tool đến giờ mới quét ID mới nhất và đăng ký.

---

## 05 — Bắn thẳng bằng ID

Dùng khi đã biết sẵn:

```text
hocphan_id
idlop
```

Ví dụ link đăng ký có dạng:

```text
/sv/dang-ky-tung-lophp?hocphan_id=871&idlop=20053&m=100
```

Thì nhập:

```text
hocphan_id = 871
idlop = 20053
```

---

## 🐞 Debug mode

Chạy:

```bash
vku-tool --debug
```

Debug giúp xem thêm:

- HTTP status code.
- Độ dài response.
- Một phần phản hồi từ server.

Nên dùng khi:

- Cookie hết hạn.
- Không lấy được danh sách môn.
- Không tìm thấy lớp.
- Đăng ký thất bại.
- Server trả về kết quả không rõ ràng.

---

## ❗ Lỗi thường gặp

### Không nhận lệnh `vku-tool`

Thử đóng terminal mở lại.

Hoặc chạy:

```bash
py -m vku_tool.cli
```

Nếu vẫn lỗi, cài lại:

```bash
py -m pip install -e .
```

---

### Không lấy được danh sách môn

Nguyên nhân thường gặp:

- Cookie sai.
- Cookie hết hạn.
- Chưa đăng nhập web.
- Hệ thống đang bảo trì.
- Mạng chập chờn.

Cách xử lý:

- Đăng nhập lại website.
- Lấy lại `XSRF-TOKEN` và `laravel_session`.
- Chạy lại tool.

---

### Không tìm thấy lớp học phần

Cách xử lý:

- Dùng chức năng 2 để xem đúng tên lớp.
- Copy đúng tên lớp hiển thị trong terminal.
- Dùng lại chức năng 3 hoặc 4.

---

### Cài từ GitHub không ra bản mới

Gỡ bản cũ:

```bash
py -m pip uninstall tooldktcvku -y
```

Cài lại:

```bash
py -m pip install --upgrade git+https://github.com/LeSyBach/ToolDktcVKU.git
```

---

## ✅ File nên đưa lên GitHub

Nên giữ:

```text
README.md
pyproject.toml
.gitignore
vku_tool/
```

Nếu code đã chuyển vào:

```text
vku_tool/cli.py
```

thì không cần giữ `tinchi.py` ở ngoài root.

---

## 🚫 File không nên đưa lên GitHub

Không nên commit:

```text
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.env
.venv/
venv/
```

Nội dung `.gitignore` gợi ý:

```gitignore
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.env
.venv/
venv/
.DS_Store
```

---

## 🚀 Đẩy thay đổi lên GitHub

Sau khi sửa code hoặc README:

```bash
git status
git add .
git commit -m "Update README"
git push origin main
```

---

## 🔒 Bảo mật

Cookie đăng nhập có giá trị như phiên đăng nhập tài khoản.

Không chia sẻ:

```text
XSRF-TOKEN
laravel_session
```

Không commit Cookie lên GitHub.

Không chụp màn hình chứa Cookie.

Nếu nghi ngờ Cookie bị lộ, hãy đăng xuất khỏi hệ thống và đăng nhập lại.

---

## ⚠️ Lưu ý sử dụng

- Chỉ dùng với tài khoản của chính bạn.
- Không dùng để spam request hoặc gây tải bất thường.
- Luôn kiểm tra lại kết quả trên website chính thức.
- Tuân thủ quy định đăng ký học phần của nhà trường.
- Tác giả không chịu trách nhiệm nếu người dùng sử dụng sai mục đích.

---

## 👤 Tác giả

**Lê Sỹ Bách**

- GitHub: `LeSyBach`
- Project: `ToolDktcVKU`
- Version: `7.0.0`

---

## 📄 Disclaimer

Dự án này chỉ phục vụ mục đích học tập và hỗ trợ thao tác cá nhân. Việc sử dụng công cụ phải tuân thủ quy định của hệ thống đào tạo và nhà trường.

<div align="center">

---

Made with Python ❤️ by **Lê Sỹ Bách**

</div>
