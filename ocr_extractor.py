import easyocr
import re

class OCR:
    def __init__(self) -> None:
        self.reader = easyocr.Reader(['ch_sim','en'])
        self.total_words = ['total', 'tota', 'amount', 'grandtotal', 'subtotal']

    def read_receipt_rule_based(self):
        result = self.reader.readtext('image')
        data = [x[1] for x in result]
        total_index = None
        for i in range(len(data)):
            if " ".join(re.findall("[a-zA-Z]+", data[i])).lower().strip() in self.total_words:
                total_index = i                
                break
        if total_index is not None:
            try:
                for j in range(total_index+1, total_index+4):
                    numbers = re.findall(r'\d+', " ".join(data[j]))
                    if numbers:
                        return int(numbers)
            except Exception as e:
                print("[Exception from read_receipt_rule_based]", data.index(data), str(e))
                return 0
        else:
            return 0