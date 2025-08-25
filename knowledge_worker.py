#!/usr/bin/env python3
"""
Knowledge Worker RAG Application

A question answering agent that uses RAG (Retrieval Augmented Generation) to provide
accurate answers based on a knowledge base. This application can be customized for
any domain by replacing the knowledge-base folder with your own documents.

Author: Your Name
Date: 2024
"""

import os
import glob
import argparse
from dotenv import load_dotenv
import gradio as gr

# LangChain imports
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Visualization imports
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
import plotly.graph_objects as go

# Configuration
MODEL = "gpt-4o-mini"
DB_NAME = "vector_db"

class KnowledgeWorker:
    def __init__(self, knowledge_base_path="knowledge-base", use_openai=True):
        """
        Initialize the Knowledge Worker

        Args:
            knowledge_base_path (str): Path to the knowledge base folder
            use_openai (bool): Whether to use OpenAI embeddings (True) or HuggingFace (False)
        """
        self.knowledge_base_path = knowledge_base_path
        self.use_openai = use_openai
        self.vectorstore = None
        self.conversation_chain = None

        # Load environment variables
        load_dotenv(override=True)

        if use_openai:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key or api_key == 'your-key-if-not-using-env':
                raise ValueError("Please set your OPENAI_API_KEY in the .env file")
            os.environ['OPENAI_API_KEY'] = api_key

    def load_documents(self):
        """Load documents from the knowledge base folder"""
        print("Loading documents from knowledge base...")

        folders = glob.glob(f"{self.knowledge_base_path}/*")
        if not folders:
            raise ValueError(f"No folders found in {self.knowledge_base_path}")

        def add_metadata(doc, doc_type):
            doc.metadata["doc_type"] = doc_type
            return doc

        # Text loader configuration
        text_loader_kwargs = {'encoding': 'utf-8'}

        documents = []
        for folder in folders:
            doc_type = os.path.basename(folder)
            loader = DirectoryLoader(
                folder,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs=text_loader_kwargs
            )
            folder_docs = loader.load()
            documents.extend([add_metadata(doc, doc_type) for doc in folder_docs])

        print(f"Loaded {len(documents)} documents from {len(folders)} folders")
        print(f"Document types found: {set(doc.metadata['doc_type'] for doc in documents)}")

        return documents

    def create_vectorstore(self, documents):
        """Create vector embeddings and store them in Chroma"""
        print("Creating vector embeddings...")

        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} text chunks")

        # Create embeddings
        if self.use_openai:
            embeddings = OpenAIEmbeddings()
        else:
            from langchain.embeddings import HuggingFaceEmbeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

        # Delete existing vectorstore if it exists
        if os.path.exists(DB_NAME):
            Chroma(persist_directory=DB_NAME, embedding_function=embeddings).delete_collection()

        # Create new vectorstore
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_NAME
        )

        count = self.vectorstore._collection.count()
        print(f"Vectorstore created with {count} documents")

        return self.vectorstore

    def visualize_vectors(self, dimensions=2):
        """Visualize the vector embeddings in 2D or 3D"""
        if not self.vectorstore:
            print("No vectorstore available. Please create one first.")
            return

        collection = self.vectorstore._collection
        result = collection.get(include=['embeddings', 'documents', 'metadatas'])

        vectors = np.array(result['embeddings'])
        documents = result['documents']
        metadatas = result['metadatas']
        doc_types = [metadata['doc_type'] for metadata in metadatas]

        # Color mapping
        type_colors = {'products': 'blue', 'employees': 'green', 'contracts': 'red', 'company': 'orange'}
        colors = [type_colors.get(t, 'gray') for t in doc_types]

        # Reduce dimensionality using t-SNE
        tsne = TSNE(n_components=dimensions, random_state=42)
        reduced_vectors = tsne.fit_transform(vectors)

        if dimensions == 2:
            fig = go.Figure(data=[go.Scatter(
                x=reduced_vectors[:, 0],
                y=reduced_vectors[:, 1],
                mode='markers',
                marker=dict(size=5, color=colors, opacity=0.8),
                text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
                hoverinfo='text'
            )])

            fig.update_layout(
                title=f'{dimensions}D Chroma Vector Store Visualization',
                width=800,
                height=600
            )
        else:
            fig = go.Figure(data=[go.Scatter3d(
                x=reduced_vectors[:, 0],
                y=reduced_vectors[:, 1],
                z=reduced_vectors[:, 2],
                mode='markers',
                marker=dict(size=5, color=colors, opacity=0.8),
                text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
                hoverinfo='text'
            )])

            fig.update_layout(
                title=f'{dimensions}D Chroma Vector Store Visualization',
                scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
                width=900,
                height=700
            )

        fig.show()

    def setup_conversation_chain(self, k=25):
        """Set up the conversational retrieval chain"""
        if not self.vectorstore:
            print("No vectorstore available. Please create one first.")
            return

        print("Setting up conversation chain...")

        # Create LLM
        llm = ChatOpenAI(temperature=0.7, model_name=MODEL)

        # Set up memory
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

        # Set up retriever
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})

        # Create conversation chain
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory
        )

        print("Conversation chain ready!")

    def ask_question(self, question):
        """Ask a question and get an answer"""
        if not self.conversation_chain:
            return "Please set up the conversation chain first by calling setup_conversation_chain()"

        try:
            result = self.conversation_chain.invoke({"question": question})
            return result["answer"]
        except Exception as e:
            return f"Error: {str(e)}"

    def chat_interface(self):
        """Launch the Gradio chat interface"""
        if not self.conversation_chain:
            print("Please set up the conversation chain first!")
            return

        def chat(question, history):
            result = self.conversation_chain.invoke({"question": question})
            return result["answer"]

        # Launch Gradio interface
        interface = gr.ChatInterface(chat, title="Knowledge Worker Chat")
        interface.launch(inbrowser=True)

    def run_full_setup(self):
        """Run the complete setup process"""
        try:
            # Load documents
            documents = self.load_documents()

            # Create vectorstore
            self.create_vectorstore(documents)

            # Set up conversation chain
            self.setup_conversation_chain()

            print("Setup complete! You can now ask questions or launch the chat interface.")

        except Exception as e:
            print(f"Setup failed: {str(e)}")

