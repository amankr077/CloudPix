from flask import Flask, request, redirect, url_for, render_template, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
CORS(app)


client = MongoClient('mongodb://localhost:27017/')  # Replace with MongoDB Atlas for cloud db
db = client['image_database']
image_collection = db['images']

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')   


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"    #uuid4 duplicate fileName hone se bachata hai
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)   #path create karega , upload image wale folder tek
    
    file.save(file_path)

    image_url = url_for('static', filename=f'images/{unique_filename}', _external=True)  #url creaation
    image_collection.insert_one({'image_url': image_url})   #mongoDb mai insert karega

    return redirect(url_for('index'))


@app.route('/images', methods=['GET'])     #jitne bhi images hai sabko return karga
def get_images():
    images = image_collection.find()
    image_urls = [image['image_url'] for image in images]
    return jsonify(image_urls)        #json mai convert kareke sariii ki sari apps se compatible hojeyga

if __name__ == '__main__':      #
    if not os.path.exists(UPLOAD_FOLDER):   #in case folder nahi bana hua hai toh bana dega
        os.makedirs(UPLOAD_FOLDER)    
    app.run(debug=True)
