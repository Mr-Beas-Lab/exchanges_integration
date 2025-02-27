import os
import time
import requests
import hmac
from hashlib import sha256
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
APIURL = "https://open-api.bingx.com"

def cancel_order(symbol, order_id):
    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "DELETE"
    paramsMap = {
        "symbol": symbol,
        "orderId": order_id,
        "timestamp": str(int(time.time() * 1000))
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRET_KEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': API_KEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "":
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':
    cancel_order("BTC-USDT", "25")
