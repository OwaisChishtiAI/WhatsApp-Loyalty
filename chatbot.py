from customer_info import CustomerInfo
from customer_journey import CustomerRatings
from customer_extras import CustomerExtras
from merchant import Merchant

class ChatBot:
    def __init__(self, customer_number):
        self.customer_number = customer_number
        self.customer_name = None
        self.places = {}
        self.customer_record = CustomerInfo()
        self.ratings = {'1' : 'Love your service 😍', "2" : 'Service was good 😃', '3' : 'It was ok 😐',\
            '4' : 'Dissapointing service 😔', '5' : 'Really upset 😤'}
        self.merchant = Merchant()
        self.customer_extras = CustomerExtras(self.customer_number)

    def welcome_state(self):
        state = "welcome_state"
        next_state = "greetings_state"
        message = "Hi.\nGood day.\n1. Customer\n2. Merchant\nPlease reply with 1,2,3.. for respective option.\nAt any point of time, if you want to restart conversation reply with *hi*"
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
                message = "What is your good name please?\nPlease reply with your name only.\nThanks"
                return {'state' : state, 'next_state' : 'registering_customer_name', 'message' : message}
        elif is_customer == '2': #MERCHANT
            message = "Hi, Please select from following,\n1. Register Store.\n2. Signin into Store."
            return {'state' : state, 'next_state' : 'enrollment_state', 'message' : message}
        else:
            message = "invalid Option. Please select\n1. Customer\n2. Merchant\n"
            return {'state' : state, 'next_state' : state, 'message' : message}

    def registering_customer_name(self, customer_name):
        state = "registering_customer_name_state"
        next_state = "greetings_state"
        self.customer_name = customer_name
        self.customer_record.post_customer_name(customer_name, self.customer_number)
        return {'state' : state, 'next_state' : next_state, 'message' : f'Hi {customer_name}, Good Day!\n1. Customer\n2. Merchant\nPlease reply with 1,2,3.. for respective option.'}

    def places_state(self, place_option):
        state = "places_state"
        next_state = 'checked_in_state'

        if place_option == "1":
            places = self.customer_record.get_places_list(self.customer_number)
            if places is not None:
                message_places = ""
                
                for i in range(len(places)):
                    if message_places:
                        message_places += f"\n{str(i+1)}. {places[i]}"
                    else:
                        message_places += f"{str(i+1)}. {places[i]}"
                    # self.places[str(i+1)] = places[i]
                message = "Please select your previous place\n" + message_places
                return {'state' : state, 'next_state' : next_state, 'message' : message}
            else:
                message = "Sorry, You don't have any places registered, please add new place.\nThanks"
                return {'state' : state, 'next_state' : 'greetings_state', 'message' : message,\
                     'proactive' : True} # leads to option == 2

        elif place_option == "2":
            message = "Please reply with your visited place name"
            return {'state' : state, 'next_state' : next_state, 'message' : message}

        elif place_option == "3":
            message = "Thanks for choosing us, see you soon"
            return {'state' : state, 'next_state' : 'welcome_state', 'message' : message}

        else:
            message = "Wrong Option, Please select appropiate corresponding option"
            return {'state' : state, 'next_state' : 'greetings_state', 'message' : message}

    def checked_in_state(self, previous_place):
        state = "checked_in_state"
        next_state = "upload_receipt_state"

        if previous_place.isdigit():
            places = self.customer_record.get_places_list(self.customer_number)
            place_name = places[int(previous_place) - 1]
            if place_name:
                message = f"You have checked into {place_name}"
                self.customer_extras.post_put_last_visited_place(place_name)
            else:
                message = "Not valid place"
                return {'state' : state, 'next_state' : state, 'message' : message}
        else:
            allowed_places = self.customer_record.get_allowed_places_list()
            if previous_place in allowed_places:
                self.customer_record.put_places_list(self.customer_number, previous_place)
                message = f"You have checked into {previous_place}"
                self.customer_extras.post_put_last_visited_place(previous_place)
                place_name = previous_place
            else:
                message = "Your entered place has no corresponding merchant.\nIf you have visited any places registered with us, please select from following,"
                for i in range(len(allowed_places)):
                    message = message + "\n" + str(i+1) + ". " + allowed_places[i]
                return {'state' : state, 'next_state' : 'checked_in_state_for_allowed_places', 'message' : message}

        customer_points = self.customer_record.get_points_balance(self.customer_number, place_name)
        message = message + f"\nYour points balance is {customer_points}"
        message = message + "\nWhat would you like to do?\n1. Redeem\n2. Add\n3. More Options"
        return {'state' : state, 'next_state' : next_state, 'message' : message}

    def checked_in_state_for_allowed_places(self, allowed_place):
        state = "checked_in_state_for_allowed_places"
        next_state = "upload_receipt_state"

        if allowed_place.isdigit():
            places = self.customer_record.get_allowed_places_list()
            place_name = places[int(allowed_place) - 1]
            if place_name:
                message = f"You have checked into {place_name}"
                self.customer_record.put_places_list(self.customer_number, place_name)
                self.customer_extras.post_put_last_visited_place(place_name)
            else:
                message = "Not valid place"
                return {'state' : state, 'next_state' : state, 'message' : message}
        else:
            return {'state' : state, 'next_state' : state, 'message' : 'Please select appropiate option'}

        customer_points = self.customer_record.get_points_balance(self.customer_number, place_name)
        message = message + f"\nYour points balance is {customer_points}"
        message = message + "\nWhat would you like to do?\n1. Redeem\n2. Add\n3. More Options"
        return {'state' : state, 'next_state' : next_state, 'message' : message}

    def upload_receipt_state(self, to_do):
        state = "upload_receipt_state"
        next_state = "confirm_uploaded_recipt"

        if to_do == "1":
            message = f"Please Enter Merchant Secret Code for *{self.customer_extras.get_last_visited_place()}*"
            return {'state' : state, 'next_state' : 'enter_secret_code_state', 'message' : message}

        elif to_do == "2":
            message = "Let's do it!\nTake a clear picture of your receipt and upload it."
            return {'state' : state, 'next_state' : next_state, 'message' : message}

        elif to_do == "3":
            message = "What would you like to do?\n1. Rate our services\n2. Checkin to another place\n\
                3. Go back\n4. Exit"
            return {'state' : state, 'next_state' : 'possible_next_states_state', 'message' : message}

    def enter_secret_code_state(self, code):
        state = "enter_secret_code_state"
        next_state = "redeem_points_state"

        merchant_code = self.merchant.get_merchant_secret_number_and_place(self.customer_extras.get_last_visited_place(), self.customer_number)
        print("CODES: ", merchant_code, code)
        if code == merchant_code:
            available_points = self.customer_record.get_points_balance(self.customer_number, self.customer_extras.get_last_visited_place())
            message = f"How many points you want to redeem from {available_points} points available?"
            return {'state' : state, 'next_state' : next_state, 'message' : message}
        else:
            message = f"Wrong Merchant Code."
            return {'state' : state, 'next_state' : "enter_secret_code_state", 'message' : message}

    def redeem_points_state(self, points):
        state = "redeem_points_state"
        next_state = "greetings_state"

        if points:
            try:
                available_points = self.customer_record.get_points_balance(self.customer_number, self.customer_extras.get_last_visited_place())
                if float(points) <= available_points:
                    available_points = available_points - float(points)
                    message = f"{points} points redeemed, your points balance is {available_points}"
                    self.customer_record.post_points_balance(available_points, self.customer_number, self.customer_extras.get_last_visited_place())
                    return {'state' : state, 'next_state' : next_state, 'message' : message}
                else:
                    message = f"Your redeem points must be less than your balance, you have *{available_points}* balanace points."
                    return {'state' : state, 'next_state' : state, 'message' : message}
            except:
                message = "Invalid amount, please reply with appropiate amount."
                return {'state' : state, 'next_state' : state, 'message' : message}
        else:
            message = "Reply with non-empty amount."
            return {'state' : state, 'next_state' : state, 'message' : message}
                

    def confirm_uploaded_recipt(self):
        state = 'confirm_uploaded_recipt'
        next_state = 'process_uploaded_recipt'

        message = "We will now process your receipt, Check if your receipt was uploaded successfully by replying *ok*"
        return {'state' : state, 'next_state' : next_state, 'message' : message}

    def process_uploaded_recipt(self, total_amount):
        state = 'process_uploaded_recipt'
        next_state = 'greetings_state'

        if int(total_amount) > 0:
            last_visited_place = self.customer_extras.get_last_visited_place()
            merchant_awarded_points = self.merchant.get_points_by_place_name(last_visited_place)
            total_amount = merchant_awarded_points * total_amount
            print("[INFO] Points Calculator: ", last_visited_place, merchant_awarded_points, total_amount)
            message = f"Congratulations! {total_amount} points have been added to your wallet\nYour new balance is {float(self.customer_record.get_points_balance(self.customer_number, self.customer_extras.get_last_visited_place())) + float(total_amount)}"
            self.customer_record.post_points_balance(total_amount, self.customer_number, last_visited_place)
        else:
            message = "You are not awarded this time, your purchases are not sufficient."
        return {'state' : state, 'next_state' : next_state, 'message' : message, 'proactive' : True}

    def possible_next_states_state(self, more_option):
        state = 'possible_next_states_state'
        next_state = None

        if more_option == '1':
            message = 'We would love to get your feedback for this promotion.' + "\n"
            for key, val in self.ratings.items():
                message = message + f'{key}. {val}\n'
            return {'state' : state, 'next_state' : 'rating_ack', 'message' : message}
        
        elif more_option == '2':
            return {'state' : state, 'next_state' : 'greetings_state', 'message' : '', 'proactive' : True}

        elif more_option == '3':
            message = "Thanks for choosing us, see you soon"
            return {'state' : state, 'next_state' : 'welcome_state', 'message' : message}

    def rating_ack(self, stars):
        state = 'rating_ack'
        next_state = 'greetings_state'

        rating = self.ratings[stars]
        CustomerRatings().post_rating(rating, self.customer_number, stars)
        message = "Thank You, your feedback has been registered, we will furnish our services as per your feedback."
        return {'state' : state, 'next_state' : next_state, 'message' : message, 'proactive' : True}

