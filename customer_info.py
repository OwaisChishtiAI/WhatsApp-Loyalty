import ast
import json

from database import Connect

class CustomerInfo(Connect):
    def get_customer_name(self, customer_number):
        cursor = self.pointer()[0]
        sql = f"SELECT customer_name FROM ly_customer_info WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        customer_name = cursor.fetchone()
        print("[INFO] GET Customer Name", customer_name)
        self.close()
        
        if not customer_name is None:
            return customer_name[0]
        else:
            return None

    def post_customer_name(self, customer_name, customer_number):
        cursor, db = self.pointer()
        sql = "INSERT INTO ly_customer_info (customer_number, customer_name, customer_points, places)\
             VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (customer_number, customer_name, 0, '[0]'))
        db.commit()
        print("[INFO] POST Customer Name")
        self.close()

    def get_places_list(self, customer_number):
        cursor = self.pointer()[0]
        sql = f"SELECT places FROM ly_customer_info WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        places = cursor.fetchone()
        self.close()
        if not places is None:
            places = places[0]
            places = ast.literal_eval(places)
            print("[INFO] GET Places", places)
            if places[0] != 0:
                return places
            else:
                return None
        else:
            return None

    def put_places_list(self, customer_number, place_name):
        previous_places = self.get_places_list(customer_number)
        if previous_places is not None:
            if place_name not in previous_places:
                previous_places.append(place_name)
            else:
                print(f"[INFO] Place {place_name} already exists.")
        else:
            previous_places = [place_name]
        previous_places = json.dumps(previous_places)
        
        cursor, db = self.pointer()
        sql = f"UPDATE ly_customer_info SET places = '{previous_places}' WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT Customer Name")
        self.close()

    def get_points_balance(self, customer_number):
        cursor = self.pointer()[0]
        sql = f"SELECT customer_points FROM ly_customer_info WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        points = cursor.fetchone()
        self.close()

        if not points is None:
            points = points[0]
            print("[INFO] GET Points", points)
            return int(points)
        else:
            return 0

    def put_points_balance(self, total_amount, customer_number):
        if int(total_amount) > 0:
            cursor, db = self.pointer()
            sql = f"UPDATE ly_customer_info SET customer_points = '{total_amount}' \
                WHERE customer_number = '{customer_number}'"
            cursor.execute(sql)
            db.commit()
            print("[INFO] PUT Customer Points")
            self.close()
        else:
            print("[INFO] Insufficient Amount to add", total_amount)

# print(CustomerInfo().get_customer_name('03132609629'))
# CustomerInfo().post_customer_name('owais', '03132609629')
# CustomerInfo().get_places_list('03132609629')
# CustomerInfo().post_places_list('03132609629', 'alabama')
# print(CustomerInfo().get_points_balance('03132609629'))
# CustomerInfo().put_points_balance(0, '03132609629')
# print(CustomerInfo().get_points_balance('03132609629'))