import io
from imageio import imread
import numpy as np
from imutils import paths
import os
from flask import Flask, request, render_template
import cv2
import pytesseract
import base64   

PROJECT = os.path.dirname(os.path.realpath("C:\\Users\\91933\\blur-detection\\TESSERACT"))
FOLDER  = '{}\\TESSERACT'.format(PROJECT)

app = Flask(__name__)
app.config['FOLDER'] = FOLDER  

@app.route("/", methods=['GET','POST'])
def upload():
    return """
        <!doctype html>
        <form action="/ocr" method="post" enctype="multipart/form-data">
          <p><input type="file" name="file"/>
             <input type="submit" value="Upload">
        </form>
        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['FOLDER'], ))

@app.route('/ocr', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)  
        name=f.filename
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'   
    with open(name, "rb") as fid:
        data = fid.read()
    b64_bytes = base64.b64encode(data)
    b64_string = b64_bytes.decode()
    image = imread(io.BytesIO(base64.b64decode(b64_string)))
    name = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(name, cv2.COLOR_BGR2GRAY)
    noise = cv2.medianBlur(gray,5)
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(noise, cv2.MORPH_OPEN, kernel)
    config = ('-l eng --oem 1 --psm 3')
    ocr = pytesseract.image_to_string(opening, config=config)
    return render_template("ocr.html", ocrtext= ocr) 

if __name__ == "__main__":
    app.debug = False
    app.run()
