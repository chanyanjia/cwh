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
    storing = req.get("result").get("action")
    if storing == "orderstatus":
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
    
    elif storing == "purchasereq":
        result = req.get("result")
        parameters = result.get("parameters")
        req = parameters.get("purreq")

        status = {'PR46315555':'Pending Approval. Requested date: 10/1/2018.', 'PR46312222':'Approved. PO issued: 8/1/18.'}

        speech = "The status of " + req + " is " + status[req]
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "BankRates"
        }
        
        
    elif storing == "img":
        result = req.get("result")
        parameters = result.get("parameters")
        item = parameters.get("itemsreq")

        speech = "Showing item " + item

        print("Response:")
        print(speech)
        
        telegram_message = [
            {
                "imageUrl": "https://s3.amazonaws.com/warehousehappybotprototype/SKUPump.JPG",
                "platform": "telegram",
                "type": 3
            }
        ]

        print(json.dumps(telegram_message))
       

        return {
            "speech": speech,
            "displayText": speech,
            "data": {"telegram": telegram_message},
            # "contextOut": [],
            "source": "apiai-kik-images"}
        
    speech = "a"
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "BankRates"
        } 


    


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
