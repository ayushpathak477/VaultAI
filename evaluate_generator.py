import numpy as np
import pandas as pd
import tensorflow as tf
from tqdm import tqdm
import random
import string
import json

# Import the heuristic analysis functions from your Flask app
from app import calculate_entropy, check_password_strength

# --- 1. Load the Keras Model and the SAVED Vocabulary ---
print("Loading the AI model and its vocabulary...")
try:
    model = tf.keras.models.load_model('strong_password_generator.h5')
    with open('char_to_int.json', 'r') as f:
        char_to_int = json.load(f)
    
    int_to_char = {i: c for c, i in char_to_int.items()}
    vocab_size = len(char_to_int)
    seq_length = model.input_shape[1] 

    print("Model and vocabulary loaded successfully!")
except Exception as e:
    print(f"Error loading model or vocabulary: {e}")
    exit()

# --- 2. FINAL Generation Function with Rule Enforcement ---
def generate_password_keras(model, seed, length=12, temperature=0.75):
    """Generates a password and then enforces character type rules."""
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
        result = int_to_char.get(index, '')
        password += result
        pattern.append(index)
        pattern = pattern[1:]
    
    # Rule Enforcement Part
    # Ensure at least one of each required character type is present.
    if not any(c.islower() for c in password):
        password += random.choice(string.ascii_lowercase)
    if not any(c.isupper() for c in password):
        password += random.choice(string.ascii_uppercase)
    if not any(c.isdigit() for c in password):
        password += random.choice(string.digits)
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        password += random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
        
    return password

# --- 3. Generate a Large Sample of Passwords ---
num_passwords_to_generate = 500
print(f"\\nGenerating {num_passwords_to_generate} final passwords...")
seeds = ["password", "dragon", "sunshine", "qwerty123", "secret", "football", "master", "trustno1"]
generated_passwords = []
for i in tqdm(range(num_passwords_to_generate)):
    seed = random.choice(seeds)
    new_password = generate_password_keras(model, seed, length=random.randint(12, 16))
    generated_passwords.append(new_password)
print("Password generation complete.")

# --- 4. Analyze the Quality of the Generated Passwords ---
print("\\nAnalyzing final generated passwords...")
total_entropy = 0
strong_password_count = 0
for pwd in generated_passwords:
    total_entropy += calculate_entropy(pwd)
    analysis = check_password_strength(pwd)
    if analysis['strength'] == 'Strong':
        strong_password_count += 1

# Calculate final metrics
average_entropy = total_entropy / num_passwords_to_generate
uniqueness_percentage = (len(set(generated_passwords)) / num_passwords_to_generate) * 100
strength_percentage = (strong_password_count / num_passwords_to_generate) * 100

# --- 5. Print the Final Report ---
print("\\n--- FINAL AI Generator Evaluation Report ---")
print(f"Total Passwords Generated: {num_passwords_to_generate}")
print(f"Average Shannon Entropy:   {average_entropy:.2f} bits")
print(f"Uniqueness:                {uniqueness_percentage:.1f}%")
print(f"Rated 'Strong' by Analyzer: {strength_percentage:.1f}%")
print("------------------------------------------")