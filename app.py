import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
# Connect to MongoDB (replace with your connection details)
client = MongoClient('mongodb+srv://rele:123@cluster0.u0z21ys.mongodb.net/')
db = client['tecnologiasEmergentes']
collection = db['infopipol']

app = Flask(__name__)

class ColorGenerator(nn.Module):
    def __init__(self):
        super(ColorGenerator, self).__init__()
        self.fc1 = nn.Linear(3, 256)  # Increase the size of the hidden layers
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))
        return x

# Create the model
model = ColorGenerator()

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Generate a larger and more diverse dataset
num_samples = 5000
background_colors = torch.rand(num_samples, 3)
text_colors = torch.rand(num_samples, 3)

# Training loop
num_epochs = 5000  # Increase the number of epochs for better training
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(background_colors)
    loss = criterion(outputs, text_colors)
    loss.backward()
    optimizer.step()
# Load phrases from the text file into a list with UTF-8 encoding
with open('frases.txt', 'r', encoding='utf-8') as file:
    phrases = [line.strip() for line in file]
def calculate_contrast_ratio(color):
    # Calculate the relative luminance of the color
    r, g, b = color
    r = r / 255.0 if r <= 1.0 else r
    g = g / 255.0 if g <= 1.0 else g
    b = b / 255.0 if b <= 1.0 else b
    luminance = 0.299 * r + 0.587 * g + 0.114 * b

    # Calculate the contrast ratio
    contrast_ratio = (luminance + 0.05) / (0.05 + luminance)

    return contrast_ratio
@app.route('/like', methods=['POST'])
def like_color():
    # Get the background color, predicted color, and random phrase
    background_color = request.form.get('background_color')
    predicted_color = request.form.get('predicted_color')
    random_phrase = request.form.get('random_phrase')
    
    # Get the current timestamp
    timestamp = datetime.now()
    # Get the user's IP address
    user_ip = request.remote_addr
    # Create a document to insert into MongoDB
    doc = {
        'background_color': background_color,
        'text_color': predicted_color,
        'phrase': random_phrase,
        'timestamp': timestamp,
        'ip_address': user_ip,
        'action': 'like'
    }
    
    # Insert the document into MongoDB
    collection.insert_one(doc)
    
    # Handle any additional logic here
    return 'Soy ese'

@app.route('/dislike', methods=['POST'])
def dislike_color():
    # Get the background color, predicted color, and random phrase
    background_color = request.form.get('background_color')
    predicted_color = request.form.get('predicted_color')
    random_phrase = request.form.get('random_phrase')
    
    # Get the current timestamp
    timestamp = datetime.now()
    # Get the user's IP address
    user_ip = request.remote_addr
    # Create a document to insert into MongoDB
    doc = {
        'background_color': background_color,
        'text_color': predicted_color,
        'phrase': random_phrase,
        'timestamp': timestamp,
        'ip_address': user_ip,
        'action': 'dislike'
    }
    
    # Insert the document into MongoDB
    collection.insert_one(doc)
    
    # Handle any additional logic here
    return 'Ni modo'
@app.route('/')
def index():
     # Generate random background color
    random_background_color = torch.rand(3).tolist()

    # Use the trained model to predict text color
    random_background_color_tensor = torch.tensor(random_background_color, dtype=torch.float32)
    predicted_text_color_tensor = model(random_background_color_tensor)
    predicted_text_color = predicted_text_color_tensor.tolist()

    # Calculate the contrast ratio between background and predicted text color
    contrast_ratio = calculate_contrast_ratio(predicted_text_color)

    # Determine the text color based on the contrast ratio
    if contrast_ratio >= 4.5:
        text_color = [0, 0, 0]  # Use black text on light background
    else:
        text_color = [255, 255, 255]  # Use white text on dark background

    # Choose a random phrase from the list
    random_phrase = random.choice(phrases)

    return render_template('index.html', random_color=random_background_color, predicted_color=predicted_text_color, random_phrase=random_phrase, text_color=text_color)

if __name__ == '__main__':
    app.run(debug=True)
