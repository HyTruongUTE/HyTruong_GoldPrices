# Dự Án Thu Thập Dữ Liệu Giá Vàng Trên Trang PNJ

## Giới thiệu

Hiện nay, giá vàng biến đổi liên tục nên cần crawl giá vàng để dễ theo dõi và phân tích, dự đoán.

## Công nghệ sử dụng

- GitHub Actions: Tự động hóa việc thu thập dữ liệu, đảm bảo tính minh bạch và có thể theo dõi lịch sử thay đổi
- Python: Ngôn ngữ lập trình chính được sử dụng để crawl dữ liệu
- CSV: Định dạng lưu trữ dữ liệu

## Cấu trúc dữ liệu

Dữ liệu được lưu trữ trong các file CSV, được cập nhật định kỳ. Bạn có thể tìm thấy dữ liệu tại thư mục `result/`.

## Nguyên lý hoạt động

Dự án sử dụng bot tự động để thu thập dữ liệu từ trang web iqair.com với chu kỳ 1 giờ/lần. Các thông tin được thu thập bao gồm:
- Thời gian đo
- Loại vàng
- Giá mua vào
- Giá bán ra
- Thời gian cập nhật

### Cấu trúc dữ liệu chi tiết

Dữ liệu được tổ chức theo cấu trúc thư mục:
```
result/
├── gold_prices/
   ├── 
   ├──
   └── ...


Mỗi file CSV chứa các cột dữ liệu:
- `timestamp`: Thời gian lấy dữ liệu
- `city`: Tên thành phố
- `aqi`: Chỉ số chất lượng không khí
- `weather`: Điều kiện thời tiết
- `wind_speed`: Tốc độ gió
- `humidity`: Độ ẩm

## Hướng dẫn sử dụng

1. Clone repository này về máy:
```bash
git clone https://github.com/nghiahsgs/iqair-dataset.git
```

2. Dữ liệu thô được lưu trong thư mục `result/` dưới định dạng CSV
3. Bạn có thể sử dụng các công cụ như Power BI, Python, R để phân tích và trực quan hóa dữ liệu

## Hướng dẫn cài đặt và chạy dự án

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package installer)
- Chromium browser (sẽ được cài đặt tự động)

### Các bước cài đặt

Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

Cài đặt Chromium cho Playwright:
```bash
playwright install chromium
```

### Chạy dự án

1. Chạy script crawl dữ liệu:
```bash
python crawl_iqair.py
```

2. Dữ liệu sau khi crawl sẽ được lưu vào thư mục `result/` dưới dạng file CSV

### Lưu ý
- Script được thiết kế để chạy tự động mỗi giờ thông qua GitHub Actions
- Bạn có thể tùy chỉnh tần suất cập nhật trong file `.github/workflows/crawl.yml`
- Đảm bảo bạn có đủ quyền truy cập internet để script có thể lấy dữ liệu

## Tần suất cập nhật

Dữ liệu được cập nhật tự động mỗi giờ thông qua GitHub Actions, đảm bảo tính liên tục và độ tin cậy của dữ liệu.
