"""RAG Agent - Retrieval-Augmented Generation from documents."""


from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from langchain.chains import RetrievalQA
from src.config.settings import get_llm, load_vector_store, DEFAULT_FAISS_INDEX_PATH
from src.utils import log_agent_execution
import json


# Module-level Cache
_qa_chain = None
_current_index_path = None

def _get_qa_chain(index_path: str = DEFAULT_FAISS_INDEX_PATH) -> RetrievalQA:
    """
    Get or create the RAG QA chain (cached per index path).
    
    Args:
        index_path: Path to FAISS index directory
        
    Returns:
        RetrievalQA chain instance
    """
    global _qa_chain, _current_index_path
    
    # Reload if path changed
    if _qa_chain is None or _current_index_path != index_path:
        llm = get_llm(temperature=0)
        vector_store = load_vector_store(index_path)
        
        _qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            ),
            return_source_documents=True,
        )
        _current_index_path = index_path
    
    return _qa_chain




def execute_rag_query(
    question: str,
    index_path: str = DEFAULT_FAISS_INDEX_PATH,
    log_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a RAG query against the document index.
    
    Args:
        question: Natural language question
        index_path: Path to FAISS index
        log_file: Optional path to log file
        
    Returns:
        Dict with 'answer', 'source_documents', and 'duration_seconds'
    """
    qa_chain = _get_qa_chain(index_path)
    start_time = datetime.now()
    
    log_entry = {
        "agent_type": "rag",
        "question": question,
        "answer": "",
        "source_documents": [],
        "duration_seconds": 0,
        "num_sources": 0
    }
    
    try:
        result = qa_chain.invoke({"query": question})
        
        source_docs = [
            {
                "content": doc.page_content[:200],  # Truncate for logs
                "metadata": doc.metadata
            }
            for doc in result["source_documents"]
        ]
        
        log_entry["answer"] = result["result"]
        log_entry["source_documents"] = source_docs
        log_entry["num_sources"] = len(source_docs)
        
        response = {
            "answer": result["result"],
            "source_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in result["source_documents"]
            ],
        }
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        log_entry["error"] = str(e)
        log_entry["answer"] = error_msg
        
        response = {
            "answer": error_msg,
            "error": str(e),
            "source_documents": [],
        }
    
    # Duration
    log_entry["duration_seconds"] = (datetime.now() - start_time).total_seconds()
    response["duration_seconds"] = log_entry["duration_seconds"]
    
    # Log
    log_agent_execution(log_entry, log_file=log_file, log_type="rag")
    
    return response



if __name__ == "__main__":
    import argparse


    argparser = argparse.ArgumentParser(description="RAG Agent for answering queries using FAISS index.")
    argparser.add_argument("--index_path", "-i", type=str, default=DEFAULT_FAISS_INDEX_PATH, help="Path to the FAISS index.")
    argparser.add_argument("--query", "-q", type=str, required=True, help="Query to be answered.")
    argparser.add_argument("--output", "-o", type=str, help="Path to the output JSON file.")
    argparser.add_argument("--log_file", "-l", type=str, help="Path to the log file.")
    args = argparser.parse_args()

    result = execute_rag_query(args.query, args.index_path, args.log_file)

    # Print to console
    print(f"\nAnswer: {result['answer']}\n")
    print(f"Sources: {len(result.get('source_documents', []))} documents")
    print(f"Duration: {result.get('duration_seconds', 0):.2f}s\n")

    # Optionally save to JSON file
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=4)
        print(f"Saved to: {args.output}")
