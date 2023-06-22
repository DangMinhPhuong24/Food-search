import mysql.connector

# Tạo kết nối đến CSDL
def getConnection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="******",
        database="mmdb_demo"
    )
    return mydb

# Thêm tâm cụm vào csdl
def insertCentroid(data):
    mydb = getConnection()
    mycursor = mydb.cursor()

    sql = "INSERT INTO centroids ("
    for i in range(256):
        sql += "r_" + str(i) + ", "
    for i in range(256):
        sql += "g_" + str(i) + ", "
    for i in range(255):
        sql += "b_" + str(i) + ", "
    sql += "b_255)"

    sql += " VALUES ("
    for i in range(767):
        sql += "%s, "
    sql += "%s)"
    val = data
    mycursor.executemany(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "inserted.")
    mydb.close()

# Thêm bộ đặc trưng vào csdl
def insertFeatures(data):
    mydb = getConnection()
    mycursor = mydb.cursor()

    sql = "INSERT INTO features ("
    sql += "centroid_id, "
    for i in range(256):
        sql += "r_" + str(i) + ", "
    for i in range(256):
        sql += "g_" + str(i) + ", "
    for i in range(256):
        sql += "b_" + str(i) + ", "
    sql += "link)"

    sql += " VALUES ("
    for i in range(769):
        sql += "%s, "
    sql += "%s)"
    val = data
    mycursor.executemany(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "inserted.")
    mydb.close()

# Lấy toàn bộ dữ liệu của một bảng nào đó
def getAllData(table: str):
    mydb = getConnection()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM " + table)
    myresult = mycursor.fetchall()
    mydb.close()

    return myresult

# Xoá dữ liệu
def deleteAll(table: str):
    mydb = getConnection()
    mycursor = mydb.cursor()
    sql = "DELETE FROM " + table
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    mydb.close()

# Cập nhập dữ liệu bảng đặc trưng
def updateFeatures(data):
    mydb = getConnection()
    mycursor = mydb.cursor()

    sql = "UPDATE features SET centroid_id = %s WHERE id = %s"
    val = (data[1], data[0])
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()

# Lấy dữ liệu đặc trưng thuộc cụm nào đó
def getFeaturesData(centroid_id: int):
    mydb = getConnection()
    mycursor = mydb.cursor()

    sql = "SELECT * FROM features WHERE centroid_id = " +  str(centroid_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mydb.close()
    return myresult