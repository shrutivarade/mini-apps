# RAG (Retrieval-Augmented Generation) Project

This project implements a RAG system that allows you to query a PDF document using vector embeddings and OpenAI's language models. The system processes a PDF, creates embeddings, stores them in a Qdrant vector database, and enables semantic search with AI-powered responses.

## Architecture

- **Document Processing**: PDF loading and text chunking using LangChain
- **Vector Database**: Qdrant for storing and retrieving embeddings
- **Embeddings**: OpenAI's `text-embedding-3-large` model
- **LLM**: OpenAI's GPT-4.1 for generating responses
- **Containerization**: Docker Compose for vector database

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API key

## Setup Instructions

### 1. Environment Setup

Since you're using a common virtual environment, ensure it's activated:

```bash
# Navigate to the project root
cd "/Users/shrutivarade/D drive/mini-apps"

# Activate the virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

The required packages should already be installed in your common requirements.txt. If you need to install additional dependencies specific to this project:

```bash
pip install langchain-community langchain-text-splitters langchain-openai langchain-qdrant pypdf qdrant-client
```

### 3. Environment Variables

Create a `.env` file in the `04-RAG` directory:

```bash
cd 04-RAG
touch .env
```

Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Start Vector Database

- Pre req: Docker installed

Start the Qdrant vector database using Docker Compose:

```bash
# Make sure you're in the 04-RAG directory
docker-compose up -d
```

This will start Qdrant on `http://localhost:6333`.

## Execution Steps

### Step 1: Index the PDF Document

First, run the indexing script to process the PDF and create vector embeddings:

```bash
python indexing.py
```

This script will:
- Load the PDF document (`data.pdf`)
- Split it into chunks (1000 characters with 400 character overlap)
- Create embeddings using OpenAI's embedding model
- Store the embeddings in Qdrant vector database

You should see the output: `"Indexing of Documents Done..."`

### Step 2: Query the Document

Run the main application to start querying:

```bash
python main.py
```

The application will:
- Connect to the existing vector database
- Prompt you to enter a query
- Perform semantic search to find relevant document chunks
- Generate an AI response based on the retrieved context
- Provide page numbers for reference

## Usage Example

```bash
$ python main.py
> What is the main topic of this document?
🤖: Based on the provided context from the PDF, [AI response with relevant information and page references]
```

## Project Structure

```
04-RAG/
├── README.md              # This file
├── docker-compose.yml     # Qdrant vector database configuration
├── indexing.py           # PDF processing and vector indexing
├── main.py              # Main query interface
├── data.pdf             # Source PDF document
└── .env                 # Environment variables (create this)
```

## File Descriptions

- **`indexing.py`**: Processes the PDF document, creates text chunks, generates embeddings, and stores them in the vector database
- **`main.py`**: Interactive query interface that performs semantic search and generates AI responses
- **`docker-compose.yml`**: Configuration for running Qdrant vector database
- **`data.pdf`**: The source document for the RAG system

## Troubleshooting

### Vector Database Connection Issues
- Ensure Docker is running: `docker ps`
- Check if Qdrant is accessible: `curl http://localhost:6333/health`
- Restart the database: `docker-compose restart`

### OpenAI API Issues
- Verify your API key is correct in the `.env` file
- Check your OpenAI account has sufficient credits
- Ensure the model names are correct (`text-embedding-3-large`, `gpt-4.1`)

### Missing Dependencies
```bash
pip install langchain-community langchain-text-splitters langchain-openai langchain-qdrant pypdf qdrant-client
```

## Cleanup

To stop the vector database:

```bash
docker-compose down
```

To remove the vector database data:

```bash
docker-compose down -v
```

## Notes

- The vector database runs on port 6333
- Embeddings are stored in a collection named "learning_vectors"
- The system uses a chunk size of 1000 characters with 400 character overlap
- Responses include page number references for easy navigation
- This project shares the virtual environment with other mini-apps in the workspace
