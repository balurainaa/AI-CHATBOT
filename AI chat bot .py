# AI Mental Health Chatbot with Brain Scan Analysis

# ----------------------------
# app.py – Streamlit Web Interface
# ----------------------------
import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from chatbot import chatbot_response

model = load_model('saved_model/brain_diagnosis_model.h5')
IMG_SIZE = 150

def predict_scan(img):
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    prediction = model.predict(img_array)[0][0]
    return 'Tumor Detected' if prediction > 0.5 else 'No Tumor Detected'

st.title("AI Mental Health Chatbot & Brain Scan Analysis")
menu = ["Chatbot", "Brain Scan Upload"]
choice = st.sidebar.selectbox("Select Mode", menu)

if choice == "Chatbot":
    st.header("Talk to AI Mental Health Assistant")
    user_input = st.text_input("Your Message")
    if st.button("Send"):
        response = chatbot_response(user_input)
        st.text_area("Chatbot:", value=response, height=100)

elif choice == "Brain Scan Upload":
    st.header("Upload MRI Brain Scan")
    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded MRI Scan', use_column_width=True)
        if st.button("Analyze"):
            result = predict_scan(image)
            st.success(f"Prediction: {result}")


# ----------------------------
# chatbot.py – Sentiment-Based Chatbot
# ----------------------------
from transformers import pipeline
import random

chatbot_pipe = pipeline('text-generation', model='gpt2')
sentiment_pipe = pipeline('sentiment-analysis')

responses = {
    "greeting": [
        "Hi there! How are you feeling today?",
        "Hello! I’m here to talk if you’d like to share anything."
    ],
    "sad": [
        "I'm sorry you're feeling that way. Do you want to talk about it?",
        "It's okay to feel sad. I'm here to listen."
    ],
    "happy": [
        "That’s great to hear! Keep smiling!",
        "Wonderful! Happiness is contagious."
    ]
}

def classify_sentiment(user_input):
    sentiment = sentiment_pipe(user_input)[0]
    return sentiment['label'], sentiment['score']

def chatbot_response(user_input):
    label, score = classify_sentiment(user_input)
    if label == 'NEGATIVE':
        return random.choice(responses['sad'])
    elif label == 'POSITIVE':
        return random.choice(responses['happy'])
    else:
        return random.choice(responses['greeting'])


# ----------------------------
# brain_scan_analysis.py – CNN Model Trainer
# ----------------------------
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

IMG_SIZE = 150
BATCH_SIZE = 32
EPOCHS = 10

data_dir = 'data/brain_mri'
train_dir = os.path.join(data_dir, 'train')
val_dir = os.path.join(data_dir, 'val')

def build_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    train_datagen = ImageDataGenerator(rescale=1./255)
    val_datagen = ImageDataGenerator(rescale=1./255)
    train_gen = train_datagen.flow_from_directory(train_dir, target_size=(IMG_SIZE, IMG_SIZE),
                                                  batch_size=BATCH_SIZE, class_mode='binary')
    val_gen = val_datagen.flow_from_directory(val_dir, target_size=(IMG_SIZE, IMG_SIZE),
                                              batch_size=BATCH_SIZE, class_mode='binary')
    model = build_model()
    model.fit(train_gen, epochs=EPOCHS, validation_data=val_gen)
    model.save('saved_model/brain_diagnosis_model.h5')

if __name__ == '__main__':
    train_model()