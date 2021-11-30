from flask.wrappers import Response
import requests
from torch.utils import data

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