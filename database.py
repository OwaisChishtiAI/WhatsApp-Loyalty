import pymysql.cursors

class Connect:
    def pointer(self):
        mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="loyalty",
        )
        self.db = mydb
        self.cursor = self.db.cursor()
        print("[INFO] Connected to Data base.")
        return (self.cursor, self.db)

    def close(self):
        self.cursor.close()
        self.db.close()

    def test_connection(self):
        cursor = self.pointer()[0]
        sql = "SELECT * FROM ly_customer_info"
        cursor.execute(sql)
        myresult = cursor.fetchall()
        print("[INFO] Connection Successful.", myresult)
        self.close()
