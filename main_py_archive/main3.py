from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI()

@app.post('/')  # Webhooks send POST requests, so this should be POST
async def handle_request(request: Request):
    # Parse the incoming request body as JSON
    payload = await request.json()

    # Extract intent and parameters
    intent = payload.get('queryResult', {}).get('intent', {}).get('displayName', "")
    parameters = payload.get('queryResult', {}).get('parameters', {})
    output_contexts = payload.get('queryResult', {}).get('outputContexts', [])

    # Check the intent name and handle accordingly
    if intent == 'add.expense':
        # Extract relevant data from parameters
        unit_currency = parameters.get("unit-currency", [{}])[0]
        category = parameters.get("category", [""])[0]
        amount = unit_currency.get("amount", "unknown")
        currency = unit_currency.get("currency", "unknown")

        # Formulate the response message
        response_message = f"Your expense has been logged successfully, under the category - {category} for the amount - {amount} {currency}."

        # Return the response in Dialogflow's required format
        return JSONResponse(content={
            "fulfillmentText": response_message,
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [response_message]
                    }
                }
            ]
        })

    # Default response for unknown intents
    return JSONResponse(content={
        "fulfillmentText": f"Received intent: {intent}",
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [f"Received intent: {intent}"]
                }
            }
        ]
    })


async def health_check():
    return {"message": "Server is running. Use POST for webhook calls."}
