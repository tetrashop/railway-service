import os
import uuid
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from engine_3d import Engine3D

app = Flask(__name__)
engine = Engine3D(max_height=0.28, max_faces=12000)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return render_template("index.html")
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return render_template("index.html")

    filename = secure_filename(file.filename)
    temp_input = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
    file.save(temp_input)

    output_filename = f"{uuid.uuid4()}.obj"
    temp_output = os.path.join(UPLOAD_FOLDER, output_filename)

    try:
        success, result = engine.process(temp_input, temp_output)
        if not success:
            return render_template("index.html")
        return render_template("index.html")
    except Exception as e:
        return render_template("index.html")
    finally:
        if os.path.exists(temp_input):
            os.remove(temp_input)
        if os.path.exists(temp_output):
            os.remove(temp_output)

@app.route('/health', methods=['GET'])
def health():
    return render_template("index.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
