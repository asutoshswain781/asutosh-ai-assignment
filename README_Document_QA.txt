HOW TO RUN
1. Install Python 3.8 or later. No external packages are required.
2. Save document_qa_system.py.
3. Run: python document_qa_system.py
4. Press Enter to use the built-in sample document, or enter the path to a .txt file.
5. Ask questions and type exit to close the program.

LIMITATIONS
- Input is plain-text (.txt); PDF/DOCX conversion is outside this prototype.
- Retrieval is based on word overlap, so it may miss synonyms or complex questions.
- The system only answers from extracted sentences and its three explicit rules.
- It does not use NLP, embeddings, a language model, or RAG.
