# something.py (Final Version)

import tensorflow as tf
import numpy as np
import json
import random
import string

# --- Load the Keras Model and Vocabulary ---
print("Loading Keras model and vocabulary...")
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

# --- Password Generation Function ---
def generate_password_keras(model, seed, length=12, temperature=0.75):
    """Generates a password and enforces character type rules."""
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
    
    if not any(c.islower() for c in password): password += random.choice(string.ascii_lowercase)
    if not any(c.isupper() for c in password): password += random.choice(string.ascii_uppercase)
    if not any(c.isdigit() for c in password): password += random.choice(string.digits)
    if not any(c in "!@#$%" for c in password): password += random.choice("!@#$%")
        
    return password

# --- Main Execution Block ---
if __name__ == "__main__":
    seed_text = input("Enter a seed text for password generation: ")
    generated_password = generate_password_keras(model, seed_text, length=random.randint(12, 16))
    print("Generated password:", generated_password)