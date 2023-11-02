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
        nut="https://en.wikipedia.org/wiki/Indian_cuisine";
        category="Indian cuisine"
        price="0"
        details=""
        hazards=""

        if predicted_label == "0 burger":
            cal = 300
            details="Health Benefits: Provides protein, carbs, and essential nutrients. May contain fresh vegetables"
            hazards="Health Hazards: High in saturated fat, calories, and sodium. Processed meats could pose health risks."
            zid=9055
            price="₹50 - ₹200"
            nut="https://en.wikipedia.org/wiki/Veggie_burger";
            category="Fast Food / Sandwiches"
        
        elif predicted_label == "1 butter_naan":
            cal = 350
            zid=68387
            details="Health Benefits: Offers carbohydrates for energy and some protein from the flour. It might provide a small amount of essential nutrients."
            hazards="Health Hazards: High in calories and refined carbohydrates, which could contribute to weight gain and elevated blood sugar levels. Contains saturated fats due to butter, which might pose cardiovascular risks if consumed in excess."
            price="₹20 - ₹50"
            category=" North Indian / Punjabi Cuisine"
            nut="https://en.wikipedia.org/wiki/Naan";
            
        

        elif predicted_label == "2 chai":
            cal = 40
            zid=13620
            details="Health Benefits: Contains antioxidants, particularly if brewed from tea leaves, offering potential health-promoting properties such as improved heart health and reduced risk of chronic diseases."
            hazards="Health Hazards: May have high sugar content, especially in sweetened chai, contributing to increased calorie intake. Caffeine in chai might pose concerns for some individuals, causing sleep disturbances or heightened anxiety."
            price="₹10 - ₹30 (per cup)"
            category="Beverages / Tea"
            nut="https://en.wikipedia.org/wiki/Masala_chai";
        elif predicted_label == "3 chapati":
            cal = 80
            zid=26919
            details="Health Benefits: Good source of complex carbohydrates and some protein."
            hazards="Health Hazards: Generally healthy but might contribute to weight gain if consumed in excess."
            price="₹5 - ₹15 (for 2-3 chapatis)"
            category="North Indian / Gujarati Cuisine"
            nut="https://en.wikipedia.org/wiki/Chapati";
        elif predicted_label == "4 chole_bhature":
            cal = 450
            zid=60192
            details="Health Benefits: Contains protein, fiber, and some vitamins. Offers a moderate nutritional profile due to the chickpeas, potentially aiding digestive health."
            hazards="Health Hazards: Often high in calories, unhealthy fats, and refined carbohydrates due to deep-fried bhature, contributing to weight gain and increased risk of heart disease."
            price="₹50 - ₹100"
            category="North Indian / Punjabi Cuisine"
            nut="https://en.wikipedia.org/wiki/Chole_bhature";
        elif predicted_label == "5 dal_makhani":
            cal = 200
            zid=44987
            details="Health Benefits: Rich in protein, fiber, and essential nutrients. The lentils used in the dish provide a good amount of dietary fiber, promoting digestive health."
            hazards="Health Hazards: Might be high in calories and saturated fats if made with excessive cream or ghee, contributing to weight gain and potentially elevating cholesterol levels."
            price="₹100 - ₹200"
            category="North Indian / Punjabi Cuisine"
            nut="https://en.wikipedia.org/wiki/Dal_makhani";
        elif predicted_label == "6 dholkla":
            cal = 200
            zid=66471
            details="Health Benefits: Made from a fermented batter, potentially aiding digestion and improving gut health due to beneficial probiotics."
            hazards="Health Hazards: May contain added sugars in the preparation, affecting overall calorie content, and potentially elevating blood sugar levels."
            price="₹30 - ₹70"
            category="Gujarati Cuisine"
            nut="https://en.wikipedia.org/wiki/Dhokla";
        elif predicted_label == "7 fried_rice":
            cal = 250
            zid=35301
            details="Health Benefits: Contains vegetables and carbohydrates."
            hazards="Health Hazards: High in calories, sodium, and potentially unhealthy fats depending on preparation."
            price="₹80 - ₹150"
            category="Indo-Chinese Cuisine"
            nut="https://en.wikipedia.org/wiki/Fried_rice";
        elif predicted_label == "8 idli":
            cal = 50
            zid=35114
            details="Health Benefits: Gluten-free, low in calories, and easily digestible."
            hazards="Health Hazards: Might be high in sodium, depending on the recipe."
            price="₹40 - ₹80 (4-6 idlis)"
            category="South Indian / Tamil Nadu Cuisine"
            nut="https://en.wikipedia.org/wiki/Idli";
        elif predicted_label == "9 jalebi":
            cal = 400
            price="₹20 - ₹50 (per serving)"
            zid=37104
            details="Health Benefits: None significant, except for energy from carbohydrates."
            hazards="Health Hazards: High in calories, sugar, and unhealthy fats due to frying process, contributing to weight gain and increased risk of diabetes and heart disease."
            category="Indian Sweet / Dessert (found across India)"
            nut="https://en.wikipedia.org/wiki/Jalebi";
        elif predicted_label == "10 kaathi_rolls":
            cal = 300
            zid=62927
            details="Health Benefits: Kathi rolls may offer a balance of macronutrients with carbohydrates from the wrap (paratha or roti) and proteins and essential nutrients from the fillings, potentially promoting satiety and energy."
            hazards="Health Hazards: These rolls can be calorically dense, with potential health risks associated with excessive calorie intake and potential adverse effects on lipid profiles due to high-fat content, particularly if deep-fried or laden with fatty ingredients."
            price="₹50 - ₹100"
            category="Indian Street Food (originated in Kolkata)"
            nut="https://en.wikipedia.org/wiki/Kati_roll";
        elif predicted_label == "11 kadai_paneer":
            cal = 250
            price=" ₹100 - ₹200"
            zid=63440
            hazards="Health Hazards: The preparation often involves high-calorie ingredients such as cream, ghee, and paneer, leading to a high energy density dish, potentially contributing to weight gain and adverse lipid profiles."
            details="Health Benefits: Kadai paneer provides a significant source of dietary protein from paneer (Indian cottage cheese) and calcium, contributing to essential nutrient intake."
            category=" North Indian / Punjabi Cuisine"
            nut="https://en.wikipedia.org/wiki/Kadai_paneer";
        elif predicted_label == "12 kulfi":
            cal = 250
            zid=32439
            details="Health Benefits: Provides calcium and some protein."
            hazards="Health Hazards: High in calories, sugar, and potentially unhealthy fats."
            price="₹50 (per serving)"
            category="North Indian Dessert"
            nut="https://en.wikipedia.org/wiki/Kulfi";
        elif predicted_label == "13 masala_dosa":
            cal = 200
            zid=70735
            details="Health Benefits: Masala dosa is typically low in fat and may provide dietary fiber if filled with vegetables. The fermentation process used in dosa preparation potentially improves bioavailability of nutrients and aids digestion."
            hazards="Health Hazards: High in carbohydrates due to rice and lentil batter, which may contribute to postprandial glycemic responses, particularly if served with high-carbohydrate fillings."
            price="₹50 - ₹110"
            category="South Indian / Karnataka Cuisine"
            nut="https://en.wikipedia.org/wiki/Masala_dosa"
        elif predicted_label == "14 momos":
            cal = 80
            zid=8497
            details="Health Benefits: Can contain vegetables and some protein."
            hazards="Health Hazards: Might be high in sodium, and potential for unhealthy fats depending on fillings."
            price="₹40 - ₹100 (6-8 pieces)"
            category="Tibetan / Nepali, Popular in Northeast India"
            nut="https://en.wikipedia.org/wiki/Momos";
        elif predicted_label == "15 paani_puri":
            cal = 70
              # Note: This is an approximate value per serving, not per 100 grams.
            zid=70230
            details="Health Benefits: Pani puri may contain some nutrients from fillings like sprouts and spices, potentially providing vitamins and antioxidants."
            hazards="Health Hazards: The dish is high in refined carbohydrates, causing rapid postprandial glycemic spikes and may lead to gastrointestinal discomfort if ingredients are not fresh."
            price="₹20 - ₹50 (6-8 pieces)"
            category="Indian Street Food (found across India)"
            nut="https://en.wikipedia.org/wiki/Panipuri";
        elif predicted_label == "16 pakode":
            cal = 300
            zid=13094
            details="Health Benefits: Pakode are a source of protein from chickpea flour (besan) and may offer dietary fiber if vegetables are incorporated in the batter."
            hazards="Health Hazards: These fried snacks are calorically dense and high in unhealthy trans fats and saturated fats, contributing to an energy-dense diet and increased risk of cardiovascular diseases."
            price="₹30 - ₹60"
            category="North Indian Snack (found across India)"
            nut="https://en.wikipedia.org/wiki/Falafel";
        elif predicted_label == "17 pav_bhaji":
            cal = 250
            zid=63559
            details="Health Benefits: Offers some vegetables and carbohydrates."
            hazards="Health Hazards: High in calories and potentially unhealthy due to butter and bread."
            price="₹50 - ₹100"
            category="Mumbai Street Food"
            nut="https://en.wikipedia.org/wiki/Pav_bhaji";
        elif predicted_label == "18 pizza":
            cal = 300
            details="Health Benefits: Can have some vegetables and dairy."
            hazards="Health Hazards: High in calories, unhealthy fats, and sodium. Processed meats can pose health risks."
            price="₹150 - ₹400 (varies widely based on size and toppings)"
            zid=68987
            category=" Italian origin but widely consumed in India with various toppings and variations"
            nut="https://en.wikipedia.org/wiki/Pizza";
        elif predicted_label == "19 samosa":
            cal = 350
            price="₹20 to ₹60 (2-3)"
            zid=871
            hazards="Health Hazards: High in calories, unhealthy fats, and potential allergens from fillings."
            details="Health Benefits: None significant, except for energy from carbohydrates."
            category="a popular snack in Indian cuisine"
            nut="https://en.wikipedia.org/wiki/Samosa";
        else:
            cal = 100
            zid=13620
            price=0
            hazards=""
            details=""
            category="NA"
            nut="https://en.wikipedia.org/wiki/Indian_cuisine";
    

        if zid !=11:
            return render_template('index.html',result=f'Prediction: {that} and calories per 100 grams is {cal}',pid=f'https://www.zomato.com/chennai/delivery?dishv2_id={zid}',nit=f'{nut}',cati=f'The category of food is :{category} and',pri=f'the cost for the food item is->{price}',deta=f'{details}',haza=f'{hazards}')
        else:
            return render_template('index.html',result=f'Prediction: {that} and calories per 100 grams is {cal}',pid=f'https://www.zomato.com/chennai',nit=f'{nut}',cati=f'The category of food is :{category} and',pri=f'the cost for the food item is->{price}',deta=f'{details}',haza=f'{hazards}')


if __name__ == '__main__':
    app.run(debug=True)