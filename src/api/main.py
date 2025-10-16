from fastapi import FastAPI, Query
from src.agents.hybrid_agent import execute_hybrid_query

app = FastAPI() 

@app.get("/ask")
def ask_question(question: str = Query(..., description="The question to ask the SQL agent")):
    result = execute_hybrid_query(question, log_file="logs/hybrid_agent.log")
    return {'answer': result['answer']}