from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import numpy as np
import streamlit as st
import tempfile

model = YOLO("model.pt")

st.title("🦸‍♂️ Superhero Predictions")
st.write("Upload an image and look what happen!!")

uploaded_file = st.file_uploader("📂 Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB") # Menghindari gambar RGBA 32 bit
    st.image(image, caption="🖼 Uploaded Image", use_column_width=True)

    # 👉 Simpan ke file temporer
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)  # simpan image ke path temporer
        temp_image_path = tmp.name

    # 👉 Pakai file path ini untuk prediksi
    results = model(temp_image_path, verbose=False)
    pred = results[0]

    st.write("🏆 Top Predictions:")
    st.write(f"{pred.names[pred.probs.top1]}")