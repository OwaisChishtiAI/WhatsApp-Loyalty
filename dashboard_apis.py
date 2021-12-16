import json
import ast

from database import Connect

class DashBoardAPI(Connect):
    def admin_login_api(self, username, password):
        cursor = self.pointer()[0]
        sql = f"SELECT admin_id FROM ly_admin_login WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(sql)
        admin_id = cursor.fetchone()
        print("[INFO] GET Admin ID", admin_id)
        self.close()
        
        if not admin_id is None:
            return admin_id[0]
        else:
            return "None"

    def get_admin_customer_info_table(self):
        all_records = []
        cursor = self.pointer()[0]
        sql = f"SELECT *  FROM ly_customer_info"
        cursor.execute(sql)
        customer_records = cursor.fetchall()
        print("[INFO] GET Customer Info Records", customer_records)
        self.close()

        for i in range(len(customer_records)):
            individual_record = {}
            individual_record['customer_id'] = customer_records[i][0]
            individual_record['customer_number'] = customer_records[i][1]
            individual_record['customer_name'] = customer_records[i][2]
            individual_record['customer_points'] = customer_records[i][3]
            places = ast.literal_eval(customer_records[i][4])
            if len(places) == 1 and places[0] == 0:
                customer_places = "No Places"
            else:
                customer_places = ",".join(places)
            individual_record['places'] = customer_places
            
            all_records.append(individual_record)

        return all_records

    def put_admin_customer_info_table(self, record):
        cursor, db = self.pointer()
        record['places'] = json.dumps(record['places'].split(","))
        sql = "UPDATE ly_customer_info SET "
        for i in range(len(record.values())):
            if not list(record.keys())[i] == "customer_id":
                sql = sql + "{0} = '{1}', ".format(list(record.keys())[i], list(record.values())[i])
        sql = sql[:-2] + " "
        sql = sql + "WHERE {0} = '{1}'".format("customer_id", record['customer_id'])
        cursor.execute(sql)
        db.commit()
        print("[INFO] UPDATE Customer Info Records", record)
        self.close()

    def delete_admin_customer_info_table(self, record_id):
        cursor, db = self.pointer()
        sql = f"DELETE FROM ly_customer_info WHERE customer_id='{record_id}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] DELETE Customer Info Record", record_id)
        self.close()

    def get_admin_customer_ratings_table(self):
        all_records = []
        cursor = self.pointer()[0]
        sql = f"SELECT *  FROM ly_customer_ratings"
        cursor.execute(sql)
        ratings_records = cursor.fetchall()
        print("[INFO] GET Customer Ratings Records", ratings_records)
        self.close()

        for i in range(len(ratings_records)):
            individual_record = {}
            individual_record['customer_number'] = ratings_records[i][1]
            individual_record['ratings'] = ratings_records[i][2]
            individual_record['created_at'] = str(ratings_records[i][3])
            individual_record['stars'] = ratings_records[i][4]
            all_records.append(individual_record)

        return all_records

    def get_admin_merchant_creds_table(self):
        all_records = []
        cursor = self.pointer()[0]
        sql = f"SELECT place_name, merchant_number, points_offer  FROM ly_merchant_creds"
        cursor.execute(sql)
        merchant_info = cursor.fetchall()
        print("[INFO] GET Merchant Info", merchant_info)
        self.close()

        for i in range(len(merchant_info)):
            individual_record = {}
            individual_record['place_name'] = merchant_info[i][0]
            individual_record['merchant_number'] = merchant_info[i][1]
            individual_record['points_offer'] = merchant_info[i][2]
            all_records.append(individual_record)

        return all_records

    def get_store_status(self):
        cursor = self.pointer()[0]
        sql = f"SELECT * FROM ly_merchant_place_verification"
        cursor.execute(sql)
        records = cursor.fetchall()
        print("[INFO] GET Store Status", records)
        self.close()

        all_records = []
        for i in range(len(records)):
            individual_record = {}
            individual_record['merchant_id'] = records[i][0]
            individual_record['merchant_number'] = records[i][1]
            individual_record['place'] = records[i][2]
            individual_record['status'] = records[i][3]
            all_records.append(individual_record)

        return all_records

    def put_store_status(self, status, merchant_number):
        cursor, db = self.pointer()
        sql = f"SELECT place FROM ly_merchant_place_verification WHERE merchant_id = (SELECT MAX(merchant_id)\
             FROM ly_merchant_place_verification WHERE merchant_number = '{merchant_number}')"
        cursor.execute(sql)
        place_name = cursor.fetchone()[0]
        sql = f"UPDATE ly_merchant_place_verification SET status = '{status}'\
             WHERE merchant_number = '{merchant_number}' AND place = '{place_name}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT Store Status", status, place_name)
        self.close()


# print(DashBoardAPI().put_store_status('live', '23232'))