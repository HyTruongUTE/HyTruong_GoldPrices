from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import csv
import os
import pathlib
from zoneinfo import ZoneInfo

# URL của trang giá vàng PNJ
URL = "https://www.pnj.com.vn/site/gia-vang"

def get_vietnam_time():
    """Lấy thời gian hiện tại theo múi giờ Việt Nam (GMT+7)"""
    return datetime.now(ZoneInfo("Asia/Bangkok"))

def crawl_gold_prices(page):
    """Hàm crawl giá vàng từ trang PNJ"""
    print(f"Truy cập trang: {URL}")

    try:
        # Điều hướng tới URL
        page.goto(URL)

        # Chờ cho dữ liệu tải hoàn toàn
        page.wait_for_selector("table")

        # Lấy ngày cập nhật
        date_element = page.query_selector("p.text-sm.text-gray-400.mt-1")
        update_time = date_element.text_content().strip() if date_element else "Không có thông tin"

        # Lấy danh sách tất cả các hàng trong bảng giá vàng
        rows = page.query_selector_all("table tbody tr")
        if not rows:
            print("Không tìm thấy dữ liệu giá vàng!")
            return None
        
        gold_prices = []
        for row in rows:
            columns = row.query_selector_all("td")
            if len(columns) < 3:
                continue  # Bỏ qua nếu không đủ dữ liệu

            # Lấy dữ liệu từ từng cột
            gold_type = columns[0].text_content().strip()  # Loại vàng
            buy_price = columns[1].text_content().strip()  # Giá mua
            sell_price = columns[2].text_content().strip()  # Giá bán

            gold_prices.append({
                "timestamp": get_vietnam_time().isoformat(),
                "gold_type": gold_type,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "update_time": update_time
            })
        
        return gold_prices

    except Exception as e:
        print(f"Lỗi khi crawl giá vàng: {str(e)}")
        return None

def save_to_csv(data):
    """Lưu dữ liệu vào file CSV"""
    if not data:
        print("Không có dữ liệu để lưu!")
        return None

    now = get_vietnam_time()
    result_dir = pathlib.Path("result/gold_prices")
    result_dir.mkdir(parents=True, exist_ok=True)

    filename = f"gold_prices_{now.year}_{now.strftime('%b').lower()}.csv"
    filepath = result_dir / filename

    headers = ["timestamp", "gold_type", "buy_price", "sell_price", "update_time"]

    file_exists = filepath.exists()

    with open(filepath, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        
        if not file_exists:
            writer.writeheader()  # Ghi header nếu file chưa tồn tại
        
        writer.writerows(data)  # Ghi dữ liệu

    print(f"Dữ liệu đã được lưu vào: {filepath}")

def main():
    """Hàm chính để chạy toàn bộ quá trình crawl và lưu dữ liệu"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Crawl giá vàng từ trang PNJ
            gold_prices = crawl_gold_prices(page)

            # Lưu dữ liệu vào CSV
            save_to_csv(gold_prices)

            # Hiển thị dữ liệu đã crawl
            print("\nDữ liệu giá vàng:")
            print(json.dumps(gold_prices, indent=2, ensure_ascii=False))

            browser.close()

    except Exception as e:
        print(f"Lỗi khi chạy crawler: {str(e)}")

if __name__ == "__main__":
    main()
