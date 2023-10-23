import streamlit as st
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np

st.title("Clasificador de Películas")

# Carga del modelo previamente entrenado
model = keras.models.load_model("films_classifier.h5")

# Clases de películas
classes = ["El Padrino", "El señor de los anillos: El retorno del rey", "Titanic", "El caballero oscuro"]  # Reemplaza con las clases reales

# Sube una imagen para clasificar
uploaded_image = st.file_uploader("Sube una imagen de película", type=["jpg", "png"])

if uploaded_image is not None:
    # Procesa la imagen subida para que coincida con el formato de entrada del modelo
    img = image.load_img(uploaded_image, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0 # Normaliza la imagen

    # Realiza la predicción
    predictions = model.predict(img)
    predicted_class_index = np.argmax(predictions)
    predicted_class = classes[predicted_class_index]
    confidence = predictions[0][predicted_class_index]

    # Muestra el resultado de la predicción
    st.image(uploaded_image, caption="Imagen subida", use_column_width=True)
    st.write(f"Clase predicha: {predicted_class}")
    st.write(f"Confianza: {confidence:.2f}")