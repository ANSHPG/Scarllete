from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")  # Route for Dialogflow webhook (POST method)
async def handle_webhook(request: Request):
    # Parse the incoming JSON payload
    body = await request.json()

    # Extract parameters from the request
    parameters = body.get("queryResult", {}).get("parameters", {})
    category = parameters.get("category", ["Unknown"])[0]  # Default to "Unknown" if not found
    amount = parameters.get("unit-currency", [{}])[0].get("amount", 0)  # Default to 0 if not found

    # Create your custom fulfillment response
    response = {
        "fulfillmentText": "The server is up and running!",
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        "The server is up and running!"
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
    # Replace this with actual logic if needed to fetch data dynamically
    sample_response = {
        "category": "Food",  # Replace with extracted or dummy value
        "amount": 560        # Replace with extracted or dummy value
    }

    # Return the response as JSON
    return JSONResponse(content=sample_response)
