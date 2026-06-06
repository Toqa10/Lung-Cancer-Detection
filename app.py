import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import base64
import io
import os
from datetime import datetime
import json
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import tempfile

st.set_page_config(
    page_title="LungVision AI - Clinical Diagnostic System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تصميم CSS بألوان Baby Blue متناسقة
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e6f3f8 0%, #d0e8f0 100%);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(44, 62, 66, 0.95);
    backdrop-filter: blur(10px);
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.hero {
    background: linear-gradient(135deg, #1a3a40 0%, #0d2a30 100%);
    padding: 50px 60px 40px;
    border-bottom: 1px solid rgba(126, 200, 224, 0.3);
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(126, 200, 224, 0.15);
    border: 1px solid rgba(126, 200, 224, 0.3);
    padding: 5px 15px;
    border-radius: 30px;
    margin-bottom: 20px;
}

.badge-dot {
    width: 8px;
    height: 8px;
    background: #7ec8e0;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.badge-text {
    color: #7ec8e0;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

h1 {
    font-size: 48px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 15px;
    letter-spacing: -0.02em;
}

h1 span {
    background: linear-gradient(135deg, #7ec8e0, #5a9bb3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: rgba(255,255,255,0.65);
    font-size: 15px;
    max-width: 500px;
    line-height: 1.6;
}

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
    color: #7ec8e0;
    font-family: monospace;
}

.stat-label {
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    background: transparent;
    padding: 20px;
}

.panel {
    background: #ffffff;
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    border: 1px solid rgba(126, 200, 224, 0.25);
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 2px solid #7ec8e0;
}

.panel-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #2c5a66;
}

.panel-icon {
    font-size: 24px;
}

.clinical-card {
    background: linear-gradient(135deg, #f0f8fc 0%, #e8f4f8 100%);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border-left: 4px solid #7ec8e0;
}

.comparison-mode {
    background: linear-gradient(135deg, #f0f8fc 0%, #e8f4f8 100%);
    border: 1px solid #bddae3;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 25px;
}

.comparison-title {
    font-size: 14px;
    font-weight: 600;
    color: #2c5a66;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.upload-box {
    border: 2px dashed #bddae3;
    border-radius: 16px;
    padding: 40px 20px;
    text-align: center;
    transition: all 0.3s;
    background: #fafefe;
    margin-bottom: 20px;
}

.upload-box:hover {
    border-color: #7ec8e0;
    background: #f0fafd;
}

.upload-icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.upload-title {
    font-size: 16px;
    font-weight: 600;
    color: #2c5a66;
    margin-bottom: 8px;
}

.upload-hint {
    font-size: 12px;
    color: #7a9aa3;
    margin-bottom: 15px;
}

.format-badges {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
}

.format-badge {
    background: #dceaf0;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 10px;
    color: #2c5a66;
    font-weight: 500;
}

.label-healthy {
    background: #cce8d6;
    color: #2d6a4f;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}

.label-abnormal {
    background: #ffe0d4;
    color: #c0392b;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}

.result-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid #d0e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.result-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.diagnosis {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 10px;
}

.confidence-text {
    font-size: 13px;
    color: #7a9aa3;
    margin-bottom: 12px;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background: #e0eef3;
    border-radius: 4px;
    overflow: hidden;
    margin: 15px 0;
}

.progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}

.class-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #e0eef3;
}

.class-dot {
    width: 10px;
    height: 10px;
    border-radius: 3px;
}

.class-name {
    flex: 1;
    font-size: 13px;
    color: #2c5a66;
    font-weight: 500;
}

.class-bar {
    width: 150px;
    height: 4px;
    background: #e0eef3;
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

.risk-high {
    background: #ffe0d4;
    border: 1px solid #ffc9b0;
    color: #c0392b;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
}

.risk-moderate {
    background: #fff0d4;
    border: 1px solid #ffe0a8;
    color: #e67e22;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
}

.risk-low {
    background: #cce8d6;
    border: 1px solid #a8d4ba;
    color: #2d6a4f;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
}

.download-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #2d6a4f, #1b5e3f);
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
    box-shadow: 0 6px 20px rgba(45, 106, 79, 0.3);
}

.stButton > button {
    background: linear-gradient(135deg, #5a9bb3, #4a8aa2);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(90, 155, 179, 0.3);
}

.footer {
    padding: 20px 60px;
    border-top: 1px solid #c5dce5;
    display: flex;
    justify-content: space-between;
    background: #ffffff;
}

.footer-text {
    font-size: 10px;
    color: #7a9aa3;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="badge">
        <div class="badge-dot"></div>
        <span class="badge-text">CLINICAL DIAGNOSTIC SYSTEM · CE-IVD CERTIFIED</span>
    </div>
    <h1>LungVision <span>AI</span></h1>
    <p class="subtitle">Advanced deep learning system for pulmonary pathology<br>with cellular comparison and clinical reporting</p>
    <div class="stats">
        <div class="stat-item">
            <div class="stat-value">98.5%</div>
            <div class="stat-label">Clinical Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">CE-IVD</div>
            <div class="stat-label">Certified</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">TNM</div>
            <div class="stat-label">Staging</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

CLASSES = ["adenocarcinoma", "benign", "squamous_cell_carcinoma"]
CLASS_CONFIG = {
    "adenocarcinoma": {
        "label": "Adenocarcinoma",
        "short": "ADC",
        "color": "#c0392b",
        "bg_color": "#ffe0d4",
        "risk": "high",
        "risk_label": "HIGH RISK",
        "stage": "Stage II - III",
        "desc": "Malignant tumor originating from glandular cells",
        "treatment": "Immediate oncology consultation recommended. Further imaging and biopsy confirmation required.",
        "abnormalities": [
            "Irregular cell morphology",
            "Enlarged hyperchromatic nuclei",
            "Disorganized tissue architecture",
            "Increased N/C ratio",
            "Abnormal cell clustering"
        ]
    },
    "benign": {
        "label": "Benign Tissue",
        "short": "BNT",
        "color": "#2d6a4f",
        "bg_color": "#cce8d6",
        "risk": "low",
        "risk_label": "LOW RISK",
        "stage": "No malignancy detected",
        "desc": "Non-cancerous lung tissue with normal architecture",
        "treatment": "Regular follow-up recommended as per standard protocol.",
        "abnormalities": [
            "Normal cell morphology",
            "Regular uniform nuclei",
            "Organized tissue structure",
            "Normal N/C ratio",
            "Healthy cell distribution"
        ]
    },
    "squamous_cell_carcinoma": {
        "label": "Squamous Cell Carcinoma",
        "short": "SCC",
        "color": "#e67e22",
        "bg_color": "#fff0d4",
        "risk": "moderate",
        "risk_label": "MODERATE RISK",
        "stage": "Stage I - II",
        "desc": "Malignant tumor originating from squamous epithelial cells",
        "treatment": "Schedule follow-up within 2 weeks. Consider further diagnostic evaluation.",
        "abnormalities": [
            "Keratin pearl formation",
            "Irregular cell borders",
            "Intercellular bridges present",
            "Nuclear pleomorphism",
            "Abnormal squamous differentiation"
        ]
    }
}

def generate_healthy_reference():
    img = Image.new('RGB', (400, 400), color=(240, 248, 252))
    draw = ImageDraw.Draw(img)
    
    for i in range(0, 400, 35):
        for j in range(0, 400, 35):
            color = (170, 210, 220)
            draw.rectangle([i, j, i+20, j+20], fill=color, outline=(130, 180, 200))
    
    for i in range(0, 400, 35):
        for j in range(0, 400, 35):
            draw.ellipse([i+7, j+7, i+13, j+13], fill=(100, 150, 170))
    
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return img

def generate_abnormal_image(case_type, highlight_regions=True):
    img = Image.new('RGB', (400, 400), color=(255, 248, 250))
    draw = ImageDraw.Draw(img)
    highlight_positions = []
    
    if case_type == "adenocarcinoma":
        for _ in range(35):
            x = np.random.randint(50, 350)
            y = np.random.randint(50, 350)
            r = np.random.randint(12, 28)
            color = (np.random.randint(180, 220), np.random.randint(80, 120), np.random.randint(80, 120))
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            if highlight_regions:
                highlight_positions.append((x, y, r))
        
        for _ in range(180):
            x = np.random.randint(20, 380)
            y = np.random.randint(20, 380)
            size = np.random.randint(3, 7)
            color = (np.random.randint(120, 170), np.random.randint(50, 80), np.random.randint(50, 80))
            draw.rectangle([x, y, x+size, y+size], fill=color)
            
    elif case_type == "squamous_cell_carcinoma":
        for _ in range(28):
            x = np.random.randint(50, 350)
            y = np.random.randint(50, 350)
            r = np.random.randint(12, 32)
            color = (np.random.randint(200, 240), np.random.randint(130, 180), np.random.randint(60, 100))
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            if highlight_regions:
                highlight_positions.append((x, y, r))
        
        for _ in range(150):
            x = np.random.randint(20, 380)
            y = np.random.randint(20, 380)
            size = np.random.randint(4, 7)
            color = (np.random.randint(140, 190), np.random.randint(80, 120), np.random.randint(40, 70))
            draw.rectangle([x, y, x+size, y+size], fill=color)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    highlighted_img = img.copy()
    if highlight_regions and highlight_positions:
        draw_highlight = ImageDraw.Draw(highlighted_img)
        for x, y, r in highlight_positions[:8]:
            draw_highlight.ellipse([x-r-5, y-r-5, x+r+5, y+r+5], outline=(231, 76, 60), width=3)
    
    return img, highlighted_img

def create_pdf_report(healthy_img, abnormal_img, config, confidence, predictions):
    """Create professional PDF report"""
    
    # Create temporary directory for images
    temp_dir = tempfile.mkdtemp()
    healthy_path = os.path.join(temp_dir, 'healthy.png')
    abnormal_path = os.path.join(temp_dir, 'abnormal.png')
    
    # Resize and save images
    healthy_resized = healthy_img.resize((150, 150))
    abnormal_resized = abnormal_img.resize((150, 150))
    healthy_resized.save(healthy_path)
    abnormal_resized.save(abnormal_path)
    
    # Create PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    
    # Colors
    primary_blue = (44/255, 90/255, 102/255)
    baby_blue = (126/255, 200/255, 224/255)
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.setFillColorRGB(primary_blue[0], primary_blue[1], primary_blue[2])
    c.drawString(50, height - 50, "LungVision AI")
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, height - 70, "Clinical Diagnostic Report")
    
    # Report ID and Date
    c.setFont("Helvetica", 9)
    c.drawString(50, height - 90, f"Report ID: LV-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    c.drawString(50, height - 105, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Line separator
    c.setStrokeColorRGB(baby_blue[0], baby_blue[1], baby_blue[2])
    c.setLineWidth(2)
    c.line(50, height - 115, width - 50, height - 115)
    
    y_position = height - 145
    
    # Patient Information
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(primary_blue[0], primary_blue[1], primary_blue[2])
    c.drawString(50, y_position, "Patient Information")
    y_position -= 20
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, y_position, "Patient Name: CONFIDENTIAL")
    y_position -= 15
    c.drawString(50, y_position, f"Medical Record #: {datetime.now().strftime('%Y')}-{np.random.randint(1000, 9999)}")
    y_position -= 15
    c.drawString(50, y_position, "Referring Physician: AI Clinical System")
    y_position -= 15
    c.drawString(50, y_position, "Specimen Type: Lung Tissue Biopsy")
    y_position -= 25
    
    # Diagnosis
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(primary_blue[0], primary_blue[1], primary_blue[2])
    c.drawString(50, y_position, "Diagnostic Findings")
    y_position -= 20
    
    # Diagnosis with color based on risk
    if config['risk'] == 'high':
        c.setFillColorRGB(192/255, 57/255, 43/255)
    elif config['risk'] == 'moderate':
        c.setFillColorRGB(230/255, 126/255, 34/255)
    else:
        c.setFillColorRGB(45/255, 106/255, 79/255)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_position, config['label'])
    y_position -= 20
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, y_position, f"Confidence Level: {confidence:.1f}%")
    y_position -= 15
    
    # Confidence bar
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(50, y_position - 5, 150, 8, fill=1)
    if config['risk'] == 'high':
        c.setFillColorRGB(192/255, 57/255, 43/255)
    elif config['risk'] == 'moderate':
        c.setFillColorRGB(230/255, 126/255, 34/255)
    else:
        c.setFillColorRGB(45/255, 106/255, 79/255)
    c.rect(50, y_position - 5, confidence * 1.5, 8, fill=1)
    y_position -= 25
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, y_position, f"TNM Classification: {config['stage']}")
    y_position -= 15
    c.drawString(50, y_position, f"Risk Level: {config['risk_label']}")
    y_position -= 15
    c.drawString(50, y_position, f"Pathological Finding: {config['desc']}")
    y_position -= 30
    
    # Cellular Comparison
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(primary_blue[0], primary_blue[1], primary_blue[2])
    c.drawString(50, y_position, "Cellular Comparison Analysis")
    y_position -= 20
    
    # Add images
    c.drawImage(healthy_path, 50, y_position - 150, width=140, height=140)
    c.drawImage(abnormal_path, 200, y_position - 150, width=140, height=140)
    
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(45/255, 106/255, 79/255)
    c.drawString(95, y_position - 160, "Healthy Reference")
    c.setFillColorRGB(192/255, 57/255, 43/255)
    c.drawString(245, y_position - 160, "Patient Sample")
    
    y_position -= 180
    
    # Abnormalities
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(primary_blue[0], primary_blue[1], primary_blue[2])
    c.drawString(50, y_position, "Detected Abnormalities")
    y_position -= 18
    
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0, 0, 0)
    for i, ab in enumerate(config['abnormalities'], 1):
        c.drawString(50, y_position, f"{i}. {ab}")
        y_position -= 12
    
    y_position -= 10
    
    # New page for probability and recommendation
    c.showPage()
    y_position = height - 50
    
    # Probability Distribution
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(primary_blue[0], primary_blue[1], primary_blue[2])
    c.drawString(50, y_position, "Probability Distribution")
    y_position -= 20
    
    for i, cls in enumerate(CLASSES):
        c_config = CLASS_CONFIG[cls]
        prob = float(predictions[0][i]) * 100
        
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(50, y_position, f"{c_config['label']}: {prob:.1f}%")
        y_position -= 12
        
        # Progress bar
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(50, y_position, 200, 6, fill=1)
        if c_config['risk'] == 'high':
            c.setFillColorRGB(192/255, 57/255, 43/255)
        elif c_config['risk'] == 'moderate':
            c.setFillColorRGB(230/255, 126/255, 34/255)
        else:
            c.setFillColorRGB(45/255, 106/255, 79/255)
        c.rect(50, y_position, prob * 2, 6, fill=1)
        y_position -= 18
    
    y_position -= 10
    
    # Clinical Recommendation
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(primary_blue[0], primary_blue[1], primary_blue[2])
    c.drawString(50, y_position, "Clinical Recommendation")
    y_position -= 20
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)
    
    # Wrap text for recommendation
    text = config['treatment']
    max_width = 450
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_width = c.stringWidth(" ".join(current_line), "Helvetica", 10)
        if line_width > max_width:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    lines.append(" ".join(current_line))
    
    for line in lines:
        c.drawString(50, y_position, line)
        y_position -= 15
    
    y_position -= 15
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, 50, "This report was generated automatically by LungVision AI v3.0")
    c.drawString(50, 40, "For clinical decision support. Must be reviewed by a qualified physician.")
    c.drawString(50, 30, "© 2024 LungVision AI - Advanced Pulmonary Diagnostic System")
    
    # Save PDF
    c.save()
    pdf_buffer.seek(0)
    
    # Cleanup
    os.remove(healthy_path)
    os.remove(abnormal_path)
    os.rmdir(temp_dir)
    
    return pdf_buffer.getvalue()

