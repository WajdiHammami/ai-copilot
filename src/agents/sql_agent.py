"""SQL Agent - Information Generation from SQL database."""



from logging import log
from typing import Dict, Any, Optional
import dotenv
from langchain_community.utilities import SQLDatabase
from src.db.connection import DB_URI
from langchain_openai import AzureChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from datetime import datetime
import json
from src.utils import load_prompt, log_agent_execution
from src.config.settings import get_llm


dotenv.load_dotenv()  # Load environment variables from .env file

_db = SQLDatabase.from_uri(DB_URI)
_toolkit = None
_agent_executor = None

def _get_agent_executor():
    global _toolkit, _agent_executor
    if _agent_executor is None:
        llm = get_llm(temperature=0)
        _toolkit = SQLDatabaseToolkit(db=_db, llm=llm)
        system_prompt = load_prompt("sql_agent_prompt")
        _agent_executor = create_sql_agent(
            llm=llm,
            toolkit=_toolkit,
            verbose=False,
            return_intermediate_steps=True,
            prefix=system_prompt,
        )
    return _agent_executor



def execute_sql_query(
    question: str,
    log_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a natural language query against the SQL database.
    
    Args:
        question: Natural language question
        log_file: Optional path to log file
        
    Returns:
        Dict with 'answer', 'steps', 'duration_seconds', and optional 'error'
    """
    agent_executor = _get_agent_executor()
    start_time = datetime.now()
    
    log_entry = {
        "agent_type": "sql",
        "question": question,
        "answer": "",
        "steps": [],
        "duration_seconds": 0,
    }
    
    try:
        result = agent_executor.invoke({"input": question})
        log_entry["answer"] = result["output"]
        
        # Extract steps
        if "intermediate_steps" in result:
            for i, (action, observation) in enumerate(result["intermediate_steps"]):
                step = {
                    "step_number": i + 1,
                    "tool": getattr(action, 'tool', str(action)),
                    "tool_input": getattr(action, 'tool_input', str(action)),
                    "observation": str(observation)[:500],
                }
                log_entry["steps"].append(step)
                
                # Capture SQL query
                if "sql" in str(step["tool_input"]).lower():
                    log_entry["generated_sql"] = step["tool_input"]
        
        response = {
            "answer": result["output"],
            "steps": log_entry["steps"],
        }
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        log_entry["error"] = str(e)
        log_entry["answer"] = error_msg
        response = {
            "answer": error_msg,
            "error": str(e),
            "steps": [],
        }
    
    # Duration
    log_entry["duration_seconds"] = (datetime.now() - start_time).total_seconds()
    response["duration_seconds"] = log_entry["duration_seconds"]
    
    # Log
    log_agent_execution(log_entry, log_file=log_file, log_type="sql")
    
    return response


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser(
        description="SQL Agent Executor", 
        epilog='Example: python -m src.agents.sql_agent --question "How many customers?"'
        )
    argparser.add_argument("--question", '-q', type=str, required=True, help="The question to ask the SQL agent.")
    argparser.add_argument("--log_file", '-l', type=str, default="logs/agent_execution_log.json", help="Path to the logging file.")

    args = argparser.parse_args()
    question = args.question
    # Test the database connection and LLM
    result = execute_sql_query(args.question, args.log_file)
    print(result)
