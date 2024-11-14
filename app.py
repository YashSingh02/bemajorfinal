import os
from webbrowser import BackgroundBrowser
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from gevent.pywsgi import WSGIServer


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Define a flask app
app = Flask(__name__)

# Load your trained model
model = load_model('/Users/yashsingh/Downloads/be major project/model.h5')


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        if f and allowed_file(f.filename):
            img_path = file_path  # Use file_path instead of filename
            img = image.load_img(img_path, target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = img / 255.0

            # Make prediction using the loaded model
            pred = model.predict(img)
            # Get top 3 predicted classes
            pred_classes = pred.argsort()[0][-3:][::-1]
            # Get corresponding probabilities
            pred_probs = pred[0][pred_classes]

            # Define a list of classes
            classes = ['adhirasam','aloo_gobi','aloo_matar','aloo_methi','aloo_shimla_mirch','aloo_tikki','anarsa',
                       'ariselu','bandar_laddu','basundi','bhatura','bhindi_masala','biryani',
    'boondi',
    'butter_chicken',
    'chak_hao_kheer',
    'cham_cham',
    'chana_masala',
    'chapati',
    'chhena_kheeri',
    'chicken_razala',
    'chicken_tikka',
    'chicken_tikka_masala',
    'chikki',
    'daal_baati_churma',
    'daal_puri',
    'dal_makhani',
    'dal_tadka',
    'dharwad_pedha',
    'doodhpak',
    'double_ka_meetha',
    'dum_aloo',
    'gajar_ka_halwa',
    'gavvalu',
    'ghevar',
    'gulab_jamun',
    'imarti',
    'jalebi',
    'kachori',
    'kadai_paneer',
    'kadhi_pakoda',
    'kajjikaya',
    'kakinada_khaja',
    'kalakand',
    'karela_bharta',
    'kofta',
    'kuzhi_paniyaram',
    'lassi',
    'ledikeni',
    'litti_chokha',
    'lyangcha',
    'maach_jhol',
    'makki_di_roti_sarson_da_saag',
    'malapua',
    'misi_roti',
    'misti_doi',
    'modak',
    'mysore_pak',
    'naan',
    'navrattan_korma',
    'palak_paneer',
    'paneer_butter_masala',
    'phirni',
    'pithe',
    'poha',
    'poornalu',
    'pootharekulu',
    'qubani_ka_meetha',
    'rabri',
    'ras_malai',
    'rasgulla',
    'sandesh',
    'shankarpali',
    'sheer_korma',
    'sheera',
    'shrikhand',
    'sohan_halwa',
    'sohan_papdi',
    'sutar_feni',
    'unni_appam'
]  # Replace with actual class names

            # Create a list of strings containing the predicted class names and corresponding probabilities
            result = [
                f'{classes[pred_classes[i]]}: {pred_probs[i]:.2%}' for i in range(3)]

            # Join the list elements with newline character
            result = '\n'.join(result)

            return result
        else:
            return "Invalid file format."



if __name__ == '__main__':
    app.run(debug=True, port=5001)