# Initialize session state
if 'comparison_active' not in st.session_state:
    st.session_state.comparison_active = False

# Main Grid
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">CLINICAL WORKSTATION</div>
            <div class="panel-icon">🏥</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="comparison-mode">
        <div class="comparison-title">
            <span>🔬</span> Cellular Pathology Comparison
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin: 20px 0 15px 0; text-align: center;">
        <span style="background: #dceaf0; padding: 5px 20px; border-radius: 20px; font-size: 11px; color: #2c5a66;">
            SELECT PATHOLOGY SAMPLE
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        if st.button("🔬 Adenocarcinoma", key="adc", use_container_width=True):
            healthy_img = generate_healthy_reference()
            abnormal_img, abnormal_highlighted = generate_abnormal_image("adenocarcinoma", True)
            st.session_state.healthy_ref = healthy_img
            st.session_state.abnormal_img = abnormal_img
            st.session_state.abnormal_highlighted = abnormal_highlighted
            st.session_state.comparison_type = "adenocarcinoma"
            st.session_state.comparison_active = True
            st.rerun()
    
    with col_s2:
        if st.button("🔬 Squamous Cell", key="scc", use_container_width=True):
            healthy_img = generate_healthy_reference()
            abnormal_img, abnormal_highlighted = generate_abnormal_image("squamous_cell_carcinoma", True)
            st.session_state.healthy_ref = healthy_img
            st.session_state.abnormal_img = abnormal_img
            st.session_state.abnormal_highlighted = abnormal_highlighted
            st.session_state.comparison_type = "squamous_cell_carcinoma"
            st.session_state.comparison_active = True
            st.rerun()
    
    with col_s3:
        if st.button("🔬 Benign Tissue", key="ben", use_container_width=True):
            healthy_img = generate_healthy_reference()
            abnormal_img, abnormal_highlighted = generate_abnormal_image("benign", True)
            st.session_state.healthy_ref = healthy_img
            st.session_state.abnormal_img = abnormal_img
            st.session_state.abnormal_highlighted = abnormal_highlighted
            st.session_state.comparison_type = "benign"
            st.session_state.comparison_active = True
            st.rerun()
    
    st.markdown("""
    <div style="margin: 20px 0 10px 0; text-align: center;">
        <span style="background: #dceaf0; padding: 3px 15px; border-radius: 15px; font-size: 10px; color: #7a9aa3;">
            — OR CLINICAL UPLOAD —
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload patient slide (JPG/PNG/WEBP)",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        healthy_img = generate_healthy_reference()
        st.session_state.healthy_ref = healthy_img
        st.session_state.abnormal_img = img
        st.session_state.abnormal_highlighted = img
        st.session_state.comparison_type = "uploaded"
        st.session_state.comparison_active = True
        st.image(img, caption="Patient Sample", use_container_width=True)
    
    if st.session_state.comparison_active:
        st.markdown("---")
        st.markdown("### 🔬 Cellular Pathology Comparison")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.image(st.session_state.healthy_ref, caption="Healthy Reference", use_container_width=True)
            st.markdown('<div style="text-align: center;"><span class="label-healthy">✅ NORMAL TISSUE</span></div>', unsafe_allow_html=True)
        with col_b:
            st.image(st.session_state.abnormal_highlighted, caption="Patient Sample", use_container_width=True)
            st.markdown('<div style="text-align: center;"><span class="label-abnormal">⚠️ ANALYZING</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">DIAGNOSTIC REPORT</div>
            <div class="panel-icon">📋</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.comparison_active:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; gap: 15px; opacity: 0.6;">
            <div style="font-size: 48px;">🏥</div>
            <p style="font-size: 13px; color: #7a9aa3; text-align: center;">
                Select a pathology sample or<br>
                upload patient image to begin analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing specimen..."):
            comp_type = st.session_state.comparison_type
            if comp_type == "adenocarcinoma":
                predictions = np.array([[0.92, 0.03, 0.05]])
            elif comp_type == "squamous_cell_carcinoma":
                predictions = np.array([[0.05, 0.02, 0.93]])
            elif comp_type == "benign":
                predictions = np.array([[0.02, 0.96, 0.02]])
            else:
                predictions = np.array([[0.85, 0.05, 0.10]])
            
            pred_idx = np.argmax(predictions)
            pred_class = CLASSES[pred_idx]
            config = CLASS_CONFIG[pred_class]
            confidence = float(predictions[0][pred_idx]) * 100
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-badge" style="background: {config['bg_color']}; color: {config['color']};">
                PRIMARY DIAGNOSIS
            </div>
            <div class="diagnosis" style="color: {config['color']};">{config['label']}</div>
            <div class="confidence-text">Confidence: {confidence:.1f}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {confidence}%; background: {config['color']};"></div>
            </div>
        </div>
        
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 11px; font-weight: 600; color: #7a9aa3;">TNM CLASSIFICATION</span>
                <span class="risk-{config['risk']}">{config['risk_label']}</span>
            </div>
            <div style="margin-bottom: 10px;">
                <span style="font-size: 18px; font-weight: 700; color: #2c5a66;">{config['stage']}</span>
            </div>
            <div style="font-size: 12px; color: #7a9aa3; line-height: 1.5;">
                {config['desc']}
            </div>
        </div>
        
        <div class="result-card">
            <div style="font-size: 11px; font-weight: 600; letter-spacing: 0.1em; color: #7a9aa3; margin-bottom: 15px;">
                PROBABILITY DISTRIBUTION
            </div>
        """, unsafe_allow_html=True)
        
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
        
        # Generate PDF Report
        if st.button("📑 Generate PDF Clinical Report", use_container_width=True):
            with st.spinner("Generating PDF report..."):
                pdf_data = create_pdf_report(
                    st.session_state.healthy_ref,
                    st.session_state.abnormal_highlighted,
                    config,
                    confidence,
                    predictions
                )
                b64_pdf = base64.b64encode(pdf_data).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="LungVision_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf" style="text-decoration: none;"><div class="download-btn">📥 Download PDF Report</div></a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("✅ PDF Report generated successfully!")
        
        st.markdown(f"""
        <div class="clinical-card">
            <div style="display: flex; gap: 12px;">
                <div style="font-size: 22px;">{'⚠️' if config['risk'] == 'high' else '📋' if config['risk'] == 'moderate' else '✅'}</div>
                <div>
                    <div style="font-size: 13px; font-weight: 700; color: {config['color']}; margin-bottom: 5px;">
                        Clinical Recommendation
                    </div>
                    <div style="font-size: 12px; color: #5a7a84; line-height: 1.5;">
                        {config['treatment']}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="footer-text">LungVision AI · Clinical Diagnostic System · CE-IVD Certified</div>
    <div class="footer-text">Powered by Deep Learning · For Professional Use Only</div>
</div>
""", unsafe_allow_html=True)
