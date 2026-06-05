import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image

model = tf.keras.models.load_model("best_model.keras")

classes = ["adenocarcinoma", "benign", "squamous_cell_carcinoma"]

st.set_page_config(page_title="Lung Cancer Detection", layout="centered")

st.title("🔬 Lung Cancer Histopathology Image Classifier")
st.write("Upload a Histopathological Image to predict the Type")

uploaded_file = st.file_uploader("Upload a Picture", type=["jpg", "jpeg", "png","webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Picture", use_container_width=True)

    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalization

    prediction = model.predict(img_array)
    predicted_class = classes[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    st.subheader("Resluts:")
    st.write(f"**Class:** {predicted_class}")
    st.write(f"**Confidence:** {confidence:.2f}%")