#--------------------------------------------------------------------------------------------------------------#
#///////////////////////////////////////****** MERCHANT STORIES *******////////////////////////////////////////#
#--------------------------------------------------------------------------------------------------------------#

    def enrollment_state(self, enroll):
        state = 'enrollment_state'
        next_state = None

        if enroll == "1":
            message = "Please enter your store name."
            return {'state' : state, 'next_state' : 'store_name_state', 'message' : message}
            
        elif enroll == "2":
            message = "Please enter your store name."
            return {'state' : state, 'next_state' : 'login_store_name_state', 'message' : message}
        else:
            message = "Invalid Selection."
            return {'state' : state, 'next_state' : 'enrollment_state', 'message' : message}

    def store_name_state(self, store_name):
        state = 'store_name_state'
        next_state = 'register_username_state'

        user_store_name = store_name
        store_name = self.merchant.get_store_name(store_name)
        if store_name:
            message = f"Store name {store_name} already exists, please login.\nEnter your {store_name}'s username."
            return {'state' : state, 'next_state' : 'login_username_state', 'message' : message}

        else:
            self.merchant.post_merchant_secret_number_and_place(self.customer_number, user_store_name)
            message = "Please enter username e.g. *admin@wallmart.com*"
            self.merchant.post_store_name(user_store_name, self.customer_number)
            self.merchant.post_store_status(user_store_name, self.customer_number)
            return {'state' : state, 'next_state' : next_state, 'message' : message}

    def login_store_name_state(self, store_name):
        state = 'login_store_name_state'
        next_state = 'login_username_state'

        store_name = self.merchant.get_store_name(store_name)
        if store_name:
            message = "Please enter username e.g. *admin@wallmart.com*"
            return {'state' : state, 'next_state' : next_state, 'message' : message}

        else:
            message = f"Store name {store_name} does not exists, please register."
            # self.merchant.post_store_name(store_name, self.customer_number)
            return {'state' : state, 'next_state' : 'welcome_state', 'message' : message, 'proactive' : True}

    def register_username_state(self, username):
        state = 'register_username_state'
        next_state = 'register_password_state'

        if username:
            self.merchant.put_user_name(username, self.customer_number)
            message = "Please enter password."
            return {'state' : state, 'next_state' : next_state, 'message' : message}
        else:
            message = "Username cannot be empty, please re-enter valid username e.g. *admin@wallmart.com*"
            return {'state' : state, 'next_state' : 'register_username_state', 'message' : message}

    def login_username_state(self, username):
        state = 'login_username_state'
        next_state = 'login_password_state'

        stored_username = self.merchant.get_username(self.customer_number)
        if stored_username:
            if stored_username == username:
                message = "Please enter your password."
                return {'state' : state, 'next_state' : next_state, 'message' : message}
            else:
                message = "Wrong username."
                return {'state' : state, 'next_state' : state, 'message' : message}
        else:
            message = "Your store name exists but your username does not, it seems like someone already has registered,\nPlease contact technical dept. for more assistance. Apologies for inconvinience"
            return {'state' : state, 'next_state' : 'welcome_state', 'message' : message}

    def register_password_state(self, password):
        state = 'register_password_state'
        next_state = 'add_points_state'

        if password:
            self.merchant.put_password(password, self.customer_number)
            message = "Welcome, your store has been registered.\nYou can now add points for customers\nHow many points you want to give to customers for each *1 USD* purchase?\nPlease reply with numbers e.g. 1, 5, 10, etc."
            return {'state' : state, 'next_state' : next_state, 'message' : message}
        else:
            message = "password cannot be empty, please re-enter valid strong password"
            return {'state' : state, 'next_state' : 'register_password_state', 'message' : message}

    def login_password_state(self, password):
        state = 'login_password_state'
        next_state = 'add_points_state'

        stored_password = self.merchant.get_password(self.customer_number)
        if stored_password:
            if stored_password == password:
                points_offer = self.merchant.get_points(self.customer_number)
                message = f"Welcome, you are now logged in.\nYou can now add points for customers\nHow many points you want to give to customers for each *1 USD* purchase?\nPlease reply with numbers e.g. 1, 5, 10, etc.\nPreviously you offered *{points_offer}* for each 1 USD purchase, enter same\npoints if you don't want to change points offerings."
                return {'state' : state, 'next_state' : next_state, 'message' : message}
            else:
                message = "Wrong password."
                return {'state' : state, 'next_state' : state, 'message' : message}
        else:
            message = "Your store name exists but your password does not, it seems like technical error,\n\
                Please contact technical dept. for more assistance. Apologies for inconvinience"
            return {'state' : state, 'next_state' : 'welcome_state', 'message' : message}

    def add_points_state(self, points):
        state = "add_points_state"
        next_state = "add_secret_code_state"

        if points.isdigit():
            self.merchant.put_points(int(points), self.customer_number)
            message = f"Thanks, your points have been saved, for each dollar purchase cutomer will get\n{points} points.\nPlease Enter *SECRET CODE* for points redeem purpose."#, You're now *Logged out* from current session, but you can signin any time, Thanks."
            return {'state' : state, 'next_state' : 'add_secret_code_state', 'message' : message}
        else:
            message = "Points cannot be empty or non-numeric, please re-enter valid numerical points."
            return {'state' : state, 'next_state' : 'add_points_state', 'message' : message}
    
    def add_secret_code_state(self, code):
        state = "add_secret_code_state"
        next_state = "welcome_state"

        if code:
            self.merchant.put_merchant_secret_number_and_place(self.customer_number, code)
            message = f"Your code has been registered, use this code when customer needs to redeem points, You're now *Logged out* from current session, but you can signin any time, Thanks."
            return {'state' : state, 'next_state' : next_state, 'message' : message}
        else:
            message = "Code cannot be empty, please re-enter valid numerical points."
            return {'state' : state, 'next_state' : 'add_secret_code_state', 'message' : message}