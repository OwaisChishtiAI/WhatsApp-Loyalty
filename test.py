import requests

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
            elif 'exit' in take:
                self.talk = False
                response = "Bye!"
            else:
                response = self.api(take, 'text')
            print("Bot Says: ", response)

Test('whatsapp:+923132609629').run()
# a = {'1' : 'Love your service 😍', "2" : 'Service was good 😃', '3' : 'It was ok 😐','4' : 'Dissapointing service 😔', '5' : 'Really upset 😤'}
