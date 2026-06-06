import streamlit as st
import numpy as np
from PIL import Image
import base64
import io
import os

st.set_page_config(
    page_title="LungVision AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080C12 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #080C12 !important;
}

[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"] { display: none; }

/* ─── HERO HEADER ─── */
.hero {
    position: relative;
    padding: 60px 60px 40px;
    overflow: hidden;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.hero::before {
    content: '';
    position: absolute;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(0,210,140,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero::after {
    content: '';
    position: absolute;
    top: -100px; right: -100px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(100,120,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,210,140,0.1);
    border: 1px solid rgba(0,210,140,0.25);
    color: #00D28C;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 20px;
    margin-bottom: 20px;
}

.badge-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00D28C;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin-bottom: 14px;
}

.hero-title span {
    background: linear-gradient(135deg, #00D28C 0%, #4ECAFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    color: rgba(255,255,255,0.45);
    font-size: 15px;
    font-weight: 300;
    line-height: 1.6;
    max-width: 480px;
}

.stats-row {
    display: flex;
    gap: 32px;
    margin-top: 36px;
}

.stat-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
}

.stat-label {
    font-size: 12px;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.stat-divider {
    width: 1px;
    background: rgba(255,255,255,0.08);
    align-self: stretch;
}

/* ─── MAIN GRID ─── */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: rgba(255,255,255,0.06);
    min-height: calc(100vh - 280px);
}

.panel {
    background: #080C12;
    padding: 40px;
}

.panel-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.25);
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.panel-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ─── UPLOAD ZONE ─── */
.upload-zone {
    border: 1px dashed rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 48px 32px;
    text-align: center;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.02);
    cursor: pointer;
}

.upload-zone:hover {
    border-color: rgba(0,210,140,0.35);
    background: rgba(0,210,140,0.03);
}

.upload-icon {
    width: 56px; height: 56px;
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    font-size: 24px;
}

.upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: rgba(255,255,255,0.8);
    margin-bottom: 6px;
}

.upload-hint {
    font-size: 12px;
    color: rgba(255,255,255,0.25);
}

/* ─── RESULT CARD ─── */
.result-main {
    margin-bottom: 24px;
}

.result-type {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.result-name {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 6px;
}

.result-confidence {
    font-size: 13px;
    color: rgba(255,255,255,0.4);
}

.result-confidence span {
    font-weight: 500;
}

/* ─── CONFIDENCE BAR ─── */
.conf-bar-wrap {
    margin-bottom: 28px;
}

.conf-bar-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 8px;
}

.conf-bar-label {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.conf-bar-val {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #fff;
}

.conf-bar-bg {
    height: 4px;
    background: rgba(255,255,255,0.07);
    border-radius: 2px;
    overflow: hidden;
}

.conf-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s ease;
}

/* ─── CLASS BREAKDOWN ─── */
.breakdown-title {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.25);
    margin-bottom: 16px;
}

.class-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}

.class-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

.class-name {
    font-size: 13px;
    color: rgba(255,255,255,0.55);
    flex: 1;
    white-space: nowrap;
}

.class-bar-bg {
    flex: 2;
    height: 2px;
    background: rgba(255,255,255,0.06);
    border-radius: 1px;
    overflow: hidden;
}

.class-bar-fill {
    height: 100%;
    border-radius: 1px;
}

.class-pct {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    min-width: 40px;
    text-align: right;
}

/* ─── STATUS TAGS ─── */
.tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.04em;
}

.tag-benign {
    background: rgba(0,210,140,0.1);
    color: #00D28C;
    border: 1px solid rgba(0,210,140,0.2);
}

.tag-malignant {
    background: rgba(255,80,80,0.1);
    color: #FF7070;
    border: 1px solid rgba(255,80,80,0.2);
}

.tag-warning {
    background: rgba(255,175,50,0.1);
    color: #FFAF32;
    border: 1px solid rgba(255,175,50,0.2);
}

/* Streamlit overrides */
[data-testid="stFileUploader"] {
    background: transparent !important;
}

[data-testid="stFileUploader"] > div {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    padding: 40px !important;
    transition: all 0.3s !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(0,210,140,0.35) !important;
    background: rgba(0,210,140,0.03) !important;
}

[data-testid="stFileUploaderDropzone"] label {
    color: rgba(255,255,255,0.5) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: rgba(0,210,140,0.12) !important;
    color: #00D28C !important;
    border: 1px solid rgba(0,210,140,0.3) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    transition: all 0.2s !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: rgba(0,210,140,0.2) !important;
}

[data-testid="stImage"] img {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}

div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

