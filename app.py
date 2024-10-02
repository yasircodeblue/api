from flask import Flask, jsonify, request

import pyautogui
import cloudinary
import cloudinary.uploader
import os
from datetime import datetime
import cv2
import numpy as np
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Cloudinary configuration
cloudinary.config(
    cloud_name = "dsfr7nm3a",
    api_key = "613432913295629",
    api_secret = "GRG6PWwNc2mlc2-6t-IQiKQiGv4"
)
@app.route('/take_screenshot', methods=['POST'])
def take_screenshot():
    print('called')
    try:
        # Get the cart width from the POST request
        data = request.json
        cart_width = data.get('cart_width', None)

        if cart_width is None:
            return jsonify({"success": False, "error": "Cart width not provided"}), 400

        # Define the region based on the cart width and screen dimensions
        screen_width, screen_height = pyautogui.size()

        # Assuming cart drawer is on the right side, adjust this if needed
        x = screen_width - cart_width  # Start x from the left of the cart drawer
        y = 0  # Start at the top of the screen
        width = cart_width
        height = screen_height  # Capture from top to bottom of the screen

        # Take screenshot of the specified region (x, y, width, height)
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        
        # Generate a unique filename
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Save screenshot temporarily
        screenshot.save(filename)
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(filename)
        
        # Delete the temporary file
        os.remove(filename)
        print(upload_result['secure_url'])
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

if __name__ == '__main__':
    app.run(debug=True)