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

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "orderstatus":
        result = req.get("result")
        parameters = result.get("parameters")
        order = parameters.get("order_number")

        status = {'#FED12345':'Pending Confirmation', '#FED1234':'In Transit', '#FED12334':'Awaiting Pick-up', '#FED54321':'Awaiting pick-up'}

        speech = "The order status of " + order + " is " + status[order]
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "BankRates"
        }
    elif req.get("result").get("action") == "img":
        result = req.get("result")
        parameters = result.get("parameters")
        item = parameters.get("itemsreq")

        speech = "Showing item " + item

        print("Response:")
        print(speech)
        
        kik_message = [
            {
                "type": "text",
                "body": "Here's the picture of item " + item
            },
            {
                "type": "picture",
                "picUrl": "https://s3.amazonaws.com/warehousehappybotprototype/SKUPump.JPG"
            }
        ]

        print(json.dumps(kik_message))

        return {
            "speech": speech,
            "displayText": speech,
            "data": {"kik": kik_message},
            # "contextOut": [],
            "source": "apiai-kik-images"
        }
    else
        return {}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run()
