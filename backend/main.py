from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent.agent import process_input
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Calendar Booking Agent API", version="1.0.0")

# Enable CORS for Streamlit to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Calendar Booking Agent API is running!"}

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        
        if not user_input:
            raise HTTPException(status_code=400, detail="Message is required")
        
        logger.info(f"Received chat request: {user_input}")
        response = process_input(user_input)
        
        return {"response": response, "status": "success"}
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return {"response": f"⚠️ Error processing request: {str(e)}", "status": "error"}
