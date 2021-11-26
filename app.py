import os
from dotenv import load_dotenv
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from customer_journey import CustomerJourney
from chatbot import ChatBot

load_dotenv()
# print(os.environ.get("TWILIO_ACCOUNT_SID"))

app = Flask(__name__)
client = Client()

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

@app.route('/message', methods=['POST'])
def reply():
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0') 
    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        customer_number = sender.split(':')[1]  # remove the whatsapp: prefix from the number
        if content_type == 'image/jpeg':
            filename = f'uploads/{customer_number}/{message}.jpg'
        elif content_type == 'image/png':
            filename = f'uploads/{customer_number}/{message}.png'
        elif content_type == 'image/gif':
            filename = f'uploads/{customer_number}/{message}.gif'
        else:
            filename = None
        if filename:
            if not os.path.exists(f'uploads/{customer_number}'):
                os.mkdir(f'uploads/{customer_number}')
            with open(filename, 'wb') as f:
                f.write(r.content)
            return respond('Thank you! Your image was received.')
        else:
            return respond('The file that you submitted is not a supported image type.')
    else:
        print("[User Message] ", message)
        customer_number = sender.split(':')[1]
        print("[User Name] ", customer_number)

    next_state = CustomerJourney().get_next_state(customer_number)
    chatbot = ChatBot(customer_number)
    if next_state is None:
        reply = chatbot.welcome_message()
        CustomerJourney().post_customer_number(customer_number)
        CustomerJourney().put_states(reply['state'], reply['next_state'], customer_number)
        return respond(reply['message'])
    else:
        if next_state == "confirm_uploaded_recipt":
            reply = eval("chatbot." + next_state)
        else:
            reply = eval("chatbot." + next_state)(message)
        CustomerJourney().put_states(reply['state'], reply['next_state'], customer_number)
        return respond(reply['message'])

if __name__ == "__main__":
  app.run(debug=True)