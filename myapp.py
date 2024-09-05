# Libraries
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO


load_dotenv()

# Configure the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
                "mime_type": uploaded_file.type,
                "data": bytes_data
            })
    return image_parts

# Static prompt for generating testing instructions
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

# Streamlit App Layout
st.title("Gemini Vision API - Testing Instructions Generator")
st.write("Upload screenshots and provide context to generate testing instructions for the Red Bus mobile app.")

# Input Prompt
input_prompt = st.text_area("Enter any optional context for the testing instructions:", "")

# Image Upload
uploaded_files = st.file_uploader("Upload screenshots (PNG or JPEG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Button to generate instructions
if st.button('Describe Testing Instructions'):
    if uploaded_files:
        # Prepare images for processing
        image_data = prepare_images(uploaded_files)

        # Call the Gemini API
        response_text = get_gemini_response(input_prompt, image_data, static_prompt)

        # Display the result
        st.subheader("Generated Testing Instructions:")
        st.write(response_text)
    else:
        st.error("Please upload at least one image.")
