from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")
async def dialogflow_webhook(request: Request):
    """
    Handle POST requests from Dialogflow webhook and return a JSON response with fulfillment
    """
    # Parse the JSON payload from Dialogflow
    payload = await request.json()
    intent = payload.get("queryResult", {}).get("intent", {}).get("displayName", "Unknown")
    parameters = payload.get("queryResult", {}).get("parameters", {})

    # Handle the "add.expense" intent
    if intent == "add.expense":
        unit_currency = parameters.get("unit-currency", [{}])[0]
        category = parameters.get("category", [""])[0]

        # Extract amount and currency
        amount = unit_currency.get("amount", "unknown")
        currency = unit_currency.get("currency", "unknown")
        category_name = category if category else "unknown"

        # Fulfillment message
        response_message = (
            f"Your expense has been logged successfully, "
            f"under the category - {category_name} for the amount - {amount} {currency}."
        )

        # JSON response for webhook and to display
        response = {
            "fulfillmentText": response_message,
            "fulfillmentMessages": [
                {"text": {"text": [response_message]}}
            ],
            "intent": intent,
            "parameters": parameters
        }
        return JSONResponse(content=response)

    # Default response for unhandled intents
    return JSONResponse(content={
        "fulfillmentText": "Sorry, I didn't understand that.",
        "intent": intent,
        "parameters": parameters
    })

@app.get("/")
async def health_check():
    """
    Handle GET requests to check the server health
    """
    return {"message": "The server is up and running!"}
