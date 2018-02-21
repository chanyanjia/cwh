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

        status = {'#FED12345':'Pending Confirmation', '#FED1234':'In Transit', '#FED12334':'Awaiting Pick-up. ETA 30/1/2018', '#FED54321':'Awaiting pick-up'}

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
    elif storing == "ordercheck":
        result = req.get("result")
        parameters = result.get("parameters")
        item = parameters.get("itemschk")

        Orderstatus = ['PO00100234', ['Blackpipe', 'Pump']],['PO0040500', ['Blackpipe']]

        check = ''

        for i in range(0,len(Orderstatus)):
            if item in Orderstatus[i][1]:
                check += ' ' + Orderstatus[i][0]
        if check == '':
            speech = " There are no pending orders for this item. "
        else:
            speech = "Orders have been made for this item. Please refer to " + check

        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            #"source": ""
        }    

    elif storing == "purchasereq":
        result = req.get("result")
        parameters = result.get("parameters")
        req = parameters.get("purreq")

        status = {'PR46315555':'Pending Approval. Requested date: 25/1/2018.', 'PR46312222':'Approved. PO issued: 8/1/18. PO Number: PO0040500. PO status: Open'}

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
        
    elif storing == "PO_status":
        result = req.get("result")
        parameters = result.get("parameters")
        req = parameters.get("POnumber")

        status = {'PO00100234':'Rejected', 'PO0040500':'Open', 'PO00405000':'Cancelled'}

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
        tele_message=[
            {
                "photo": "https://s3.amazonaws.com/warehousehappybotprototype/SKUPump.JPG"
            }
        ]

        print(json.dumps(tele_message))

        return {
            "speech": speech,
            "displayText": speech,
            "data": {"telegram": tele_message},
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