def main():
    """Main function to run the knowledge worker"""
    parser = argparse.ArgumentParser(description="Knowledge Worker RAG Application")
    parser.add_argument("--knowledge-base", default="knowledge-base",
                       help="Path to knowledge base folder")
    parser.add_argument("--use-openai", action="store_true", default=True,
                       help="Use OpenAI embeddings (default: True)")
    parser.add_argument("--no-openai", dest="use_openai", action="store_false",
                       help="Use HuggingFace embeddings instead of OpenAI")
    parser.add_argument("--chat", action="store_true",
                       help="Launch chat interface after setup")
    parser.add_argument("--visualize", action="store_true",
                       help="Show vector visualization after setup")

    args = parser.parse_args()

    try:
        # Create knowledge worker
        kw = KnowledgeWorker(
            knowledge_base_path=args.knowledge_base,
            use_openai=args.use_openai
        )

        # Run setup
        kw.run_full_setup()

        # Optional: show visualization
        if args.visualize:
            kw.visualize_vectors(dimensions=2)
            kw.visualize_vectors(dimensions=3)

        # Optional: launch chat interface
        if args.chat:
            kw.chat_interface()
        else:
            # Interactive mode
            print("\n" + "="*50)
            print("Knowledge Worker is ready! Ask questions or type 'quit' to exit.")
            print("="*50)

            while True:
                question = input("\nYour question: ").strip()
                if question.lower() in ['quit', 'exit', 'q']:
                    break

                if question:
                    answer = kw.ask_question(question)
                    print(f"\nAnswer: {answer}")

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
