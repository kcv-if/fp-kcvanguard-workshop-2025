from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from utils import load_model_pkl, generate_image_from_pkl, generate_image_from_onnx
from random import randint

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=False, # gapake creds
)
styleganv2 = load_model_pkl("styleganv2.pkl")

@app.get("/")
def root():
    return {"message": "Welcome to the StyleGAN API!"}

@app.get("/ping")
def ping():
    return {"status": "pong"}

@app.get("/generate/stylegan")
def generate_stylegan_onnx():
    image_stream = generate_image_from_onnx("stylegan.onnx", model='stylegan')
    return StreamingResponse(image_stream, media_type="image/png")

@app.get("/generate/styleganv2")
def generate_styleganv2(seed: int = Query(None)):
    if seed is None:
        seed = randint(0, 2**32 - 1)
    image_stream = generate_image_from_pkl(styleganv2, seed=seed, trunc=1)
    return StreamingResponse(image_stream, media_type="image/png")

@app.get("/generate/progan")
def generate_progan():
    image_stream = generate_image_from_onnx("progan.onnx", model='progan')
    return StreamingResponse(image_stream, media_type="image/png")

@app.get("/generate/dcgan")
def generate_dcgan():
    image_stream = generate_image_from_onnx("batik_dcgan.onnx", model='dcgan')
    return StreamingResponse(image_stream, media_type="image/png")

@app.get("/generate/vanillagan")
def generate_vanillagan():
    image_stream = generate_image_from_onnx("vanillagan.onnx", model='vanillagan')
    return StreamingResponse(image_stream, media_type="image/png")
