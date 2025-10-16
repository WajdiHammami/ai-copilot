import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.hybrid_agent import execute_hybrid_query

def test_hybrid_agent_executor_returns_response():
    log_file = '/tmp/test_hybrid_agent_log.jsonl'
    result = execute_hybrid_query("How does the hybrid agent work?", log_file=log_file)
    assert result is not None
    assert "answer" in result
    assert isinstance(result["answer"], str)

