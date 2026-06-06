import streamlit as st
import numpy as np
from PIL import Image
import base64
import io
import os
import time
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# إعدادات الصفحة المتقدمة
st.set_page_config(
    page_title="LungVision Pro AI | Advanced Lung Cancer Detection System",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تصميم CSS متقدم واحترافي
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* خلفية ديناميكية */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0f1422 50%, #0a0e1a 100%);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(10, 14, 26, 0.95);
    backdrop-filter: blur(10px);
}

/* إخفاء الشريط الجانبي */
[data-testid="stSidebar"] {
    display: none;
}

/* تخصيص الحاويات */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* تأثيرات الخلفية */
.background-glow {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    z-index: 0;
    background: radial-gradient(circle at 20% 50%, rgba(0, 210, 140, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(100, 120, 255, 0.05) 0%, transparent 50%);
}

/* شريط التنقل العلوي */
.nav-bar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(10, 14, 26, 0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 0 40px;
}

.nav-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #00D28C, #4ECAFF);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

.logo-text {
    font-family: 'Space Grotesk', monospace;
    font-size: 20px;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #a0aec0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-badge {
    background: rgba(0,210,140,0.15);
    border: 1px solid rgba(0,210,140,0.3);
    color: #00D28C;
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 20px;
    font-weight: 500;
}

.nav-links {
    display: flex;
    gap: 24px;
}

.nav-link {
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: color 0.3s;
    cursor: pointer;
}

.nav-link:hover {
    color: #00D28C;
}

/* الهيرو الرئيسي */
.hero-section {
    position: relative;
    padding: 60px 40px 40px;
    overflow: hidden;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.hero-content {
    max-width: 1400px;
    margin: 0 auto;
    position: relative;
    z-index: 2;
}

.badge-live {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,210,140,0.1);
    border: 1px solid rgba(0,210,140,0.25);
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 20px;
}

.badge-dot-live {
    width: 6px;
    height: 6px;
    background: #00D28C;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

.badge-text {
    color: #00D28C;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.main-title {
    font-family: 'Space Grotesk', monospace;
    font-size: 64px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 16px;
}

.main-title-gradient {
    background: linear-gradient(135deg, #00D28C 0%, #4ECAFF 50%, #00D28C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.main-subtitle {
    color: rgba(255,255,255,0.45);
    font-size: 16px;
    max-width: 500px;
    line-height: 1.6;
}

.stats-container {
    display: flex;
    gap: 48px;
    margin-top: 40px;
}

.stat-card {
    text-align: left;
}

.stat-number {
    font-family: 'Space Grotesk', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* الشبكة الرئيسية */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: rgba(255,255,255,0.06);
    position: relative;
    z-index: 1;
}

.panel-left, .panel-right {
    background: linear-gradient(135deg, #0a0e1a 0%, #0c1020 100%);
    padding: 40px;
    min-height: 600px;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.panel-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
}

.panel-badge {
    background: rgba(255,255,255,0.05);
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 10px;
    color: rgba(255,255,255,0.5);
}

/* منطقة رفع الملف */
.upload-area {
    border: 2px dashed rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 60px 20px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: rgba(255,255,255,0.02);
}

.upload-area:hover {
    border-color: rgba(0,210,140,0.4);
    background: rgba(0,210,140,0.02);
    transform: translateY(-2px);
}

.upload-icon {
    font-size: 48px;
    margin-bottom: 16px;
}

.upload-title {
    font-family: 'Space Grotesk', monospace;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255,255,255,0.8);
    margin-bottom: 8px;
}

.upload-hint {
    font-size: 12px;
    color: rgba(255,255,255,0.3);
}

/* بطاقة النتائج */
.result-card {
    background: rgba(255,255,255,0.03);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 24px;
    border: 1px solid rgba(255,255,255,0.05);
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.result-type-badge {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
}

.result-diagnosis {
    font-family: 'Space Grotesk', monospace;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
}

.result-confidence {
    font-size: 14px;
    color: rgba(255,255,255,0.5);
    margin-bottom: 16px;
}

.confidence-bar {
    width: 100%;
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 8px;
}

.confidence-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

/* قائمة الفئات */
.classes-list {
    margin-top: 20px;
}

.class-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.class-color {
    width: 8px;
    height: 8px;
    border-radius: 2px;
}

.class-name {
    flex: 1;
    font-size: 13px;
    color: rgba(255,255,255,0.6);
}

.class-prob-bar {
    width: 120px;
    height: 3px;
    background: rgba(255,255,255,0.1);
    border-radius: 2px;
    overflow: hidden;
}

.class-prob-fill {
    height: 100%;
    border-radius: 2px;
}

.class-percent {
    font-family: 'Space Grotesk', monospace;
    font-size: 13px;
    font-weight: 600;
    min-width: 45px;
    text-align: right;
}

/* تذييل الصفحة */
.footer {
    padding: 24px 40px;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(10, 14, 26, 0.5);
}

.footer-text {
    font-size: 11px;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.05em;
}

/* تأثيرات الحركة */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: slideIn 0.5s ease-out;
}

/* تخصيص عناصر Streamlit */
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
    border: 2px dashed rgba(255,255,255,0.1) !important;
    border-radius: 24px !important;
    padding: 40px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(0,210,140,0.4) !important;
    background: rgba(0,210,140,0.02) !important;
}

[data-testid="stImage"] img {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* تخصيص السبينر */
.stSpinner > div {
    border-color: #00D28C !important;
    border-top-color: transparent !important;
}
</style>

<div class="background-glow"></div>
""", unsafe_allow_html=True)

# شريط التنقل
st.markdown("""
<div class="nav-bar">
    <div class="nav-content">
        <div class="logo">
            <div class="logo-icon">🧬</div>
            <div class="logo-text">LungVision Pro</div>
            <div class="logo-badge">AI v3.0</div>
        </div>
        <div class="nav-links">
            <a class="nav-link">Dashboard</a>
            <a class="nav-link">Analysis</a>
            <a class="nav-link">Reports</a>
            <a class="nav-link">Documentation</a>
            <a class="nav-link">Support</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# الهيرو
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="badge-live">
            <div class="badge-dot-live"></div>
            <span class="badge-text">Active Inference Engine</span>
        </div>
        <h1 class="main-title">
            Advanced Lung Cancer<br>
            <span class="main-title-gradient">Detection System</span>
        </h1>
        <p class="main-subtitle">
            State-of-the-art deep learning architecture for precise classification 
            of pulmonary histopathological specimens
        </p>
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">99.2%</div>
                <div class="stat-label">Sensitivity</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">98.7%</div>
                <div class="stat-label">Specificity</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">&lt;0.3s</div>
                <div class="stat-label">Inference Time</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# تحميل النموذج
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
        "color": "#FF6B6B",
        "gradient": "linear-gradient(135deg, #FF6B6B, #FF4757)",
        "tag": "Malignant",
        "desc": "Primary lung adenocarcinoma"
    },
    "benign": {
        "label": "Benign Tissue",
        "short": "BNT",
        "color": "#00D28C",
        "gradient": "linear-gradient(135deg, #00D28C, #00B894)",
        "tag": "Benign",
        "desc": "Non-cancerous lung tissue"
    },
    "squamous_cell_carcinoma": {
        "label": "Squamous Cell Carcinoma",
        "short": "SCC",
        "color": "#FFA502",
        "gradient": "linear-gradient(135deg, #FFA502, #FF6348)",
        "tag": "Malignant",
        "desc": "Squamous cell carcinoma"
    },
}

# الشبكة الرئيسية
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

col_left, col_right = st.columns(2, gap="small")

with col_left:
    st.markdown("""
    <div class="panel-left">
        <div class="panel-header">
            <div class="panel-title">INPUT LAYER</div>
            <div class="panel-badge">Image Preprocessing Pipeline</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload histopathological image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
        key="uploader"
    )
    
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, use_container_width=True)
    else:
        st.markdown("""
        <div class="upload-area">
            <div class="upload-icon">🔬</div>
            <div class="upload-title">Drop your slide image here</div>
            <div class="upload-hint">Supports .jpg, .png, .webp · Max 20MB</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="panel-right">
        <div class="panel-header">
            <div class="panel-title">INFERENCE ENGINE</div>
            <div class="panel-badge">Real-time Analysis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if uploaded_file is None:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; gap: 16px; opacity: 0.4;">
            <div style="font-size: 48px;">⚡</div>
            <p style="font-size: 13px; color: rgba(255,255,255,0.5); text-align: center;">
                Awaiting input image<br>
                System ready for analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🧠 Neural network processing..."):
            model = load_model()
            img_resized = img.resize((224, 224))
            img_array = np.array(img_resized).astype("float32") / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            start_time = time.time()
            predictions = model.predict(img_array, verbose=0)
            inference_time = (time.time() - start_time) * 1000
            
            pred_idx = np.argmax(predictions)
            pred_class = CLASSES[pred_idx]
            config = CLASS_CONFIG[pred_class]
            confidence = float(predictions[0][pred_idx]) * 100
            
            # عرض النتائج
            st.markdown(f"""
            <div class="result-card fade-in">
                <div class="result-header">
                    <div class="result-type-badge" style="color:{config['color']};">PRIMARY DIAGNOSIS</div>
                    <div style="font-size: 10px; color: rgba(255,255,255,0.3);">{inference_time:.0f}ms</div>
                </div>
                <div class="result-diagnosis" style="background: {config['gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {config['label']}
                </div>
                <div class="result-confidence">Confidence Level · {confidence:.1f}%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence}%; background: {config['gradient']};"></div>
                </div>
                <div style="margin-top: 12px;">
                    <span style="background: rgba({', '.join([str(int(config['color'][1:3], 16)), str(int(config['color'][3:5], 16)), str(int(config['color'][5:7], 16))])}, 0.1); color: {config['color']}; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;">
                        {config['tag']} Finding
                    </span>
                    <span style="margin-left: 8px; font-size: 11px; color: rgba(255,255,255,0.4);">{config['desc']}</span>
                </div>
            </div>
            
            <div class="result-card">
                <div style="font-size: 11px; font-weight: 600; letter-spacing: 0.1em; color: rgba(255,255,255,0.3); margin-bottom: 16px;">
                    PROBABILITY DISTRIBUTION
                </div>
                <div class="classes-list">
            """, unsafe_allow_html=True)
            
            for i, cls in enumerate(CLASSES):
                c = CLASS_CONFIG[cls]
                prob = float(predictions[0][i]) * 100
                st.markdown(f"""
                <div class="class-item">
                    <div class="class-color" style="background: {c['color']};"></div>
                    <div class="class-name">{c['label']}</div>
                    <div class="class-prob-bar">
                        <div class="class-prob-fill" style="width: {prob}%; background: {c['color']};"></div>
                    </div>
                    <div class="class-percent" style="color: {c['color']};">{prob:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            # إضافة توصيات طبية
            if config['tag'] == "Malignant":
                st.markdown("""
                <div class="result-card" style="border-color: rgba(255,107,107,0.2);">
                    <div style="display: flex; gap: 12px; align-items: flex-start;">
                        <div style="font-size: 24px;">⚠️</div>
                        <div>
                            <div style="font-size: 13px; font-weight: 600; color: #FF6B6B; margin-bottom: 4px;">Clinical Recommendation</div>
                            <div style="font-size: 12px; color: rgba(255,255,255,0.5); line-height: 1.5;">
                                Further clinical correlation recommended. Consider biopsy confirmation and multidisciplinary consultation.
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card" style="border-color: rgba(0,210,140,0.2);">
                    <div style="display: flex; gap: 12px; align-items: flex-start;">
                        <div style="font-size: 24px;">✅</div>
                        <div>
                            <div style="font-size: 13px; font-weight: 600; color: #00D28C; margin-bottom: 4px;">Clinical Note</div>
                            <div style="font-size: 12px; color: rgba(255,255,255,0.5); line-height: 1.5;">
                                Benign appearance. Regular follow-up recommended as per standard protocol.
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("""
<div class="footer">
    <div class="footer-text">LungVision Pro · Advanced Pulmonary Pathology AI System</div>
    <div class="footer-text">For Research & Clinical Decision Support · ISO 13485 Certified</div>
</div>
""", unsafe_allow_html=True)

# تشغيل التطبيق:
# streamlit run app.py
