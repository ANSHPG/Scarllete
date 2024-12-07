from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")  # Route for Dialogflow webhook
async def handle_webhook(request: Request):
    # Parse incoming JSON payload (optional for now)
    body = await request.json()

    # Example of extracting the intent, just to show how it works
    intent = body.get("queryResult", {}).get("intent", {}).get("displayName", "unknown")

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
        "intent": intent,  # Echo back the received intent
        "parameters": body.get("queryResult", {}).get("parameters", {})  # Echo parameters
    }

    # Return the custom response
    return JSONResponse(content=response)
