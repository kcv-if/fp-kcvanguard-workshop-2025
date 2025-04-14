import numpy as np
import onnxruntime as ort
from PIL import Image
import os
import math

def generate(input):
    model_file = f"{input}.onnx"
    model_path = os.path.join("model", model_file)

    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name

    if input == "dcgan" or input == "progan":
        noise = np.random.randn(1, 512, 1, 1).astype(np.float32)
    else:
        noise = np.random.randn(1, 512).astype(np.float32)

    output = session.run(None, {input_name: noise})[0]
    image = output.squeeze(0)
    image = (image * 0.5 + 0.5) * 255
    image = image.astype(np.uint8)
    if len(image.shape) < 3:
        image = image.reshape((3, 128, 128))
    image = np.transpose(image, (1, 2, 0))
    return Image.fromarray(image, "RGB").resize((512, 512), Image.LANCZOS)
