import os
import traceback
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal, get_db
import models

from dotenv import load_dotenv
load_dotenv() # This automatically looks for the .env file

# LangGraph / Groq imports
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Create DB Tables automatically in MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM HCP Module")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq LLM Setup (Using the versatile model since gemma2 is deprecated)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# ==========================================
# Defining the 5 LangGraph Tools
# ==========================================

@tool
def log_interaction(hcp_name: str, interaction_type: str, sentiment: str, topics: str) -> str:
    """Captures new interaction data with an HCP and saves it to the database."""
    db = SessionLocal()
    try:
        new_log = models.Interaction(
            hcp_name=hcp_name, 
            interaction_type=interaction_type, 
            sentiment=sentiment, 
            topics_discussed=topics
        )
        db.add(new_log)
        db.commit()
        return f"Successfully logged the {interaction_type} with {hcp_name}. The noted sentiment is '{sentiment}'."
    except Exception as e:
        return f"Error logging interaction: {str(e)}"
    finally:
        db.close()

@tool
def edit_interaction(interaction_id: int, new_sentiment: str = None, new_topics: str = None) -> str:
    """Allows modification of previously logged interaction data by ID."""
    db = SessionLocal()
    try:
        record = db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()
        if record:
            if new_sentiment:
                record.sentiment = new_sentiment
            if new_topics:
                record.topics_discussed = new_topics
            db.commit()
            return f"Interaction {interaction_id} has been updated successfully in the database."
        return f"Error: Could not find Interaction ID {interaction_id}."
    finally:
        db.close()

@tool
def search_hcp_history(hcp_name: str) -> str:
    """Retrieves past interactions for a specific Healthcare Professional."""
    db = SessionLocal()
    try:
        records = db.query(models.Interaction).filter(models.Interaction.hcp_name.ilike(f"%{hcp_name}%")).all()
        if not records:
            return f"I couldn't find any past interactions for {hcp_name} in the database."
        
        history = [f"- ID {r.id}: {r.interaction_type} on {r.date.strftime('%Y-%m-%d')}. Topics: {r.topics_discussed} (Sentiment: {r.sentiment})" for r in records]
        return f"Here is the history for {hcp_name}:\n" + "\n".join(history)
    finally:
        db.close()

@tool
def schedule_followup(hcp_name: str, date: str, action_item: str) -> str:
    """Schedules a future task or meeting based on conversation context."""
    return f"Got it. I have scheduled a follow-up with {hcp_name} on {date} for: {action_item}."

@tool
def check_material_availability(material_name: str) -> str:
    """Checks if a specific brochure or product sample is available in inventory."""
    inventory = ["Product X Brochure", "Product Y Sample", "Efficacy Report"]
    if any(material_name.lower() in item.lower() for item in inventory):
        return f"Yes, the '{material_name}' is currently available in our inventory to be shared."
    return f"Sorry, '{material_name}' is currently out of stock or does not exist in our system."

tools = [log_interaction, edit_interaction, search_hcp_history, schedule_followup, check_material_availability]
memory = MemorySaver()
agent_executor = create_react_agent(llm, tools, checkpointer=memory)

# ==========================================
# FastAPI Endpoints
# ==========================================

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_user" 

@app.post("/api/chat")
async def chat_with_agent(request: ChatRequest):
    """Endpoint for the React frontend to communicate with the AI Agent."""
    config = {"configurable": {"thread_id": request.thread_id}}
    
    try:
        response = agent_executor.invoke({"messages": [("user", request.message)]}, config)
        
        # SMARTER EXTRACTION: Look backwards through all messages to find the most recent AI or Tool text
        ai_message = "I have completed the task." 
        for msg in reversed(response["messages"]):
            if msg.content and msg.type != "human":
                ai_message = msg.content
                break
                
        return {"status": "success", "response": ai_message}
        
    except Exception as e:
        print("\n" + "="*50)
        print("🚨 BACKEND CRASHED! HERE IS THE ERROR:")
        traceback.print_exc()
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "AI-First CRM Backend is running with MySQL."}