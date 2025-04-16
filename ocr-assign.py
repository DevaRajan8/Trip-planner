import streamlit as st
import requests
import time
import os
from PIL import Image
import easyocr
import numpy as np
import cv2  # For image preprocessing

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

class GroqAPIClient:
    def __init__(self, groq_api_key: str):
        self.groq_api_key = groq_api_key

    def _call_groq_api(self, prompt: str, max_retries: int = 3) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gemma2-9b-it",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.2
        }
        attempt = 0
        while attempt < max_retries:
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("choices", [{}])[0].get("message", {}).get("content", "No content found.")
                else:
                    st.error(f"Error: Received status code {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(2)
        return "Failed to get a valid response from the Groq API after multiple retries."

    def generate_caption(self, prompt: str) -> str:
        return self._call_groq_api(prompt)

# Page Title & Description
st.title("AI-Based Image Caption Generator")
st.write("Upload an image and let our AI generate an engaging image caption. Optionally, add Instagram-style hashtags for extra flair!")

# Upload Image
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# API Key Input
groq_api_key = "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"
if not groq_api_key:
    groq_api_key = st.text_input("Enter your Groq API key", type="password")

if groq_api_key:
    groq_client = GroqAPIClient(groq_api_key)

def preprocess_image_for_ocr(image_np: np.ndarray) -> np.ndarray:
    """
    Convert image to grayscale, apply Otsu thresholding,
    and perform optional morphological operations to improve OCR.
    """
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    return processed

# Optional manual image description input
manual_description = st.text_area("Or, provide a short description of the image (optional)", "")

if uploaded_file and groq_api_key:
    # Open and display the image
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Perform OCR extraction
    try:
        preprocessed_image = preprocess_image_for_ocr(image_np)
        results = reader.readtext(preprocessed_image)
        ocr_text = " ".join([result[1] for result in results]).strip()
    except Exception as e:
        ocr_text = ""
        st.error(f"OCR failed: {e}")

    st.subheader("Extracted Text (OCR)")
    if ocr_text:
        st.write(ocr_text)
    else:
        st.write("No text detected in the image.")

    # Option to include Instagram-style hashtags
    add_hashtags = st.checkbox("Include Instagram-style hashtags in the caption")

    # Build the prompt for caption generation
    if ocr_text:
        base_context = f"The following text was extracted from an image:\n\n{ocr_text}\n\n"
    elif manual_description:
        base_context = f"Image Description:\n\n{manual_description}\n\n"
    else:
        base_context = ""

    caption_prompt = (
        f"{base_context}"
        "Based on the above details and the overall visual context of the image, generate a creative and engaging image caption."
    )
    
    # Modify prompt to include hashtags if selected
    if add_hashtags:
        caption_prompt += " Please also include relevant Instagram-style hashtags."

    # Button to generate caption
    if st.button("Generate Caption"):
        with st.spinner("Generating caption..."):
            caption = groq_client.generate_caption(caption_prompt)
        st.subheader("Generated Image Caption")
        st.write(caption)
else:
    st.info("Please upload an image")
