import numpy as np
from pathlib import Path
from rembg import remove
from PIL import Image
from skimage import feature
import os
from sklearn.cluster import KMeans
from skimage import io
import mysql_connection
import cv2

# Cac ham trich dac trung
# Xác định biểu đồ tần xuất tích luỹ
def acc_his(arr):
    new_arr = []
    s = sum(arr)
    v = 0
    for i in range(len(arr)):
        v += arr[i]
        new_arr.append(v*100/s)
    return new_arr

# Tạo nền trắng
def changeWhiteBG(url: str):
    path = Path(url)
    in_img = Image.open(path)
    out_img = remove(in_img)
    white_bg = Image.new("RGBA", size=in_img.size, color=(255, 255, 255))
    white_bg.paste(out_img, (0, 0), mask=out_img)
    new_img = white_bg.convert("RGB")
    new_img.save(path)

# Xác định bộ đặc trưng của ảnh
def getFeature(url: str):
    # Đọc dữ liệu ảnh
    path = Path(url)
    img = Image.open(path)
    
    # Lay 3 kenh mau r, g, b
    wr = img.getdata(band=0)
    wg = img.getdata(band=1)
    wb = img.getdata(band=2)

    # Xac dinh bien canny
    gray_img = img.convert("L")
    matrix = np.array(gray_img.getdata()).reshape(gray_img.size)
    edge_canny = feature.canny(matrix, low_threshold=10, high_threshold=30)
    height, width = img.size

    # Tinh so pixel nam o khu vuc nen
    co = 0
    for i in range(height):
        if not any(edge_canny[i]):
            co += width
            continue
        limit = 0
        for j in range(width):
            if edge_canny[i][j] == True:
                limit = j
                break
            else:
                co += 1
        for j in range(width-1, limit, -1):
            if edge_canny[i][j] == True:
                # print(i, j)
                break
            else:
                co += 1

    # Xay dung bieu do tan xuat cho 3 kenh mau
    r_his = wr.histogram()
    g_his = wg.histogram()
    b_his = wb.histogram()
    bg_pixel = min(co, r_his[255], g_his[255], b_his[255])
    r_his[255] = r_his[255] - bg_pixel
    g_his[255] = g_his[255] - bg_pixel
    b_his[255] = b_his[255] - bg_pixel

    # Xay dung bo dac trung
    image_feature = []
    image_feature += acc_his(r_his)
    image_feature += acc_his(g_his)
    image_feature += acc_his(b_his)
    # print(len(image_feature))
    return image_feature

# Cac ham tim anh tương đồng
# Xác định khoảng cách giữa các bộ đặc trưng
def square_distance(a: list, b: list):
    val = 0
    for i in range(len(a)):
        val += (a[i] - b[i])**2
    return val

# Hàm tìm tâm cụm gần nhất
def findCentroid(centroids):
    min_distance = -1
    center = -1
    for i in centroids.keys():
        if (min_distance < 0) or (min_distance > centroids[i]):
            min_distance = centroids[i]
            center = i
    centroids.pop(center)
    return center

# def showInTerminal(path):
#     img = io.imread(Path(path))
#     io.imshow(img)

# Hàm tìm ảnh tương đồng
def findSimilarImg(imgFeature):
    # Lấy ra dữ liệu tâm cụm từ csdl
    savedCentroids = mysql_connection.getAllData(table="centroids")
    disDict = {}
    for i in savedCentroids:
        # Lưu thông tin khoảng cách của ảnh mới đối với từng tâm
        disDict[i[0]] = square_distance(i[1:], imgFeature)
    count = 10

    # Lặp đến khi đủ 10 ảnh
    featureDict = {}
    distance = []
    while len(featureDict) < count:
        center = findCentroid(disDict)
        results = mysql_connection.getFeaturesData(centroid_id=center)
        for re in results:
            featureDict[re[0]] = re
            distance.append([re[0], square_distance(re[2:770], imgFeature)])

    # Chọn ra 10 ảnh tương đồng nhất
    distance = sorted(distance, key=lambda l:l[1], reverse=False)
    for i in range(count):
        id = distance[i][0]
        # print(id)
        img = featureDict[id][-1]
        print(i+1, img)
        print()
        # showInTerminal(img)


# Chạy thuật toán
print()
print("-----Bat dau chay-----")
print()
while True:
    input_str = input("\nNhap Y hoac y de bat dau: ")

    if (input_str.strip().lower() != "y"):
        break
    
    path = input("\nNhap duong dan anh: \n").strip()
    path = path.replace("\\", "\\\\")

    try:
        Image.open(path)
    except:
        print("\nCo loi xay ra.")
    else:
        imgFeature = getFeature(url=path)
        # print(imgFeature)
        # showInTerminal(path=path)
        print("\nCac anh tuong dong (giam dan): \n")
        findSimilarImg(imgFeature=imgFeature)
print()
print("-----Dung chay-----")
print()

# path = "D:\Projects\Multimedia-DB\photo-test\\banh-chung.jpg"
# path = path.replace("\\", "\\\\")


