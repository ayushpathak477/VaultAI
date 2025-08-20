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
    elif analysis['entropy'] >= 4.0: analysis['score'] += 2
    elif analysis['entropy'] >= 3.0: analysis['score'] += 1
    
    # Character diversity
    diversity_score = sum([analysis['has_uppercase'], analysis['has_lowercase'], 
                         analysis['has_numbers'], analysis['has_special']])
    analysis['score'] += diversity_score
    
    # Penalties
    if analysis['is_common_password']:
        analysis['score'] -= 5
    
    # Final strength determination with adjusted thresholds for long passwords
    if analysis['length'] >= 20 and analysis['score'] >= 8:  # Special case for very long passwords
        analysis['strength'] = 'strong'
    elif analysis['score'] >= 10:
        analysis['strength'] = 'strong'
    elif analysis['score'] >= 6:
        analysis['strength'] = 'medium'
    else:
        analysis['strength'] = 'weak'
    
    return analysis

# --- Model Setup and Loading ---
app = Flask(__name__)

# Load the trained model and character mappings
try:
    model = tf.keras.models.load_model('strong_password_generator.h5')
    print("Model loaded successfully!")
    
    # Load character mappings
    with open('char_to_int.json', 'r') as f:
        char_to_int = json.load(f)
    
    int_to_char = {v: k for k, v in char_to_int.items()}
    print(f"Character mappings loaded. Vocabulary size: {len(char_to_int)}")
    
except Exception as e:
    print(f"Error loading model or character mappings: {e}")
    model = None
    char_to_int = None
    int_to_char = None

# --- Password Generation ---
def generate_password_with_model(length=12):
    if model is None or char_to_int is None:
        # Fallback to heuristic generation
        return generate_heuristic_password(length)
    
    try:
        # Start with a random character from vocabulary
        start_char = random.choice(list(char_to_int.keys()))
        generated = start_char
        
        # Use model to predict next characters
        for _ in range(length - 1):
            # Prepare input sequence (last 10 chars or available chars)
            input_sequence = generated[-10:] if len(generated) >= 10 else generated
            
            # Convert to integers
            input_ints = [char_to_int.get(c, 0) for c in input_sequence]
            
            # Pad if necessary
            while len(input_ints) < 10:
                input_ints.insert(0, 0)
            
            # Reshape for model
            input_array = np.array(input_ints).reshape(1, 10, 1)
            
            # Predict next character
            prediction = model.predict(input_array, verbose=0)
            
            # Sample from the prediction (with some randomness)
            predicted_int = np.random.choice(len(prediction[0]), p=prediction[0])
            
            # Convert back to character
            next_char = int_to_char.get(predicted_int, random.choice(list(char_to_int.keys())))
            generated += next_char
        
        return generated
        
    except Exception as e:
        print(f"Error in model generation: {e}")
        return generate_heuristic_password(length)

def generate_heuristic_password(length=12):
    """Fallback password generation using heuristics"""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one from each category
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest randomly
    all_chars = lowercase + uppercase + digits + special
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    
    # Shuffle to avoid predictable pattern
    random.shuffle(password)
    return ''.join(password)

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        length = data.get('length', 12)
        
        # Ensure length is within reasonable bounds
        length = max(8, min(50, int(length)))
        
        generated_password = generate_password_with_model(length)
        
        return jsonify({'password': generated_password})
    
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    password = data.get('password', '')
    
    analysis = check_password_strength(password)
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)
