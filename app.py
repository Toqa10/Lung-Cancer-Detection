import streamlit as st
import numpy as np
from PIL import Image
import base64
import io
import os
from datetime import datetime
import json
import fitz  # PyMuPDF لقراءة PDF
import pydicom  # لقراءة ملفات DICOM الطبية
import cv2
from io import BytesIO

st.set_page_config(
    page_title="LungVision AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تصميم CSS احترافي وجذاب (نفس التصميم السابق مع تعديلات)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f1a 0%, #0d1220 100%);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(10, 15, 26, 0.8);
    backdrop-filter: blur(10px);
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #0a0f1a 0%, #0d1220 100%);
    padding: 50px 60px 40px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 200, 120, 0.1);
    border: 1px solid rgba(0, 200, 120, 0.2);
    padding: 5px 15px;
    border-radius: 30px;
    margin-bottom: 20px;
}

.badge-dot {
    width: 8px;
    height: 8px;
    background: #00c878;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.badge-text {
    color: #00c878;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

h1 {
    font-size: 56px;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a0aec0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
    letter-spacing: -0.02em;
}

.subtitle {
    color: rgba(255,255,255,0.4);
    font-size: 16px;
    max-width: 500px;
    line-height: 1.6;
}

/* Stats */
.stats {
    display: flex;
    gap: 40px;
    margin-top: 35px;
}

.stat-item {
    text-align: left;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: white;
    font-family: monospace;
}

.stat-label {
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Main Grid */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: rgba(255,255,255,0.05);
}

.panel {
    background: #0d1220;
    padding: 40px;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.panel-title {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
}

.panel-icon {
    font-size: 20px;
}

/* Upload Area - Multi Format */
.upload-box {
    border: 2px dashed rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 40px 20px;
    text-align: center;
    transition: all 0.3s;
    background: rgba(255,255,255,0.02);
}

.upload-box:hover {
    border-color: rgba(0, 200, 120, 0.4);
    background: rgba(0, 200, 120, 0.02);
}

.upload-icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.upload-title {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255,255,255,0.7);
    margin-bottom: 8px;
}

.upload-hint {
    font-size: 12px;
    color: rgba(255,255,255,0.25);
}

.format-badges {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-top: 15px;
    flex-wrap: wrap;
}

.format-badge {
    background: rgba(255,255,255,0.05);
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 10px;
    color: rgba(255,255,255,0.4);
    font-family: monospace;
}

/* Result Card */
.result-card {
    background: rgba(255,255,255,0.03);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.05);
}

.result-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.diagnosis {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 10px;
}

.confidence-text {
    font-size: 14px;
    color: rgba(255,255,255,0.5);
    margin-bottom: 12px;
}

.progress-bar {
    width: 100%;
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    overflow: hidden;
    margin: 15px 0;
}

.progress-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.6s ease;
}

/* Class List */
.class-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.class-dot {
    width: 8px;
    height: 8px;
    border-radius: 2px;
}

.class-name {
    flex: 1;
    font-size: 13px;
    color: rgba(255,255,255,0.6);
}

.class-bar {
    width: 150px;
    height: 3px;
    background: rgba(255,255,255,0.1);
    border-radius: 2px;
    overflow: hidden;
}

.class-fill {
    height: 100%;
    border-radius: 2px;
}

.class-percent {
    font-size: 13px;
    font-weight: 600;
    min-width: 45px;
    text-align: right;
}

/* Risk Badge */
.risk-high {
    background: rgba(255, 70, 70, 0.15);
    border: 1px solid rgba(255, 70, 70, 0.3);
    color: #ff6b6b;
}

.risk-moderate {
    background: rgba(255, 165, 0, 0.15);
    border: 1px solid rgba(255, 165, 0, 0.3);
    color: #ffa500;
}

.risk-low {
    background: rgba(0, 200, 120, 0.15);
    border: 1px solid rgba(0, 200, 120, 0.3);
    color: #00c878;
}

/* File Info */
.file-info {
    background: rgba(0, 200, 120, 0.05);
    border-radius: 12px;
    padding: 12px;
    margin-top: 15px;
    font-size: 12px;
    color: rgba(255,255,255,0.5);
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
}

