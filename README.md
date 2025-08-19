<<<<<<< HEAD
# VaultAI - AI-Powered Password Strength Analyzer & Generator

## Overview
This project is an advanced **Password Strength Analyzer and AI Generator**, originally developed for the Barclays Hack-O-Earth Hackathon. It features a sophisticated front-end that provides real-time, heuristic-based strength analysis and an AI backend that generates highly secure and unique passwords.

The core of the project is a refined **TensorFlow LSTM model** trained on a "gold standard" dataset of over 3 million complex, high-entropy passwords filtered from the RockYou dataset. This ensures the generated passwords are not only random but also learn the structural patterns of real-world secure passwords.

## Final Performance Metrics
After a full refinement and debugging cycle, the final AI model achieves the following performance on a sample of 500 generated passwords:
- **Average Shannon Entropy:** 3.63 bits
- **Uniqueness:** 100.0%
- **Rated "Strong" by Heuristic Analyzer:** 94.0%

## Features
- **Real-Time Strength Analysis:** An interactive web interface powered by Flask and JavaScript provides instant feedback on password strength as you type.
- **AI-Powered Password Generation:** Uses the trained LSTM model with temperature sampling to generate creative, non-repetitive, and secure passwords.
- **Rule Enforcement:** A post-processing step ensures that every AI-generated password meets strict criteria (e.g., contains uppercase, lowercase, numbers, and symbols).
- **High-Quality Training Data:** The model was trained on a filtered, high-entropy subset of the RockYou dataset.
- **Complete Project Documentation:** Includes a Jupyter Notebook (`xaibarclays.ipynb`) detailing all research, data processing, and model training steps.

## Files
- `app.py`: The main Flask web application.
- `strong_password_generator.h5`: The final, trained TensorFlow/Keras AI model.
- `char_to_int.json`: The vocabulary file required by the trained model.
- `requirements.txt`: Dependencies required to run the project.
- `evaluate_generator.py`: A script to evaluate the performance of the trained AI model.
- `xaibarclays.ipynb`: The Jupyter notebook for research, data processing, and model training.
- `templates/index.html`: The frontend user interface.

## Installation
### Prerequisites
- Python 3.8+
- TensorFlow
- Flask
- Pandas, Scikit-learn, and other packages listed in `requirements.txt`.

### Installation Steps
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/VaultAI](https://github.com/your-username/VaultAI)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd VaultAI
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download the Model Files:**
    - Download the trained model and vocabulary from this link: **[https://drive.google.com/file/d/1JrfdgfRbcnNn8gqqYwL6aGwayb3gf2nB/view?usp=sharing]**
    - Unzip the file and place `strong_password_generator.h5` and `char_to_int.json` in the root of the `VaultAI/` directory.

## Usage
1.  **Run the Flask application:**
    ```bash
    python app.py
    ```

2.  **Open your browser and go to:**
    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

## Future Improvements
- **Integrate the AI Generator:** Connect the "Generate Better Password" button on the frontend to the `/generate` API endpoint to use the AI model in the UI.
- **Containerize the Application:** Use Docker to make deployment easier.
- **Expand the Heuristic Analyzer:** Add more advanced checks to the real-time analyzer, such as checking for dictionary words.

## Authors
- **CaptHeisenberg**
- **bhitsho**
- **ayushpathak477**

## License
=======
# VaultAI - AI-Powered Password Strength Analyzer & Generator

## Overview
This project is an advanced **Password Strength Analyzer and AI Generator**, originally developed for the Barclays Hack-O-Earth Hackathon. It features a sophisticated front-end that provides real-time, heuristic-based strength analysis and an AI backend that generates highly secure and unique passwords.

The core of the project is a refined **TensorFlow LSTM model** trained on a "gold standard" dataset of over 3 million complex, high-entropy passwords filtered from the RockYou dataset. This ensures the generated passwords are not only random but also learn the structural patterns of real-world secure passwords.

## Final Performance Metrics
After a full refinement and debugging cycle, the final AI model achieves the following performance on a sample of 500 generated passwords:
- **Average Shannon Entropy:** 3.63 bits
- **Uniqueness:** 100.0%
- **Rated "Strong" by Heuristic Analyzer:** 94.0%

## Features
- **Real-Time Strength Analysis:** An interactive web interface powered by Flask and JavaScript provides instant feedback on password strength as you type.
- **AI-Powered Password Generation:** Uses the trained LSTM model with temperature sampling to generate creative, non-repetitive, and secure passwords.
- **Rule Enforcement:** A post-processing step ensures that every AI-generated password meets strict criteria (e.g., contains uppercase, lowercase, numbers, and symbols).
- **High-Quality Training Data:** The model was trained on a filtered, high-entropy subset of the RockYou dataset.
- **Complete Project Documentation:** Includes a Jupyter Notebook (`xaibarclays.ipynb`) detailing all research, data processing, and model training steps.

## Files
- `app.py`: The main Flask web application.
- `strong_password_generator.h5`: The final, trained TensorFlow/Keras AI model.
- `char_to_int.json`: The vocabulary file required by the trained model.
- `requirements.txt`: Dependencies required to run the project.
- `evaluate_generator.py`: A script to evaluate the performance of the trained AI model.
- `xaibarclays.ipynb`: The Jupyter notebook for research, data processing, and model training.
- `templates/index.html`: The frontend user interface.

## Installation
### Prerequisites
- Python 3.8+
- TensorFlow
- Flask
- Pandas, Scikit-learn, and other packages listed in `requirements.txt`.

### Installation Steps
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/VaultAI](https://github.com/your-username/VaultAI)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd VaultAI
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download the Model Files:**
    - Download the trained model and vocabulary from this link: **[https://drive.google.com/file/d/1JrfdgfRbcnNn8gqqYwL6aGwayb3gf2nB/view?usp=sharing]**
    - Unzip the file and place `strong_password_generator.h5` and `char_to_int.json` in the root of the `VaultAI/` directory.

## Usage
1.  **Run the Flask application:**
    ```bash
    python app.py
    ```

2.  **Open your browser and go to:**
    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

## Future Improvements
- **Integrate the AI Generator:** Connect the "Generate Better Password" button on the frontend to the `/generate` API endpoint to use the AI model in the UI.
- **Containerize the Application:** Use Docker to make deployment easier.
- **Expand the Heuristic Analyzer:** Add more advanced checks to the real-time analyzer, such as checking for dictionary words.

## Authors
- **CaptHeisenberg**
- **bhitsho**
- **ayushpathak477**

## License
>>>>>>> b2f0d7519b170a91b4365f41d6d6d73b8b24de16
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.