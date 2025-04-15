# Use official Python image as base
FROM python:3.9-slim


# Create a non-root user with UID 1000
RUN useradd -m -u 1000 user

# Set home directory and PATH
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Switch to the new user
USER user

# Set working directory
WORKDIR $HOME/app

# Upgrade pip while running as user
RUN pip install --user --no-cache-dir --upgrade pip

# Copy application files with correct ownership
COPY --chown=user requirements.txt $HOME/app

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy and run model preparation script
COPY --chown=user prepare.py .
RUN python3 prepare.py

# Ensure correct PATH (no more `/root/.local/bin`)
ENV PATH="/home/user/.local/bin:$PATH"

# Copy application file
COPY --chown=user app.py .

COPY --chown=user static /home/user/app/static

# Expose FastAPI default port
EXPOSE 7860

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]