import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

API_KEY = os.getenv("OPENAI_API_KEY")

# Demo disease predictor (Replace with ML model later)
def predict_disease(image_path):
    return "Tomato Leaf Blight"

# Generate AI explanation
def generate_description(disease_name):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": f"Explain the plant disease {disease_name}, including causes, symptoms, and treatment in simple language."
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error generating description. Check your API key."

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No file uploaded"

    file = request.files['image']
    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    disease = predict_disease(filepath)
    description = generate_description(disease)

    return render_template(
        "result.html",
        disease=disease,
        description=description,
        image=file.filename
    )

if __name__ == '__main__':
    app.run(debug=True)
