import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Thông tin từ ứng dụng Zalo của bạn (Đã điền sẵn từ ảnh bạn gửi)
ZALO_APP_ID = os.environ.get("ZALO_APP_ID", "994176035432772032")
ZALO_APP_SECRET = os.environ.get("ZALO_APP_SECRET", "JQ44Drb2Do4OW61qyVO6")

# Access Token và Refresh Token
ZALO_ACCESS_TOKEN = os.environ.get("ZALO_ACCESS_TOKEN", "m_lz6jSx9sp7-VyOr3ebRyRx-nt8JK0LhVZf2ljED2JiouuUl1SKFAxMdIN8Ra06WCQQBFG5E5c3jeLOcd9P89VfyncEVKy9dzhg4-eQG7wOjC1JYG919zo_WJM833KRcOo05EeEA27wog4hut4lAO7ccb7pN3X6lUcNCAfCDZlJvvOmYNq35igqZ1ZP1onre9sO1D4_J0kUXiaPtJeLAuo-YnsLEqidpu_e0y8wDdIkk8rHp0KpQO6nZ73r6XK5je6VA-CU6Zgcshapm78M0wxPmYJMObenXyd38CLWLmITvjOZ-YLqBh6Es074KdOlW_p-BlfbJ06g_jKvttzi2gZgznZTALKQkA7QBCXfKoYIruet_bGzE3aWyUr0roGfOm")
ZALO_REFRESH_TOKEN = os.environ.get("ZALO_REFRESH_TOKEN", "AXnuMBdKiG4k7dfQkjMp0YySVb-cayL1ELyF7j_lWnaXU0mKpD777L9aVG6uhjeFRW8JBv-Hr0zhAc8ilUhHC2frOIR3kT8xINGL5fdRip5yOGSyi_wj6r9A2a2DyS9k76DqHjclnnX86rn5YANkVHqP94BjWx1S1Ji00CgEaGTSHZTSo--TPpf7CJsfyuDhTtWJPPZZtJjhNHKTbEUXDtOi1Iw6axvqSoGuL8sCgGDz3oSMbw7h45bXGZgxhOmCI1qm2O2sY2ni70mkeRB1C4zuLnERwy8ZI4DUTTlFw4LDNqbYtvVk82iZHXxXzzP4Aaj-Sz_JwaL0RY9jjFkpLaCxB068i-1RRd9kHbQd-VvlkSk_3W")

def get_new_access_token():
    """Lấy Access Token mới từ Refresh Token"""
    global ZALO_ACCESS_TOKEN, ZALO_REFRESH_TOKEN
    
    if not ZALO_REFRESH_TOKEN:
        print("Lỗi: Không có ZALO_REFRESH_TOKEN để lấy token mới.")
        return False
        
    url = "https://oauth.zaloapp.com/v4/oa/access_token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "secret_key": ZALO_APP_SECRET
    }
    data = {
        "refresh_token": ZALO_REFRESH_TOKEN,
        "app_id": ZALO_APP_ID,
        "grant_type": "refresh_token"
    }
    
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    
    if "access_token" in result:
        ZALO_ACCESS_TOKEN = result["access_token"]
        ZALO_REFRESH_TOKEN = result.get("refresh_token", ZALO_REFRESH_TOKEN)
        print("Đã làm mới Access Token thành công!")
        return True
    else:
        print("Lỗi khi làm mới token:", result)
        return False

def send_zalo_message(user_id, text):
    """Hàm gửi tin nhắn phản hồi qua Zalo OA API"""
    global ZALO_ACCESS_TOKEN
    
    if not ZALO_ACCESS_TOKEN and ZALO_REFRESH_TOKEN:
        print("Không có Access Token. Đang thử làm mới...")
        get_new_access_token()

    url = "https://openapi.zalo.me/v3.0/oa/message/cs"
    headers = {
        "Content-Type": "application/json",
        "access_token": ZALO_ACCESS_TOKEN
    }
    payload = {
        "recipient": {
            "user_id": user_id
        },
        "message": {
            "text": text
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    # Mã lỗi -216 của Zalo nghĩa là Access Token đã hết hạn
    if result.get("error") == -216 and ZALO_REFRESH_TOKEN:
        print("Access Token hết hạn. Đang làm mới...")
        if get_new_access_token():
            headers["access_token"] = ZALO_ACCESS_TOKEN
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
    return result

@app.route("/", methods=["GET"])
def home():
    """Route kiểm tra bot có đang chạy không"""
    return """
    <html>
      <head>
        <meta name="zalo-platform-site-verification" content="lUE_2977QGXdx-u8kUTa84NNoXQfeHz1CJWm" />
      </head>
      <body>
        Zalo Bot is running on Render with Auto-Refresh Token!
      </body>
    </html>
    """, 200

@app.route("/zalo_verifierlUE_2977QGXdx-u8kUTa84NNoXQfeHz1CJWm.html", methods=["GET"])
def zalo_verifier():
    """Endpoint để Zalo xác thực domain"""
    return "lUE_2977QGXdx-u8kUTa84NNoXQfeHz1CJWm", 200

@app.route("/webhook", methods=["POST", "GET"])
def zalo_webhook():
    """Endpoint Webhook để Zalo gửi sự kiện về"""
    if request.method == "GET":
        return jsonify({"status": "success"}), 200

    data = request.json
    print("Nhận sự kiện từ Zalo:", data)
    
    event_name = data.get('event_name')
    
    # Xử lý sự kiện người dùng gửi tin nhắn
    if event_name == 'user_send_text':
        sender_id = data.get('sender', {}).get('id')
        message_text = data.get('message', {}).get('text')
        
        print(f"Tin nhắn từ {sender_id}: {message_text}")
        
        # Phản hồi lại tin nhắn
        reply_text = f"Bot đã nhận được tin nhắn của bạn: '{message_text}'"
        send_zalo_message(sender_id, reply_text)
        
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
