# from flask.wrappers import Response
import requests
# from torch.utils import data
from database import Connect

BASE_URL = "http://localhost:5000/message"

class Test:
    def __init__(self, customer_number):
        self.customer_number = customer_number
        self.talk = True

    def api(self, msg, type):
        if type == "text":
            body = {'From' : self.customer_number, 'Body' : msg}
        elif type == "media":
            body = {'From' : self.customer_number, 'MediaUrl0' : msg}
        else:
            raise(f"Invalid type {type}")

        response = requests.post(BASE_URL, data=body)

        return response.text

    def run(self):
        while(self.talk):
            take = input("> ")
            if 'http' in take:
                response = self.api(take, 'media')
            else:
                response = self.api(take, 'text')
            print("Bot Says: ", response)

Test('whatsapp:+923132609629').run()
# a = {'1' : 'Love your service 😍', "2" : 'Service was good 😃', '3' : 'It was ok 😐','4' : 'Dissapointing service 😔', '5' : 'Really upset 😤'}
# print(a['1'][-1])
# python app.py dev ip 5000
# self = Connect()
# cursor = self.pointer()[0]
# sql = "SELECT place_name FROM ly_merchant_creds"
# cursor.execute(sql)
# places = cursor.fetchall()
# self.close()
# if all(places):
#     print ([x[0] for x in places])
# else:
#     print ("None")
# print(places)