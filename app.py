from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from steganography import SteganographyTool

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/encode', methods=['POST'])
def encode():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    message = request.form.get('message', '')
    
    # If no selected file
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Secure filename and create input/output paths
        filename = secure_filename(file.filename)
        input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'encoded_{filename}')
        
        # Save the uploaded file
        file.save(input_filepath)
        
        try:
            # Encode the message
            SteganographyTool.encode_image(input_filepath, message, output_filepath)
            
            # Remove the original uploaded file
            os.remove(input_filepath)
            
            return jsonify({
                "message": "Image encoded successfully",
                "output_image": output_filepath
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/decode', methods=['POST'])
def decode():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    
    # If no selected file
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Secure filename and create input path
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        file.save(filepath)
        
        try:
            # Decode the message
            message = SteganographyTool.decode_image(filepath)
            
            # Remove the uploaded file
            os.remove(filepath)
            
            return jsonify({
                "message": "Image decoded successfully",
                "decoded_text": message
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)