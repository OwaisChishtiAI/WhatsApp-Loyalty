from flask import Flask, request
import re
import easyocr
import threading
import os

app = Flask(__name__)


def ocr(num):
    print(num)
    reader = easyocr.Reader(['ch_sim','en'])
    total_words = ['total', 'tota', 'amount', 'grandtotal', 'subtotal']
    image = os.listdir(f'uploads/{num}')[0]
    print("[INFO] Analyzing Image: ", image)
    result = reader.readtext(os.path.join(f'uploads/{num}', image))
    data = [x[1] for x in result]
    total_index = None
    for i in range(len(data)):
        if " ".join(re.findall("[a-zA-Z]+", data[i])).lower().strip() in total_words:
            total_index = i                
            break
    if total_index is not None:
        try:
            for j in range(total_index+1, total_index+4):
                numbers = re.findall(r'\d+(?:[,.]\d+)*', "".join(data[j]))
                if numbers:
                    # print(numbers, type(numbers))
                    print(float("".join(numbers)))
        except Exception as e:
            print("[Exception from read_receipt_rule_based]", str(e))

@app.route("/home", methods=['GET'])
def tes():
    thr = threading.Thread(target=ocr, args=(['+923132609629']), kwargs={})
    thr.start()
    # thr.join()
    return "OK"

app.run(debug=True)