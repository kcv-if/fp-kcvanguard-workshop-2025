FROM python:3.10-slim

WORKDIR /app

# Salin file requirements
COPY requirements.txt .

# Salin model weight and infrastructure
COPY model.pt .

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies ke folder terpisah
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Salin source code
COPY main.py .

# Expose port for Streamlit
EXPOSE 8501

# Jalankan aplikasi Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]