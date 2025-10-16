from pathlib import Path
import os
import json
from typing import Any, Dict, Optional
import sys


DEFAULT_LOG_DIR = "logs"
DEFAULT_LOG_FILE = "agent_executions.jsonl"



def load_prompt(prompt_name: str) -> str:
    prompt_path = Path(__file__).parent / "prompts" / f"{prompt_name}.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
    

def log_agent_execution(log_entry: dict, log_file: str, log_type: str = "generic"):
    """
    Append a log entry to a JSONL file in a safe, consistent way.
    
    Args:
        log_entry: Dictionary containing log data
        log_file: Path to log file. If None, uses default path.
        log_type: Type of log for organizing files (e.g., 'sql', 'rag', 'hybrid')
    """
    if log_file is None:
        log_file = os.path.join(DEFAULT_LOG_DIR, log_type, DEFAULT_LOG_FILE)

    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    if "timestamp" not in log_entry:
        from datetime import datetime
        log_entry["timestamp"] = datetime.now().isoformat()

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Failed to write log to {log_file}: {e}", file=sys.stderr)
        print(f"Log entry: {json.dumps(log_entry, ensure_ascii=False)}", file=sys.stderr)


def read_logs(log_file: str) -> list:
    """
    Read all log entries from a JSONL file.
    
    Args:
        log_file: Path to the log file
        
    Returns:
        List of log entry dictionaries
    """
    if not os.path.exists(log_file):
        return []
    
    logs = []
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Failed to read logs from {log_file}: {e}", file=sys.stderr)
    
    return logs 
    