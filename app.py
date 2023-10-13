import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify, request,redirect,url_for
from pymongo import MongoClient
from datetime import datetime
import requests
from werkzeug.middleware.proxy_fix import ProxyFix
# Connect to MongoDB (replace with your connection details)
client = MongoClient('mongodb+srv://rele:123@cluster0.u0z21ys.mongodb.net')
db = client['tecnologiasEmergentes']
collection = db['infopipol']

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Load phrases from the text file into a list with UTF-8 encoding
with open('frasesbuenas.txt', 'r', encoding='utf-8') as file:
    phrasesb = [line.strip() for line in file]
# Load phrases from the text file into a list with UTF-8 encoding
with open('frasesmalas.txt', 'r', encoding='utf-8') as file:
    phrasesm = [line.strip() for line in file]
@app.route('/like', methods=['POST'])
def like_color():
    # Get the background color, predicted color, and random phrase
    background_color = request.form.get('background_color')
    predicted_color = request.form.get('predicted_color')
    random_phrase = request.form.get('random_phrase')
    # Convert background_color and predicted_color to RGB format
    background_color_rgb = f'rgb({background_color[0]}, {background_color[1]}, {background_color[2]})'
    predicted_color_rgb = f'rgb({predicted_color[0]}, {predicted_color[1]}, {predicted_color[2]})'
    # Get the current timestamp
    timestamp = datetime.now()
    
    # Check if the random phrase is from 'prasesb' (good phrases) or 'prasesm' (bad phrases)
    if random_phrase in phrasesb:
        phrase_type = 'good'
    elif random_phrase in phrasesm:
        phrase_type = 'bad'
    
     # Get the user's IP address
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_list = user_ip.split(',')
    first_ip = ip_list[0].strip() 
    # Perform an IP geolocation lookup
    response = requests.get(f'http://ip-api.com/json/{first_ip}')
    
    if response.status_code == 200:
        data = response.json()
        user_city = data.get('city', 'Unknown')
    else:
        user_city = 'Unknown'
    # Create a document to insert into MongoDB
    doc = {
        'background_color': background_color,
        'text_color': predicted_color,
        'phrase': random_phrase,
        'timestamp': timestamp,
        'action': 'like',
        'ip': user_ip,
        'phrase_type': phrase_type,
        'city': user_city
        
    }
    
    # Insert the document into MongoDB
    collection.insert_one(doc)
    
    # Handle any additional logic here
    return ('', 204)

@app.route('/dislike', methods=['POST'])
def dislike_color():
    # Get the background color, predicted color, and random phrase
    background_color = request.form.get('background_color')
    predicted_color = request.form.get('predicted_color')
    random_phrase = request.form.get('random_phrase')
    # Convert background_color and predicted_color to RGB format
    background_color_rgb = f'rgb({background_color[0]}, {background_color[1]}, {background_color[2]})'
    predicted_color_rgb = f'rgb({predicted_color[0]}, {predicted_color[1]}, {predicted_color[2]})'
    # Get the current timestamp
    timestamp = datetime.now()
    
    # Check if the random phrase is from 'prasesb' (good phrases) or 'prasesm' (bad phrases)
    if random_phrase in phrasesb:
        phrase_type = 'good'
    elif random_phrase in phrasesm:
        phrase_type = 'bad'
    
     # Get the user's IP address
    user_ip = request.remote_addr
    ip_list = user_ip.split(',')
    first_ip = ip_list[0].strip() 
    # Perform an IP geolocation lookup
    response = requests.get(f'http://ip-api.com/json/{first_ip}')
    
    if response.status_code == 200:
        data = response.json()
        user_city = data.get('city', 'Unknown')
    else:
        user_city = 'Unknown'
    # Create a document to insert into MongoDB
    doc = {
        'background_color': background_color,
        'text_color': predicted_color,
        'phrase': random_phrase,
        'timestamp': timestamp,
        'action': 'like',
        'phrase_type': phrase_type,
        'city': user_city
        
    }
    
    # Insert the document into MongoDB
    collection.insert_one(doc)
    
    # Handle any additional logic here
    return ('', 204)
@app.route('/')
def index():
    # Generate a random background color from the seven rainbow colors
    rainbow_colors = [
        [255, 128, 0],   # Orange
        [255, 0, 0],     # Red
        [255, 255, 0],   # Yellow
        [0, 255, 0],     # Green
        [0, 0, 255],     # Blue
        [75, 0, 130],    # Indigo
        [148, 0, 211]    # Violet
    ]

    random_background_color = random.choice(rainbow_colors)

    # Use the trained model to predict text color
    #random_background_color_tensor = torch.tensor(random_background_color, dtype=torch.float32)
    #predicted_text_color_tensor = model(random_background_color_tensor)
    #predicted_text_color = predicted_text_color_tensor.tolist()
# Generate random text color 
    
    predicted_text_color = random.choice(rainbow_colors)
    # Choose a random phrase from either 'phrasesb' or 'phrasesm' at random
    if random.randint(0, 1) == 0:
        random_phrase = random.choice(phrasesb)
    else:
        random_phrase = random.choice(phrasesm)

    return render_template('index.html', random_color=random_background_color, predicted_color=predicted_text_color, random_phrase=random_phrase)
@app.route('/futuro')
def prediction():
    # Generate a random background color from the seven rainbow colors
    rainbow_colors = [
        [255, 128, 0],   # Orange
        [255, 0, 0],     # Red
        [255, 255, 0],   # Yellow
        [0, 255, 0],     # Green
        [0, 0, 255],     # Blue
        [75, 0, 130],    # Indigo
        [148, 0, 211]    # Violet
    ]

    random_background_color = random.choice(rainbow_colors)

    # Use the trained model to predict text color
    #random_background_color_tensor = torch.tensor(random_background_color, dtype=torch.float32)
    #predicted_text_color_tensor = model(random_background_color_tensor)
    #predicted_text_color = predicted_text_color_tensor.tolist()
# Generate random text color 
    
    predicted_text_color = random.choice(rainbow_colors)
    # Choose a random phrase from either 'phrasesb' or 'phrasesm' at random
    if random.randint(0, 1) == 0:
        random_phrase = random.choice(phrasesb)
    else:
        random_phrase = random.choice(phrasesm)
    
    return render_template('prediction.html', random_color=random_background_color, predicted_color=predicted_text_color, random_phrase=random_phrase)
    
    
if __name__ == '__main__':
    app.run(debug=True)
