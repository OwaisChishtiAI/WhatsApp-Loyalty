import smtplib
from database import Connect
from email.message import EmailMessage

class Email:
    gmail_user = 'mustufa.shark@gmail.com'
    gmail_password = 'Abcd@1234abcd'
    def __init__(self):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(Email.gmail_user, Email.gmail_password)
        self.server = server

    def details_template(self, recipients, data):
        if data['drivable'] == "1":
            drivable = "Yes"
        else:
            drivable = "No"
        subject = "User Query Regarding Shipment " + data['user_email']
        body = """
        Hi,
        User submitted query for {0} transportation, which is Driveable: {1}, from {2} to {3} in {4} requested timeframe.
        Car Make: {5},
        Car Model: {6},
        User Email: {7}
        """.format(data['transport_type'], drivable, data['collection_location'], data['destination_location'], data['delivery_timeframe'], data['vehicle_make'], data['vehicle_model'], data['user_email'])
        email_text = """%s""" % (body)
        msg = EmailMessage()
        msg.set_content(email_text)

        msg['Subject'] = subject
        msg['From'] = Email.gmail_user
        msg['To'] = recipients
        return msg

    def cell_template(self, cell_number, user_email, recipients):
        subject = "User Query Regarding Shipment " + user_email
        body = """
        User has provided the cell number: {}
        """.format(cell_number)
        email_text = """%s""" % (body)
        msg = EmailMessage()
        msg.set_content(email_text)

        msg['Subject'] = subject
        msg['From'] = Email.gmail_user
        msg['To'] = recipients
        return msg

    def get_recipients(self):
        connect = Connect()
        cursor = connect.pointer()[0]
        cursor.execute("SELECT recipient_email FROM email_recipients")
        recipients = cursor.fetchall()
        recipients_li = []
        print("Recipients: ", recipients)
        for each in recipients:
            recipients_li.append(each[0])
        connect.close()
        return recipients_li

    def send_email_details(self, data, user_email):
        recipients_li = self.get_recipients()
        email = self.details_template(recipients_li, data)
        self.server.sendmail(Email.gmail_user, recipients_li, email.as_string())
        self.server.close()
        print("[INFO] Email Sent with Details")

    def send_email_cell(self, cell_number, sale_id):
        recipients_li = self.get_recipients()
        connect = Connect()
        cursor = connect.pointer()[0]
        cursor.execute("SELECT user_email FROM shipment_details WHERE shipment_id = {}".format(int(sale_id)))
        user_email = cursor.fetchone()[0]
        connect.close()
        email = self.cell_template(cell_number, user_email, recipients_li)
        self.server.sendmail(Email.gmail_user, recipients_li, email.as_string())
        self.server.close()
        print("[INFO] Email Sent with Cell")