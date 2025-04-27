import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, jsonify, render_template
import logging
import config
from inference.predictions import MultimodalPredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app directly (standard pattern for Hugging Face Spaces)
app = Flask(__name__)

# Initialize predictor
predictor = MultimodalPredictor()

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html', features=config.FEATURE_NAMES)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Get tabular data from form
        tabular_data = {}
        for feature in config.FEATURE_NAMES:
            value = request.form.get(feature)
            if value is None:
                return jsonify({
                    'error': f'Missing required feature: {feature}'
                }), 400
            tabular_data[feature] = float(value)
        
        # Get uploaded image
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
            
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
            
        # Save image temporarily
        image_path = config.TEMP_IMAGE_PATH
        image_file.save(image_path)
        
        # Get text description
        text = request.form.get('title', '')
        if not text:
            return jsonify({'error': 'No title text provided'}), 400
        
        # Make prediction
        logger.info("Making prediction for property")
        predicted_price = predictor.predict(tabular_data, image_path, text)
        
        # Clean up temporary file
        if os.path.exists(image_path):
            os.remove(image_path)
            
        # Return prediction
        return jsonify({
            'predicted_price_millions': predicted_price,
            'currency': 'IDR'
        })
        
    except ValueError as e:
        logger.error(f"Value error in prediction: {str(e)}")
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)