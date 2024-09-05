# Red Bus QA Instructions Generator



## Overview
This project is a web-based tool designed to automatically generate QA instructions for the Red Bus mobile app. The tool leverages the **Google Gemini API** to analyze both uploaded screenshots and accompanying text input from the user. It generates detailed test cases, including **user flows, pre-conditions, and expected results**, for various app features visible in the screenshots. This can be especially useful for QA engineers who want to streamline the creation of test cases for different app components.

## Features
- **Screenshot Analysis**: Users can upload screenshots of the Red Bus app, and the tool will analyze the content to generate relevant test cases.
- **Text Input for Context**: Users can provide additional text inputs (prompts) to guide the system in generating more specific test instructions.
- **Automated Test Case Generation**: Based on the screenshot and input prompt, the tool will automatically generate test cases, including expected results, pre-conditions, and scenarios for normal and edge cases.
- **Uses Google Gemini API**: The Gemini API is integrated to handle both image and text processing, ensuring accurate and context-aware QA instructions.

## Setup

### Prerequisites
- **Python**
- **Flask Framework**
- **Google Gemini API Key**

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rafe2001/Myracle-Challenge.git
   cd Myracle-Challenge
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then install the necessary Python packages.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```

4. **Run the application**:
   To start the Flask web app:
   ```bash
   flask run
   ```

5. **Access the application**:
   Open your browser and go to:
   ```
   http://localhost:5000
   ```

6. **Usage**:
   - Upload one or more screenshots of the Red Bus app.
   - Optionally provide additional text context (e.g., "Test the seat selection feature").
   - Submit to generate detailed QA instructions based on the image and input.

## Prompting Strategy
This project employs a customized prompting strategy to extract and generate relevant QA instructions based on user inputs and screenshots. The goal is to ensure that the test cases generated are aligned with the visible features of the Red Bus app and the specific input context provided by the user.

### Steps in the Prompting Strategy:
1. **Image Analysis**: The tool first processes the uploaded image through the Google Gemini API to determine if the screenshot is from the Red Bus app and to identify key components (e.g., seat selection, payment options).
   
2. **Contextual Prompting**: Based on the user-provided text input, the prompt is constructed to ensure that the generated test cases are specific to the input scenario. For example, if the prompt mentions "seat selection", the generated test cases will focus on testing that feature.

3. **Test Case Generation**:
   - **Pre-conditions**: Automatically generates any necessary pre-conditions (e.g., "User must be logged into the Red Bus app").
   - **User Flow**: Provides step-by-step instructions for testing the feature identified in the screenshot or prompt (e.g., "Select a seat and verify availability").
   - **Edge Cases**: Includes edge cases like invalid inputs or alternative flows (e.g., "Try selecting an already booked seat").

4. **Filtering Irrelevant Content**:
   - If the uploaded screenshot is not from the Red Bus app or does not contain recognizable features, the tool will return a message indicating that the image is unrelated. This ensures that the user does not receive irrelevant or incorrect test cases.

### Prompting Logic:
- The prompt instructs the model to first verify whether the screenshot is from the Red Bus app. If verified, the model proceeds to identify the specific app feature (e.g., seat selection, payment options).
- The model is then asked to generate detailed test cases, including expected outcomes for both normal user flows and edge cases.
- The tool is designed to reject irrelevant or unrelated screenshots, preventing test case generation for images outside the Red Bus context.

### Challenges & Adjustments:
- Ensuring that the model accurately identifies Red Bus app features from screenshots was critical. We refined the prompt to prioritize correct feature identification before generating test cases.
- Special attention was given to handling cases where the user input and screenshot context may not perfectly align. For such cases, the tool defaults to analyzing the image and generates test cases based on the visual content.


## Example Test Cases Generated:

### Scenario: Seat Selection Feature

1. **User Flow and Functionality**:
   - The user is expected to select an available seat on the bus selection screen. Upon selection, the seat should be highlighted, and the "Proceed" button should become active.

2. **Pre-conditions**:
   - The user should be logged in to the Red Bus app.
   - The bus route and date must have been selected.

3. **Step-by-Step Instructions**:
   - Select a bus from the available options on the screen.
   - Attempt to select a seat. Verify that the seat is marked as selected (highlighted) and that the "Proceed" button becomes enabled.
   - Select a seat that is already booked. Verify that an error message appears, indicating that the seat is unavailable.

4. **Expected Results**:
   - On selecting an available seat, the seat is highlighted, and the user can proceed to payment.
   - On selecting a booked seat, the app should display an error and prevent the user from proceeding.
