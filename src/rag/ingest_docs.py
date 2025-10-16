from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import json

def load_and_split_documents(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Load and split documents from a given file path.

    Args:
        file_path (str): Path to the document file (PDF or text).
        chunk_size (int): Size of each text chunk.
        chunk_overlap (int): Overlap between chunks.
    Returns:
        List of text chunks.
    """
    if file_path.lower().endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith('.txt'):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and TXT are supported.")

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


def read_documents_from_folder(folder_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Read and split documents from all files in a given folder.

    Args:
        folder_path (str): Path to the folder containing document files.
        chunk_size (int): Size of each text chunk.
        chunk_overlap (int): Overlap between chunks.
    Returns:
        List of text chunks from all documents.
    """
    all_chunks = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and (filename.lower().endswith('.pdf') or filename.lower().endswith('.txt')):
            chunks = load_and_split_documents(file_path, chunk_size, chunk_overlap)
            all_chunks.extend(chunks)
    return all_chunks


def save_chunks_to_files(chunks, output_folder: str):
    """
    Save text chunks to individual text files in the specified output folder, in jsonl format.

    Args:
        chunks (list): List of text chunks.
        output_folder (str): Path to the output folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, "documents.jsonl"), 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            # Save each chunk as a JSON line
            f.write(json.dumps({"text": chunk.page_content, "metadata": chunk.metadata}) + "\n")
    

if __name__ == "__main__":
    input_folder = "data/docs"
    output_folder = "data/processed_documents"
    chunk_size = 1000
    chunk_overlap = 200

    chunks = read_documents_from_folder(input_folder, chunk_size, chunk_overlap)
    save_chunks_to_files(chunks, output_folder)
    print(f"Processed {len(chunks)} chunks and saved to {output_folder}")