
# RAG System Evaluation Report

## 1. Evaluation Objective

Evaluate whether the RAG system can:

- Retrieve course-specific content.
- Generate relevant educational answers.
- Display supporting source references.
- Reject questions outside the course scope.
- Retrieve data from four file formats.
- Run locally through Gradio.

## 2. Dataset Summary

| Course | PDF | DOCX | CSV | TXT |
|---|---:|---:|---:|---:|
| Computer Networks | 145 | 5 | 17 | 9 |
| Database Systems | 267 | 7 | 16 | 9 |
| Python Programming | 542 | 11 | 41 | 11 |
| Total | 954 | 23 | 74 | 29 |

Total vector records: 1080

Note: The counts represent chunks,
not the number of source files.

## 3. Positive Question Tests

| Course | Test Question | Result |
|---|---|---|
| Python | What is a Python function? | Answer generated |
| Database | What is a primary key? | Answer generated |
| Database | What is database normalization? | Answer generated |
| Networks | What is an IP address? | Answer generated |

These tests showed relevant responses
with retrieved source information.

## 4. Negative Question Tests

| Course | Question | Result |
|---|---|---|
| Database | Who won the FIFA World Cup in 2022? | Refused |
| Python | What is the capital of France? | Refused |
| Networks | Explain how photosynthesis works. | Refused |

Observed result: 3/3 negative tests passed.

The responses stated that the answers
could not be found in course materials.

This is a small test set and does not
prove that hallucinations are impossible.

## 5. Multi-Format Retrieval

Formats tested:
- PDF: Passed
- DOCX: Passed
- CSV: Passed
- TXT: Passed

Observed result: 4/4 format smoke tests passed.

This confirms that indexed content
could be retrieved from each format.

It is not a full answer-quality
benchmark for all document formats.

## 6. Local Deployment Tests

- Python environment installed.
- ChromaDB opened successfully.
- 1080 stored chunks verified.
- Embedding model loaded.
- Gemini API connection tested.
- Gradio interface launched locally.
- Question answering tested through UI.
- Source references displayed.

## 7. Qualitative Observations

The system generated relevant answers
for several course-related questions.

Some retrieval results contained less
relevant text or duplicate information.

Basic filtering was added to reduce
repeated and unnecessary chunks.

## 8. Limitations

- Small manually selected evaluation set.
- No measured retrieval precision or recall.
- No quantitative faithfulness benchmark.
- Some content duplicated across formats.
- Source correctness requires human review.
- Gemini output may vary between runs.

## 9. Conclusion

The system successfully demonstrated
a functional local end-to-end RAG pipeline.

The observed tests support the project's
core functionality, while larger-scale
evaluation remains future work.
