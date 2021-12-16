import os
import re
import requests

from customer_extras import CustomerExtras
from classify_label import ReceiptClassifier

class NanoNetsOCR:
    def compare_data(self, data1, data2):
            return True if data1 == data2 else False

    def parse_data_from_receipt(self, customer_number):
        url = 'https://app.nanonets.com/api/v2/OCR/Model/3e9d1eae-3e0f-4ac5-97e7-87400c4fc796/LabelFile/'
        filename = f"uploads/{customer_number}/.jpg"
        data = {'file': open(filename, 'rb')}
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('68AfQsx5Q-G_LWU0O2BQjBT3CV1OLf-V', ''), files=data)
        data = response.json()
        receipt_data = {}
        if response.status_code == 200:
            if data['message'] == "Success":
                for each in data['result'][0]['prediction']:
                    receipt_data[each['label']] = each['ocr_text'].replace("\n", " ")
            else:
                return None
        else:
            return None
        
        customer_extra = CustomerExtras(customer_number)
        old_receipt_data = customer_extra.get_last_receipt_data()
        if old_receipt_data is None:
            print("[INFO] No Last Receipt Records Found")
            customer_extra.put_last_receipt_data(receipt_data)
            total_amount = receipt_data.get('Total_Amount')
            merchant_name = receipt_data.get('Merchant_Name')
            print("[INFO] Total Amount, Merchant Name: ", total_amount, merchant_name)
            if not merchant_name is None:
                if customer_extra.get_last_visited_place().lower().strip() in merchant_name.lower().strip():
                    print("[INFO] Place Match: ", customer_extra.get_last_visited_place().lower().strip(), merchant_name.lower().strip())
                else:
                    print("[INFO] Place NOT Match: ", customer_extra.get_last_visited_place().lower().strip(), merchant_name.lower().strip())
                    return "invalid place"
            else:
                return "cannot find"
            if not total_amount is None:
                total_amount = re.findall(r'\d+(?:[,.]\d+)*', receipt_data['Total_Amount'])
                total_amount = "".join(total_amount).replace(",", "")
                return float(total_amount)
            else:
                return "cannot find"
        else:
            print("[INFO] Last Receipt Records Found ", old_receipt_data)
            is_same = self.compare_data(old_receipt_data, receipt_data)
            if is_same:
                print("[INFO] User is cheating by giving same reciept")
                return "same"
            else:
                print("[INFO] Receipt is UNIQUE")
                customer_extra.put_last_receipt_data(receipt_data)
                total_amount = receipt_data.get('Total_Amount')
                merchant_name = receipt_data.get('Merchant_Name')
                print("[INFO] Total Amount, Merchant Name: ", total_amount, merchant_name)
                if not merchant_name is None:
                    if customer_extra.get_last_visited_place().lower().strip() in merchant_name.lower().strip():
                    # if customer_extra.get_last_visited_place().lower().strip() in ReceiptClassifier(customer_number).predict():
                        print("[INFO] NANO NETS Place Match: ", customer_extra.get_last_visited_place().lower().strip(), merchant_name.lower().strip())
                    else:
                        print("[INFO] NANO NETS Place NOT Match: ", customer_extra.get_last_visited_place().lower().strip(), merchant_name.lower().strip())
                        return "invalid place"
                else:
                    if customer_extra.get_last_visited_place().lower().strip() in ReceiptClassifier(customer_number).predict():
                        print("[INFO] CNN Place Match: ", customer_extra.get_last_visited_place().lower().strip(), merchant_name.lower().strip())
                    else:
                        print("[INFO] CNN Place NOT Match: ", customer_extra.get_last_visited_place().lower().strip(), merchant_name.lower().strip())
                        return "invalid place"
                if not total_amount is None:
                    total_amount = re.findall(r'\d+(?:[,.]\d+)*', receipt_data['Total_Amount'])
                    total_amount = "".join(total_amount).replace(",", "")
                    return float(total_amount)
                else:
                    return "cannot find"

# print(NanoNetsOCR().parse_data_from_receipt("+923132609629"))