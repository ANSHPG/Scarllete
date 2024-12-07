from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import get_db_connection

app = FastAPI()
latest_parameters = {"category": "Unknown", "amount": 0 , "intent": "Unkown"}

@app.post("/")  # Route for Dialogflow webhook (POST method)
async def handle_webhook(request: Request):
    global latest_parameters

    # Parse the incoming JSON payload
    body = await request.json()

    # Extract parameters from the request
    parameters = body.get("queryResult", {}).get("parameters", {})
    categories = parameters.get("category", [])
    amounts = [entry['amount'] for entry in parameters.get("unit-currency", [{}])]
    intent = body.get("queryResult", {}).get("intent", {}).get("displayName")

    latest_parameters = {"category": categories, "amount": amounts, "intent": intent}

    # Response for the user
    response_msg = f"Expense logged successfully under the categories: {categories} for the amounts: {amounts}."
    
    # Database logic
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        for category, amount in zip(categories, amounts):
            # Map category names to category IDs
            cursor.execute("SELECT category_id FROM category WHERE category_name = %s", (category,))
            result = cursor.fetchone()

            if result:
                category_id = result[0]
                # Call the stored procedure
                cursor.callproc('insert_expense_and_update_category', (category_id, amount, 1))  # Assuming user_id = 1
            else:
                response_msg = f"Category '{category}' not found in the database."

        connection.commit()
    except Exception as e:
        response_msg = f"Error occurred: {e}"
    finally:
        cursor.close()
        connection.close()

    # Return the custom fulfillment response
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
        "intent": intent
    }

    return JSONResponse(content=response)


@app.get("/")  # Route for testing
async def get_status():
    return JSONResponse(content=latest_parameters)
