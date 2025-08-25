#!/usr/bin/env python3
"""
Example usage of the Knowledge Worker RAG Application

This script shows how to use the KnowledgeWorker class in your own code.
"""

from knowledge_worker import KnowledgeWorker

def main():
    """Example of how to use the KnowledgeWorker"""

    print("🚀 Knowledge Worker Example")
    print("=" * 40)

    # Create a knowledge worker instance
    # You can specify a custom knowledge base path
    kw = KnowledgeWorker(knowledge_base_path="knowledge-base")

    try:
        # Run the full setup (loads documents, creates embeddings, sets up conversation)
        print("Setting up knowledge worker...")
        kw.run_full_setup()

        # Ask some questions
        questions = [
            "What is Insurellm?",
            "What products does the company offer?",
            "Who are some key employees?",
            "Tell me about the company's contracts"
        ]

        print("\nAsking questions:")
        for question in questions:
            print(f"\nQ: {question}")
            answer = kw.ask_question(question)
            print(f"A: {answer}")
            print("-" * 50)

        # You can also visualize the vector embeddings
        print("\nCreating vector visualization...")
        kw.visualize_vectors(dimensions=2)

        print("\nExample complete! You can now:")
        print("1. Use kw.ask_question() to ask more questions")
        print("2. Call kw.chat_interface() to launch the web interface")
        print("3. Use kw.visualize_vectors() to see your embeddings")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set up your OpenAI API key in .env file")
        print("2. The knowledge-base folder contains your documents")

if __name__ == "__main__":
    main()
