"""
Rule-Based Document Question Answering System
Student: Akarsh | Register No: 25ETAI410012
Course: AID201A - Artificial Intelligence

This program uses simple document parsing, a structured knowledge base,
keyword-based retrieval, and explicit inference rules. It does NOT use NLP
libraries, embeddings, large language models, or RAG.
"""

import re
from pathlib import Path

SAMPLE_DOCUMENT = """\
Artificial Intelligence (AI) is the field of building machines that can perform
tasks requiring human-like intelligence.
An intelligent agent perceives its environment through sensors and acts upon
that environment through actuators.
A knowledge base stores facts about a domain in a structured form.
Breadth First Search (BFS) explores nodes level by level and uses a queue.
Depth First Search (DFS) explores a path as deeply as possible before backtracking
and uses a stack.
A heuristic is an estimate that helps a search algorithm choose a promising path.
A* search uses the evaluation function f(n) = g(n) + h(n).
"""

def split_into_sentences(document_text):
    """Split a plain-text document into sentence-like units."""
    cleaned = re.sub(r"\s+", " ", document_text).strip()
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]

def build_knowledge_base(document_text):
    """
    Convert each sentence into a fact record.
    A small rule-based subject detector assigns a topic where possible.
    """
    topic_terms = {
        "artificial intelligence": ["artificial intelligence", " ai "],
        "intelligent agent": ["intelligent agent", "sensors", "actuators"],
        "knowledge base": ["knowledge base"],
        "breadth first search": ["breadth first search", " bfs "],
        "depth first search": ["depth first search", " dfs "],
        "heuristic": ["heuristic"],
        "a star search": ["a* search", "a star"]
    }
    facts = []
    for number, sentence in enumerate(split_into_sentences(document_text), start=1):
        padded = " " + sentence.lower() + " "
        topic = "general"
        for label, patterns in topic_terms.items():
            if any(pattern in padded for pattern in patterns):
                topic = label
                break
        facts.append({
            "id": number,
            "topic": topic,
            "statement": sentence
        })
    return facts

STOP_WORDS = {
    "what", "is", "are", "the", "a", "an", "of", "in", "on", "and",
    "does", "do", "how", "which", "explain", "define", "tell", "me",
    "about", "use", "uses", "used", "by", "to", "for", "it"
}

def question_terms(question):
    """Normalize a question using lowercase and simple word filtering."""
    words = re.findall(r"[a-zA-Z0-9*]+", question.lower())
    return {word for word in words if word not in STOP_WORDS and len(word) > 1}

def retrieve_facts(question, knowledge_base):
    """Rank facts by the number of question terms found in each statement."""
    terms = question_terms(question)
    ranked = []
    for fact in knowledge_base:
        statement_words = set(re.findall(r"[a-zA-Z0-9*]+", fact["statement"].lower()))
        score = len(terms.intersection(statement_words))
        if score > 0:
            ranked.append((score, fact))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [fact for _, fact in ranked]

def infer_answer(question, knowledge_base):
    """Apply small explicit rules, otherwise return the best retrieved fact."""
    q = question.lower().strip()
    results = retrieve_facts(question, knowledge_base)

    # Rule 1: identify the data structure used by BFS or DFS.
    if "bfs" in q or "breadth first search" in q:
        for fact in knowledge_base:
            if fact["topic"] == "breadth first search":
                if "queue" in fact["statement"].lower():
                    return "Breadth First Search (BFS) uses a queue. " + fact["statement"]
                return fact["statement"]

    if "dfs" in q or "depth first search" in q:
        for fact in knowledge_base:
            if fact["topic"] == "depth first search":
                if "stack" in fact["statement"].lower():
                    return "Depth First Search (DFS) uses a stack. " + fact["statement"]
                return fact["statement"]

    # Rule 2: explain the A* evaluation formula from its stored fact.
    if "a*" in q or "a star" in q:
        for fact in knowledge_base:
            if fact["topic"] == "a star search":
                return "A* search evaluates a node using f(n) = g(n) + h(n). " + fact["statement"]

    # Rule 3: return an explicit not-found response rather than inventing facts.
    if not results:
        return "The answer is not available in the supplied document."

    best_score = len(question_terms(question).intersection(
        set(re.findall(r"[a-zA-Z0-9*]+", results[0]["statement"].lower()))
    ))
    tied = [fact for fact in results if len(question_terms(question).intersection(
        set(re.findall(r"[a-zA-Z0-9*]+", fact["statement"].lower()))
    )) == best_score]
    return " ".join(fact["statement"] for fact in tied[:2])

def load_document():
    path_text = input("Enter the path of a .txt document (press Enter for sample): ").strip()
    if not path_text:
        return SAMPLE_DOCUMENT
    path = Path(path_text)
    if not path.exists() or path.suffix.lower() != ".txt":
        print("File not found or unsupported format. Loading the sample document.")
        return SAMPLE_DOCUMENT
    return path.read_text(encoding="utf-8")

def main():
    document = load_document()
    kb = build_knowledge_base(document)
    print(f"Knowledge base created with {len(kb)} fact(s).")
    print("Ask questions about the document. Type 'exit' to stop.")
    while True:
        question = input("\\nQuestion: ").strip()
        if question.lower() == "exit":
            break
        print("Answer:", infer_answer(question, kb))

if __name__ == "__main__":
    main()
