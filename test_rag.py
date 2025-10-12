"""
Test RAG system with OpenAI
"""
from src.rag.retriever import RAGRetriever
from src.utils.logger import logger


def test_rag():
    """Test RAG functionality with OpenAI"""

    print("\n" + "="*60)
    print("🧠 Testing RAG System with OpenAI")
    print("="*60 + "\n")

    # Initialize RAG (will build vector store)
    print("Initializing RAG system...")
    rag = RAGRetriever(reset_db=True)

    # Get stats
    stats = rag.get_stats()
    print(f"\n✅ RAG System Ready!")
    print(f"   Documents indexed: {stats['vector_store']['document_count']}")
    print(f"   LLM Provider: {stats['llm']['provider']}")
    print(f"   LLM Model: {stats['llm']['model']}")
    print(f"   Framework: {stats['framework']}")

    # Test queries
    test_questions = [
        "How many years of experience does Sarjak have?",
        "What technologies is Sarjak skilled in for AI development?",
        "Tell me about Sarjak's work at XNODE Inc.",
        "What AI projects has Sarjak built?",
        "Where did Sarjak study and what was his GPA?",
    ]

    print("\n" + "="*60)
    print("🤖 Testing Queries")
    print("="*60 + "\n")

    for i, question in enumerate(test_questions, 1):
        print(f"❓ Q{i}: {question}")
        answer = rag.answer_query(question)
        print(f"💡 A{i}: {answer}\n")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    test_rag()
