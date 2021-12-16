from datetime import datetime, time
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading
import sys

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from customer_journey import CustomerJourney
from chatbot import ChatBot
if sys.argv[1] != 'dev':
    from ocr_extractor import OCR
else:
    class OCR:
        def __init__(self) -> None:
            return None
    print("DEV SERVER...")
from dashboard_apis import DashBoardAPI

# For NanoNets API
from ocr_nanonets import NanoNetsOCR

load_dotenv()
# print(os.environ.get("TWILIO_ACCOUNT_SID"))

is_test = True if sys.argv[1] == 'test' or sys.argv[1] == 'dev' else False
ip_addr = '0.0.0.0' if sys.argv[2] == 'ip' else '127.0.0.1'
port = sys.argv[3]
if is_test:
    print("Initiating Testing Server...")
else:
    print("Initiating Production Server...")

app = Flask(__name__)
CORS(app)
client = Client()
ocr = OCR()

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

@app.route("/test", methods=['POST'])
def test():
    response = MessagingResponse()
    response.message("message received")
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
            # filename = f'uploads/{customer_number}/{message}.gif'
            return respond('The file that you submitted is not a supported image type.')
        else:
            filename = None
        if filename:
            if not os.path.exists(f'uploads/{customer_number}'):
                os.mkdir(f'uploads/{customer_number}')
            with open(filename, 'wb') as f:
                f.write(r.content)
            # return respond('Thank you! Your image was received.')
        else:
            return respond('The file that you submitted is not a supported image type.')
    else:
        print("[User Message] ", message)
        customer_number = sender.split(':')[1]
        print("[User Name] ", customer_number)

    next_state, created_at = CustomerJourney().get_next_state(customer_number)
    chatbot = ChatBot(customer_number)
    if message == "hi" or message == "Hi" or message == "HI":
        print("[INFO] Re-initiating Conversation.")
        next_state = None
    if not next_state is None:
        time_diff = datetime.now() - created_at
        if time_diff.total_seconds() > 1800:
            print("[INFO] Half an hour passed while last response.")
            next_state = None
        else:
            print("[INFO] In Allowed time bound.")
    if next_state is None:
        print("[INFO] Welcome Message")
        reply = chatbot.welcome_state()
        CustomerJourney().post_customer_number(customer_number)
        CustomerJourney().put_states(reply['state'], reply['next_state'], customer_number)
        if is_test:
            print("TESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSST")
            return reply['message']
        else:
            print("[REPLY]", reply)
            return respond(reply['message'])
    else:
        print("[INFO] Tree Messages")
        if next_state == "confirm_uploaded_recipt" or next_state == "welcome_state":
            reply = eval("chatbot." + next_state)()
        elif next_state == "process_uploaded_recipt":
            def async_ocr_call(customer_number, chatbot):
                total_amount = NanoNetsOCR().parse_data_from_receipt(customer_number)
                if total_amount is None:
                    print(['[INFO] Nano Nets has failed'])
                    total_amount = ocr.extract_roi_from_reciept(customer_number)
                    print("[INFO] Total Amount Fetched: ", total_amount)
                    reply = eval("chatbot." + next_state)(total_amount)
                elif total_amount == "same":
                    reply = {}
                    reply['message'] = "Please be fair, this receipt has already been processed"
                    reply['next_state'] = "process_uploaded_recipt"
                elif total_amount == "invalid place":
                    reply = {}
                    reply['message'] = "Please be fair, this receipt is not of your signed-in place."
                    reply['next_state'] = "process_uploaded_recipt"
                elif total_amount == "cannot find":
                    reply = {}
                    reply['message'] = "We are unable to read receipt properly, please change angle of reciept or capture picture in proper lightnings."
                    reply['next_state'] = "process_uploaded_recipt"
                else:
                    print(['[INFO] Nano Nets has worked'])
                    print("[INFO] Total Amount Fetched: ", total_amount)
                    reply = eval("chatbot." + next_state)(total_amount)

                from_whatsapp_number = 'whatsapp:+14155238886'
                to_whatsapp_number = f'whatsapp:{customer_number}'
                print("[INFO] Sending async message to ", customer_number)
                message = client.messages.create(body=reply['message'],
                                    media_url='https://static8.depositphotos.com/1006899/896/i/950/depositphotos_8961765-stock-photo-prize.jpg',
                                    from_=from_whatsapp_number,
                                    to=to_whatsapp_number)
                print("Message Sent, ", message.sid)
            threading.Thread(target=async_ocr_call, args=([customer_number, chatbot]), kwargs={}).start()
            reply = {'state' : 'process_uploaded_recipt', 'next_state' : 'greetings_state', 'message' : \
                'Please wait, we are validating your receipt and shortly we will notify you, please do not send any message meanwhile\nThanks.'}
        else:
            reply = eval("chatbot." + next_state)(message)
        print("REPLY", reply)
        if not reply is None:
            proactive = reply.get('proactive')
            if proactive:
                print("[INFO] Results has fallback proactive call.")
                next_state = reply['next_state']
                previous_message = reply['message'] + "\n"
                if next_state == "confirm_uploaded_recipt" or next_state == "welcome_state":
                    reply = eval("chatbot." + next_state)()
                elif next_state == "process_uploaded_recipt":
                    total_amount = ocr.extract_roi_from_reciept(customer_number)
                    print("[INFO] Total Amount Fetched: ", total_amount)
                    reply = eval("chatbot." + next_state)(total_amount)
                else:
                    if next_state == "greetings_state":
                        reply = eval("chatbot." + next_state)("1")
                reply['message'] = previous_message + reply['message']
            CustomerJourney().put_states(reply['state'], reply['next_state'], customer_number)
            if is_test:
                print("TESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSST")
                return reply['message']
            else:
                print("[REPLY] ", reply['message'])
                return respond(reply['message'])
        else:
            print("reply is None", reply)

