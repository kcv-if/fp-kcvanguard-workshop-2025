# Use official Python image as base
FROM python:3.12-slim

# Create a non-root user with UID 1000
RUN useradd -m -u 1000 user

# Setup ENV 
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Switch to the new user
USER user

# Set working directory
WORKDIR $HOME/app

# Upgrade pip while running as user
RUN pip install --user --no-cache-dir --upgrade pip

# Explicitly install gunicorn and nltk first
RUN pip install --user --no-cache-dir gunicorn nltk

# Download NLTK data as the user - this is the key addition
RUN python -m nltk.downloader -d /home/user/nltk_data punkt stopwords

# Copy application files with correct ownership
COPY --chown=user requirements.txt $HOME/app/

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('all', download_dir='/home/user/nltk_data')"

# Copy application files
COPY --chown=user app.py $HOME/app/
COPY --chown=user config.py $HOME/app/
COPY --chown=user inference $HOME/app/inference/
COPY --chown=user model $HOME/app/model/ 
COPY --chown=user utils $HOME/app/model_utils/
COPY --chown=user processor $HOME/app/processor/ 
COPY --chown=user templates $HOME/app/templates/
COPY --chown=user static $HOME/app/static/

# Create temp directory for image uploads
RUN mkdir -p $HOME/app/temp

# Ensure correct PATH - Make it more explicit with the full path
ENV PATH="/home/user/.local/bin:$PATH"

# Verify gunicorn is installed and in PATH
RUN which gunicorn || echo "gunicorn not found in PATH"

# Expose Hugging Face Spaces default port (7860)
EXPOSE 7860

# Use absolute path to gunicorn or run through python
CMD ["/home/user/.local/bin/gunicorn", "--bind", "0.0.0.0:7860", "app:app"]