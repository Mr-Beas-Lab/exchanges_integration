import time
import hmac
import requests
from hashlib import sha256

def create_signature(api_secret, params):
    sorted_keys = sorted(params.keys())
    params_str = "&".join([f"{key}={params[key]}" for key in sorted_keys])
    signature = hmac.new(api_secret.encode("utf-8"), params_str.encode("utf-8"), digestmod=sha256).hexdigest()
    return signature

def get_balance(api_key, secret_key):
    params = {
        "timestamp": str(int(time.time() * 1000)),
    }

    signature = create_signature(secret_key, params)
    params['signature'] = signature

    url = f"https://open-api.bingx.com/openApi/swap/v3/user/balance?{requests.compat.urlencode(params)}"

    headers = {
        'X-BX-APIKEY': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

if __name__ == "__main__":
    APIKEY = "test_key"
    SECRETKEY = "test_key"

    balance_info = get_balance(APIKEY, SECRETKEY)