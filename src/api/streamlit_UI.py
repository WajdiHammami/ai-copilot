import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from src.agents.hybrid_agent import execute_hybrid_query

st.title("Enterprise AI Copilot")

q = st.text_input("Ask a question")

if st.button("Ask"):
    if q.strip():
        with st.spinner("Thinking..."):
            result = execute_hybrid_query(q)
        
        st.markdown(f"**Answer:**\n\n{result['answer']}")
    else:
        st.warning("Please enter a question!")