from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import get_db_connection

app = FastAPI()

@app.post("/")  # Route for Dialogflow webhook (POST method)
async def handle_webhook(request: Request):
    # Parse the incoming JSON payload
    body = await request.json()

    # Extract parameters from the request
    global categories 
    parameters = body.get("queryResult", {}).get("parameters", {})
    intent = body.get("queryResult", {}).get("intent", {}).get("displayName")
    categories = parameters.get("category", [])
    amounts = [entry['amount'] for entry in parameters.get("unit-currency", [{}])]


    response_msg = ""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if intent == "add.expense":
            for category, amount in zip(categories, amounts):
                # Map category names to category IDs
                cursor.execute("SELECT category_id FROM category WHERE category_name = %s", (category,))
                result = cursor.fetchone()
                if result:
                    category_id = result[0]
                    # Call the stored procedure for adding expense
                    cursor.callproc('insert_expense_and_update_category', (category_id, amount, 1))  # Assuming user_id = 1
                    response_msg += f"Expense added for category '{category}' with amount {amount}.\n"
                    connection.commit()
                else:
                    response_msg += f"Category '{category}' not found in the database.\n"

        elif intent == "track.expense":
            for category in [categories]:
                try:
                    # Initialize total_spent for each category
                    total_spent = 0

                    # Call the stored procedure to get total spent
                    cursor.callproc('get_category_total_track', (category,0))

                    for res in cursor.stored_results():
                        result = res.fetchone()

                        if result:  # Ensure a result is returned
                            total_spent = result[0]
                            response_msg += f"Total spent for category '{category}': {total_spent}"
                        else:
                            response_msg += f"No data found for category '{category}'.\n"

                    # if total_spent is not None:
                    #     response_msg += f"Total spent for category '{category}': {total_spent}.\n"
                    # else:
                    #     response_msg += f"No data found for category '{category}'.\n"
                except Exception as e:
                    response_msg += f"Error occurred while processing category '{category}': {e}\n"
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
    return {f"categories - {categories}"}
