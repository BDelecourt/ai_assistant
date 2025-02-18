import PyPDF2
import re
import os
from database_handling import init_database, add_to_database
from embeddings import generate_embedding
import pandas as pd

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Function to chunk text by words with overlap
def text_chunker_by_words(text, chunk_size=100, overlap_size=20):
    words = re.findall(r'\S+', text)  # Split the text into words
    chunks = []
    start = 0
    
    while start < len(words)-overlap_size:
        # Determine the end index for the chunk
        end = min(start + chunk_size, len(words))
        
        # Create the chunk by joining the words from 'start' to 'end'
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        
        # Move the start index forward to create overlap
        start = max(0, end - overlap_size)
    
    return chunks

def process_pdfs(pdf_folder_path,chunk_size=100, overlap_size=20):
    
    conn=init_database("chunck_database.db")

    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.lower().endswith(".pdf")]
    
    try:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_folder_path, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]  # Extract PDF name once
            
            # Extract text from the PDF
            text = extract_text_from_pdf(pdf_path)
            
            # Chunk the text
            chunks = text_chunker_by_words(text, chunk_size, overlap_size)
            
            # Assign IDs to each chunk
            for i, chunk in enumerate(chunks):
                chunk_id = f"{pdf_name}_chunk_{i+1}"
                chunk_vector=generate_embedding(chunk)
                add_to_database(conn,chunk_id,chunk,chunk_vector)
    except:
        return False
    
    return conn

conn=process_pdfs(r"C:\dev\GitHub\ai_assistant\test_documents",chunk_size=100, overlap_size=20)

# Run SQL query and fetch results as a Pandas DataFrame
result = conn.execute("SELECT * FROM text_embeddings LIMIT 10").fetchdf()

# Show the result (Pandas DataFrame)

print(result.head())
