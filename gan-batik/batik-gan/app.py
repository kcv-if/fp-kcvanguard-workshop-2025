import gradio as gr
from stylegan2_generator import generate_stylegan2
from generator import generate

def generate_image(model_name):
    if model_name == "GAN / VanillaGAN":
        return generate("vanillagan")
    elif model_name == "DCGAN":
        return generate("dcgan") 
    elif model_name == "ProGAN":
        return generate("progan")
    elif model_name == "StyleGAN":
        return generate("stylegan")
    elif model_name == "StyleGAN2":
        return generate_stylegan2()

model_options = ["GAN / VanillaGAN", "DCGAN", "ProGAN", "StyleGAN", "StyleGAN2"]

gr.Interface(
    fn=generate_image,
    inputs=gr.Dropdown(choices=model_options, label="Select Model"),
    outputs="image",
    title="BatikGAN",
    allow_flagging="never",
    submit_btn="Generate"
).launch()