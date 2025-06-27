📅 AI Calendar Booking Assistant
A conversational AI agent that helps you book meetings in Google Calendar via natural language chat. Built using FastAPI, Streamlit, LangGraph, and Google Calendar API.





🚀 Features
💬 Natural Language Chat for Booking

🗓️ Checks Google Calendar Availability

✅ Books Events Automatically

⚡ Real-Time Responses

🌐 Clean FastAPI Backend

🎨 User-Friendly Streamlit Frontend

📂 Project Structure
text
Copy
Edit
📁 internshala-internship
│
├── 📁 agent               # AI agent logic
│   └── agent.py
│
├── 📁 backend             # FastAPI backend
│   └── main.py
│
├── 📁 frontend            # Streamlit frontend
│   └── app.py
│
├── 📁 utils               # Utility functions
│   ├── calendar_api.py    # Google Calendar API integration
│   └── utils.py           # Date parsing, slot checking, etc.
│
├── credentials.json       # Google Service Account credentials
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
⚙️ Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/calendar-booking-assistant.git
cd calendar-booking-assistant
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Set up Google Calendar API
Create a Service Account in Google Cloud.

Download the credentials.json file and place it in the project root.

Share your calendar with the Service Account Email with "Make changes to events" permission.

4. Start Backend Server
bash
Copy
Edit
uvicorn backend.main:app --reload
5. Start Frontend (Streamlit)
bash
Copy
Edit
streamlit run frontend/app.py
💬 Usage
Start the app and interact with the chatbot.

Example prompt:

kotlin
Copy
Edit
Do you have time this Friday at 2 PM?
The bot will check availability and either:

✅ Book the event

❌ Inform you if the slot is unavailable

✅ Example API Request
http
Copy
Edit
POST /chat
Content-Type: application/json

{
    "message": "Book a meeting tomorrow at 4 PM"
}
📦 Technologies Used
Python 3.11

FastAPI

Streamlit

LangGraph

Google Calendar API

Uvicorn

📚 Learnings
Google Calendar API Integration

Natural Language Time Parsing

Asynchronous FastAPI Development

Real-Time Frontend with Streamlit

Role-Based Calendar Access

🤝 Contributions
Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.

