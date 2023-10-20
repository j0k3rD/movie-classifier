import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np

st.title("Clasificador de Películas")

# Carga del modelo previamente entrenado
model = keras.models.load_model("films_classifier.h5")

# Clases de películas
classes = ["El Padrino", "El señor de los anillos: El retorno del rey", "Titanic", "El caballero oscuro"]  # Reemplaza con las clases reales

# Sube una imagen para clasificar
uploaded_image = st.file_uploader("Sube una imagen de película", type=["jpg", "png"])
