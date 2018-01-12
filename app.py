import urllib
import json
import os
import telebot

from flask import Flask
from flask import request
from flask import make_response


bot = telebot.TeleBot("532987050:AAEkQ6FqXHWGI29JTFY0Bojwgy91Xw4hnxU")

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
    elif storing == "img":
        result = req.get("result")
        parameters = result.get("parameters")
        item = parameters.get("itemsreq")

        speech = "Showing item " + item

        print("Response:")
        print(speech)
        
        kik_message = [
            {
                "text": "my reply text"
            }
        ]
       
        print(json.dumps(kik_message))
        tb.send_message(chatid, "hello)

        return {
            "speech": speech,
            "displayText": speech,
            "data": {"telegram": kik_message},
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
