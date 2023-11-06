import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify, request,redirect,url_for
from datetime import datetime
import requests
from werkzeug.middleware.proxy_fix import ProxyFix
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import itertools
from flask import session
cred = credentials.Certificate('frases-d0c4a-firebase-adminsdk-pouqr-d21029a1af.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://frases-d0c4a-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Load phrases from the text file into a list with UTF-8 encoding
with open('frasesbuenas.txt', 'r', encoding='utf-8') as file:
    phrasesb = [line.strip() for line in file]
# Load phrases from the text file into a list with UTF-8 encoding
with open('frasesmalas.txt', 'r', encoding='utf-8') as file:
    phrasesm = [line.strip() for line in file]
@app.route('/like', methods=['POST'])
@app.route('/like', methods=['POST'])
def like_color():
    background_color =  get_color_name(request.form.get('background_color'))
    predicted_color =  get_color_name(request.form.get('predicted_color'))
    random_phrase = request.form.get('random_phrase')
    random_button_color =  get_color_name(request.form.get('random_button_color'))
    timestamp = datetime.now()

    # Check if the random phrase is from 'phrasesb' (good phrases) or 'phrasesm' (bad phrases)
    if random_phrase in phrasesb:
        phrase_type = 'good'
    elif random_phrase in phrasesm:
        phrase_type = 'bad'

    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_list = user_ip.split(',')
    first_ip = ip_list[0].strip()

    response = requests.get(f'http://ip-api.com/json/{first_ip}')
    user_city = 'Unknown'
    if response.status_code == 200:
        data = response.json()
        user_city = data.get('city', 'Unknown')
    answer = [
        "yes",
        "no"
    ]
    partner_answer = random.choice(answer) 
    # Create a document to insert into Firebase
    doc = {
        'background_color': background_color,
        'text_color': predicted_color,
        'phrase': random_phrase,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'action': 'like',
        'ip': user_ip,
        'phrase_type': phrase_type,
        'city': user_city,
        'pareja': partner_answer,
        'random_button_color': random_button_color
    }

    # Push the document to Firebase
    ref = db.reference('Datos')
    ref.push(doc)

    # Handle any additional logic here
    return ('', 204)

@app.route('/dislike', methods=['POST'])
def dislike_color():
    background_color =  get_color_name(request.form.get('background_color'))
    predicted_color =  get_color_name(request.form.get('predicted_color'))
    random_phrase = request.form.get('random_phrase')
    random_button_color =  get_color_name(request.form.get('random_button_color'))
    timestamp = datetime.now()

    # Check if the random phrase is from 'phrasesb' (good phrases) or 'phrasesm' (bad phrases)
    if random_phrase in phrasesb:
        phrase_type = 'good'
    elif random_phrase in phrasesm:
        phrase_type = 'bad'

    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_list = user_ip.split(',')
    first_ip = ip_list[0].strip()

    response = requests.get(f'http://ip-api.com/json/{first_ip}')
    user_city = 'Unknown'
    if response.status_code == 200:
        data = response.json()
        user_city = data.get('city', 'Unknown')
    answer = [
        "yes",
        "no"
    ]
    partner_answer = random.choice(answer) 
    # Create a document to insert into Firebase
    doc = {
        'background_color': background_color,
        'text_color': predicted_color,
        'phrase': random_phrase,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'action': 'dislike',
        'ip': user_ip,
        'phrase_type': phrase_type,
        'city': user_city,
        'pareja': partner_answer,
        'random_button_color': random_button_color
    }

    # Push the document to Firebase
    ref = db.reference('Datos')
    ref.push(doc)

    # Handle any additional logic here
    return ('', 204)
class CustomRandomColor:
    def __init__(self, colors):
        self.colors = colors
        self.color_iterator = itertools.cycle(colors)

    def get_random_color(self):
        return next(self.color_iterator)
colors = [
        (255, 103, 0),   # Orange
        (255, 0, 0),     # Red
        (255, 255, 0),   # Yellow
        (0, 255, 0),     # Green
        (0, 0, 255),     # Blue
        (75, 0, 130),    # Indigo
        (238,130,238),    # Violet
        
    ]
color_names = {
    tuple([255, 103, 0]): 'Naranja',
    tuple([255, 0, 0]): 'Rojo',
    tuple([255, 255, 0]): 'Amarillo',
    tuple([0, 255, 0]): 'Verde',
    tuple([0, 0, 255]): 'Azul',
    tuple([75, 0, 130]): 'Indigo',
    tuple([238, 130, 238]): 'Violeta',
}

def get_color_name(rgb):
    # Convert the string representation to a list
    rgb_list = eval(rgb)

    for color, name in color_names.items():
        print(f"Comparing {color} with {rgb_list}")
        if color == tuple(rgb_list):
            return name

    return 'Naranja'



    
 # Return 'Unknown' if the RGB value is not found in the dictionary


class ColorPicker:
    def __init__(self):
        self.colors = [
            [255, 103, 0],   # Orange
            [255, 0, 0],     # Red
            [255, 255, 0],   # Yellow
            [0, 255, 0],     # Green
            [0, 0, 255],     # Blue
            [75, 0, 130],    # Indigo
            [238,130,238]    # Violet
        ]
        random.shuffle(self.colors)
        self.color_index = 0

    def get_next_color(self):
        color = self.colors[self.color_index]
        self.color_index = (self.color_index + 1) % len(self.colors)
        return color

# Initialize the ColorPicker
color_picker = ColorPicker()
# Create an instance of the custom random color generator
color_generator = CustomRandomColor(colors)
@app.route('/')
def index():
    # Generate a random background color from the seven rainbow colors
    random_background_color = color_picker.get_next_color()
    if request.method == 'POST':
        partner_answer = request.form.get('partnerAnswer')
        session['partner_answer'] = partner_answer

    # Use the trained model to predict text color
    #random_background_color_tensor = torch.tensor(random_background_color, dtype=torch.float32)
    #predicted_text_color_tensor = model(random_background_color_tensor)
    #predicted_text_color = predicted_text_color_tensor.tolist()
# Generate random text color 
    
    predicted_text_color = color_picker.get_next_color()

    # Choose a random phrase from either 'phrasesb' or 'phrasesm' at random
    if random.randint(0, 1) == 0:
        random_phrase = random.choice(phrasesb)
    else:
        random_phrase = random.choice(phrasesm)

    return render_template('index.html', random_color=random_background_color, predicted_color=predicted_text_color, random_phrase=random_phrase)
@app.route('/futuro', methods=['GET', 'POST'])
def prediction():
    partner_answer = None

    if request.method == 'POST':
        # Capture the selected partner answer from the form
        partner_answer = request.form.get('partner')

    random_background_color = color_picker.get_next_color()
    random_button_color = color_picker.get_next_color()
    # Use the trained model to predict text color
    #random_background_color_tensor = torch.tensor(random_background_color, dtype=torch.float32)
    #predicted_text_color_tensor = model(random_background_color_tensor)
    #predicted_text_color = predicted_text_color_tensor.tolist()
# Generate random text color 
    
    predicted_text_color = color_picker.get_next_color()

    # Choose a random phrase from either 'phrasesb' or 'phrasesm' at random
    if random.randint(0, 1) == 0:
        random_phrase = random.choice(phrasesb)
    else:
        random_phrase = random.choice(phrasesm)
    if request.referrer is None:
        return redirect(url_for('index'))  # Redirect to the root URL
    else:
        # Continue with normal rendering for non-direct access
        return render_template('prediction.html', random_color=random_background_color, predicted_color=predicted_text_color, random_phrase=random_phrase,partner_answer=partner_answer,random_button_color=random_button_color)
    
if __name__ == '__main__':
    app.run(debug=True)
