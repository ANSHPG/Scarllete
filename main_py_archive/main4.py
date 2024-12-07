from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")
async def dialogflow_webhook(request: Request):
    """
    Handle POST requests from Dialogflow webhook
    """
    # Parse the JSON payload from Dialogflow
    payload = await request.json()
    intent = payload.get("queryResult", {}).get("intent", {}).get("displayName", "Unknown")
    parameters = payload.get("queryResult", {}).get("parameters", {})

    # Example: Handle the "add.expense" intent
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

        # Dialogflow response structure
        dialogflow_response = {
            "fulfillmentText": response_message,
            "fulfillmentMessages": [
                {"text": {"text": [response_message]}}
            ],
        }
        return JSONResponse(content=dialogflow_response)

    # Default response for unhandled intents
    return JSONResponse(content={"fulfillmentText": "Sorry, I didn't understand that."})

@app.get("/")
async def health_check():
    """
    Handle GET requests to check the server health
    """
    return {"message": "The server is up and running!"}

# Run the app locally
# uvicorn your_file_name:app --host 0.0.0.0 --port 8000 --reload
