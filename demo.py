#!/usr/bin/env python3
"""
Demo script for the Knowledge Worker RAG Application

This script demonstrates how to use the KnowledgeWorker class programmatically.
"""

from knowledge_worker import KnowledgeWorker

def main():
    """Demo the knowledge worker functionality"""

    print("🚀 Knowledge Worker RAG Demo")
    print("=" * 50)

    try:
        # Create knowledge worker instance
        print("📚 Initializing Knowledge Worker...")
        kw = KnowledgeWorker()

        # Run the full setup process
        print("\n⚙️ Setting up knowledge base and vector embeddings...")
        kw.run_full_setup()

        # Ask some example questions
        print("\n❓ Asking some example questions...")

        questions = [
            "What is Insurellm?",
            "Who are the key employees?",
            "What products does Insurellm offer?",
            "Tell me about the company's contracts"
        ]

        for question in questions:
            print(f"\nQ: {question}")
            answer = kw.ask_question(question)
            print(f"A: {answer}")
            print("-" * 50)

        # Show vector visualization
        print("\n📊 Creating vector visualizations...")
        print("(This will open in your browser)")
        kw.visualize_vectors(dimensions=2)

        # Ask if user wants to launch chat interface
        print("\n💬 Would you like to launch the chat interface? (y/n)")
        response = input().lower().strip()

        if response in ['y', 'yes']:
            print("Launching chat interface...")
            kw.chat_interface()
        else:
            print("Demo complete! You can run 'python knowledge_worker.py --chat' to launch the chat interface later.")

    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        print("\n💡 Make sure you have:")
        print("1. Installed all dependencies: pip install -r requirements.txt")
        print("2. Set up your OpenAI API key in .env file")
        print("3. The knowledge-base folder contains your documents")

if __name__ == "__main__":
    main()
