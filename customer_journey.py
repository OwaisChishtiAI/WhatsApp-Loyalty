from database import Connect

class CustomerJourney(Connect):
    
    def get_next_state(self, customer_number):
        cursor = self.pointer()[0]
        sql = f"SELECT next_state FROM ly_customer_journey WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        next_state = cursor.fetchone()
        print("[INFO] GET Next State", next_state)
        self.close()
        if not next_state is None:
            return next_state[0]
        else:
            return None

    def post_customer_number(self, customer_number):
        cursor, db = self.pointer()
        sql = "INSERT INTO ly_customer_journey (customer_number, current_state, next_state)\
             VALUES (%s, %s, %s)"
        cursor.execute(sql, (customer_number, '', ''))
        db.commit()
        print("[INFO] POST Customer Number")
        self.close()

    def put_states(self, current_state, next_state, customer_number):
        cursor, db = self.pointer()
        sql = f"UPDATE ly_customer_journey SET current_state = '{current_state}', next_state = '{next_state}' \
            WHERE customer_number = '{customer_number}'"
        cursor.execute(sql)
        db.commit()
        print("[INFO] PUT States")
        self.close()

# print(CustomerJourney().get_next_state('03132609629'))
# CustomerJourney().post_customer_number('03132609629')
# CustomerJourney().put_states('a', 'b','03132609629')
# print(CustomerJourney().get_next_state('03132609629'))