.stSpinner { color: #00D28C !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    try:
        import keras
        return keras.saving.load_model("best_model.keras")
    except Exception:
        import tensorflow as tf
        return tf.keras.models.load_model("best_model.keras")


CLASSES = ["adenocarcinoma", "benign", "squamous_cell_carcinoma"]
CLASS_CONFIG = {
    "adenocarcinoma": {
        "label": "Adenocarcinoma",
        "short": "ADC",
        "color": "#FF7070",
        "tag": "malignant",
        "tag_label": "Malignant",
        "desc": "Glandular tissue malignancy"
    },
    "benign": {
        "label": "Benign Tissue",
        "short": "BNT",
        "color": "#00D28C",
        "tag": "benign",
        "tag_label": "Non-cancerous",
        "desc": "Normal lung tissue"
    },
    "squamous_cell_carcinoma": {
        "label": "Squamous Cell Carcinoma",
        "short": "SCC",
        "color": "#FFAF32",
        "tag": "warning",
        "tag_label": "Malignant",
        "desc": "Squamous epithelial malignancy"
    },
}

# ─── HERO ───
st.markdown("""
<div class="hero">
    <div class="badge"><span class="badge-dot"></span>AI Diagnostics · v2.0</div>
    <h1 class="hero-title">LungVision<br><span>AI Classifier</span></h1>
    <p class="hero-sub">Deep learning analysis of histopathological images for lung cancer detection across three tissue classifications.</p>
    <div class="stats-row">
        <div class="stat-item">
            <span class="stat-value">97%</span>
            <span class="stat-label">Accuracy</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
            <span class="stat-value">3</span>
            <span class="stat-label">Classes</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
            <span class="stat-value">CNN</span>
            <span class="stat-label">Architecture</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
            <span class="stat-value">224px</span>
            <span class="stat-label">Input size</span>
        </div>
    </div>
</div>
<div class="main-grid">
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="panel-label">Input · Upload image</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload histopathological image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, use_container_width=True)

with col2:
    st.markdown('<div class="panel-label">Output · Analysis results</div>', unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown("""
        <div style="height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; opacity:0.3;">
            <div style="font-size:36px;">🔬</div>
            <p style="font-size:13px; color:rgba(255,255,255,0.5); text-align:center; max-width:200px; line-height:1.5;">
                Upload an image to begin analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing tissue..."):
            model = load_model()
            img_r = img.resize((224, 224))
            arr = np.array(img_r).astype("float32") / 255.0
            arr = np.expand_dims(arr, axis=0)
            preds = model.predict(arr, verbose=0)

        pred_idx = int(np.argmax(preds))
        pred_class = CLASSES[pred_idx]
        cfg = CLASS_CONFIG[pred_class]
        confidence = float(preds[0][pred_idx]) * 100

        tag_class = f"tag-{cfg['tag']}"

        st.markdown(f"""
        <div class="result-main">
            <div class="result-type" style="color:{cfg['color']};">{cfg['short']} · {cfg['desc']}</div>
            <div class="result-name" style="color:{cfg['color']};">{cfg['label']}</div>
            <span class="tag {tag_class}">{cfg['tag_label']}</span>
        </div>

        <div class="conf-bar-wrap">
            <div class="conf-bar-header">
                <span class="conf-bar-label">Confidence</span>
                <span class="conf-bar-val">{confidence:.1f}%</span>
            </div>
            <div class="conf-bar-bg">
                <div class="conf-bar-fill" style="width:{confidence}%; background:{cfg['color']};"></div>
            </div>
        </div>

        <div class="breakdown-title">Class probabilities</div>
        """, unsafe_allow_html=True)

        for i, cls in enumerate(CLASSES):
            c = CLASS_CONFIG[cls]
            prob = float(preds[0][i]) * 100
            st.markdown(f"""
            <div class="class-row">
                <div class="class-dot" style="background:{c['color']};"></div>
                <span class="class-name">{c['label']}</span>
                <div class="class-bar-bg">
                    <div class="class-bar-fill" style="width:{prob}%; background:{c['color']};"></div>
                </div>
                <span class="class-pct" style="color:{c['color']};">{prob:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="padding:20px 60px; border-top:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center;">
    <span style="font-size:11px; color:rgba(255,255,255,0.18); letter-spacing:0.06em; text-transform:uppercase;">
        LungVision AI · For research & educational use only
    </span>
    <span style="font-size:11px; color:rgba(255,255,255,0.15); letter-spacing:0.06em; text-transform:uppercase;">
        TF · Keras · Streamlit
    </span>
</div>
""", unsafe_allow_html=True)
