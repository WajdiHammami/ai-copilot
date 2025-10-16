
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.sql_agent import execute_sql_query

def test_sql_agent_executor_returns_executor():
    log_file = '/tmp/test_sql_agent_log.jsonl'
    result = execute_sql_query("SELECT 1", log_file=log_file)
    assert result is not None
    assert "answer" in result

