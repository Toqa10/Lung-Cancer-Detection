import streamlit as st
import numpy as np
from PIL import Image
import os

# Try to load model with keras or tensorflow
try:
    import keras
    model = keras.saving.load_model("best_model.keras")
    using = "keras"
except Exception:
    import tensorflow as tf
    model = tf.keras.models.load_model("best_model.keras")
    using = "tensorflow"

classes = ["adenocarcinoma", "benign", "squamous_cell_carcinoma"]

CLASS_INFO = {
    "adenocarcinoma": {"label": "Adenocarcinoma", "color": "#FF4B4B", "icon": "🔴"},
    "benign": {"label": "Benign (Normal)", "color": "#21C354", "icon": "🟢"},
    "squamous_cell_carcinoma": {"label": "Squamous Cell Carcinoma", "color": "#FF8C00", "icon": "🟠"},
}

st.set_page_config(page_title="Lung Cancer Detection", layout="centered")
st.title("🔬 Lung Cancer Histopathology Image Classifier")
st.write("Upload a Histopathological Image to predict the Type")

uploaded_file = st.file_uploader("Upload a Picture", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Picture", use_container_width=True)

    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized).astype("float32") / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = classes[np.argmax(prediction)]
    confidence = float(np.max(prediction)) * 100

    info = CLASS_INFO[predicted_class]

    st.subheader("Results:")
    st.markdown(
        f"<h3 style='color:{info['color']}'>{info['icon']} {info['label']}</h3>",
        unsafe_allow_html=True
    )
    st.write(f"**Confidence:** {confidence:.2f}%")
    st.progress(confidence / 100)

    st.write("---")
    st.write("**All Class Probabilities:**")
    for i, cls in enumerate(classes):
        prob = float(prediction[0][i]) * 100
        cls_info = CLASS_INFO[cls]
        st.write(f"{cls_info['icon']} {cls_info['label']}: **{prob:.2f}%**")
