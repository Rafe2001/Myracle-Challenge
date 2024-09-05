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
    
You are a QA expert tasked with generating detailed testing instructions based on screenshots of the Red Bus mobile app. 
The app includes features for selecting travel source, destination, and date, viewing available buses, choosing seats, and specifying pick-up and drop-off points.

For each screenshot provided, generate detailed testing instructions following:

1. Identify the Feature:
   - Analyze the screenshot to determine which feature of the Red Bus app is displayed (e.g., source/destination selection, bus selection, seat selection, etc.).

2. Generate Test Cases:
   - User Flow and Functionality: Describe the expected user interaction with the feature shown in the screenshot.
   - Pre-conditions: List any necessary setup or conditions needed before testing the feature.
   - Step-by-Step Instructions: Provide clear, step-by-step instructions on how to test the feature. Include variations such as invalid inputs and edge cases if applicable.
   - Expected Results: Outline what should happen if the feature works correctly.

3. Include Related Features:
   - If relevant, include checks for related features visible in the screenshot, such as available offers, sorting filters, or bus information.

Ensure that the test cases are thorough, covering both normal and edge case scenarios.

"""



    # response from Gemini API
    #response_text = get_gemini_response(input_prompt, image_data, static_prompt)
    
    #return jsonify({'response_text': response_text})
    try:
        response_text = get_gemini_response(input_prompt, image_data, static_prompt)
        return jsonify({'response_text': response_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)

