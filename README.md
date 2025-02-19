# AI Assistant with Embedding-Based Context Retrieval

This project is an AI-powered assistant that utilizes embedding-based context retrieval to find the most relevant text chunks from a database and generate responses using a pre-trained language model.

## Features
- Stores text embeddings in a DuckDB database.
- Retrieves the most relevant text chunks using cosine similarity.
- Uses SentenceTransformers for embedding generation.
- Implements DistilBERT for answering user queries based on retrieved context.
- Extracts text from PDFs, chunks it, and stores it in a database.

## Installation
### Prerequisites
Ensure you have Python installed along with the necessary dependencies:
```sh
pip install duckdb numpy sentence-transformers torch transformers PyPDF2 pandas
```
You can also use the requirements file:
```sh
pip install requirements.txt
```

## File Overview

### 1. `pdf_processor.py`
- Extracts text from PDF files.
- Splits extracted text into overlapping chunks.
- Generates embeddings for each chunk and stores them in the database.
- Allows processing of multiple PDFs in a folder and saves them for retrieval.

### 2. `database_handling.py`
- Initializes a DuckDB database to store text embeddings.
- Provides functions to insert and retrieve text chunks by ID.

### 3. `embeddings.py`
- Uses SentenceTransformers to generate vector embeddings for text chunks.

### 4. `query_chunk.py`
- Computes cosine similarity to find the top-k most relevant text chunks.
- Implements a multi-threaded approach for efficient similarity computation.

### 5. `main_run_assistant.py`
- Loads the DistilBERT model for answering user questions.
- Retrieves relevant text chunks from the database.
- Forms a structured prompt using retrieved chunks and provides AI-generated responses.


## Usage

To process PDFs and store their text embeddings, run:
```sh
python pdf_processor.py
```

Run the assistant by executing:
```sh
python main_run_assistant.py
```
You can then enter questions, and the assistant will retrieve relevant text chunks before generating an answer.


## Further Improvements to come

1. Integrate the pdf processing phase into the main pipeline
2. Look up for new pdf addition when launching the assistant and update database accordingly
3. Build and deploy (Docker/API)
