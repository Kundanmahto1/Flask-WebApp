# Install if needed
# !pip install streamlit google-generativeai

import streamlit as st
import google.generativeai as genai
import os

# Set your Gemini API Key here
GEMINI_API_KEY = "AIzaSyCK83SHzFcSc4RVfoFBa3oXyrypunciERM"

genai.configure(api_key=GEMINI_API_KEY)

# Function to call Gemini API for text recommendations
def get_fashion_recommendations(gender, style, age_group, colors, occasion):
    prompt = f"""
    You are a fashion stylist assistant.
    Suggest 3 outfit ideas for a user with the following details:
    - Gender: {gender}
    - Style: {style}
    - Age Group: {age_group}
    - Preferred Colors: {colors}
    - Occasion: {occasion}

    Be detailed in clothing, shoes, and accessories recommendations.
    """

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("👗 Apparel Recommendation App (AI-powered)")

st.header("Upload your photo or take a picture")

# 1. Gender selection
gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])

# 2. Image Upload or Webcam
image_option = st.radio("How would you like to provide your image?", ["Upload Image", "Use Webcam"])

image = None

if image_option == "Upload Image":
    image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
elif image_option == "Use Webcam":
    image = st.camera_input("Take a picture")

# 3. Style Preference
style = st.selectbox("Choose your style preference", ["Modern", "Traditional", "Sporty", "Vintage", "Bohemian"])

# 4. Age Group
age_group = st.selectbox("Select your age group", ["Teen", "Young Adult", "Adult", "Senior"])

# 5. Clothing Colors
colors = st.text_input("Preferred clothing colors (e.g., blue, black, pastel)")

# 6. Occasion
occasion = st.selectbox("Select the occasion", ["Casual", "Formal", "Party", "Travel", "Work"])

# 7. Submit Button
if st.button("Get Recommendations"):
    if not image:
        st.warning("Please upload or capture an image first!")
    else:
        with st.spinner("Generating your personalized fashion recommendations..."):
            try:
                recommendation = get_fashion_recommendations(gender, style, age_group, colors, occasion)
                st.success("Here are your recommendations!")
                st.markdown(recommendation)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
