# Food-search
Ảnh được nhận dạng thông qua thuộc tính là biểu đồ tần suất màu sắc của ảnh.
Tiến hành xác định biểu đồ tần suất màu của vật thể trong ảnh bằng cách:
•	Xác định biểu đồ tần suất tích luỹ của 3 màu đỏ, xanh lá, xanh nước biển của toàn bộ ảnh. 
•	Sử dụng Canny để phát hiện biên. Qua đó tính được số pixel nằm ở vị trí nền (màu trắng). 
•	Trừ số lượng pixel tính được bên trên vào số lượng pixel có màu nền, ta tính được biểu đồ tần suất màu cho vật thể trong ảnh. 
•	Tính biểu đồ tần suất màu tích luỹ cho vật thể trong ảnh.


Hệ thống sẽ xác định 10 ảnh tương đồng với ảnh đầu vào nhất và print ra màn hình
