#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    # number
    if req.get("result").get("action") == "getAccountNumber":
        result = req.get("result")
        parameters = result.get("parameters")
        constrains = parameters.get("constrains")
        if constrains == "" or constrains == "all":
            url = "https://nyu-bank-system.mybluemix.net/accounts"
        elif constrains == "active":
            url = "https://nyu-bank-system.mybluemix.net/accounts?active=true"
        elif constrains == "inactive":
            url = "https://nyu-bank-system.mybluemix.net/accounts?active=false"
        elif if "type" in constrains:
            typeNum = constrains[5:6]
            if typeNum == 0 or typeNum == 1 or typeNum == 2 or typeNum == 3:
                url = "https://nyu-bank-system.mybluemix.net/accounts?type=" + typeNum
        else:
            return {}
        results = urllib.urlopen(url).read()
        data = json.loads(results)
        print(len(data))
        res = makeWebhookResultNumber(len(data))
        return res
    # list
    elif req.get("result").get("action") == "listAccounts":
        result = req.get("result")
        parameters = result.get("parameters")
        constrains = parameters.get("constrains")
        if constrains == "" or constrains == "all":
            url = "https://nyu-bank-system.mybluemix.net/accounts"
        elif constrains == "active":
            url = "https://nyu-bank-system.mybluemix.net/accounts?active=true"
        elif constrains == "inactive":
            url = "https://nyu-bank-system.mybluemix.net/accounts?active=false"
        elif if "type" in constrains:
            typeNum = constrains[5:6]
            if typeNum == 0 or typeNum == 1 or typeNum == 2 or typeNum == 3:
                url = "https://nyu-bank-system.mybluemix.net/accounts?type=" + typeNum
        else:
            return {}
        results = urllib.urlopen(url).read()
        data = json.loads(results)
        print(data)
        res = makeWebhookResultList(constrains, data)
        return res
    else:
        return {}

def makeWebhookResultList(constrains, data):
    speech = constrains + " accounts are listed here: " + str(data)
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "api-ai-webhook-sample"
    }
def makeWebhookResultNumber(constrains, length):
    speech = "The total number of "+ constrains + " accounts is  " + str(length)
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "api-ai-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print "Starting app on port %d" % port
    app.run(debug=False, port=port, host='0.0.0.0')
