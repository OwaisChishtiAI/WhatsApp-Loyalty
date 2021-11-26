from customer_info import CustomerInfo

class ChatBot:
    def __init__(self, customer_number):
        self.customer_number = customer_number
        self.customer_name = None
        self.customer_record = CustomerInfo()

    def welcome_message(self):
        state = "welcome_state"
        next_state = "greetings_state"
        message = "Hi.\nGood day.\n1. Customer\n2. Merchant\nPlease reply with 1,2,3.. for respective option."
        return {'state' : state, 'next_state' : next_state, 'message' : message}

    def greetings_state(self, is_customer): # Name is required at this method
        state = "greetings_state"
        next_state = "places_state"
        if is_customer == '1': # CUSTOMER
            customer_name = self.customer_record.get_customer_name(self.customer_number)
            if customer_name is not None:
                message = f"Welcome {customer_name}\n1. List of Previous Places\n2. Add New Place.\n3. Exit"
                return {'state' : state, 'next_state' : next_state, 'message' : message}
            else:
                message = "What is your good name please?\nThanks"
                return {'state' : state, 'next_state' : 'registering_customer_name', 'message' : message}
        else: #MERCHANT
            NotImplementedError()

    def registering_customer_name(self, customer_name):
        state = "registering_customer_name_state"
        next_state = "greetings_state"
        self.customer_name = customer_name
        self.customer_record.post_customer_name(customer_name, self.customer_number)
        return {'state' : state, 'next_state' : next_state, 'message' : f'Hi {customer_name}, Good Day!\n\
            1. Customer\n2. Merchant\nPlease reply with 1,2,3.. for respective option.'}

    def places_state(self, place_option):
        state = "places_state"
        next_state = 'checked_in_state'

        if place_option == "1":
            places = self.customer_record.get_places_list(self.customer_number)
            if places is not None:
                message_places = ""
                self.places = {}
                for i in range(len(places)):
                    if message_places:
                        message_places += f"\n{str(i+1)}. {places[i]}"
                    else:
                        message_places += f"{str(i+1)}. {places[i]}"
                    self.places[str(i+1)] = places[i]
                message = "Please select your previous place\n" + message_places
                return {'state' : state, 'next_state' : next_state, 'message' : message}
            else:
                message = "Sorry, You don't have any places registered, please add new place.\nThanks"
                return {'state' : state, 'next_state' : 'greetings_state', 'message' : message} # leads to option == 2

        elif place_option == "2":
            message = "Please reply with your visited place name"
            return {'state' : state, 'next_state' : next_state, 'message' : message}

        elif place_option == "3":
            message = "Thanks for choosing us, see you soon"
            return {'state' : state, 'next_state' : 'end_state', 'message' : message}

        else:
            message = "Wrong Option, Please select appropiate corresponding option"
            return {'state' : state, 'next_state' : 'greetings_state', 'message' : message}

    def checked_in_state(self, previous_place):
        state = "checked_in_state"
        next_state = "upload_receipt_state"

        if previous_place.isdigit():
            place_name = self.places.get(previous_place)
            if place_name:
                message = f"You have checked into {place_name}"
            else:
                print("Not valid place")
        else:
            self.customer_record.put_places_list(self.customer_number, previous_place)
            message = f"You have checked into {previous_place}"

        customer_points = self.customer_record.get_points_balance(self.customer_number)
        message = message + f"\nYour points balance is {customer_points}"
        message = message + "\nWhat would you like to do?\n1. Redeem\n2. Add\n3. More Options"
        return {'state' : state, 'next_state' : next_state, 'message' : message}

    def upload_receipt_state(self, to_do):
        state = "upload_receipt_state"
        next_state = "confirm_uploaded_recipt"

        if to_do == "1":
            NotImplementedError()

        elif to_do == "2":
            message = "Let's do it!\nTake a clear picture of your receipt and upload it."
            return {'state' : state, 'next_state' : next_state, 'message' : message}

        elif to_do == "3":
            message = "What would you like to do?\n1. Rate our services\n2. Checkin to another place\n\
                3. Go back\n4. Exit"
            return {'state' : state, 'next_state' : 'possible_next_states_state', 'message' : message}

    def confirm_uploaded_recipt(self):
        state = 'confirm_uploaded_recipt'
        next_state = 'process_uploaded_recipt'

        message = "We will now process your receipt, Check if your receipt was uploaded successfully by replying *ok*"
        return {'state' : state, 'next_state' : next_state, 'message' : message}

    def process_uploaded_recipt(self, total_amount):
        state = 'process_uploaded_recipt'
        next_state = 'checked_in_state'

        if int(total_amount) > 0:
            message = f"Congratulations! {total_amount} points have been added to your wallet\n\
                Your new balance is \
                    {int(self.customer_record.get_points_balance(self.customer_number)) + int(total_amount)}"
            self.customer_record.put_points_balance(total_amount, self.customer_number)
        else:
            message = "You are not awarded this time, your purchases are not sufficient."
        return {'state' : state, 'next_state' : next_state, 'message' : message}