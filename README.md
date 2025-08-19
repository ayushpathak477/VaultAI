# VaultAI - AI-Powered Password Strength Analyzer & Generator

## Overview
This project is an advanced **Password Strength Analyzer and AI Generator**, originally developed for the Barclays Hack-O-Earth Hackathon. It features a sophisticated front-end that provides real-time, heuristic-based strength analysis and an AI backend that generates highly secure and unique passwords.

The core of the project is a refined **TensorFlow LSTM model** trained on a "gold standard" dataset of over 4,600 complex, high-entropy passwords filtered from the RockYou dataset. This ensures the generated passwords are not only random but also learn the structural patterns of real-world secure passwords.

## Final Performance Metrics
After a full refinement and debugging cycle, the final AI model achieves the following performance on a sample of 500 generated passwords:
- **Average Shannon Entropy:** 3.62 bits
- **Uniqueness:** 100.0%
- **Rated "Strong" by Analyzer:** 100.0%

## Features
- **Real-Time Strength Analysis:** An interactive web interface powered by Flask provides instant feedback on password strength as you type, using backend API calls for consistent analysis.
- **AI-Powered Password Generation:** Uses the trained LSTM model with temperature sampling to generate creative, non-repetitive, and secure passwords.
- **Enhanced Scoring Logic:** Improved password strength assessment that properly weights length and entropy, especially for very long passwords.
- **Rule Enforcement:** A post-processing step ensures that every AI-generated password meets strict criteria (e.g., contains uppercase, lowercase, numbers, and symbols).
- **High-Quality Training Data:** The model was trained on a filtered, high-entropy subset of the RockYou dataset.
- **Complete Project Documentation:** Includes a Jupyter Notebook (`xaibarclays.ipynb`) detailing all research, data processing, and model training steps.

## Files
- `app.py`: The main Flask web application with `/analyze` endpoint for password strength evaluation.
- `strong_password_generator.h5`: The final, trained TensorFlow/Keras AI model.
- `char_to_int.json`: The vocabulary file required by the trained model.
- `requirements.txt`: Dependencies required to run the project.
- `evaluate_generator.py`: A script to evaluate the performance of the trained AI model.
- `test_generator.py`: Interactive script to test individual password generation.
- `xaibarclays.ipynb`: The Jupyter notebook for research, data processing, and model training.
- `templates/index.html`: The frontend user interface that connects to the Flask backend.
- `gold_standard_passwords.csv`: The curated dataset of high-entropy passwords used for training.

## Installation
### Prerequisites
- Python 3.10+
- TensorFlow
- Flask
- Pandas, Scikit-learn, and other packages listed in `requirements.txt`.

### Installation Steps
1. **Clone the repository:**
    ```bash
    git clone https://github.com/ayushpathak477/VaultAI.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd VaultAI
    ```

3. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

4. **Activate the virtual environment:**
    - Windows: `.venv\Scripts\activate`
    - macOS/Linux: `source .venv/bin/activate`

5. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Run the Flask application:**
    ```bash
    python app.py
    ```

2. **Open your browser and go to:**
    ```
    http://127.0.0.1:5000/
    ```

3. **Test the password strength analyzer by typing any password in the input field**

4. **Use the "Generate Better Password" button to create AI-generated secure passwords**

## Model Training
To retrain the model with your own data:

1. **Run the data preparation cell in the Jupyter notebook** to create your gold standard dataset
2. **Execute the model training cells** to train a new LSTM model
3. **Use `evaluate_generator.py`** to test the performance of your trained model

## API Endpoints
- `GET /` - Main web interface
- `POST /generate` - Generate AI-powered passwords (requires seed text)
- `POST /analyze` - Analyze password strength (requires password)

## Recent Improvements
- **Enhanced Password Scoring:** Fixed scoring logic to properly evaluate very long passwords
- **Backend Integration:** Frontend now uses Flask backend for consistent password analysis
- **Improved Entropy Weighting:** Better assessment of password randomness and complexity
- **Special Case Handling:** Passwords over 30 characters with decent entropy are properly rated as strong

## Future Improvements
- **Containerize the Application:** Use Docker to make deployment easier
- **Advanced Pattern Detection:** Add more sophisticated pattern recognition for common password structures
- **Multi-language Support:** Extend the interface to support multiple languages

## Authors
- **CaptHeisenberg**
- **bhitsho**
- **ayushpathak477**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.