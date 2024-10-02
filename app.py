from flask import Flask, jsonify, request
import pyautogui
import cloudinary
import cloudinary.uploader
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

# Cloudinary configuration
cloudinary.config(
    cloud_name="dsfr7nm3a",
    api_key="613432913295629",
    api_secret="GRG6PWwNc2mlc2-6t-IQiKQiGv4"
)

@app.route('/take_screenshot', methods=['POST'])
def take_screenshot():
    try:
        print('called')
        # Get the cart width from the POST request
        data = request.json
        cart_width = data.get('cart_width', None)

        if cart_width is None:
            return jsonify({"success": False, "error": "Cart width not provided"}), 400

        # Define the region based on the cart width and screen dimensions
        screen_width, screen_height = pyautogui.size()
        x = screen_width - cart_width
        y = 0
        width = cart_width
        height = screen_height

        # Take a screenshot of the specified region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Save screenshot to a BytesIO object
        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Upload to Cloudinary directly from memory
        upload_result = cloudinary.uploader.upload(img_byte_arr, resource_type="image")

        # Return the Cloudinary URL
        return jsonify({
            "success": True,
            "url": upload_result['secure_url']
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'res running'})

if __name__ == '__main__':
    app.run(debug=True)
