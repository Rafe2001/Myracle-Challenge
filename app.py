# Import Libraries
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


app = Flask(__name__)


# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_text, image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text


# Function to prepare the uploaded images for API
def prepare_images(uploaded_files):
    image_parts = []
    for uploaded_file in uploaded_files:
        if uploaded_file:
            bytes_data = uploaded_file.read()
            image_parts.append({
                "mime_type": uploaded_file.content_type,
                "data": bytes_data
            })
    return image_parts


# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# API route to process the images and input text
@app.route('/describe', methods=['POST'])
def describe():
    input_prompt = request.form.get('input_prompt')
    uploaded_files = request.files.getlist('uploaded_files')
    
    image_data = prepare_images(uploaded_files)
    
 
    # Static prompt 
    static_prompt = """
    You are a QA expert tasked with testing the Red Bus mobile app. 
    The app allows users to select their travel source, destination, and date, view available buses, choose a seat, and specify pick-up and drop-off points. 
    
    For each of these features, generate detailed testing instructions, covering:
    
    1. User flow and functionality.
    2. Pre-conditions necessary for testing.
    3. Step-by-step test instructions, including variations such as invalid inputs and edge cases.
    4. Expected results for each step.
    5. Include checks for related features like available offers, sorting filters, and bus information.

    Ensure that the test cases are thorough, covering both normal and edge case scenarios.

    """


    # response from Gemini API
    response_text = get_gemini_response(input_prompt, image_data, static_prompt)
    
    return jsonify({'response_text': response_text})



if __name__ == '__main__':
    app.run(debug=True)
