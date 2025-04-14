import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLEGAN2_DIR = os.path.join(BASE_DIR, "stylegan2")
MODEL_PATH = os.path.join(BASE_DIR, "model", "network-snapshot-000560.pkl")

sys.path.append(STYLEGAN2_DIR)

import torch
import legacy
import dnnlib
import numpy as np
from PIL import Image

torch.autograd.set_grad_enabled(False)
torch.backends.cudnn.benchmark = True

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with dnnlib.util.open_url(MODEL_PATH) as f:
    G = legacy.load_network_pkl(f)['G_ema'].to(device)

def generate_stylegan2():
    seed = np.random.randint(0, 2**32)
    z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)).to(device)
    label = torch.zeros([1, G.c_dim], device=device)
    img = G(z, label, truncation_psi=1.0, noise_mode='const')
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

    pil_img = Image.fromarray(img[0].cpu().numpy(), 'RGB')
    resized = pil_img.resize((512, 512), Image.LANCZOS)
    return resized
