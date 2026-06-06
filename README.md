# Lung Cancer Classification🤖

Detecting lung cancer has never been this visual — or this smart!  

A deep learning-powered image classifier that identifies different types of lung tissue from histopathological images. Whether it's **Adenocarcinoma**, **Squamous Cell Carcinoma**, or **Benign tissue**, this model sees it clearly.

---

## 🚀 Features

- Classifies lung tissue images into **3 categories** with high accuracy
- Uses **CNN (Convolutional Neural Networks)** for image analysis
- Includes **data augmentation** for robust performance
- Built with **TensorFlow & Keras**
- Ready for **research, educational, or clinical prototyping**  

---

## 📊 Dataset

I used the [Lung Cancer Histopathological Images Dataset](https://www.kaggle.com/datasets/rm1000/lung-cancer-histopathological-images/data?select=squamous_cell_carcinoma), which contains:

- **Adenocarcinoma** – malignant glandular tissue  
- **Squamous Cell Carcinoma** – malignant squamous cells  
- **Benign** – normal tissue  

Images are organized in folders by class.

🚀 **Try the Streamlit App here:** 
https://lung-cancer-detection-gbnmxwzd8adqbbg27qfwqs.streamlit.app/
---

## ⚡ Training

- **Epochs:** 30  
- **Batch Size:** 32  
- **Data Augmentation:** rotation, shift, shear, zoom  
- **Callbacks:** EarlyStopping, ReduceLROnPlateau, ModelCheckpoint  

The model was trained on **224x224 RGB histopathological images** from the Lung Cancer Dataset, achieving high accuracy in classifying:

1. Adenocarcinoma  
2. Squamous Cell Carcinoma  
3. Benign tissue  

---

## 📈 Training Results

After training for 30 epochs, the model achieved **excellent performance**:

- **Test Accuracy:** 97% 
- **Test Loss:** 0.0752  
- **Training Accuracy (final epoch):** 98.3%  
- **Training Loss (final epoch):** 0.0623  

These results show that the model can reliably classify lung tissue images into **Adenocarcinoma, Squamous Cell Carcinoma, and Benign tissue**.
 
