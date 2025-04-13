from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from PIL import Image
import tensorflow as tf
import numpy as np
import json
import io

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = tf.keras.models.load_model("model.h5")

# Load class labels
with open("class.json", "r") as f:
    CLASS_NAMES = json.load(f)

# Preprocess image
def preprocess_image(image: Image.Image):
    image = image.convert("RGB")  # Convert to RGB
    image = image.resize((224, 224))  # Resize
    image = np.array(image, dtype=np.float32)  # Convert to NumPy array
    image = tf.keras.applications.efficientnet.preprocess_input(image)  # Apply EfficientNet preprocessing
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Prediction endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Preprocess image
    img = preprocess_image(image)
    
    # Model prediction
    predictions = model.predict(img)
    predicted_class_index = np.argmax(predictions)  # Get highest probability index
    predicted_class = CLASS_NAMES[str(predicted_class_index)]  # Get class label
    
    return {"prediction": predicted_class, "confidence": float(np.max(predictions))}

# Root endpoint to serve index.html
@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = Path("static/index.html")
    return index_path.read_text(encoding="utf-8")
