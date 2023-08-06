import os
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = 'arn:aws:s3:::yic-heroku'
S3_REGION = 'us-east-2'

s3 = boto3.client('s3', region_name=S3_REGION)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
        return jsonify({'message': 'File uploaded successfully'}), 200
    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not set'}), 500

if __name__ == '__main__':
    app.run(debug=True)
