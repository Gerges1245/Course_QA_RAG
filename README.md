
# Course Q&A RAG System

## Project Overview

This project implements a Retrieval-Augmented
Generation (RAG) system that answers student
questions using educational course materials.

The system retrieves relevant information from
course documents and uses Google's Gemini LLM
to generate answers with source references.

## Objectives

- Build an end-to-end RAG pipeline.
- Support three different courses.
- Extract text from PDF, DOCX, CSV and TXT.
- Generate semantic embeddings.
- Store embeddings in ChromaDB.
- Retrieve relevant course information.
- Generate answers using Gemini.
- Display source references and page numbers.
- Provide a user-friendly Gradio interface.

## Supported Courses

1. Python Programming
2. Database Systems
3. Computer Networks

## Technologies

| Component | Technology |
|---|---|
| Programming | Python 3.11 |
| PDF Extraction | PyMuPDF |
| DOCX Extraction | python-docx |
| CSV Processing | Pandas |
| Embeddings | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| LLM | Google Gemini API |
| Interface | Gradio |

## Dataset Statistics

- Courses: 3
- File types: PDF, DOCX, CSV, TXT
- Total vector records: 1,080
- PDF chunks: 954
- Additional format chunks: 126
- Embedding dimensions: 384

The DOCX, CSV, and TXT test files were
derived from the source PDF books.

## RAG Pipeline

1. Load course documents.
2. Extract and clean the text.
3. Divide documents into chunks.
4. Generate text embeddings.
5. Store embeddings in ChromaDB.
6. Convert the student's question into
   an embedding.
7. Retrieve relevant chunks using
   semantic similarity.
8. Provide retrieved context to Gemini.
9. Generate a grounded answer.
10. Display the answer and its sources.

## Local Installation

Requirements:
- Windows
- Python 3.11
- Internet connection for Gemini API
- Gemini API key

Create a virtual environment:

    py -3.11 -m venv .venv

Install the dependencies:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Create a `.env` file based on `.env.example`
and add your Gemini API key.

Run the application:

    .\.venv\Scripts\python.exe app.py

Open the local Gradio URL displayed
in the terminal, usually:

http://127.0.0.1:7860

## How to Use

1. Select a course.
2. Select All Files or a file type.
3. Enter a question.
4. Click Send.
5. Read the AI-generated response.
6. Review retrieved sources.

## Features

- Course-specific retrieval
- Multi-format document support
- Semantic similarity search
- Context-grounded answer generation
- Source attribution
- Chat interface
- Suggested questions
- Clear Chat functionality

## Testing

The project was tested using:
- Questions from all three courses
- Out-of-scope questions
- Document retrieval for all four formats
- Local Gradio interface tests

See EVALUATION.md for the observed results.

## Limitations

- Answer quality depends on retrieved context.
- AI-generated answers require verification.
- Some data is duplicated across formats.
- Page numbers may refer to PDF page positions.
- Adding new documents requires re-indexing.
- The system requires Gemini API access.

## Security

Keep the Gemini API key in `.env`.
Never publish real API keys.

## Project Status

The local RAG application has been
implemented and functionally tested.

## Author

Gerges William