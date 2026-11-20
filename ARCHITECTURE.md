
# RAG System Architecture

## 1. System Overview

The system consists of two main pipelines:

- Document Indexing Pipeline
- Question Answering Pipeline

## 2. Document Indexing Pipeline

Course Materials
(PDF / DOCX / CSV / TXT)
         |
         v
Text Extraction
         |
         v
Text Cleaning
         |
         v
Text Chunking
         |
         v
Sentence Transformers
(all-MiniLM-L6-v2)
         |
         v
384-Dimensional Embeddings
         |
         v
ChromaDB Vector Database

## 3. Question Answering Pipeline

Student Question
         |
         v
Gradio Interface
         |
         v
Question Embedding
         |
         v
ChromaDB Semantic Search
         |
         v
Course and File-Type Filtering
         |
         v
Relevant Chunks
         |
         v
Context + Grounding Instructions
         |
         v
Gemini LLM
         |
         v
Answer with Source References
         |
         v
Gradio Chat Interface

## 4. Components

### Document Loader

Processes four file types:
PDF, DOCX, CSV and TXT.

### Text Chunking

The initial indexing process used:
- Chunk size: 180 words
- Chunk overlap: 30 words

Short chunks may be excluded.

### Embedding Model

Model: all-MiniLM-L6-v2

Embedding dimension: 384

Purpose: represent text numerically
for semantic similarity search.

### Vector Database

Database: ChromaDB

Collection:
course_materials_all_formats_v1

Stored records: 1080

Each record contains text and metadata,
including course, file type, source
filename and page information.

### Retriever

The retriever:
- Embeds the user question
- Filters by course
- Optionally filters by file type
- Retrieves similar chunks
- Applies basic duplicate filtering
- Returns relevant context

### Gemini LLM

Gemini receives retrieved course context
and generates an educational response.

The prompt instructs the model not to
use outside knowledge and to cite sources.

These instructions reduce, but do not
eliminate, hallucination risks.

### Gradio Interface

The interface allows students to:
- Select a course
- Choose a file type
- Ask questions
- View answers and sources
- Clear previous messages
- Use suggested questions

## 5. Source Attribution

Each retrieved chunk retains metadata
that identifies its original file.

PDF/CSV records may contain a page number.

For records without page metadata,
the interface displays page unavailable.

Retrieved sources are presented to help
users verify the generated answer.
