import easyocr
import re
import os
from ocr_yolo import crop_roi_from_reciept

class OCR:
    def __init__(self) -> None:
        self.reader = easyocr.Reader(['ch_sim','en'])
        self.total_words = ['total', 'tota', 'amount', 'grandtotal', 'subtotal']

    def extract_roi_from_reciept(self, customer_number):
        try:
            has_cropped = crop_roi_from_reciept(customer_number)
            if has_cropped:
                points = self.read_receipt_part_yolo(customer_number)
                if not points is None:
                    print("[INFO] YOLO Model +1")
                    return points
                else:
                    points = self.read_receipt_rule_based(customer_number)
                    print("[INFO] Rule Based Model +1")
                    return points
            else:
                points = self.read_receipt_rule_based(customer_number)
                print("[INFO] Rule Based Model +1")
                return points
        except Exception as e:
            print("[Exception] extract_roi_from_reciept ", str(e))
            points = self.read_receipt_rule_based(customer_number)
            print("[INFO] Rule Based Model +1")
            return points
        

    def read_receipt_rule_based(self, customer_number):
        image = os.listdir(f'uploads/{customer_number}')[0]
        print("[INFO] Analyzing Image: ", image)
        result = self.reader.readtext(os.path.join(f'uploads/{customer_number}', image))
        data = [x[1] for x in result]
        total_index = None
        for i in range(len(data)):
            if " ".join(re.findall("[a-zA-Z]+", data[i])).lower().strip() in self.total_words:
                total_index = i                
                break
        if total_index is not None:
            try:
                for j in range(total_index+1, total_index+4):
                    numbers = re.findall(r'\d+(?:[,.]\d+)*', "".join(data[j]))
                    if numbers:
                        return float("".join(numbers))
            except Exception as e:
                print("[Exception from read_receipt_rule_based]", str(e))
                return 0
        else:
            return 0

    def read_receipt_part_yolo(self, customer_number):
        image = "cropped.jpg"
        result = self.reader.readtext(os.path.join(f'uploads/{customer_number}', image))
        # result = '$' + result[0][1] + '.53'
        result = re.findall(r'\d+(?:[,.]\d+)*', result[0][1])
        if result:
            return result[0].replace(',', '')
        else:
            return None

# ocr = OCR()
# print(ocr.extract_roi_from_reciept("+923132609629"))