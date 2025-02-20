import duckdb
import numpy as np

def init_database(database_name):
    # Connect (creates a file-based database)
    conn = duckdb.connect(database_name)

    # Create table with vector support
    conn.execute("""
        CREATE TABLE IF NOT EXISTS text_embeddings (
            chunk_id TEXT,
            text_chunk TEXT,
            embedding FLOAT[384]  -- Native array support!
        )
    """)
    # Create table to track processed PDFs
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed_pdfs (
            pdf_name TEXT PRIMARY KEY
        )
    """)
    print(f"successfully initialized {database_name}")
    return conn

def add_chunk_to_database(conn,chunk_id,text_chunk,embedding):
    """Add chunk into the database"""
    try:
        conn.execute("INSERT INTO text_embeddings (chunk_id,text_chunk, embedding) VALUES (?,?,?)", (chunk_id, text_chunk, embedding))
    except Exception as e:
        print(f"Error ! Could not add Chunk:{chunk_id} to the database because of:\n{e}")

        return False
    return True

def get_chunks_by_ids(conn, chunk_ids):
    """Query text chunks based on their ids"""
    if not chunk_ids:
        return []
    
    query = "SELECT text_chunk FROM text_embeddings WHERE chunk_id IN ({})".format(
        ','.join(['?'] * len(chunk_ids))
    )
    
    results = conn.execute(query, chunk_ids).fetchall()
    return [chunk[0] for chunk in results]

def is_pdf_processed(conn, pdf_name):
    """Check if a PDF file has already been processed."""
    result = conn.execute("SELECT COUNT(*) FROM processed_pdfs WHERE pdf_name = ?", (pdf_name,)).fetchone()
    return result[0] > 0

def mark_pdf_as_processed(conn, pdf_name):
    """Mark a PDF as processed."""
    conn.execute("INSERT INTO processed_pdfs (pdf_name) VALUES (?)", (pdf_name,))