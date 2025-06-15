import torch
import torch.nn as nn
import numpy as np

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

def generate_password(model, seed, char2idx, idx2char, vocab_size, gen_length=10):
    model.eval()
    with torch.no_grad():
        input_seq = [char2idx[ch] for ch in seed if ch in char2idx]
        # Add batch dimension
        input_tensor = torch.tensor(input_seq, dtype=torch.long).unsqueeze(0)
        hidden = None
        generated = seed
        for _ in range(gen_length):
            output, hidden = model(input_tensor, hidden)
            last_output = output[:, -1, :]
            prob = torch.softmax(last_output, dim=-1).squeeze().cpu().numpy()
            # Sample a token according to the probability distribution
            sampled_token_index = np.random.choice(range(vocab_size), p=prob)
            sampled_char = idx2char[sampled_token_index]
            generated += sampled_char
            input_tensor = torch.tensor([[sampled_token_index]], dtype=torch.long)
        return generated

pipeline = torch.load("password_rnn_pipeline.h5")
char2idx = pipeline["char2idx"]
idx2char = pipeline["idx2char"]
vocab_size = pipeline["vocab_size"]
hidden_size = pipeline["hidden_size"]
num_layers = pipeline["num_layers"]
model = PasswordRNN(vocab_size, hidden_size, num_layers)
model.load_state_dict(pipeline["model_state_dict"])
seed_text = input("Enter a seed text for password generation: ")
generated_password = generate_password(model, seed_text, char2idx, idx2char, vocab_size, gen_length=8)
print("Generated password:", generated_password)