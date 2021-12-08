import os
import re
import requests

from customer_extras import CustomerExtras

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
            customer_extra.put_last_receipt_data(receipt_data)
            total_amount = receipt_data.get('Total_Amount')
            if not total_amount is None:
                total_amount = re.findall(r'\d+(?:[,.]\d+)*', receipt_data['Total_Amount'])
                total_amount = "".join(total_amount).replace(",", "")
                return float(total_amount)
            else:
                return "cannot find"
        else:
            is_same = self.compare_data(old_receipt_data, receipt_data)
            if is_same:
                return "same"
            else:
                customer_extra.put_last_receipt_data(receipt_data)
                total_amount = receipt_data.get('Total_Amount')
                if not total_amount is None:
                    total_amount = re.findall(r'\d+(?:[,.]\d+)*', receipt_data['Total_Amount'])
                    total_amount = "".join(total_amount).replace(",", "")
                    return float(total_amount)
                else:
                    return "cannot find"

# print(NanoNetsOCR().parse_data_from_receipt("+923132609629"))