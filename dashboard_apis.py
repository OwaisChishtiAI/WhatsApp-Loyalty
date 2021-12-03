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

# DashBoardAPI().admin_customer_info_table()        