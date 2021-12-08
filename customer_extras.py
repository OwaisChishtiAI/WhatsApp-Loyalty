import json
import ast

from database import Connect

class CustomerExtras(Connect):
    def __init__(self, customer_number):
        self.customer_number = customer_number

    def get_last_visited_place(self):
        cursor = self.pointer()[0]
        sql = f"SELECT last_visited_place FROM ly_customer_extras WHERE customer_number = '{self.customer_number}'"
        cursor.execute(sql)
        customer_name = cursor.fetchone()
        print("[INFO] GET Customer Name", customer_name)
        self.close()
        
        if not customer_name is None:
            return customer_name[0]
        else:
            return None

    def post_put_last_visited_place(self, place):
        last_place = self.get_last_visited_place()
        cursor, db = self.pointer()
        if last_place:
            sql = f"UPDATE ly_customer_extras SET last_visited_place = '{place}' WHERE customer_number = '{self.customer_number}'"
            cursor.execute(sql)
            print("[INFO] PUT Last Visited Place")
        else:
            sql = "INSERT INTO ly_customer_extras (customer_number, last_visited_place, last_receipt_data) VALUES (%s, %s, %s)"
            cursor.execute(sql, (self.customer_number, place, ""))
            print("[INFO] POST Last Visited Place")
        db.commit()
        self.close()

    def put_last_receipt_data(self, json_data):
        json_data = json.dumps(json_data)
        cursor, db = self.pointer()
        sql = f"UPDATE ly_customer_extras SET last_receipt_data = '{json_data}' WHERE customer_number = '{self.customer_number}'"
        cursor.execute(sql)
        print("[INFO] PUT Last Receipt Data")
        db.commit()
        self.close()

    def get_last_receipt_data(self):
        cursor = self.pointer()[0]
        sql = f"SELECT last_receipt_data FROM ly_customer_extras WHERE customer_number = '{self.customer_number}'"
        cursor.execute(sql)
        last_receipt_data = cursor.fetchone()
        print("[INFO] GET Last Receipt Data", last_receipt_data)
        self.close()
        
        if last_receipt_data[0]:
            return ast.literal_eval(last_receipt_data[0])
        else:
            return None