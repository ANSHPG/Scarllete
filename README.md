# Scarlette  

Scarlette is a lightweight backend framework built with FastAPI, designed to integrate seamlessly with Dialogflow for handling user intents and dynamically triggering database procedures. This project focuses on managing and tracking expenses efficiently and provides an extendable base for conversational AI applications.  

## Features  
- Handles Dialogflow intents like adding, removing, and tracking expenses.  
- Dynamically triggers MySQL stored procedures based on recognized user queries.  
- Integrated with Telegram for real-time interactions (due to time constraints, this is the only frontend implementation currently).  
- Modular structure, making it easy to extend or adapt to different use cases.  

## Tools and Technologies  
- **FastAPI**: A modern, high-performance web framework for building APIs.  
- **Uvicorn**: An ASGI server to run the FastAPI backend.  
- **Dialogflow**: Google’s conversational AI platform for recognizing user intents.  
- **MySQL**: A relational database for storing and managing categorized expense data.  
- **Cloudflared**: Exposes the local backend server securely to the internet.  
- **Telegram Bot API**: Enables user interaction via a Telegram bot.  

## Why No Web Frontend?  
Incorporating a web frontend would have required additional time and effort, which wasn’t feasible for this project at the moment. However, the project remains open for contributors who would like to add a frontend, be it web or mobile.

## Installation and Usage  

1. **Clone the Repository**  
   ```bash  
   git clone https://github.com/your-username/scarlette.git  
   cd scarlette  
   ```  

2. **Install Dependencies**  
   Ensure Python 3.9+ is installed, then run:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Set Up the Database**  
   - Create a MySQL database.  
   - Run the provided SQL scripts (`setup.sql`) to set up tables and stored procedures.  

4. **Configure the Environment**  
   Open the `database.py` file and update it with your MySQL credentials.  

5. **Start the Backend**  
   Start the FastAPI server with:  
   ```bash  
   uvicorn main:app --reload  
   ```  

6. **Activate the Cloudflare Tunnel**  
   Expose the local server using Cloudflared:  
   ```bash  
   cloudflared tunnel --url http://localhost:8000  
   ```  

7. **Set Up Dialogflow**  
   - Add the Cloudflare URL in the Dialogflow Fulfillment webhook configuration.  
   - Ensure your intents and parameters align with the backend’s logic.  

8. **Set Up Telegram Integration**  
   - Create a bot on Telegram using BotFather.  
   - Update the bot token in the configuration.  
   - Use the bot to interact with the backend.  

9. **Test the Application**  
   - Use Dialogflow’s test console or interact with the Telegram bot to see your queries processed in real time.  

## Contributing  
If you’d like to contribute to Scarlette, feel free to fork the repository and submit a pull request. Contributions such as adding a frontend, improving backend functionalities, or enhancing the Telegram integration are most welcome.  

## License and Usage  
You are free to use this repository for personal projects. However, for commercial or public-facing applications, please contact me for approval.  

If you encounter any problems or have questions, don’t hesitate to reach out. Suggestions and feedback are always appreciated!  
```
