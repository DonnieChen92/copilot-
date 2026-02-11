from flask import Flask, request, jsonify
import joblib
import numpy as np
import logging
import time
import os

app = Flask(__name__)

# Set up monitoring (logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ml_service')

# Load model
# Check for model in possible locations (local dev vs docker)
possible_paths = ['ml_deployment/model.joblib', 'model.joblib']
model_path = None
for path in possible_paths:
    if os.path.exists(path):
        model_path = path
        break

if model_path:
    try:
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
    except Exception as e:
        logger.error(f"Failed to load model from {model_path}: {e}")
        model = None
else:
    logger.error("Model file not found in expected locations.")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()

    if not model:
        return jsonify({'error': 'Model not available'}), 500

    try:
        data = request.get_json(force=True)
        if 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400

        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)

        # Monitor latency
        latency = (time.time() - start_time) * 1000
        logger.info(f"Prediction: {prediction[0]}, Latency: {latency:.2f}ms")

        return jsonify({
            'prediction': int(prediction[0]),
            'latency_ms': latency
        })
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
