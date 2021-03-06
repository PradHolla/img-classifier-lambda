import base64
from io import BytesIO
import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Image Classifier", page_icon=":camera:", layout="wide")
st.header("Image Classifier")
st.subheader("Upload an image to classify")

url = "https://3gkl5amlb8.execute-api.us-east-1.amazonaws.com/Prod/classify_digit"

uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg"])

# Convert image to buffer
def get_image_buffer(image_file):
    image = Image.open(image_file)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

if uploaded_image is not None:
    st.sidebar.image(uploaded_image, width=200)
    classify = st.sidebar.button("Classify!")
    
    image_bytes = get_image_buffer(uploaded_image)

    if classify:
        with st.spinner('Classifying...'):
            response = requests.post(url, json=image_bytes)
            response_json = response.json()
            prediction, confidence = response_json["predicted_label"], response_json["score"]
            st.image(uploaded_image, caption=f"{prediction}", width=300)
            st.write(f'### Classified as: {prediction} with {round(confidence, 2)}% confidence')