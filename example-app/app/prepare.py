from huggingface_hub import hf_hub_download
import shutil
import os

# Hugging Face model details
REPO_ID = "xcurv/kcv-vanguard-day3-cnn-card-classification"
MODEL_FILENAME = "model.h5"
LABEL_JSON = "class.json"

def download_file(repo_id, filename, dest_filename):
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)

    # Get the absolute path of the actual file (resolves symlinks)
    real_file_path = os.path.realpath(file_path)

    # Ensure the resolved file exists before copying
    if not os.path.exists(real_file_path):
        raise FileNotFoundError(f"Resolved file path does not exist: {real_file_path}")

    # Copy the actual file to the destination
    shutil.copy2(real_file_path, dest_filename)
    os.remove(real_file_path)

# Download model if not present
if not os.path.exists(MODEL_FILENAME):
    download_file(REPO_ID, MODEL_FILENAME, MODEL_FILENAME)

# Download label JSON if not present
if not os.path.exists(LABEL_JSON):
    download_file(REPO_ID, LABEL_JSON, LABEL_JSON)
