from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Temporary storage for the latest parameters
latest_parameters = {"category": "Unknown", "amount": 0 , "intent": "Unkown"}

@app.post("/")  # Route for Dialogflow webhook (POST method)
async def handle_webhook(request: Request):
    global latest_parameters

    # Parse the incoming JSON payload
    body = await request.json()

    # Extract parameters from the request
    parameters = body.get("queryResult", {}).get("parameters", {})
    # category = parameters.get("category", ["Unknown"])
    category = parameters.get("category")
    amount = parameters.get("unit-currency", [{}])
    intent = body.get("queryResult",{}).get("intent",{}).get("displayName")

    amounts = [entry['amount'] for entry in amount ]
    categories = [entry for entry in category]
    # Update the latest parameters
    latest_parameters = {"category": categories, "amount": amounts, "intent": intent}

    # Create your custom fulfillment response
    response_msg = f"server_response: Your expense has been logged successfully, under the category - {categories} for the amount - {amounts} intent - {intent}"
    response = {
        "fulfillmentText": response_msg,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        response_msg
                    ]
                }
            }
        ],
        "intent": body.get("queryResult", {}).get("intent", {}).get("displayName", "unknown"),
        "parameters": parameters
    }

    # Return the custom response
    return JSONResponse(content=response)


@app.get("/")  # Route for GET requests
async def get_category_and_amount():
    # Return the latest extracted parameters as JSON
    return JSONResponse(content=latest_parameters)
