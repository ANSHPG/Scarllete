from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Temporary storage for the latest parameters
latest_parameters = {"category": "Unknown", "amount": 0}

@app.post("/")  # Route for Dialogflow webhook (POST method)
async def handle_webhook(request: Request):
    global latest_parameters

    # Parse the incoming JSON payload
    body = await request.json()

    # Extract parameters from the request
    parameters = body.get("queryResult", {}).get("parameters", {})
    category = parameters.get("category", ["Unknown"])[0]
    amount = parameters.get("unit-currency", [{}])[0].get("amount", 0)

    # Update the latest parameters
    latest_parameters = {"category": category, "amount": amount}

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


@app.get("/{query}")  # Route for GET requests with query
async def process_query(query: str):
    global latest_parameters

    try:
        # Extract the amount and category from the query
        words = query.split()
        amount = next((int(word) for word in words if word.isdigit()), 0)
        if "for" in query:
            category = query.split("for")[-1].strip()
        else:
            category = "Unknown"

        # Simulate a JSON payload similar to Dialogflow
        simulated_payload = {
            "queryResult": {
                "intent": {"displayName": "add.expense"},
                "parameters": {
                    "unit-currency": [{"amount": amount, "currency": "USD"}],
                    "category": [category],
                }
            }
        }

        # Pass the simulated payload to the webhook logic
        response = await handle_webhook(Request(scope={"type": "http", "json": simulated_payload}))
        return response

    except Exception as e:
        # Return a debug message in case of an error
        return JSONResponse(content={"message": "Error processing query", "error": str(e)})
