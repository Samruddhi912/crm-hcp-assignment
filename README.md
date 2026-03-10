# AI-First CRM: HCP Interaction Module

An intelligent CRM sub-module designed for Healthcare Professionals (HCPs), featuring a **React/Redux** frontend and a **FastAPI** backend powered by **LangGraph** and **Groq LLM**.



## 🚀 Features
- **AI-First Interface**: Dual-panel UI with a manual logging form and a real-time AI Assistant.
- **LangGraph Integration**: The AI uses reasoning to call 5 specific tools:
  - `log_interaction`: Saves new HCP meetings to MySQL.
  - `search_hcp_history`: Retrieves past records via semantic search.
  - `edit_interaction`: Updates existing database entries.
  - `schedule_followup`: Manages future tasks.
  - `check_material_availability`: Checks mock inventory for medical brochures.
- **Relational Database**: Full integration with **MySQL (XAMPP)** using SQLAlchemy.
- **State Management**: Powered by **Redux Toolkit** for consistent UI updates.

---

## 🛠️ Tech Stack
* **Frontend**: React.js, Vite, Redux Toolkit, CSS3.
* **Backend**: Python 3.13, FastAPI, SQLAlchemy, LangGraph.
* **LLM**: Groq (Model: `llama-3.3-70b-versatile`).
* **Database**: MySQL (via XAMPP).

---

## ⚙️ Setup Instructions

### 1. Database Setup (XAMPP)
1. Open **XAMPP Control Panel** and start **Apache** and **MySQL**.
2. Go to `http://localhost/phpmyadmin`.
3. Create a new database named: `crm_hcp_db`.
4. The backend will automatically create the `interactions` table on startup.

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pymysql langchain-groq langgraph python-dotenv

# Run the server
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
###🤖 AI Agent Testing
You can test the agent's logic by typing the following in the Chat Assistant:

Log: "I just met Dr. Arishta and discussed the new cardiovascular results. She was very impressed. Log this."

Search: "Show me my history with Dr. Arishta."

Edit: "Change the sentiment of my last meeting with Dr. Arishta to Neutral."

Inventory: "Do we have any 'Clinical Trial Summaries' in stock?"

###📁 Repository Structure
Plaintext
crm-hcp-assignment/
├── backend/
│   ├── main.py          # FastAPI & LangGraph logic
│   ├── models.py        # SQLAlchemy MySQL Models
│   ├── database.py      # Connection configuration
│   └── .env             # API Keys (Git ignored)
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # UI Components
│   │   └── store.js     # Redux State Management
└── README.md


### Final Push Commands
Once you have saved that file, run these in your terminal to finish:

```bash
git add .
git commit -m "Add professional README with bash instructions"
git push -f origin main
```
