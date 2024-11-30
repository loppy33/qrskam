from flask import Flask, send_file, Blueprint
from telethon import TelegramClient
import asyncio
import qrcode
from PIL import Image
import os
import time

# API_ID = 24665137
# API_HASH = '00fc26b44fc4fb576533a0ccc2f56b1f'
# client = TelegramClient(f"sessions/main", API_ID, API_HASH)

app = Flask(__name__)
main = Blueprint('main', __name__)


# @main.route('/api/generate', methods=['GET'])
# async def generate():
#     # result = await generate_qr_code(client)

#     if result:
#         return send_file('app/static/qr_code.png', mimetype='image/png')
#     else:
#         return "Error generating QR code or session timed out", 500

app.register_blueprint(main)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
