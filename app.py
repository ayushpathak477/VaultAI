from flask import Flask, render_template, request, jsonify
import torch
import torch.nn as nn
import numpy as np
import re
import math
from collections import Counter
import os

class PasswordRNN(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers):
        super(PasswordRNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.rnn = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)
    
    def forward(self, x, hidden=None):
        x = self.embedding(x)
        out, hidden = self.rnn(x, hidden)
        out = self.fc(out)
        return out, hidden

def calculate_entropy(password):
    """Calculate Shannon entropy of the password"""
    if not password:
        return 0
    char_counts = Counter(password)
    length = len(password)
    entropy = 0
    for count in char_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy

def check_password_strength(password):
    """Analyze password strength based on multiple parameters"""
    analysis = {
        'length': len(password),
        'entropy': calculate_entropy(password),
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_numbers': bool(re.search(r'[0-9]', password)),
        'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        'has_common_patterns': bool(re.search(r'(.)\1{2,}', password)),
        'is_common_password': password.lower() in common_passwords,
        'score': 0,
        'strength': '',
        'feedback': []
    }
    
    # Calculate score
    if analysis['length'] >= 12:
        analysis['score'] += 2
    elif analysis['length'] >= 8:
        analysis['score'] += 1
    
    if analysis['entropy'] >= 3.5:
        analysis['score'] += 2
    elif analysis['entropy'] >= 2.5:
        analysis['score'] += 1
    
    if analysis['has_uppercase']:
        analysis['score'] += 1
    if analysis['has_lowercase']:
        analysis['score'] += 1
    if analysis['has_numbers']:
        analysis['score'] += 1
    if analysis['has_special']:
        analysis['score'] += 1
    
    if analysis['has_common_patterns']:
        analysis['score'] -= 1
    if analysis['is_common_password']:
        analysis['score'] -= 2
    
    # Determine strength level
    if analysis['score'] >= 7:
        analysis['strength'] = 'Strong'
    elif analysis['score'] >= 4:
        analysis['strength'] = 'Medium'
    else:
        analysis['strength'] = 'Weak'
    
    # Generate feedback
    if analysis['length'] < 8:
        analysis['feedback'].append('Password is too short. Use at least 8 characters.')
    if not analysis['has_uppercase']:
        analysis['feedback'].append('Add uppercase letters for better security.')
    if not analysis['has_lowercase']:
        analysis['feedback'].append('Add lowercase letters for better security.')
    if not analysis['has_numbers']:
        analysis['feedback'].append('Include numbers for better security.')
    if not analysis['has_special']:
        analysis['feedback'].append('Add special characters for better security.')
    if analysis['has_common_patterns']:
        analysis['feedback'].append('Avoid repeated characters.')
    if analysis['is_common_password']:
        analysis['feedback'].append('This is a common password. Choose something more unique.')
    
    return analysis

def generate_password(model, seed, char2idx, idx2char, vocab_size, gen_length=10):
    model.eval()
    with torch.no_grad():
        input_seq = [char2idx[ch] for ch in seed if ch in char2idx]
        input_tensor = torch.tensor(input_seq, dtype=torch.long).unsqueeze(0)
        hidden = None
        generated = seed
        for _ in range(gen_length):
            output, hidden = model(input_tensor, hidden)
            last_output = output[:, -1, :]
            prob = torch.softmax(last_output, dim=-1).squeeze().cpu().numpy()
            sampled_token_index = np.random.choice(range(vocab_size), p=prob)
            sampled_char = idx2char[sampled_token_index]
            generated += sampled_char
            input_tensor = torch.tensor([[sampled_token_index]], dtype=torch.long)
        return generated

app = Flask(__name__)

# Common passwords list
common_passwords = {
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey123',
    'letmein', 'dragon', '111111', 'baseball', 'iloveyou', 'trustno1',
    'sunshine', 'master', 'welcome', 'shadow', 'ashley', 'football',
    'jesus', 'michael', 'ninja', 'mustang', 'password1'
}

# Initialize model and pipeline data
try:
    if not os.path.exists("password_rnn_pipeline.h5"):
        raise FileNotFoundError("Model file 'password_rnn_pipeline.h5' not found")
    
    pipeline = torch.load("password_rnn_pipeline.h5")
    char2idx = pipeline["char2idx"]
    idx2char = pipeline["idx2char"]
    vocab_size = pipeline["vocab_size"]
    hidden_size = pipeline["hidden_size"]
    num_layers = pipeline["num_layers"]
    model = PasswordRNN(vocab_size, hidden_size, num_layers)
    model.load_state_dict(pipeline["model_state_dict"])
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        seed_text = request.json.get('seed_text', '')
        if not seed_text:
            return jsonify({'error': 'Please provide a seed text'}), 400
        invalid_chars = [ch for ch in seed_text if ch not in char2idx]
        if invalid_chars:
            return jsonify({
                'error': f'Invalid characters in seed text: {", ".join(invalid_chars)}'
            }), 400
        
        generated_password = generate_password(model, seed_text, char2idx, idx2char, vocab_size, gen_length=8)
        return jsonify({'password': generated_password})
    
    except Exception as e:
        print(f"Error generating password: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
