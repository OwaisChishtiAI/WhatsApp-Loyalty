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
        sql = f"SELECT place_name FROM ly_merchant_creds WHERE merchant_id = (SELECT MAX(merchant_id)\
             FROM ly_merchant_creds WHERE merchant_number = '{merchant_number}')"
        cursor.execute(sql)
        place_name = cursor.fetchone()[0]
        sql = f"UPDATE ly_merchant_creds SET username = '{username}'\
             WHERE merchant_number = '{merchant_number}' AND place_name = '{place_name}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT User Name", username, place_name)
        self.close()

    def put_password(self, password, merchant_number):
        cursor, db = self.pointer()
        sql = f"SELECT place_name FROM ly_merchant_creds WHERE merchant_id = (SELECT MAX(merchant_id)\
             FROM ly_merchant_creds WHERE merchant_number = '{merchant_number}')"
        cursor.execute(sql)
        place_name = cursor.fetchone()[0]
        sql = f"UPDATE ly_merchant_creds SET password = '{password}'\
             WHERE merchant_number = '{merchant_number}' AND place_name = '{place_name}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT Password", password, place_name)
        self.close()

    def put_points(self, points_offer, merchant_number):
        cursor, db = self.pointer()
        sql = f"SELECT place_name FROM ly_merchant_creds WHERE merchant_id = (SELECT MAX(merchant_id)\
             FROM ly_merchant_creds WHERE merchant_number = '{merchant_number}')"
        cursor.execute(sql)
        place_name = cursor.fetchone()[0]
        sql = f"UPDATE ly_merchant_creds SET points_offer = '{points_offer}'\
             WHERE merchant_number = '{merchant_number}' AND place_name = '{place_name}'"
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

    def get_check_secret_entry_with_number(self, customer_number, place):
        cursor = self.pointer()[0]
        sql = f"SELECT place FROM ly_merchant_secret WHERE customer_number = '{customer_number}' AND place = '{place}'"
        cursor.execute(sql)
        place = cursor.fetchone()
        self.close()

        if not place is None:
            return place[0]
        else:
            return None

    def post_merchant_secret_number_and_place(self,  customer_number, place):
        existing_record = self.get_check_secret_entry_with_number(customer_number, place)
        if existing_record is None:
            cursor, db = self.pointer()
            sql = "INSERT INTO ly_merchant_secret (customer_number, place, secret_code) VALUES (%s, %s, %s)"
            cursor.execute(sql, (customer_number, place, ""))
            db.commit()
            print("[INFO] POST SECRET-Number,Name")
            self.close()
        else:
            print("[INFO] Record for customer_name and place already exists in ly_merchant_secret")

    def put_merchant_secret_number_and_place(self, customer_number, secret_code):
        cursor, db = self.pointer()
        sql = f"SELECT place FROM ly_merchant_secret WHERE merchant_id = (SELECT MAX(merchant_id)\
             FROM ly_merchant_secret WHERE customer_number = '{customer_number}')"
        cursor.execute(sql)
        place = cursor.fetchone()[0]
        sql = f"UPDATE ly_merchant_secret SET secret_code = '{secret_code}'\
             WHERE customer_number = '{customer_number}' AND place = '{place}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT SECRET-Code")
        self.close()

    def get_merchant_secret_number_and_place(self, place, customer_number):
        cursor = self.pointer()[0]
        sql = f"SELECT secret_code FROM ly_merchant_secret WHERE place = '{place}' AND customer_number = '{customer_number}'"
        cursor.execute(sql)
        secret_code = cursor.fetchone()
        print("[INFO] GET SECRET CODE ", secret_code)
        self.close()

        if not secret_code is None:
            return secret_code[0]
        else:
            return None

# Merchant().put_user_name("imtiaz", "+923132609629")