# RAG with FastAPI

A Retrieval-Augmented Generation (RAG) system built with FastAPI that allows you to upload documents, process them into chunks with embeddings, and ask questions about the content using OpenAI's GPT models.

## Features

- **Document Upload**: Upload PDF and TXT files for processing
- **Intelligent Parsing**: Supports both text extraction and OCR for PDF files
- **Chunking & Embeddings**: Automatically chunks documents and creates embeddings using OpenAI's text-embedding-ada-002
- **Vector Search**: Uses PostgreSQL with pgvector extension for efficient similarity search
- **Question Answering**: Ask questions about uploaded documents using GPT-3.5-turbo
- **Background Processing**: File processing happens asynchronously to avoid blocking API requests

## Architecture

The system consists of several key components:

- **FastAPI Application** (`main.py`): Main API server with endpoints for file upload, question answering, and document retrieval
- **Database Layer** (`db.py`): PostgreSQL database with pgvector for storing files, chunks, and embeddings
- **File Parser** (`file_parser.py`): Modular parser system supporting TXT and PDF files with OCR fallback
- **Background Tasks** (`background_tasks.py`): Handles text chunking and embedding generation
- **Testing** (`api_tests.sh`): Automated API testing script

## Prerequisites

- Python 3.8+
- PostgreSQL with pgvector extension
- OpenAI API key
- Tesseract OCR (for PDF processing)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rag_with_fastapi
   ```

2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary sqlalchemy-utils pgvector python-dotenv openai nltk PyPDF2 pytesseract pillow PyMuPDF
   ```

3. **Set up PostgreSQL with pgvector**:
   ```bash
   # Install pgvector extension
   # Follow instructions at: https://github.com/pgvector/pgvector
   ```

4. **Set up the database**:
   Run the database setup script:
   ```bash
   chmod +x db_user.sh
   ./db_user.sh
   ```

5. **Download NLTK data**:
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

## Usage

1. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Upload a document**:
   ```bash
   curl -X POST "http://localhost:8000/uploadfile/" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@your_document.pdf"
   ```

3. **Ask a question**:
   ```bash
   curl -X POST "http://localhost:8000/ask/" \
        -H "Content-Type: application/json" \
        -d '{"document_id": 1, "question": "What is this document about?"}'
   ```

4. **Find similar chunks**:
   ```bash
   curl -X POST "http://localhost:8000/find-similar-chunks/1" \
        -H "Content-Type: application/json" \
        -d '{"question": "What are the key points?"}'
   ```

## API Endpoints

### `GET /`
Returns a list of all uploaded files with their IDs and names.

### `POST /uploadfile/`
Upload a PDF or TXT file for processing.
- **Parameters**: `file` (multipart/form-data)
- **Returns**: File upload confirmation with filename

### `POST /ask/`
Ask a question about a specific document.
- **Parameters**: 
  - `document_id` (int): ID of the document
  - `question` (str): Your question
- **Returns**: AI-generated answer based on document content

### `POST /find-similar-chunks/{file_id}`
Find text chunks similar to your question.
- **Parameters**: 
  - `file_id` (int): ID of the document
  - `question` (str): Your question
- **Returns**: List of similar text chunks with relevance scores

## File Structure

```
rag_with_fastapi/
├── main.py                 # FastAPI application and API endpoints
├── db.py                   # Database models and connection setup
├── file_parser.py          # Document parsing (TXT, PDF with OCR)
├── background_tasks.py     # Text chunking and embedding generation
├── api_tests.sh           # API testing script
├── db_test.py             # Database connection test
├── file_parser_tests.py   # File parser tests
├── sources/               # Directory for uploaded files
└── README.md              # This file
```

## Database Schema

### Files Table
- `file_id`: Primary key
- `file_name`: Original filename
- `file_content`: Full text content

### File Chunks Table
- `chunk_id`: Primary key
- `file_id`: Foreign key to files table
- `chunk_text`: Text content of the chunk
- `embedding_vector`: Vector embedding (1536 dimensions)

## Testing

Run the automated test script:
```bash
chmod +x api_tests.sh
./api_tests.sh
```

This will:
1. Upload a test file
2. List all files
3. Wait for processing
4. Test question answering
5. Test similar chunk retrieval

## Key Features

### Document Processing
- **PDF Support**: Extracts text from PDFs, falls back to OCR for scanned documents
- **Text Files**: Direct text file processing
- **Chunking**: Intelligent sentence-based chunking for optimal retrieval

### Vector Search
- Uses OpenAI's text-embedding-ada-002 for embeddings
- PostgreSQL with pgvector for efficient similarity search
- L2 distance for finding most relevant chunks

### Background Processing
- File upload returns immediately
- Text processing and embedding generation happens asynchronously
- Prevents API timeouts for large documents

## Configuration

The system is highly configurable through environment variables:

- **Database**: PostgreSQL connection settings
- **OpenAI**: API key for embeddings and chat completions
- **Chunking**: Configurable chunk size (default: 2 sentences)
