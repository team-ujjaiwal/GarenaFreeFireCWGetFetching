from flask import Flask, jsonify
import requests
import threading
import httpx
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime

# Import protobufs
from GetWishListItems_pb2 import CSGetWishListItemsRes
from freefire_pb2 import Getliked, Player

app = Flask(__name__)

####################################
def Encrypt_ID(x):
    x = int(x)
    dec = [ '80','81','82','83','84','85','86','87','88','89','8a','8b','8c','8d','8e','8f',
            '90','91','92','93','94','95','96','97','98','99','9a','9b','9c','9d','9e','9f',
            'a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','aa','ab','ac','ad','ae','af',
            'b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','ba','bb','bc','bd','be','bf',
            'c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','ca','cb','cc','cd','ce','cf',
            'd0','d1','d2','d3','d4','d5','d6','d7','d8','d9','da','db','dc','dd','de','df',
            'e0','e1','e2','e3','e4','e5','e6','e7','e8','e9','ea','eb','ec','ed','ee','ef',
            'f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','fa','fb','fc','fd','fe','ff']
    xxx = [ '1','01','02','03','04','05','06','07','08','09','0a','0b','0c','0d','0e','0f',
            '10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f',
            '20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f',
            '30','31','32','33','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f',
            '40','41','42','43','44','45','46','47','48','49','4a','4b','4c','4d','4e','4f',
            '50','51','52','53','54','55','56','57','58','59','5a','5b','5c','5d','5e','5f',
            '60','61','62','63','64','65','66','67','68','69','6a','6b','6c','6d','6e','6f',
            '70','71','72','73','74','75','76','77','78','79','7a','7b','7c','7d','7e','7f']
    x = x / 128
    strx = int(x)
    y = (x - int(strx)) * 128
    stry = str(int(y))
    z = (y - int(stry)) * 128
    strz = str(int(z))
    n = (z - int(strz)) * 128
    strn = str(int(n))
    return dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def convert_timestamp(release_time):
    return datetime.utcfromtimestamp(release_time).strftime('%Y-%m-%d %H:%M:%S')

####################################
jwt_token = None

def get_jwt_token():
    global jwt_token
    url = "https://project-jwt-token-ujjaiwal.vercel.app/token?uid=3892341508&password=B78C0F8F5A2FDA93948C2966DE26DD7A0681EF6C2F09A5C10629E50C4D6341B4"
    try:
        response = httpx.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            if status in ["success", "live"]:
                jwt_token = data["token"]
                print("✅ JWT Token updated successfully.")
    except Exception as e:
        print(f"❌ Exception while fetching token: {e}")

def token_updater():
    while True:
        get_jwt_token()
        time.sleep(8 * 3600)

token_thread = threading.Thread(target=token_updater, daemon=True)
token_thread.start()
get_jwt_token()

####################################
@app.route('/wishlist/<int:uid>', methods=['GET'])
def get_wishlist(uid):
    global jwt_token
    if not jwt_token:
        return jsonify({"error": "JWT token is missing or invalid"}), 500

    encrypted_id = Encrypt_ID(uid)
    encrypted_api = encrypt_api(f"08{encrypted_id}1007")
    TARGET = bytes.fromhex(encrypted_api)

    url = "https://client.ind.freefiremobile.com/GetWishListItems"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB50",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
        "Host": "clientbp.common.ggbluefox.com",
        "Connection": "close",
        "Accept-Encoding": "gzip, deflate, br",
    }

    response = requests.post(url, headers=headers, data=TARGET, verify=False)

    decoded_response = CSGetWishListItemsRes()
    decoded_response.ParseFromString(response.content)

    # Wishlist data
    image_urls = []
    item_ids = []
    release_times = []

    for item in decoded_response.items:
        image_urls.append(f"https://www.dl.cdn.freefireofficial.com/icons/{item.item_id}.png")
        item_ids.append(str(item.item_id))
        release_times.append(convert_timestamp(item.release_time))

    wishlist = [{
        "Count": len(decoded_response.items),
        "image_url": image_urls,
        "item_id": ", ".join(item_ids),
        "release_time": ", ".join(release_times)
    }]

    # Dummy player info (replace with real Free Fire Getliked API later)
    player_info = {
        "nickname": "GM?",
        "region": "IND",
        "uid": uid,
        "like": 1297897,
        "level": 74,
        "lastLogin": "?"
    }

    final_response = {
        "playerBasicInfo": player_info,
        "results": [
            {
                "wishlist": wishlist
            }
        ]
    }

    return jsonify(final_response)

####################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)