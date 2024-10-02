from flask import Flask, jsonify, request
import os
import sys
# Other imports...

app = Flask(__name__)
# CORS and Cloudinary configuration...

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'res running'})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'working'})

# Your existing screenshot route...

if __name__ == '__main__':
    app.run(debug=True)
