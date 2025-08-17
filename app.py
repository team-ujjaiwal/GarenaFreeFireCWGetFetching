from flask import Flask, jsonify, request
import requests
import threading
import httpx
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from GetWishListItems_pb2 import CSGetWishListItemsRes
from datetime import datetime

app = Flask(__name__)

# Region credentials
CREDENTIALS = {
    "IND": {
        "uid": "3892341508",
        "password": "B78C0F8F5A2FDA93948C2966DE26DD7A0681EF6C2F09A5C10629E50C4D6341B4",
        "url": "https://client.ind.freefiremobile.com/GetWishListItems"
    },
    "SG": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "NA": {
        "uid": "3943737998",
        "password": "92EB4C721DB698B17C1BF61F8F7ECDEC55D814FB35ADA778FA5EE1DC0AEAEDFF",
        "url": "https://client.us.freefiremobile.com/GetWishListItems"
    },
    "BR": {
        "uid": "3943737998",
        "password": "92EB4C721DB698B17C1BF61F8F7ECDEC55D814FB35ADA778FA5EE1DC0AEAEDFF",
        "url": "https://client.us.freefiremobile.com/GetWishListItems"
    },
    "SAC": {
        "uid": "3943737998",
        "password": "92EB4C721DB698B17C1BF61F8F7ECDEC55D814FB35ADA778FA5EE1DC0AEAEDFF",
        "url": "https://client.us.freefiremobile.com/GetWishListItems"
    },
    "US": {
        "uid": "3943737998",
        "password": "92EB4C721DB698B17C1BF61F8F7ECDEC55D814FB35ADA778FA5EE1DC0AEAEDFF",
        "url": "https://client.us.freefiremobile.com/GetWishListItems"
    },
    "ID": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "TW": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "TH": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "BD": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "ME": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "RU": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "VN": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "PK": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "CIS": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
    "EUROPE": {
        "uid": "3943739516",
        "password": "BFA0A0D9DF6D4EE1AA92354746475A429D775BCA4D8DD822ECBC6D0BF7B51886",
        "url": "https://clientbp.ggblueshark.com/GetWishListItems"
    },
}

# JWT generate URL
JWT_URL = "https://project-jwt-token-ujjaiwal.vercel.app/token"

# API Key
API_KEY = "1yearskeysforujjaiwal"

####################################
def Encrypt_ID(x):
    x = int(x)
    dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
    xxx = ['1', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']
    x = x/128 
    if x > 128:
        x = x/128
        if x > 128:
            x = x/128
            if x > 128:
                x = x/128
                strx = int(x)
                y = (x-int(strx))*128
                stry = str(int(y))
                z = (y-int(stry))*128
                strz = str(int(z))
                n = (z-int(strz))*128
                strn = str(int(n))
                m = (n-int(strn))*128
                return dec[int(m)]+dec[int(n)]+dec[int(z)]+dec[int(y)]+xxx[int(x)]
            else:
                strx = int(x)
                y = (x-int(strx))*128
                stry = str(int(y))
                z = (y-int(stry))*128
                strz = str(int(z))
                n = (z-int(strz))*128
                strn = str(int(n))
                return dec[int(n)]+dec[int(z)]+dec[int(y)]+xxx[int(x)]

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def generate_image_urls(item_ids):
    base_url = "https://www.dl.cdn.freefireofficial.com/icons/"
    return [f"{base_url}{item_id}.png" for item_id in item_ids.split(", ")]

####################################
jwt_tokens = {}

def get_jwt_token(region):
    global jwt_tokens
    if region not in CREDENTIALS:
        return None
        
    creds = CREDENTIALS[region]
    url = f"{JWT_URL}?uid={creds['uid']}&password={creds['password']}"
    
    try:
        print(f"Fetching JWT token for {region} from: {url}")
        response = httpx.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            if status in ["success", "live"]:
                jwt_tokens[region] = data["token"]
                print(f"✅ {region} JWT Token updated successfully.")
                return data["token"]
            else:
                print(f"❌ Failed for {region}: status = {status}")
        else:
            print(f"❌ HTTP Error for {region}: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception while fetching token for {region}: {e}")
    
    return None

def token_updater():
    while True:
        for region in CREDENTIALS.keys():
            get_jwt_token(region)
        time.sleep(8 * 3600)  # Update every 8 hours

token_thread = threading.Thread(target=token_updater, daemon=True)
token_thread.start()

# Initialize tokens for all regions
for region in CREDENTIALS.keys():
    get_jwt_token(region)

####################################
@app.route('/wishlist/<int:uid>', methods=['GET'])
def get_wishlist(uid):
    region = request.args.get('region', 'IND').upper()
    key = request.args.get('key')
    
    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
        
    if region not in CREDENTIALS:
        return jsonify({"error": f"Unsupported region '{region}'"}), 400
    
    jwt_token = jwt_tokens.get(region)
    if not jwt_token:
        jwt_token = get_jwt_token(region)
        if not jwt_token:
            return jsonify({"error": f"Failed to get JWT token for {region}"}), 500
    
    try:
        # Get wishlist items
        encrypted_id = Encrypt_ID(uid)
        encrypted_api = encrypt_api(f"08{encrypted_id}1007")
        TARGET = bytes.fromhex(encrypted_api)
        
        url = CREDENTIALS[region]["url"]
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB50",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
            "Host": url.split("//")[1].split("/")[0],
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate, br",
        }
        
        response = requests.post(url, headers=headers, data=TARGET, verify=False)
        decoded_response = CSGetWishListItemsRes()
        decoded_response.ParseFromString(response.content)
        
        # Process wishlist items
        item_ids = []
        release_times = []
        for item in decoded_response.items:
            item_ids.append(str(item.item_id))
            release_times.append(convert_timestamp(item.release_time))
        
        # Prepare the response
        response_data = {
            "region": region,
            "results": [{
                "wishlist": [{
                    "Count": len(item_ids),
                    "image_url": generate_image_urls(", ".join(item_ids)),
                    "item_id": ", ".join(item_ids),
                    "release_time": ", ".join(release_times)
                }]
            }]
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({
            "error": "An error occurred",
            "details": str(e),
            "region": region
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)