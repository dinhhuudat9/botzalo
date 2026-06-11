# Dự án Zalo Bot (Python + Flask)

Đây là một dự án mẫu để tạo webhook cho Zalo Official Account (OA) và dễ dàng triển khai (deploy) lên [Render](https://render.com).

## Cấu trúc thư mục
- `app.py`: Code chính xử lý server webhook và nhận tin nhắn từ Zalo.
- `requirements.txt`: Danh sách các thư viện Python cần thiết (`Flask`, `requests`, `gunicorn`).

## Cách triển khai lên Render.com

1. Đẩy mã nguồn này lên một kho lưu trữ **GitHub**.
2. Đăng nhập vào [Render.com](https://render.com) và chọn **New -> Web Service**.
3. Kết nối với kho GitHub của bạn chứa code này.
4. Ở phần thiết lập (Settings) trên Render:
   - **Environment**: Chọn `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Mở phần **Environment Variables** (Biến môi trường) trên Render và thêm biến sau:
   - Key: `ZALO_OA_ACCESS_TOKEN`
   - Value: `(Mã Access Token của Zalo OA của bạn lấy từ trang Zalo For Developers)`
6. Bấm **Create Web Service**. 
7. Sau khi Render deploy xong, bạn sẽ nhận được một đường dẫn (URL), ví dụ: `https://your-bot-name.onrender.com`.

## Cấu hình trên Zalo for Developers
1. Truy cập [Zalo for Developers](https://developers.zalo.me/).
2. Chọn ứng dụng của bạn và Official Account liên kết.
3. Trong phần cấu hình Webhook, nhập URL Webhook của bạn:
   `https://your-bot-name.onrender.com/webhook`
4. Cấp quyền nhận tin nhắn cho ứng dụng Zalo của bạn.

Bây giờ bạn có thể chat với Zalo OA của mình và Bot sẽ tự động trả lời!
