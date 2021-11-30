import easyocr
import re
import os

class OCR:
    def __init__(self) -> None:
        self.reader = easyocr.Reader(['ch_sim','en'])
        self.total_words = ['total', 'tota', 'amount', 'grandtotal', 'subtotal']

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
                        # print(numbers, type(numbers))
                        return float("".join(numbers))
            except Exception as e:
                print("[Exception from read_receipt_rule_based]", str(e))
                return 0
        else:
            return 0

# ocr = OCR()
# ocr.read_receipt_rule_based("+923132609629")