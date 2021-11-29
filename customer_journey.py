from database import Connect
from datetime import datetime

class CustomerJourney(Connect):
    
    def get_next_state(self, customer_number):
        cursor = self.pointer()[0]
        sql = f"SELECT next_state, created_at FROM ly_customer_journey WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        next_state = cursor.fetchone()
        print("[INFO] GET Next State", next_state)
        self.close()
        if not next_state is None:
            return (next_state[0], next_state[1])
        else:
            return (None, None)

    def post_customer_number(self, customer_number):
        next_state = self.get_next_state(customer_number)[0]
        if next_state:
            self.put_states('welcome_state', 'greetings_state', customer_number)
        else:
            cursor, db = self.pointer()
            sql = "INSERT INTO ly_customer_journey (customer_number, current_state, next_state)\
                VALUES (%s, %s, %s)"
            cursor.execute(sql, (customer_number, '', ''))
            db.commit()
            print("[INFO] POST Customer Number")
            self.close()

    def put_states(self, current_state, next_state, customer_number):
        cursor, db = self.pointer()
        sql = f"UPDATE ly_customer_journey SET current_state = '{current_state}', next_state = '{next_state}', \
            created_at = '{datetime.now()}' WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT States")
        self.close()

class CustomerRatings(Connect):
    def post_rating(self, rating, customer_number):
        cursor, db = self.pointer()
        sql = "INSERT INTO ly_customer_ratings (customer_number, ratings, created_at)\
            VALUES (%s, %s, %s)"
        cursor.execute(sql, (customer_number, rating, datetime.now()))
        db.commit()
        print("[INFO] POST Customer Rating")
        self.close()

# print(CustomerJourney().get_next_state('03132609629'))
# CustomerJourney().post_customer_number('03132609629')
# CustomerJourney().put_states('a', 'b','03132609629')
# print(CustomerJourney().get_next_state('03132609629'))