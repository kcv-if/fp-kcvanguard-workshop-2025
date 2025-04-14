import os
import sys
import io
import numpy as np
import pickle
import yaml
import streamlit as st
import torch
import onnxruntime as ort
from PIL import Image

sys.path.append(os.path.join('stylegan2-ada-pytorch'))
torch.autograd.set_grad_enabled(False)
torch.backends.cudnn.benchmark = True

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

DTYPE_MAPPING = {
    'u8': np.uint8,
    'f32': np.float32,
    'f64': np.float64,
    'i32': np.int32,
    'i64': np.int64,
    'str': str
}

configs = {}

for fname in os.listdir(os.path.join('configs')):
    fpath = os.path.join('configs', fname)
    with open(fpath, 'r') as file:
        config = yaml.safe_load(file)
        model_path = os.path.join('models', config['file'])
        if not 'stylegan2' in fname:
            config['session'] = ort.InferenceSession(model_path)
        else:
            with open(model_path, 'rb') as f:
                config['session'] = pickle.load(f)['G_ema'].to(DEVICE)
        configs[config['name']] = config

model = next(iter(configs))

def generate() -> None:
    config = configs[model]

    z = np.random.randn(*config['noise_shape']).astype(np.float32)

    if model != 'StyleGAN2':
        inference_args = {
            config['session'].get_inputs()[0].name: z,
            **{ name: np.array(input['value'], dtype=DTYPE_MAPPING[input['dtype']]) for name, input in config['other_inputs'].items() }
        }
        image = config['session'].run(None, inference_args)[0]
    else:
        with torch.no_grad():
            inference_args = {
                'z': torch.tensor(z, device=DEVICE),
                'c': torch.zeros(1, config['session'].c_dim, device=DEVICE),
                'truncation_psi': 0.7,
                'noise_mode': 'const'
            }
            image = config['session'](**inference_args).cpu().numpy()

    image = image.squeeze(0)
    image = (image * 0.5 + 0.5) * 255
    image = image.astype(np.uint8)
    if len(image.shape) < 3:
        image = image.reshape((3, 128, 128))
    image = np.transpose(image, (1, 2, 0))
    image = Image.fromarray(image, 'RGB')

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    st.session_state.image = buffer

if not 'image' in st.session_state:
    generate()

st.title('BatikGAN')
st.text('By fans berat ko Andrian')
model = st.selectbox('Model', list(configs.keys()))
st.image(st.session_state.image, use_container_width=True)
st.button('Generate', on_click=generate, use_container_width=True)
st.download_button('Download', data=st.session_state.image, file_name='output.png',
                   mime='data/png', use_container_width=True)
st.text('')
st.markdown(f'''
<p style="text-align: center;">Check out our other deployments</p>
<div style="display: flex; align-items: center; justify-content: center; gap: 16px;">
    <a href="https://riciii7-fastapi-batik-gan.hf.space">
        <img src="https://cdn.simpleicons.org/fastapi" width="40" height="40" />
    </a>
    <a href="https://cthleen-batik-gan.hf.space"> 
        <img src="https://cdn.simpleicons.org/gradio" width="40" height="40" />
    </a>
    <a href="https://batik-gan-fe.vercel.app">
        <img src="https://cdn.simpleicons.org/nextdotjs/000000/ffffff" width="40" height="40" />
    </a>
</div>
''', unsafe_allow_html=True)