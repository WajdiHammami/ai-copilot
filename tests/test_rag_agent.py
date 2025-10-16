import pytest
from src.agents.rag_agent import execute_rag_query

def test_rag_agent_executor_returns_response():
    log_file = '/tmp/test_rag_agent_log.jsonl'
    result = execute_rag_query("What is LangChain?", log_file=log_file)
    assert result is not None
    assert "answer" in result
    assert isinstance(result["answer"], str)

# You can add more tests for hybrid_agent, utils, etc.
