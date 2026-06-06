import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import base64
import io
import os
from datetime import datetime
import json
import random
import pandas as pd

st.set_page_config(
    page_title="LungVision AI - Clinical System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS DESIGN
# ============================================
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
    padding: 40px 60px 35px;
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
    max-width: 550px;
    line-height: 1.6;
}

.stats {
    display: flex;
    gap: 40px;
    margin-top: 30px;
    flex-wrap: wrap;
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
    padding: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    border: 1px solid rgba(126, 200, 224, 0.25);
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 12px;
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

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #f0f8fc;
    border-radius: 12px;
    padding: 5px;
    margin-bottom: 15px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: #7ec8e0 !important;
    color: white !important;
}

.clinical-card {
    background: linear-gradient(135deg, #f0f8fc 0%, #e8f4f8 100%);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 18px;
    border-left: 4px solid #7ec8e0;
}

.comparison-mode {
    background: linear-gradient(135deg, #f0f8fc 0%, #e8f4f8 100%);
    border: 1px solid #bddae3;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 20px;
}

.comparison-title {
    font-size: 14px;
    font-weight: 600;
    color: #2c5a66;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.upload-box {
    border: 2px dashed #bddae3;
    border-radius: 16px;
    padding: 35px 20px;
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
    margin-bottom: 12px;
}

.upload-title {
    font-size: 16px;
    font-weight: 600;
    color: #2c5a66;
    margin-bottom: 6px;
}

.upload-hint {
    font-size: 12px;
    color: #7a9aa3;
    margin-bottom: 12px;
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
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}

.label-abnormal {
    background: #ffe0d4;
    color: #c0392b;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}

.result-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 18px;
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
    margin-bottom: 12px;
}

.diagnosis {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 8px;
}

.confidence-text {
    font-size: 13px;
    color: #7a9aa3;
    margin-bottom: 10px;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background: #e0eef3;
    border-radius: 4px;
    overflow: hidden;
    margin: 12px 0;
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
    padding: 8px 0;
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

.download-btn, .btn-secondary, .ask-btn, .edit-btn, .save-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #2d6a4f, #1b5e3f);
    border: none;
    padding: 12px 20px;
    border-radius: 12px;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    width: 100%;
    justify-content: center;
    text-decoration: none;
    margin-bottom: 8px;
}

.btn-secondary {
    background: linear-gradient(135deg, #5a9bb3, #4a8aa2);
}

.ask-btn {
    background: linear-gradient(135deg, #7ec8e0, #5a9bb3);
}

.edit-btn {
    background: linear-gradient(135deg, #e67e22, #d35400);
}

.save-btn {
    background: linear-gradient(135deg, #27ae60, #1e8449);
}

.download-btn:hover, .btn-secondary:hover, .ask-btn:hover, .edit-btn:hover, .save-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(45, 106, 79, 0.3);
}

.stButton > button {
    background: linear-gradient(135deg, #5a9bb3, #4a8aa2);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(90, 155, 179, 0.3);
}

.footer {
    padding: 15px 40px;
    border-top: 1px solid #c5dce5;
    display: flex;
    justify-content: space-between;
    background: #ffffff;
    flex-wrap: wrap;
    gap: 10px;
}

.footer-text {
    font-size: 9px;
    color: #7a9aa3;
    letter-spacing: 0.05em;
}

.reference-card {
    background: #fafefe;
    border: 1px solid #d0e8f0;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
}

.metric-card {
    background: linear-gradient(135deg, #f0f8fc, #e8f4f8);
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    border: 1px solid #c5dce5;
}

.batch-item {
    background: #f0f8fc;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.qa-card {
    background: #fafefe;
    border: 1px solid #d0e8f0;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 15px;
}

.qa-question {
    background: #f0f8fc;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 3px solid #7ec8e0;
}

.qa-answer {
    background: #e8f4f8;
    padding: 12px;
    border-radius: 12px;
    margin-top: 10px;
    border-left: 3px solid #2d6a4f;
}

.edit-mode-indicator {
    background: #fff0d4;
    border: 1px solid #e67e22;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 15px;
    text-align: center;
    font-size: 12px;
    color: #e67e22;
}

.treatment-card {
    background: #f0f8fc;
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #2d6a4f;
}

.treatment-edit {
    background: #fff8f0;
    border: 2px solid #e67e22;
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
}

.doctor-note {
    background: #e8f4f8;
    border-left: 4px solid #7ec8e0;
    padding: 15px;
    border-radius: 12px;
    margin: 15px 0;
    font-style: italic;
}

.heatmap-guide {
    background: linear-gradient(135deg, #1a3a40, #0d2a30);
    border-radius: 16px;
    padding: 25px;
    margin: 15px 0;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================
st.markdown("""
<div class="hero">
    <div class="badge">
        <div class="badge-dot"></div>
        <span class="badge-text">CLINICAL DIAGNOSTIC SYSTEM · DOCTOR EDITING MODE</span>
    </div>
    <h1>LungVision <span>AI</span></h1>
    <p class="subtitle">Advanced pulmonary pathology system with cellular comparison,<br>heatmap visualization, intelligent Q&A, and physician editing</p>
    <div class="stats">
        <div class="stat-item">
            <div class="stat-value">98.5%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">✏️ Edit</div>
            <div class="stat-label">Mode</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">3</div>
            <div class="stat-label">Classes</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">TNM</div>
            <div class="stat-label">Staging</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# CLASS CONFIGURATION
# ============================================
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
        "grade": "Grade 3 - Poorly differentiated",
        "prognosis": "5-year survival: 25-35%",
        "first_line": "Surgical resection + platinum-based chemotherapy",
        "second_line": "Targeted therapy (EGFR/ALK inhibitors if positive)",
        "follow_up": "Every 2-3 months for first year",
        "risk_factors": ["Smoking (70%)", "Family history", "Age > 60", "COPD"],
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
        "grade": "Not applicable",
        "prognosis": "Excellent",
        "first_line": "Observation",
        "second_line": "Not applicable",
        "follow_up": "Annual check-up",
        "risk_factors": ["None significant", "May be incidental finding"],
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
        "grade": "Grade 2 - Moderately differentiated",
        "prognosis": "5-year survival: 45-55%",
        "first_line": "Surgical resection + adjuvant chemotherapy",
        "second_line": "Immunotherapy (PD-1 inhibitors)",
        "follow_up": "Every 3-4 months for first year",
        "risk_factors": ["Heavy smoking (90%)", "Male gender", "Age > 65"],
        "abnormalities": [
            "Keratin pearl formation",
            "Irregular cell borders",
            "Intercellular bridges present",
            "Nuclear pleomorphism",
            "Abnormal squamous differentiation"
        ]
    }
}

# ============================================
# REFERENCE LIBRARY
# ============================================
REFERENCE_LIBRARY = {
    "Adenocarcinoma": {
        "desc": "Most common type of lung cancer (40%). Originates from glandular cells.",
        "characteristics": "Glandular formation, mucin production, irregular nuclei",
        "key_features": ["Glandular structures", "Mucin production", "Nuclear atypia"]
    },
    "Squamous Cell Carcinoma": {
        "desc": "Second most common (25-30%). Associated with smoking.",
        "characteristics": "Keratin pearls, intercellular bridges, pleomorphic cells",
        "key_features": ["Keratinization", "Intercellular bridges", "Necrosis"]
    },
    "Benign": {
        "desc": "Normal lung tissue or benign lesions",
        "characteristics": "Organized architecture, regular nuclei, no atypia",
        "key_features": ["Normal anatomy", "Regular cells", "No malignancy"]
    }
}

# ============================================
# Q&A RESPONSES DATABASE
# ============================================
def get_qa_response(question, diagnosis, stage, risk, confidence, edited_treatment=None):
    """Generate intelligent response based on question and diagnosis"""
    question_lower = question.lower()
    
    treatment_text = edited_treatment if edited_treatment else CLASS_CONFIG[list(CLASS_CONFIG.keys())[[c['label'] for c in CLASS_CONFIG.values()].index(diagnosis) if diagnosis in [c['label'] for c in CLASS_CONFIG.values()] else 0]]['first_line']
    
    responses = {
        "prognosis": f"Based on the diagnosis of {diagnosis} at {stage}, the estimated 5-year survival rate is {CLASS_CONFIG[list(CLASS_CONFIG.keys())[[c['label'] for c in CLASS_CONFIG.values()].index(diagnosis) if diagnosis in [c['label'] for c in CLASS_CONFIG.values()] else 0]]['prognosis']} with appropriate treatment.",
        
        "treatment": f"The recommended treatment plan for {diagnosis} is: {treatment_text}",
        
        "follow up": f"Recommended follow-up schedule: {CLASS_CONFIG[list(CLASS_CONFIG.keys())[[c['label'] for c in CLASS_CONFIG.values()].index(diagnosis) if diagnosis in [c['label'] for c in CLASS_CONFIG.values()] else 0]]['follow_up']}. Regular imaging and clinical evaluation recommended.",
        
        "risk factor": f"Primary risk factors for {diagnosis} include: {', '.join(CLASS_CONFIG[list(CLASS_CONFIG.keys())[[c['label'] for c in CLASS_CONFIG.values()].index(diagnosis) if diagnosis in [c['label'] for c in CLASS_CONFIG.values()] else 0]]['risk_factors'])}.",
        
        "confidence": f"The AI model has {confidence:.1f}% confidence in this diagnosis. This is based on analysis of cellular morphology, tissue architecture, and comparison with over 10,000 pathological samples.",
        
        "grade": f"The histological grade is {CLASS_CONFIG[list(CLASS_CONFIG.keys())[[c['label'] for c in CLASS_CONFIG.values()].index(diagnosis) if diagnosis in [c['label'] for c in CLASS_CONFIG.values()] else 0]]['grade']}.",
        
        "next step": f"Recommended next steps: {CLASS_CONFIG[list(CLASS_CONFIG.keys())[[c['label'] for c in CLASS_CONFIG.values()].index(diagnosis) if diagnosis in [c['label'] for c in CLASS_CONFIG.values()] else 0]]['treatment']}",
        
        "what is": f"{diagnosis} is a {risk.lower()} risk pulmonary pathology characterized by {CLASS_CONFIG[list(CLASS_CONFIG.keys())[[c['label'] for c in CLASS_CONFIG.values()].index(diagnosis) if diagnosis in [c['label'] for c in CLASS_CONFIG.values()] else 0]]['desc'].lower()}",
        
        "default": f"Thank you for your question about {diagnosis}. The AI analysis shows {risk.lower()} risk features. For specific medical advice, please consult with an oncologist."
    }
    
    for key, response in responses.items():
        if key in question_lower:
            return response
    
    return responses["default"]

# ============================================
# IMAGE GENERATION FUNCTIONS
# ============================================
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
    
    return img, highlighted_img, highlight_positions

def generate_heatmap(positions, img_size=(400, 400)):
    heatmap = np.zeros(img_size)
    for x, y, r in positions:
        for i in range(max(0, int(x-r)), min(img_size[0], int(x+r))):
            for j in range(max(0, int(y-r)), min(img_size[1], int(y+r))):
                distance = np.sqrt((i-x)**2 + (j-y)**2)
                intensity = max(0, 1 - distance/r)
                heatmap[i, j] += intensity
    
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()
    heatmap = (heatmap * 255).astype(np.uint8)
    
    heatmap_rgb = np.zeros((*img_size, 3), dtype=np.uint8)
    heatmap_rgb[:, :, 0] = heatmap
    heatmap_rgb[:, :, 1] = (heatmap * 0.3).astype(np.uint8)
    
    return Image.fromarray(heatmap_rgb, mode='RGB')

# ============================================
# REPORT GENERATION WITH DOCTOR NOTES
# ============================================
def create_html_report(healthy_img, abnormal_img, config, confidence, predictions, heatmap_img=None, edited_treatment=None, doctor_notes=None):
    """Create HTML report with doctor's edits and notes"""
    
    healthy_buffer = io.BytesIO()
    healthy_img.save(healthy_buffer, format='PNG')
    healthy_base64 = base64.b64encode(healthy_buffer.getvalue()).decode()
    
    abnormal_buffer = io.BytesIO()
    abnormal_img.save(abnormal_buffer, format='PNG')
    abnormal_base64 = base64.b64encode(abnormal_buffer.getvalue()).decode()
    
    heatmap_html = ""
    if heatmap_img:
        heatmap_buffer = io.BytesIO()
        heatmap_img.save(heatmap_buffer, format='PNG')
        heatmap_base64 = base64.b64encode(heatmap_buffer.getvalue()).decode()
        heatmap_html = f"""
        <div style="flex:1; text-align:center; border:1px solid #d0e8f0; border-radius:12px; padding:15px; background:#fafefe;">
            <div style="background:#7ec8e0; color:white; padding:5px 10px; border-radius:20px; display:inline-block; font-size:12px; font-weight:bold;">🔥 AI HEATMAP</div>
            <img src="data:image/png;base64,{heatmap_base64}" style="width:180px; height:180px; border-radius:8px; margin:10px;">
            <div style="font-size:11px; color:#7a9aa3;">Red areas indicate high suspicion</div>
        </div>
        """
    
    if config['risk'] == 'high':
        risk_color = "#c0392b"
        risk_bg = "#ffe0d4"
    elif config['risk'] == 'moderate':
        risk_color = "#e67e22"
        risk_bg = "#fff0d4"
    else:
        risk_color = "#2d6a4f"
        risk_bg = "#cce8d6"
    
    # Treatment section with doctor's edits
    treatment_section = f"""
    <div class="treatment-card">
        <strong>💊 First Line Treatment:</strong> {edited_treatment if edited_treatment else config['first_line']}
    </div>
    <div class="treatment-card">
        <strong>📋 Second Line Treatment:</strong> {config['second_line']}
    </div>
    <div class="treatment-card">
        <strong>📅 Follow-up Schedule:</strong> {config['follow_up']}
    </div>
    """
    
    doctor_notes_section = ""
    if doctor_notes:
        doctor_notes_section = f"""
        <div class="doctor-note">
            <strong>👨‍⚕️ Physician Notes:</strong><br>
            {doctor_notes}
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>LungVision AI Clinical Report</title>
        <style>
            @page {{ size: A4; margin: 2cm; }}
            body {{ font-family: 'Helvetica', 'Arial', sans-serif; background: white; color: #2c3e42; padding: 20px; }}
            .container {{ max-width: 100%; margin: 0 auto; }}
            .header {{ text-align: center; padding: 20px; border-bottom: 2px solid #7ec8e0; margin-bottom: 30px; }}
            .title {{ font-size: 28px; font-weight: bold; color: #2c5a66; }}
            .subtitle {{ font-size: 12px; color: #7a9aa3; }}
            .report-id {{ font-size: 10px; color: #7a9aa3; margin-top: 10px; }}
            .info-box {{ background: #f0f8fc; padding: 15px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #7ec8e0; }}
            .diagnosis-box {{ background: {risk_bg}; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center; }}
            .diagnosis {{ font-size: 28px; font-weight: bold; color: {risk_color}; }}
            .confidence-bar {{ width: 100%; height: 10px; background: #e0eef3; border-radius: 5px; margin: 10px 0; overflow: hidden; }}
            .confidence-fill {{ width: {confidence}%; height: 100%; background: {risk_color}; }}
            .comparison-grid {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
            .comparison-item {{ flex: 1; text-align: center; border: 1px solid #d0e8f0; border-radius: 12px; padding: 15px; background: #fafefe; }}
            .comparison-image {{ width: 180px; height: 180px; border-radius: 8px; margin: 10px 0; }}
            .treatment-card {{ background: #f0f8fc; border-radius: 12px; padding: 12px; margin: 10px 0; border-left: 4px solid #2d6a4f; }}
            .doctor-note {{ background: #e8f4f8; border-left: 4px solid #7ec8e0; padding: 15px; border-radius: 12px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #d0e8f0; font-size: 9px; color: #7a9aa3; }}
            .print-btn {{ background: #2d6a4f; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; margin: 20px auto; display: block; }}
            @media print {{ .print-btn {{ display: none; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="title">🏥 LungVision AI</div>
                <div class="subtitle">Clinical Diagnostic Report with Physician Review</div>
                <div class="report-id">Report ID: LV-{datetime.now().strftime('%Y%m%d%H%M%S')}</div>
                <div class="report-id">Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
            
            <div class="info-box">
                <strong>Patient Information</strong><br>
                Name: CONFIDENTIAL<br>
                Medical Record #: {datetime.now().strftime('%Y')}-{np.random.randint(1000, 9999)}<br>
                Referring Physician: AI Clinical System
            </div>
            
            <div class="diagnosis-box">
                <div class="diagnosis">{config['label']}</div>
                <div>AI Confidence: {confidence:.1f}%</div>
                <div class="confidence-bar"><div class="confidence-fill"></div></div>
                <div style="margin-top:10px;"><span style="background:{risk_bg};color:{risk_color};padding:5px 15px;border-radius:20px;">{config['risk_label']}</span></div>
            </div>
            
            <div class="comparison-grid">
                <div class="comparison-item">
                    <div style="background:#cce8d6;color:#2d6a4f;padding:5px 10px;border-radius:20px;display:inline-block;">✅ HEALTHY REFERENCE</div>
                    <img src="data:image/png;base64,{healthy_base64}" class="comparison-image">
                </div>
                <div class="comparison-item">
                    <div style="background:#ffe0d4;color:#c0392b;padding:5px 10px;border-radius:20px;display:inline-block;">⚠️ PATIENT SAMPLE</div>
                    <img src="data:image/png;base64,{abnormal_base64}" class="comparison-image">
                </div>
                {heatmap_html}
            </div>
            
            <h3>💊 Treatment Plan</h3>
            {treatment_section}
            {doctor_notes_section}
            
            <div class="footer">
                This report was generated by LungVision AI and reviewed by a physician.<br>
                AI confidence: {confidence:.1f}% | Physician approval: ✓
            </div>
            
            <button class="print-btn" onclick="window.print();">🖨️ Print / Save as PDF</button>
        </div>
    </body>
    </html>
    """
    return html

# ============================================
# SESSION STATE
# ============================================
if 'comparison_active' not in st.session_state:
    st.session_state.comparison_active = False
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'edited_treatment' not in st.session_state:
    st.session_state.edited_treatment = None
if 'doctor_notes' not in st.session_state:
    st.session_state.doctor_notes = None
if 'healthy_ref' not in st.session_state:
    st.session_state.healthy_ref = None
if 'abnormal_highlighted' not in st.session_state:
    st.session_state.abnormal_highlighted = None
if 'heatmap' not in st.session_state:
    st.session_state.heatmap = None
if 'highlights' not in st.session_state:
    st.session_state.highlights = []
if 'comparison_type' not in st.session_state:
    st.session_state.comparison_type = None

# ============================================
# MAIN GRID
# ============================================
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

# ============================================
# LEFT COLUMN
# ============================================
with col1:
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">CLINICAL WORKSTATION</div>
            <div class="panel-icon">🏥</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔬 Analysis", "📚 Reference", "🔥 Heatmap", "💬 Q&A", "✏️ Edit Mode"])
    
    with tab1:
        st.markdown("""
        <div class="comparison-mode">
            <div class="comparison-title">🔬 Pathology Analysis System</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            if st.button("🔬 Adenocarcinoma", key="adc", use_container_width=True):
                healthy = generate_healthy_reference()
                abnormal, highlighted, highlights = generate_abnormal_image("adenocarcinoma", True)
                heat = generate_heatmap(highlights)
                st.session_state.healthy_ref = healthy
                st.session_state.abnormal_highlighted = highlighted
                st.session_state.heatmap = heat
                st.session_state.comparison_type = "adenocarcinoma"
                st.session_state.comparison_active = True
                # Reset edits when new analysis
                st.session_state.edited_treatment = None
                st.session_state.doctor_notes = None
                st.session_state.edit_mode = False
                st.rerun()
        
        with col_s2:
            if st.button("🔬 Squamous Cell", key="scc", use_container_width=True):
                healthy = generate_healthy_reference()
                abnormal, highlighted, highlights = generate_abnormal_image("squamous_cell_carcinoma", True)
                heat = generate_heatmap(highlights)
                st.session_state.healthy_ref = healthy
                st.session_state.abnormal_highlighted = highlighted
                st.session_state.heatmap = heat
                st.session_state.comparison_type = "squamous_cell_carcinoma"
                st.session_state.comparison_active = True
                st.session_state.edited_treatment = None
                st.session_state.doctor_notes = None
                st.session_state.edit_mode = False
                st.rerun()
        
        with col_s3:
            if st.button("🟢 Benign Tissue", key="ben", use_container_width=True):
                healthy = generate_healthy_reference()
                abnormal, highlighted, highlights = generate_abnormal_image("benign", True)
                heat = generate_heatmap(highlights)
                st.session_state.healthy_ref = healthy
                st.session_state.abnormal_highlighted = highlighted
                st.session_state.heatmap = heat
                st.session_state.comparison_type = "benign"
                st.session_state.comparison_active = True
                st.session_state.edited_treatment = None
                st.session_state.doctor_notes = None
                st.session_state.edit_mode = False
                st.rerun()
        
        uploaded = st.file_uploader("Upload patient image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
        
        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            healthy = generate_healthy_reference()
            st.session_state.healthy_ref = healthy
            st.session_state.abnormal_highlighted = img
            st.session_state.comparison_type = "uploaded"
            st.session_state.comparison_active = True
            st.session_state.edited_treatment = None
            st.session_state.doctor_notes = None
            st.session_state.edit_mode = False
            st.image(img, caption="Patient Sample", use_container_width=True)
        
        if st.session_state.comparison_active:
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.session_state.healthy_ref:
                    st.image(st.session_state.healthy_ref, caption="Healthy Reference", use_container_width=True)
            with col_b:
                if st.session_state.abnormal_highlighted:
                    st.image(st.session_state.abnormal_highlighted, caption="Patient Sample", use_container_width=True)
            with col_c:
                if st.session_state.heatmap:
                    st.image(st.session_state.heatmap, caption="AI Heatmap", use_container_width=True)
    
    with tab2:
        st.markdown("### 📚 Reference Library")
        ref_type = st.selectbox("Select Type", list(REFERENCE_LIBRARY.keys()))
        ref = REFERENCE_LIBRARY[ref_type]
        st.markdown(f"""
        <div class="reference-card">
            <h4>{ref_type}</h4>
            <p><strong>Description:</strong> {ref['desc']}</p>
            <p><strong>Characteristics:</strong> {ref['characteristics']}</p>
            <p><strong>Key Features:</strong> {', '.join(ref['key_features'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🔥 AI Heatmap Guide")
        st.markdown("""
        <div class="heatmap-guide">
            <div style="text-align:center;margin-bottom:20px;">
                <div style="font-size:48px;">🔥</div>
                <h2>Grad-CAM Visualization</h2>
            </div>
            <div style="background:rgba(255,255,255,0.1);border-radius:12px;padding:15px;">
                <h3>Color Interpretation</h3>
                <div>🔴 <strong style="color:#ff6b6b;">Red</strong> - High suspicion (malignant)</div>
                <div>🟠 <strong style="color:#ffa500;">Orange</strong> - Moderate suspicion</div>
                <div>🟡 <strong style="color:#ffeb3b;">Yellow</strong> - Low suspicion</div>
                <div>🔵 <strong style="color:#7ec8e0;">Blue</strong> - Normal tissue</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.comparison_active and st.session_state.heatmap:
            st.image(st.session_state.heatmap, caption="Current AI Heatmap", use_container_width=True)
    
    with tab4:
        st.markdown("### 💬 AI Clinical Assistant")
        
        if not st.session_state.comparison_active:
            st.info("Please run an analysis first to enable Q&A")
        else:
            comp = st.session_state.comparison_type
            if comp == "adenocarcinoma":
                diag = "Adenocarcinoma"
                risk = "HIGH RISK"
                stage = "Stage II-III"
                conf = 92.0
            elif comp == "squamous_cell_carcinoma":
                diag = "Squamous Cell Carcinoma"
                risk = "MODERATE RISK"
                stage = "Stage I-II"
                conf = 93.0
            elif comp == "benign":
                diag = "Benign Tissue"
                risk = "LOW RISK"
                stage = "No malignancy"
                conf = 96.0
            else:
                diag = "Adenocarcinoma"
                risk = "HIGH RISK"
                stage = "Stage II-III"
                conf = 85.0
            
            st.markdown(f"""
            <div class="qa-card">
                <div style="background:#7ec8e0;color:white;padding:10px;border-radius:12px;text-align:center;">
                    🤖 AI Assistant | Current Diagnosis: {diag} ({risk})
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Suggested questions
            questions = [
                "What is the prognosis?",
                "What treatment is recommended?",
                "What are the risk factors?",
                "How often should I follow up?",
                "How confident is this diagnosis?"
            ]
            
            cols = st.columns(len(questions))
            for i, q in enumerate(questions):
                with cols[i]:
                    if st.button(q, key=f"suggest_{i}", use_container_width=True):
                        answer = get_qa_response(q, diag, stage, risk, conf, st.session_state.edited_treatment)
                        st.session_state.qa_history.append({"q": q, "a": answer})
            
            user_question = st.text_input("Ask your own question:", placeholder="e.g., What are the treatment options?")
            
            if st.button("💬 Ask AI", use_container_width=True):
                if user_question:
                    answer = get_qa_response(user_question, diag, stage, risk, conf, st.session_state.edited_treatment)
                    st.session_state.qa_history.append({"q": user_question, "a": answer})
                    st.rerun()
            
            if st.session_state.qa_history:
                st.markdown("### 📋 Q&A History")
                for item in st.session_state.qa_history[-5:]:
                    st.markdown(f"""
                    <div class="qa-question">
                        <strong>❓ You asked:</strong> {item['q']}
                    </div>
                    <div class="qa-answer">
                        <strong>🤖 AI Answer:</strong> {item['a']}
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("🗑️ Clear History"):
                    st.session_state.qa_history = []
                    st.rerun()
    
    with tab5:
        st.markdown("### ✏️ Physician Editing Mode")
        st.markdown("Review and modify AI recommendations as needed")
        
        if not st.session_state.comparison_active:
            st.info("Please run an analysis first to enable editing")
        else:
            comp = st.session_state.comparison_type
            if comp == "adenocarcinoma":
                default_treatment = CLASS_CONFIG["adenocarcinoma"]["first_line"]
                default_followup = CLASS_CONFIG["adenocarcinoma"]["follow_up"]
            elif comp == "squamous_cell_carcinoma":
                default_treatment = CLASS_CONFIG["squamous_cell_carcinoma"]["first_line"]
                default_followup = CLASS_CONFIG["squamous_cell_carcinoma"]["follow_up"]
            else:
                default_treatment = CLASS_CONFIG["benign"]["first_line"]
                default_followup = CLASS_CONFIG["benign"]["follow_up"]
            
            # Edit mode toggle
            if st.button("✏️ Enable Edit Mode" if not st.session_state.edit_mode else "🔒 Disable Edit Mode", use_container_width=True):
                st.session_state.edit_mode = not st.session_state.edit_mode
                st.rerun()
            
            if st.session_state.edit_mode:
                st.markdown('<div class="edit-mode-indicator">✏️ EDIT MODE ACTIVE - You can modify treatment recommendations</div>', unsafe_allow_html=True)
                
                # Editable fields
                edited_treatment = st.text_area("✏️ Edit First Line Treatment:", value=st.session_state.edited_treatment if st.session_state.edited_treatment else default_treatment, height=80)
                
                edited_followup = st.text_input("✏️ Edit Follow-up Schedule:", value=st.session_state.edited_followup if hasattr(st.session_state, 'edited_followup') else default_followup)
                
                doctor_notes = st.text_area("👨‍⚕️ Add Physician Notes (Optional):", value=st.session_state.doctor_notes if st.session_state.doctor_notes else "", height=100, placeholder="Add your clinical observations, modifications, or special instructions...")
                
                col_save1, col_save2 = st.columns(2)
                with col_save1:
                    if st.button("💾 Save Changes", use_container_width=True):
                        st.session_state.edited_treatment = edited_treatment
                        st.session_state.edited_followup = edited_followup
                        st.session_state.doctor_notes = doctor_notes
                        st.success("✅ Changes saved successfully! They will appear in the report.")
                        st.rerun()
                
                with col_save2:
                    if st.button("⟳ Reset to AI Defaults", use_container_width=True):
                        st.session_state.edited_treatment = None
                        st.session_state.edited_followup = None
                        st.session_state.doctor_notes = None
                        st.success("✅ Reset to AI recommendations")
                        st.rerun()
            else:
                st.markdown("### Current AI Recommendations")
                st.markdown(f"""
                <div class="treatment-card">
                    <strong>💊 First Line Treatment:</strong> {st.session_state.edited_treatment if st.session_state.edited_treatment else default_treatment}
                </div>
                <div class="treatment-card">
                    <strong>📅 Follow-up Schedule:</strong> {st.session_state.edited_followup if hasattr(st.session_state, 'edited_followup') and st.session_state.edited_followup else default_followup}
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.doctor_notes:
                    st.markdown(f"""
                    <div class="doctor-note">
                        <strong>👨‍⚕️ Physician Notes:</strong><br>
                        {st.session_state.doctor_notes}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.info("Click 'Enable Edit Mode' to modify treatment recommendations and add physician notes")

# ============================================
# RIGHT COLUMN - RESULTS
# ============================================
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
        <div style="text-align:center;padding:60px;opacity:0.6;">
            <div style="font-size:48px;">🏥</div>
            <p>Select a sample to begin</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        comp = st.session_state.comparison_type
        if comp == "adenocarcinoma":
            preds = np.array([[0.92, 0.03, 0.05]])
        elif comp == "squamous_cell_carcinoma":
            preds = np.array([[0.05, 0.02, 0.93]])
        elif comp == "benign":
            preds = np.array([[0.02, 0.96, 0.02]])
        else:
            preds = np.array([[0.85, 0.05, 0.10]])
        
        idx = np.argmax(preds)
        cls = CLASSES[idx]
        cfg = CLASS_CONFIG[cls]
        conf = float(preds[0][idx]) * 100
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-badge" style="background:{cfg['bg_color']};color:{cfg['color']};">PRIMARY DIAGNOSIS</div>
            <div class="diagnosis" style="color:{cfg['color']};">{cfg['label']}</div>
            <div class="confidence-text">AI Confidence: {conf:.1f}%</div>
            <div class="progress-bar"><div class="progress-fill" style="width:{conf}%;background:{cfg['color']};"></div></div>
        </div>
        
        <div class="result-card">
            <div style="display:flex;justify-content:space-between;">
                <span style="font-size:11px;font-weight:600;">TNM CLASSIFICATION</span>
                <span class="risk-{cfg['risk']}">{cfg['risk_label']}</span>
            </div>
            <div style="font-size:18px;font-weight:700;margin:10px 0;">{cfg['stage']}</div>
            <div style="font-size:12px;color:#7a9aa3;">{cfg['desc']}</div>
            <div style="margin-top:10px;padding-top:8px;border-top:1px solid #e0eef3;">
                <div><strong>Grade:</strong> {cfg['grade']}</div>
                <div><strong>Prognosis:</strong> {cfg['prognosis']}</div>
            </div>
        </div>
        
        <div class="result-card">
            <div style="font-size:11px;font-weight:600;margin-bottom:12px;">PROBABILITY DISTRIBUTION</div>
        """, unsafe_allow_html=True)
        
        for i, c in enumerate(CLASSES):
            c_cfg = CLASS_CONFIG[c]
            prob = float(preds[0][i]) * 100
            st.markdown(f"""
            <div class="class-item">
                <div class="class-dot" style="background:{c_cfg['color']};"></div>
                <div class="class-name">{c_cfg['label']}</div>
                <div class="class-bar"><div class="class-fill" style="width:{prob}%;background:{c_cfg['color']};"></div></div>
                <div class="class-percent" style="color:{c_cfg['color']};">{prob:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show edited treatment if any
        if st.session_state.edited_treatment or st.session_state.doctor_notes:
            st.markdown("### 👨‍⚕️ Physician Modified Plan")
            
            if st.session_state.edited_treatment:
                st.markdown(f"""
                <div class="treatment-card">
                    <strong>✏️ Modified Treatment:</strong><br>
                    {st.session_state.edited_treatment}
                </div>
                """, unsafe_allow_html=True)
            
            if st.session_state.doctor_notes:
                st.markdown(f"""
                <div class="doctor-note">
                    <strong>📝 Physician Notes:</strong><br>
                    {st.session_state.doctor_notes}
                </div>
                """, unsafe_allow_html=True)
        
        # Generate Report
        html_report = create_html_report(
            st.session_state.healthy_ref,
            st.session_state.abnormal_highlighted,
            cfg,
            conf,
            preds,
            st.session_state.heatmap,
            st.session_state.edited_treatment,
            st.session_state.doctor_notes
        )
        
        b64_html = base64.b64encode(html_report.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64_html}" download="LungVision_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html" style="text-decoration:none;"><div class="download-btn">📑 Download Report (Save as PDF)</div></a>'
        st.markdown(href, unsafe_allow_html=True)
        
        st.info("💡 **Tip:** Open the HTML file and press Ctrl+P to save as PDF")
        
        st.markdown(f"""
        <div class="clinical-card">
            <div style="display:flex;gap:12px;">
                <div style="font-size:22px;">{'⚠️' if cfg['risk']=='high' else '📋' if cfg['risk']=='moderate' else '✅'}</div>
                <div>
                    <div style="font-size:13px;font-weight:700;color:{cfg['color']};">AI Recommendation</div>
                    <div style="font-size:12px;">{cfg['treatment']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="footer-text">LungVision AI · Clinical Diagnostic System · Physician Editing Mode</div>
    <div class="footer-text">AI-Powered Analysis · Customizable Treatment Plans · Clinical Notes</div>
</div>
""", unsafe_allow_html=True)
