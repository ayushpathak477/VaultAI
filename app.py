# app.py (Final Version)

from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import re
import math
from collections import Counter
import os
import json
import random
import string

# --- Password Strength Analysis (Heuristics - No change needed here) ---
def calculate_entropy(password):
    if not password:
        return 0
    char_counts = Counter(password)
    length = len(password)
    entropy = sum([- (count / length) * math.log2(count / length) for count in char_counts.values()])
    return entropy

common_passwords = {
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey123',
    'letmein', 'dragon', '111111', 'baseball', 'iloveyou', 'trustno1'
}

def check_password_strength(password):
    analysis = {
        'length': len(password),
        'entropy': calculate_entropy(password),
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_numbers': bool(re.search(r'[0-9]', password)),
        'has_special': bool(re.search(r'[^a-zA-Z0-9]', password)),
        'is_common_password': password.lower() in common_passwords,
        'score': 0,
        'strength': ''
    }
    
    # Enhanced scoring logic that properly weights length and entropy
    # Length scoring - heavily weight very long passwords
    if analysis['length'] >= 50: analysis['score'] += 6  # Very long passwords are inherently strong
    elif analysis['length'] >= 25: analysis['score'] += 4
    elif analysis['length'] >= 16: analysis['score'] += 3
    elif analysis['length'] >= 12: analysis['score'] += 2
    elif analysis['length'] >= 8: analysis['score'] += 1
    
    # Entropy scoring - this is crucial for randomness
    if analysis['entropy'] >= 4.5: analysis['score'] += 3
    elif analysis['entropy'] >= 3.5: analysis['score'] += 2
    elif analysis['entropy'] >= 2.5: analysis['score'] += 1
    
    # Character diversity (less weight for very long passwords)
    if analysis['has_uppercase']: analysis['score'] += 1
    if analysis['has_lowercase']: analysis['score'] += 1
    if analysis['has_numbers']: analysis['score'] += 1
    if analysis['has_special']: analysis['score'] += 1
    
    # Penalties
    if analysis['is_common_password']: analysis['score'] -= 3
    
    # Special case: Very long passwords with decent entropy should be strong
    if analysis['length'] >= 30 and analysis['entropy'] >= 2.0:
        analysis['score'] = max(analysis['score'], 7)  # Ensure it's at least Strong
    
    if analysis['score'] >= 7: analysis['strength'] = 'Strong'
    elif analysis['score'] >= 4: analysis['strength'] = 'Medium'
    else: analysis['strength'] = 'Weak'
    
    return analysis
# --- AI Model Loading and Generation (Updated Section) ---
app = Flask(__name__)

try:
    print("Loading Keras model and vocabulary...")
    model = tf.keras.models.load_model('strong_password_generator.h5')
    with open('char_to_int.json', 'r') as f:
        char_to_int = json.load(f)
    
    int_to_char = {i: c for c, i in char_to_int.items()}
    vocab_size = len(char_to_int)
    seq_length = model.input_shape[1]
    print("Model and vocabulary loaded successfully!")
except Exception as e:
    print(f"FATAL: Could not load model or vocabulary. Error: {e}")
    model = None # Set model to None if loading fails

def generate_password_keras(model, seed, length=12, temperature=0.75):
    """Generates a password and enforces character type rules."""
    if model is None:
        return "Error: Model not loaded."
        
    # AI Generation Part
    pattern = [char_to_int.get(char, 0) for char in seed[-seq_length:]]
    password = seed
    for _ in range(length - len(seed)):
        x = np.reshape(pattern, (1, len(pattern), 1)) / float(vocab_size)
        prediction = model.predict(x, verbose=0)[0]
        prediction = np.log(prediction) / temperature
        exp_preds = np.exp(prediction)
        prediction = exp_preds / np.sum(exp_preds)
        index = np.random.choice(range(vocab_size), p=prediction)
        password += int_to_char.get(index, '')
        pattern.append(index)
        pattern = pattern[1:]
    
    # Rule Enforcement Part
    if not any(c.islower() for c in password): password += random.choice(string.ascii_lowercase)
    if not any(c.isupper() for c in password): password += random.choice(string.ascii_uppercase)
    if not any(c.isdigit() for c in password): password += random.choice(string.digits)
    if not any(c in "!@#$%" for c in password): password += random.choice("!@#$%")
        
    return password

# --- Flask Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if model is None:
        return jsonify({'error': 'Model is not available.'}), 500
        
    seed_text = request.json.get('seed_text', '')
    if not seed_text:
        return jsonify({'error': 'Please provide a seed text'}), 400
    
    generated_password = generate_password_keras(model, seed_text, length=random.randint(12, 16))
    return jsonify({'password': generated_password})

@app.route('/analyze', methods=['POST'])
def analyze():
    password = request.json.get('password', '')
    if not password:
        return jsonify({'error': 'Please provide a password'}), 400
    
    analysis = check_password_strength(password)
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)