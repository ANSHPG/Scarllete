from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import get_db_connection

app = FastAPI()


latest_parameters = {"category": "Unknown", "amount": 0 , "intent": "Unkown"}

@app.post("/")  # Route for Dialogflow webhook (POST method)
async def handle_webhook(request: Request):
    # Parse the incoming JSON payload
    body = await request.json()

    # Extract parameters from the request
    global categories , intent , amount , latest_parameters
    parameters = body.get("queryResult", {}).get("parameters", {})
    intent = body.get("queryResult", {}).get("intent", {}).get("displayName")
    categories = parameters.get("category", [])
    amounts = [entry['amount'] for entry in parameters.get("unit-currency", [{}])]

    latest_parameters = {"category": categories, "amount": amounts, "intent": intent}

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
                    if category == 'Food':
                        response_msg_informal = f"Hope that satisfied your cravings! I've gone ahead and logged ${amount} under food for you"
                    elif category == 'Transport':
                        response_msg_informal = f"Hope you enjoyed the journey! I've recorded ${amount} under transport for you"
                    elif category == 'Rent':
                        response_msg_informal = f"Looks like your rent is all squared away, I’ve recorded ${amount} under your rent expenses"
                    elif category == 'Subscriptions':
                        response_msg_informal = f"Got it! ${amount} for your subscriptions has been logged. Stay on top of those monthly favorites!"
                    elif category == 'Entertainment':
                        response_msg_informal = f"Had a blast at the movies or out on the town? I’ve added ${amount} to your entertainment expenses, sounds like a good time!"
                    elif category == 'Miscellaneous':
                        response_msg_informal = f"I’ve added ${amount} under miscellaneous for those little extras that keep life interesting"
                    elif category == 'Shopping':
                        response_msg_informal = f"Looks like a shopping spree is in order! ${amount} has been noted for your shopping, enjoy picking out your favorites!"
                    else:
                        response_msg_informal = f"All set! I’ve added that ${amount} you spent on {category}, hope it was worth it!"
                    # Call the stored procedure for adding expense
                    cursor.callproc('insert_expense_and_update_category', (category_id, amount, 1))  # Assuming user_id = 1
                    response_msg += response_msg_informal
                    connection.commit()
                else:
                    response_msg += f"Oops, it looks like I couldn’t find the '{category}' category in our system. Could you double-check the name and try again?"

        elif intent == "remove.expense":
            for category, amount in zip(categories, amounts):
                cursor.execute("SELECT category_id FROM category WHERE category_name = %s", (category,))
                result = cursor.fetchone()
                if result:
                    category_id = result[0]
                    if category == 'Food':
                        response_msg_informal = f"Changed my mind, looks like we’re taking that ${amount} back from food. All updated!"
                    elif category == 'Transport':
                        response_msg_informal = f"Oops, looks like you didn’t need that transport expense after all, ${amount} has been removed"
                    elif category == 'Rent':
                        response_msg_informal = f"Got it! I’ve taken the ${amount} off your rent. All set for now!"
                    elif category == 'Subscriptions':
                        response_msg_informal = f"Removed ${amount} from your subscriptions. It’s good to stay on top of those, right?"
                    elif category == 'Entertainment':
                        response_msg_informal = f"Looks like we’re trimming that entertainment budget a bit, ${amount} has been removed"
                    elif category == 'Miscellaneous':
                        response_msg_informal = f"Pulled that ${amount} from miscellaneous. It’s always good to keep track of those small expenses!"
                    elif category == 'Shopping':
                        response_msg_informal = f"Changed my mind on that shopping expense! ${amount} has been removed from your list."
                    else:
                        response_msg_informal = f"Alright, I’ve taken that ${amount} off the {category} category. All squared away!"
                    # Call the stored procedure for adding expense
                    cursor.callproc('insert_expense_and_update_category', (category_id, amount*-1, 1))  # Assuming user_id = 1
                    response_msg += response_msg_informal
                    connection.commit()
                else:
                    response_msg += f"Oops, it looks like I couldn’t find the '{category}' category in our system. Could you double-check the name and try again?"


        elif intent == "track.expense":
            for category in categories:
                try:
                    # Initialize total_spent for each category
                    total_spent = 0

                    # Call the stored procedure to get total spent
                    cursor.callproc('get_category_total_track', (category,0))

                    for res in cursor.stored_results():
                        result = res.fetchone()

                        if result:  # Ensure a result is returned
                            total_spent = result[0]
                            if category == 'Food':
                                response_msg_informal = f"Looks like you’ve been treating yourself! Total spent on food so far: ${total_spent}. Hope it was worth it!"
                            elif category == 'Transport':
                                response_msg_informal = f"All that traveling adds up! You've spent a total of ${total_spent} on transport. Keep moving!"
                            elif category == 'Rent':
                                response_msg_informal = f"Your rent is all set, huh? Total spent on rent- ${total_spent}. Hope it’s a comfy place!"
                            elif category == 'Subscriptions':
                                response_msg_informal = f"Keeping up with those subscriptions? You’ve spent ${total_spent} on subscriptions so far. Stay on top of those monthly fees!"
                            elif category == 'Entertainment':
                                response_msg_informal = f"Looks like the fun never stops! Total spent on entertainment: ${total_spent}. Hope you had a blast!"
                            elif category == 'Miscellaneous':
                                response_msg_informal = f"Life’s little extras do add up! You've spent ${total_spent} on miscellaneous. Those little things can really make life interesting!"
                            elif category == 'Shopping':
                                response_msg_informal = f"Looks like the shopping spree is ongoing! Total spent on shopping: ${total_spent}. Enjoy those goodies!"
                            else:
                                response_msg_informal = f"All set! Total spent on {category} is ${total_spent}. Hope it was worth it!"
                            response_msg += response_msg_informal
                        else:
                            response_msg += f"Oops, it looks like I couldn’t find the '{category}' category in our system. Could you double-check the name and try again?"

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
async def get_category_and_amount():
    return JSONResponse(content=latest_parameters)
