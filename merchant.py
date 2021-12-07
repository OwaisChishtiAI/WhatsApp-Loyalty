from database import Connect

class Merchant(Connect):
    def post_store_name(self, store_name, merchant_number):
        cursor, db = self.pointer()
        sql = "INSERT INTO ly_merchant_creds (place_name, username, password, merchant_number, points_offer)\
             VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (store_name, '', '', merchant_number, 0))
        db.commit()
        print("[INFO] POST Store Name")
        self.close()

    def get_store_name(self, store_name):
        cursor = self.pointer()[0]
        sql = f"SELECT place_name FROM ly_merchant_creds WHERE place_name = '{store_name}'"
        cursor.execute(sql)
        store_name = cursor.fetchone()
        print("[INFO] GET Store Name", store_name)
        self.close()

        if not store_name is None:
            return store_name[0]
        else:
            return None

    def put_user_name(self, username, merchant_number):
        cursor, db = self.pointer()
        sql = f"UPDATE ly_merchant_creds SET username = '{username}'\
             WHERE merchant_number = '{merchant_number}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT User Name")
        self.close()

    def put_password(self, password, merchant_number):
        cursor, db = self.pointer()
        sql = f"UPDATE ly_merchant_creds SET password = '{password}'\
             WHERE merchant_number = '{merchant_number}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT Password")
        self.close()

    def put_points(self, points_offer, merchant_number):
        cursor, db = self.pointer()
        sql = f"UPDATE ly_merchant_creds SET points_offer = '{points_offer}'\
             WHERE merchant_number = '{merchant_number}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT Points Offer")
        self.close()

    def get_username(self, merchant_number):
        cursor = self.pointer()[0]
        sql = f"SELECT username FROM ly_merchant_creds WHERE merchant_number = '{merchant_number}'"
        cursor.execute(sql)
        username = cursor.fetchone()
        print("[INFO] GET User Name", username)
        self.close()

        if not username is None:
            return username[0]
        else:
            return None

    def get_password(self, merchant_number):
        cursor = self.pointer()[0]
        sql = f"SELECT password FROM ly_merchant_creds WHERE merchant_number = '{merchant_number}'"
        cursor.execute(sql)
        password = cursor.fetchone()
        print("[INFO] GET Pasword", password)
        self.close()

        if not password is None:
            return password[0]
        else:
            return None

    def get_points(self, merchant_number):
        cursor = self.pointer()[0]
        sql = f"SELECT points_offer FROM ly_merchant_creds WHERE merchant_number = '{merchant_number}'"
        cursor.execute(sql)
        points = cursor.fetchone()
        print("[INFO] GET Points", points)
        self.close()

        if not points is None:
            return points[0]
        else:
            return None

    def get_points_by_place_name(self, place_name):
        cursor = self.pointer()[0]
        sql = f"SELECT points_offer FROM ly_merchant_creds WHERE place_name = '{place_name}'"
        cursor.execute(sql)
        points = cursor.fetchone()
        print("[INFO] GET Points By Name ", points, place_name)
        self.close()

        if not points is None:
            return points[0]
        else:
            return None