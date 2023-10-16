from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import requests
from bs4 import BeautifulSoup

def fetch_calories(prediction):
    
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        # st.error("Can't able to fetch the Calories")
        print(e)
    

app = Flask(__name__)

# Define the path to the model and label files
model_dir = os.path.join(os.path.dirname(__file__), 'D:\web\Food_Recognition\model')
model_path = os.path.join(model_dir, 'D:\web\Food_Recognition\model\keras_model.h5')
label_path = os.path.join(model_dir, 'D:\web\Food_Recognition\model\labels.txt')

# Check if the model and label files exist
if not os.path.exists(model_path) or not os.path.exists(label_path):
    raise FileNotFoundError("Model and/or label file not found.")

# Load the model
model = tf.keras.models.load_model(model_path)

# Load class labels from the label file
with open(label_path, 'r') as label_file:
    class_labels = label_file.read().splitlines()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        image_path = os.path.join('D:\\web\\Food_Recognition\\app\\static\\uploads', secure_filename(uploaded_file.filename))
        uploaded_file.save(image_path)

        # Preprocess the image (resize, normalize, etc.)
        image = Image.open(image_path)
        image = image.resize((224, 224))  # Adjust to your model's input size
        image = np.asarray(image) / 255.0  # Normalize

        # Make a prediction using your deep learning model
        prediction = model.predict(np.expand_dims(image, axis=0))
        class_index = np.argmax(prediction)
        predicted_label = class_labels[class_index]
        that=predicted_label[2:]
        cal =0
        zid=11

        if predicted_label == "0 burger":
            cal = 300
            zid=9055
        elif predicted_label == "1 butter_naan":
            cal = 350
            zid=68387
        elif predicted_label == "2 chai":
            cal = 40
            zid=13620
        elif predicted_label == "3 chapati":
            cal = 80
            zid=26919
        elif predicted_label == "4 chole_bhature":
            cal = 450
            zid=60192
        elif predicted_label == "5 dal_makhani":
            cal = 200
            zid=44987
        elif predicted_label == "6 dholkla":
            cal = 200
            zid=66471
        elif predicted_label == "7 fried_rice":
            cal = 250
            zid=35301
        elif predicted_label == "8 idli":
            cal = 50
            zid=35114
        elif predicted_label == "9 jalebi":
            cal = 400
            zid=37104
        elif predicted_label == "10 kaathi_rolls":
            cal = 300
            zid=62927
        elif predicted_label == "11 kadai_paneer":
            cal = 250
            zid=63440
        elif predicted_label == "12 kulfi":
            cal = 250
            zid=32439
        elif predicted_label == "13 masala_dosa":
            cal = 200
            zid=70735
        elif predicted_label == "14 momos":
            cal = 80
            zid=8497
        elif predicted_label == "15 paani_puri":
            cal = 70
              # Note: This is an approximate value per serving, not per 100 grams.
            zid=70230
        elif predicted_label == "16 pakode":
            cal = 300
            zid=13094
        elif predicted_label == "17 pav_bhaji":
            cal = 250
            zid=63559
        elif predicted_label == "18 pizza":
            cal = 300
            zid=68987
        elif predicted_label == "19 samosa":
            cal = 350
            zid=871
        else:
            cal = 0
            zid=13620
    

        if zid !=11:
            return render_template('index.html',result=f'Prediction: {that} and calories per 100 gram is {cal}',pid=f'https://www.zomato.com/chennai/delivery?dishv2_id={zid}')
        else:
            return render_template('index.html',result=f'Prediction: {that} and calories per 100 gram is {cal}',pid=f'https://www.zomato.com/chennai')


if __name__ == '__main__':
    app.run(debug=True)