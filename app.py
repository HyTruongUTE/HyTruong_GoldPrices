import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Đường dẫn đến tệp CSV
data_path = './result/gold_prices/gold_prices_2025_feb.csv'

# Đọc dữ liệu từ tệp CSV
df = pd.read_csv(data_path, parse_dates=["timestamp"])

# Chuyển đổi cột giá thành số để dễ dàng xử lý
df['buy_price'] = df['buy_price'].replace({',': ''}, regex=True).astype(float)
df['sell_price'] = df['sell_price'].replace({',': ''}, regex=True).astype(float)

# Streamlit giao diện
st.title("Phân tích giá vàng")
st.markdown("### Tính năng lọc và phân tích")

# Lọc theo loại vàng
gold_types = df['gold_type'].unique()
selected_gold_type = st.selectbox("Chọn loại vàng", gold_types)

# Lọc theo khoảng thời gian
date_range = st.date_input("Chọn khoảng thời gian", 
                           min_value=df['timestamp'].min().date(),
                           max_value=df['timestamp'].max().date(),
                           value=(df['timestamp'].min().date(), df['timestamp'].max().date()))
filtered_df = df[(df['gold_type'] == selected_gold_type) & (df['timestamp'].dt.date >= date_range[0]) & (df['timestamp'].dt.date <= date_range[1])]

# Hiển thị dữ liệu lọc
st.write(f"Hiện thị dữ liệu của {selected_gold_type} từ {date_range[0]} đến {date_range[1]}")
st.dataframe(filtered_df)

# Vẽ biểu đồ giá mua bán
st.markdown("### Biểu đồ giá vàng mua bán")
fig, ax = plt.subplots(figsize=(12, 7))

# Vẽ đường "Giá mua"
ax.plot(filtered_df['timestamp'].values, filtered_df['buy_price'].values, label='Giá mua', color='green', linestyle='--', linewidth=2, marker='o', markersize=8)

# Vẽ đường "Giá bán"
ax.plot(filtered_df['timestamp'].values, filtered_df['sell_price'].values, label='Giá bán', color='red', linestyle='-', linewidth=2, marker='s', markersize=8)

# Thêm grid và tùy chỉnh
ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

# Tùy chỉnh trục x (Ngày tháng)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Chọn mỗi ngày 1 tick
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Chỉnh sửa nhãn trục
ax.set_xlabel("Ngày", fontsize=12)
ax.set_ylabel("Giá vàng (VND)", fontsize=12)
ax.set_title(f"Biểu đồ giá mua và bán của {selected_gold_type}", fontsize=14)

# Thêm legend
ax.legend(loc='upper left')

# Hiển thị biểu đồ
st.pyplot(fig)

# Thống kê cơ bản
st.markdown("### Thống kê cơ bản")
st.write(filtered_df.describe())
