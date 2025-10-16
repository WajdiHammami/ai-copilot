"""Hybrid Agent - Routes queries to SQL, RAG, or both."""
from typing import Dict, Any, Optional
from langchain.prompts import ChatPromptTemplate

from src.config.settings import get_llm
from src.utils import load_prompt
from src.utils import log_agent_execution as write_log
from src.agents.sql_agent import execute_sql_query
from src.agents.rag_agent import execute_rag_query




def classify_query(query: str) -> str:
    """
    Classify query as 'sql', 'rag', or 'hybrid'.
    
    Args:
        query: User's natural language question
        
    Returns:
        Classification: 'sql', 'rag', or 'hybrid'
    """
    llm = get_llm(temperature=0)
    prompt_message = load_prompt("classify_query")
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt_message),
        ("user", "{query}")
    ])
    
    response = llm.invoke(prompt_template.format_messages(query=query))
    category = response.content.strip().lower()
    
    # Normalize
    if category in ["sql", "rag", "hybrid"]:
        return category
    elif "sql" in category:
        return "sql"
    elif "rag" in category:
        return "rag"
    else:
        return "hybrid"


def execute_hybrid_query(
    query: str,
    log_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a hybrid query by routing to appropriate agent(s).
    
    Args:
        query: User's question
        log_file: Optional log file path
        
    Returns:
        Dict with 'answer', 'route', and metadata
    """
    # Classify
    route = classify_query(query)
    print(f"Route: {route}")
    
    # Log classification
    write_log({
        "agent_type": "classifier",
        "query": query,
        "classification": route
    }, log_file=log_file, log_type="classification")
    
    # Execute based on route
    if route == "sql":
        sql_result = execute_sql_query(query, log_file)
        return {
            "answer": sql_result["answer"],
            "route": "sql",
            "sql_result": sql_result
        }
    
    elif route == "rag":
        rag_result = execute_rag_query(query, log_file=log_file)
        return {
            "answer": rag_result["answer"],
            "route": "rag",
            "rag_result": rag_result
        }
    
    else:  # hybrid
        # Get both results
        sql_result = execute_sql_query(query, log_file)
        rag_result = execute_rag_query(query, log_file=log_file)
        
        # Synthesize
        llm = get_llm(temperature=0)
        summarization_prompt = load_prompt("hybrid_summarization_prompt")
        
        template = ChatPromptTemplate.from_messages([
            ("system", summarization_prompt),
            ("user", "{sql_answer}\n\n{rag_answer}")
        ])
        
        final_response = llm.invoke(template.format_messages(
            sql_answer=sql_result["answer"],
            rag_answer=rag_result["answer"]
        ))
        
        return {
            "answer": final_response.content,
            "route": "hybrid",
            "sql_result": sql_result,
            "rag_result": rag_result
        }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hybrid Agent - SQL + RAG")
    parser.add_argument("--query", "-q", required=True, help="Question to ask")
    parser.add_argument("--log_file", "-l", help="Log file path")
    args = parser.parse_args()
    
    result = execute_hybrid_query(args.query, args.log_file)
    print("Answer:", result["answer"])