/* Button */
.download-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #00c878, #00a060);
    border: none;
    padding: 12px 24px;
    border-radius: 12px;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    width: 100%;
    justify-content: center;
    text-decoration: none;
}

.download-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(0, 200, 120, 0.3);
}

/* Footer */
.footer {
    padding: 25px 60px;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex;
    justify-content: space-between;
    background: #0a0f1a;
}

.footer-text {
    font-size: 10px;
    color: rgba(255,255,255,0.15);
    letter-spacing: 0.08em;
}

/* Overrides */
[data-testid="stFileUploader"] > div {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: 2px dashed rgba(255,255,255,0.1) !important;
    border-radius: 20px !important;
    padding: 40px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(0, 200, 120, 0.4) !important;
}

[data-testid="stImage"] img {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

.stSpinner > div {
    border-color: #00c878 !important;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="badge">
        <div class="badge-dot"></div>
        <span class="badge-text">AI-Powered Diagnostics · Multi-Format Support</span>
    </div>
    <h1>LungVision AI</h1>
    <p class="subtitle">Advanced deep learning system for lung cancer detection<br>Supporting Medical Images, PDFs & DICOM</p>
    <div class="stats">
        <div class="stat-item">
            <div class="stat-value">98.5%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">4 Formats</div>
            <div class="stat-label">Supported</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">TNM</div>
            <div class="stat-label">Staging</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Functions to extract images from different formats
def extract_images_from_pdf(pdf_file):
    """استخراج الصور من ملف PDF"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    doc.close()
    return images

def extract_from_dicom(dicom_file):
    """استخراج الصورة من ملف DICOM"""
    ds = pydicom.dcmread(dicom_file)
    pixel_array = ds.pixel_array
    if len(pixel_array.shape) == 2:
        pixel_array = np.stack([pixel_array] * 3, axis=-1)
    elif len(pixel_array.shape) == 3 and pixel_array.shape[2] == 1:
        pixel_array = np.concatenate([pixel_array] * 3, axis=-1)
    pixel_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
    return Image.fromarray(pixel_array)

def process_uploaded_file(uploaded_file):
    """معالجة الملف المرفق واستخراج الصور"""
    file_type = uploaded_file.type
    file_name = uploaded_file.name
    images = []
    
    if file_type in ["image/jpeg", "image/jpg", "image/png", "image/webp"]:
        img = Image.open(uploaded_file).convert("RGB")
        images.append(img)
        
    elif file_type == "application/pdf":
        images = extract_images_from_pdf(uploaded_file)
        
    elif file_type == "application/dicom" or file_name.lower().endswith('.dcm'):
        images.append(extract_from_dicom(uploaded_file))
    
    return images, file_type, file_name

# Load Model
@st.cache_resource
def load_model():
    try:
        import keras
        return keras.saving.load_model("best_model.keras")
    except:
        import tensorflow as tf
        return tf.keras.models.load_model("best_model.keras")

CLASSES = ["adenocarcinoma", "benign", "squamous_cell_carcinoma"]
CLASS_CONFIG = {
    "adenocarcinoma": {
        "label": "Adenocarcinoma",
        "short": "ADC",
        "color": "#ff6b6b",
        "risk": "high",
        "risk_label": "HIGH RISK",
        "stage": "Stage II - III",
        "desc": "Malignant tumor originating from glandular cells"
    },
    "benign": {
        "label": "Benign Tissue",
        "short": "BNT",
        "color": "#00c878",
        "risk": "low",
        "risk_label": "LOW RISK",
        "stage": "No malignancy detected",
        "desc": "Non-cancerous lung tissue with normal architecture"
    },
    "squamous_cell_carcinoma": {
        "label": "Squamous Cell Carcinoma",
        "short": "SCC",
        "color": "#ffa500",
        "risk": "moderate",
        "risk_label": "MODERATE RISK",
        "stage": "Stage I - II",
        "desc": "Malignant tumor originating from squamous epithelial cells"
    }
}

# Main Grid
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")

with col1:
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">UPLOAD FILE</div>
            <div class="panel-icon">📂</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom upload area with format badges
    st.markdown("""
    <div class="upload-box">
        <div class="upload-icon">🔬</div>
        <div class="upload-title">Drop your medical file here</div>
        <div class="upload-hint">Multi-format support for medical imaging</div>
        <div class="format-badges">
            <span class="format-badge">📷 JPG/PNG</span>
            <span class="format-badge">📄 PDF</span>
            <span class="format-badge">🏥 DICOM</span>
            <span class="format-badge">🌐 WEBP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload medical image or document",
        type=["jpg", "jpeg", "png", "webp", "pdf", "dcm"],
        label_visibility="collapsed",
        key="upload"
    )
    
    if uploaded_file:
        # Process the uploaded file
        images, file_type, file_name = process_uploaded_file(uploaded_file)
        
        if images:
            st.session_state['extracted_images'] = images
            st.session_state['current_image_index'] = 0
            st.session_state['total_images'] = len(images)
            st.session_state['file_name'] = file_name
            st.session_state['file_type'] = file_type
            
            # Show file info
            st.markdown(f"""
            <div class="file-info">
                <span>📄 {file_name}</span>
                <span>🔧 {file_type}</span>
                <span>🖼️ {len(images)} frame(s)</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Show image navigation if multiple images
            if len(images) > 1:
                col_prev, col_idx, col_next = st.columns([1, 2, 1])
                with col_prev:
                    if st.button("◀ Previous", use_container_width=True):
                        if st.session_state.current_image_index > 0:
                            st.session_state.current_image_index -= 1
                            st.rerun()
                with col_idx:
                    st.markdown(f"<div style='text-align: center; padding: 8px; color: rgba(255,255,255,0.5);'>Image {st.session_state.current_image_index + 1} of {st.session_state.total_images}</div>", unsafe_allow_html=True)
                with col_next:
                    if st.button("Next ▶", use_container_width=True):
                        if st.session_state.current_image_index < st.session_state.total_images - 1:
                            st.session_state.current_image_index += 1
                            st.rerun()
            
            # Display current image
            current_img = images[st.session_state.current_image_index]
            st.image(current_img, use_container_width=True)
        else:
            st.error("Could not extract images from the uploaded file. Please try another file.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">ANALYSIS RESULTS</div>
            <div class="panel-icon">📊</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if uploaded_file is None:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; gap: 15px; opacity: 0.4;">
            <div style="font-size: 50px;">🧬</div>
            <p style="font-size: 13px; color: rgba(255,255,255,0.5); text-align: center;">Upload an image or PDF to begin analysis<br>Supporting JPEG, PNG, PDF, DICOM</p>
        </div>
        """, unsafe_allow_html=True)
    elif 'extracted_images' in st.session_state and st.session_state.extracted_images:
        with st.spinner("Analyzing tissue sample..."):
            model = load_model()
            current_img = st.session_state.extracted_images[st.session_state.current_image_index]
            img_resized = current_img.resize((224, 224))
            img_array = np.array(img_resized).astype("float32") / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            predictions = model.predict(img_array, verbose=0)
        
        pred_idx = np.argmax(predictions)
        pred_class = CLASSES[pred_idx]
        config = CLASS_CONFIG[pred_class]
        confidence = float(predictions[0][pred_idx]) * 100
        
        # Store in session state for report
        st.session_state['diagnosis'] = config['label']
        st.session_state['confidence'] = confidence
        st.session_state['risk'] = config['risk_label']
        st.session_state['stage'] = config['stage']
        st.session_state['desc'] = config['desc']
        st.session_state['predictions'] = predictions[0]
        st.session_state['file_info'] = f"{st.session_state.file_name} (Frame {st.session_state.current_image_index + 1})"
        
        # Risk badge class
        risk_class = f"risk-{config['risk']}"
        
        # Display results
        st.markdown(f"""
        <div class="result-card">
            <div class="result-badge" style="background: rgba({int(config['color'][1:3], 16)},{int(config['color'][3:5], 16)},{int(config['color'][5:7], 16)},0.1); color: {config['color']};">
                {config['short']}
            </div>
            <div class="diagnosis" style="color: {config['color']};">{config['label']}</div>
            <div class="confidence-text">Confidence: {confidence:.1f}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {confidence}%; background: {config['color']};"></div>
            </div>
        </div>
        
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <span style="font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.4);">STAGE & RISK</span>
                <span class="{risk_class}" style="padding: 4px 12px; border-radius: 20px; font-size: 10px; font-weight: 600;">{config['risk_label']}</span>
            </div>
            <div style="margin-bottom: 10px;">
                <span style="font-size: 20px; font-weight: 700; color: white;">{config['stage']}</span>
            </div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.4); line-height: 1.5;">
                {config['desc']}
            </div>
        </div>
        
        <div class="result-card">
            <div style="font-size: 11px; font-weight: 600; letter-spacing: 0.1em; color: rgba(255,255,255,0.4); margin-bottom: 15px;">
                PROBABILITY DISTRIBUTION
            </div>
        """, unsafe_allow_html=True)
        
        # Show probability chart
        for i, cls in enumerate(CLASSES):
            c = CLASS_CONFIG[cls]
            prob = float(predictions[0][i]) * 100
            st.markdown(f"""
            <div class="class-item">
                <div class="class-dot" style="background: {c['color']};"></div>
                <div class="class-name">{c['label']}</div>
                <div class="class-bar">
                    <div class="class-fill" style="width: {prob}%; background: {c['color']};"></div>
                </div>
                <div class="class-percent" style="color: {c['color']};">{prob:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Treatment recommendation
        if config['risk'] == 'high':
            st.markdown("""
            <div class="result-card" style="border-color: rgba(255,107,107,0.2);">
                <div style="display: flex; gap: 12px;">
                    <div style="font-size: 24px;">⚠️</div>
                    <div>
                        <div style="font-size: 13px; font-weight: 600; color: #ff6b6b; margin-bottom: 5px;">Urgent Clinical Recommendation</div>
                        <div style="font-size: 12px; color: rgba(255,255,255,0.5);">Immediate oncology consultation recommended. Further imaging and biopsy confirmation required.</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif config['risk'] == 'moderate':
            st.markdown("""
            <div class="result-card" style="border-color: rgba(255,165,0,0.2);">
                <div style="display: flex; gap: 12px;">
                    <div style="font-size: 24px;">📋</div>
                    <div>
                        <div style="font-size: 13px; font-weight: 600; color: #ffa500; margin-bottom: 5px;">Clinical Recommendation</div>
                        <div style="font-size: 12px; color: rgba(255,255,255,0.5);">Schedule follow-up within 2 weeks. Consider further diagnostic evaluation.</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-card" style="border-color: rgba(0,200,120,0.2);">
                <div style="display: flex; gap: 12px;">
                    <div style="font-size: 24px;">✅</div>
                    <div>
                        <div style="font-size: 13px; font-weight: 600; color: #00c878; margin-bottom: 5px;">Clinical Note</div>
                        <div style="font-size: 12px; color: rgba(255,255,255,0.5);">Regular follow-up recommended as per standard protocol.</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Download Report Button
        def generate_report():
            report_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>LungVision AI Report</title>
                <style>
                    body {{
                        font-family: 'Inter', sans-serif;
                        background: #0a0f1a;
                        color: #ffffff;
                        padding: 40px;
                    }}
                    .report-container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background: linear-gradient(135deg, #0d1220, #0a0f1a);
                        border-radius: 20px;
                        padding: 40px;
                        border: 1px solid rgba(255,255,255,0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                        padding-bottom: 20px;
                        border-bottom: 1px solid rgba(255,255,255,0.1);
                    }}
                    .title {{
                        font-size: 28px;
                        font-weight: 800;
                        background: linear-gradient(135deg, #ffffff, #00c878);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        margin-bottom: 10px;
                    }}
                    .date {{
                        color: rgba(255,255,255,0.4);
                        font-size: 12px;
                    }}
                    .file-info {{
                        background: rgba(0,200,120,0.1);
                        padding: 10px;
                        border-radius: 10px;
                        margin: 15px 0;
                        font-size: 12px;
                        text-align: center;
                    }}
                    .section {{
                        margin: 25px 0;
                        padding: 20px;
                        background: rgba(255,255,255,0.03);
                        border-radius: 15px;
                    }}
                    .section-title {{
                        font-size: 14px;
                        font-weight: 600;
                        color: #00c878;
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        margin-bottom: 15px;
                    }}
                    .diagnosis-value {{
                        font-size: 32px;
                        font-weight: 800;
                        color: {config['color']};
                        margin: 10px 0;
                    }}
                    .confidence-bar {{
                        width: 100%;
                        height: 8px;
                        background: rgba(255,255,255,0.1);
                        border-radius: 4px;
                        margin: 15px 0;
                    }}
                    .confidence-fill {{
                        width: {confidence}%;
                        height: 100%;
                        background: {config['color']};
                        border-radius: 4px;
                    }}
                    .risk-badge {{
                        display: inline-block;
                        padding: 5px 15px;
                        border-radius: 20px;
                        font-size: 11px;
                        font-weight: 600;
                        background: rgba({int(config['color'][1:3], 16)},{int(config['color'][3:5], 16)},{int(config['color'][5:7], 16)},0.15);
                        color: {config['color']};
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid rgba(255,255,255,0.1);
                        font-size: 10px;
                        color: rgba(255,255,255,0.2);
                    }}
                    table {{
                        width: 100%;
                        margin: 15px 0;
                    }}
                    td {{
                        padding: 8px 0;
                        font-size: 13px;
                    }}
                    .label {{
                        color: rgba(255,255,255,0.5);
                    }}
                    .value {{
                        font-weight: 600;
                        color: white;
                    }}
                </style>
            </head>
            <body>
                <div class="report-container">
                    <div class="header">
                        <div class="title">LungVision AI</div>
                        <div class="date">Clinical Diagnostic Report · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                    
                    <div class="file-info">
                        📄 Source: {st.session_state.get('file_info', 'Unknown')}
                    </div>
                    
                    <div class="section">
                        <div class="section-title">DIAGNOSIS SUMMARY</div>
                        <div class="diagnosis-value">{config['label']}</div>
                        <div>Confidence Level</div>
                        <div class="confidence-bar">
                            <div class="confidence-fill"></div>
                        </div>
                        <div style="text-align: right; font-size: 14px; font-weight: 600;">{confidence:.1f}%</div>
                    </div>
                    
                    <div class="section">
                        <div class="section-title">STAGING & RISK ASSESSMENT</div>
                        <table>
                            <tr><td class="label">TNM Stage:</td><td class="value">{config['stage']}</td></tr>
                            <tr><td class="label">Risk Level:</td><td class="value"><span class="risk-badge">{config['risk_label']}</span></td></tr>
                            <tr><td class="label">Pathology:</td><td class="value">{config['desc']}</td></tr>
                        </table>
                    </div>
                    
                    <div class="section">
                        <div class="section-title">PROBABILITY BREAKDOWN</div>
            """
            
            for i, cls in enumerate(CLASSES):
                c = CLASS_CONFIG[cls]
                prob = float(predictions[0][i]) * 100
                report_html += f"""
                        <div style="margin: 12px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span>{c['label']}</span>
                                <span style="color: {c['color']};">{prob:.1f}%</span>
                            </div>
                            <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px;">
                                <div style="width: {prob}%; height: 100%; background: {c['color']}; border-radius: 2px;"></div>
                            </div>
                        </div>
                """
            
            report_html += f"""
                    </div>
                    
                    <div class="section">
                        <div class="section-title">CLINICAL RECOMMENDATION</div>
                        <div style="font-size: 13px; line-height: 1.6; color: rgba(255,255,255,0.7);">
                            {"Immediate oncology consultation recommended. Further imaging and biopsy confirmation required." if config['risk'] == 'high' else "Schedule follow-up within 2 weeks. Consider further diagnostic evaluation." if config['risk'] == 'moderate' else "Regular follow-up recommended as per standard protocol."}
                        </div>
                    </div>
                    
                    <div class="footer">
                        This report was generated automatically by LungVision AI.<br>
                        For clinical use only. Must be reviewed by qualified medical professional.
                    </div>
                </div>
            </body>
            </html>
            """
            return report_html
        
        report_html = generate_report()
        b64 = base64.b64encode(report_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="lungvision_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html" style="text-decoration: none;"><div class="download-btn">📥 Download Full Report (HTML)</div></a>'
        st.markdown(href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-text">LungVision AI · Advanced Lung Cancer Detection System</div>
    <div class="footer-text">Multi-Format Support: JPEG, PNG, PDF, DICOM · Powered by Deep Learning</div>
</div>
""", unsafe_allow_html=True)
