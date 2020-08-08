# MÔ TẢ ĐỒ ÁN
## 1.	Mô tả bài toán
-	Tên bài toán: Dự đoán kết quả trận đấu dựa trên chỉ số đánh giá của Fifa.
-	Input: Thông tin trận đấu bao gồm: chỉ số của 22 cầu thủ, lịch sử đấu.
-	Ouput: Kết quả thắng, thua , hòa của đội nhà.

## 2.	Mô tả bộ dữ liệu
Cách thức xây dựng bộ dữ liệu: 
 - Dữ liệu lấy của 4 giải đấu (EPL, Laliga, Bundesliga, Serie A) của 10 mùa giải 2010 - 2020
 -	Dùng `webs craper`, `scrapy` để crawl dữ liệu từ trang web.
 -	Lấy dữ liệu về chỉ số cầu thủ từ trang web: https://www.fifaindex.com/
 - Lấy dữ liệu về trận đấu (tên 2 đội, ngày giờ thi đấu, đội hình của 2 đội) từ trang web: https://www.skysports.com/
 - Số lượng: 14.192 trận đấu, 23.861 cầu thủ.

Các thao tác tiền xử lý dữ liệu:
 - Đồng bộ tên đội bóng của 2 bộ dữ liệu.
 - Gán ID cho mỗi đội để dễ truy cập.
 - Tạo dictionary quản lý các cầu thủ mỗi đội mỗi mùa giải.
 - Từ thông tin về đội hình mỗi trận đấu, đồng bộ với chỉ số của cầu thủ của mùa giải đó.
 
Phân chia dữ liệu 75% train, 25% test.

## 3.	Mô tả về đặc trưng
22 chỉ số của 22 cầu thủ. 

Lịch sử đấu của hai đội trong 5 trận gần nhất: số nguyên a1, a2, b1, b2 tương ứng số trận thắng, hòa của đội nhà, đội khách.

**Input:** là một mảng số nguyên 38 phần tử. Trong đó 36 phần tử đầu chia đều cho 2 đội (vì đội hình các trận đấu của các đội khác nhau nên ta sẽ dành trong đó 1 phần tử cho chỉ số thủ môn, 6 phần tử tiếp theo cho chỉ số hậu vệ, 7 phần tử tiếp theo cho các tiền vệ, và 4 cho các tiền đạo). Các phần tử tiếp theo đại diện các các chỉ số lịch sử đấu.

**Ouput:** 1 – thắng, 0 – hòa, -1 – thua.

## 4.	Thuật toán máy học: Thử các thuật toán: KNN, SVM, Logistic Regression, Neural Network

## 5.	Tinh chỉnh tham số: sử dụng GridSearchCV của scikit-learn để thử qua các tham số.

## 6. Kết quả dự đoán: 
f1-score = 53%

