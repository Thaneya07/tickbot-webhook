from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if testing locally with tools

# In-memory user data for demo
USERS = {
    "default_user": {
        "pin": "1234",
        "wallet": 1000
    }
}

@app.route('/')
def index():
    return "TickBot Dialogflow Webhook Running"

def get_intent_name(req):
    return req.get("queryResult", {}).get("intent", {}).get("displayName", "")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = get_intent_name(req)
    user = "default_user"  # For simplicity, fixed user

    if intent == "ServiceSelection":
        service = req["queryResult"]["parameters"].get("service")
        if service:
            response_text = f"You selected {service}. Please provide details (destination/event name)."
        else:
            response_text = "Please select a valid service: Flight, Movie, Bus, or Event."

    elif intent == "ProvideDetails":
        # Store details in session or DB in real app
        detail = req["queryResult"]["parameters"].get("details")
        if detail:
            response_text = "Please enter date (DD-MM-YYYY)."
        else:
            response_text = "I didn't catch the details. Please provide them again."

    elif intent == "ProvideDate":
        date = req["queryResult"]["parameters"].get("date")
        if date:
            response_text = "Please enter time (e.g., 6 PM)."
        else:
            response_text = "Please specify a valid date."

    elif intent == "ProvideTime":
        time = req["queryResult"]["parameters"].get("time")
        if time:
            response_text = "Enter your 4-digit PIN to confirm payment."
        else:
            response_text = "Please specify a valid time."

    elif intent == "EnterPIN":
        pin = req["queryResult"]["parameters"].get("pin")
        if pin == USERS[user]["pin"]:
            price = 200  # fixed demo price
            if USERS[user]["wallet"] < price:
                response_text = "Sorry, your wallet balance is insufficient for this booking."
            else:
                USERS[user]["wallet"] -= price
                response_text = (
                    f"Payment successful! Your ticket is confirmed. "
                    f"Remaining wallet balance: ₹{USERS[user]['wallet']}"
                )
        else:
            response_text = "Incorrect PIN entered. Booking failed."

    else:
        response_text = "Sorry, I didn't understand that. Can you please repeat?"
i
    return jsonify({"fulfillmentText": response_text})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
