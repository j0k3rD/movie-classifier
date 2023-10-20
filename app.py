import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np

st.title("Clasificador de Películas")

# Carga del modelo previamente entrenado
model = keras.models.load_model("tu_modelo.h5")

# Clases de películas
classes = ["Clase1", "Clase2", "Clase3", "Clase4"]  # Reemplaza con las clases reales

# Sube una imagen para clasificar
uploaded_image = st.file_uploader("Sube una imagen de película", type=["jpg", "png"])

if uploaded_image is not None:
    # Realiza la clasificación
    image = tf.image.decode_image(uploaded_image.read(), channels=3)
    image = tf.image.resize(image, (100, 100))
    image = np.expand_dims(image, axis=0)
    result = model.predict(image)
    predicted_class = classes[np.argmax(result)]

    st.image(uploaded_image, caption="Imagen cargada", use_column_width=True)
    st.write(f"Predicción: {predicted_class}")