@app.route("/admin_login", methods=['POST'])
def admin_login_func():
    data = request.form
    username, password = data['username'], data['password']
    admin_id = DashBoardAPI().admin_login_api(username, password)

    return jsonify({'admin_id' : admin_id})

@app.route("/get_admin_customer_info_table_endpoint", methods=['POST'])
def get_admin_customer_info_table_func():
    customer_records = DashBoardAPI().get_admin_customer_info_table()

    return jsonify({'customer_records' : customer_records})

@app.route("/put_admin_customer_info_table_endpoint", methods=['POST'])
def put_admin_customer_info_table_func():
    record = request.form.to_dict()
    DashBoardAPI().put_admin_customer_info_table(record)

    return jsonify({'customer_records' : record})

@app.route("/delete_admin_customer_info_table_endpoint", methods=['POST'])
def delete_admin_customer_info_table_func():
    record = request.form.to_dict()
    DashBoardAPI().delete_admin_customer_info_table(record['customer_id'])

    return jsonify({'customer_records' : record})

@app.route("/get_admin_customer_ratings_table_endpoint", methods=['POST'])
def get_admin_customer_ratings_table_func():
    customer_ratings = DashBoardAPI().get_admin_customer_ratings_table()

    return jsonify({'customer_ratings' : customer_ratings})

@app.route("/get_admin_merchant_creds_table_endpoint", methods=['POST'])
def get_admin_merchant_creds_table_func():
    merchant_info = DashBoardAPI().get_admin_merchant_creds_table()

    return jsonify({'merchant_info' : merchant_info})

@app.route("/get_store_status_endpoint", methods=['POST'])
def get_store_status_func():
    records = DashBoardAPI().get_store_status()

    return jsonify({'store_records' : records})

@app.route("/put_store_status_endpoint", methods=['POST'])
def put_store_status_func():
    record = request.form.to_dict()
    status = record['status']
    merchant_number = record['merchant_number']
    DashBoardAPI().put_store_status(status, merchant_number)

    return jsonify({'store_records' : "updated"})

if __name__ == "__main__":
  app.run(ip_addr,port=port, debug=True)