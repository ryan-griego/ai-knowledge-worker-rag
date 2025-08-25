# Knowledge Worker RAG Application

A powerful question-answering agent that uses RAG (Retrieval Augmented Generation) to provide accurate answers based on your custom knowledge base. This application can be tailored for any domain - from company knowledge bases to personal documentation.

## Features

- **RAG-powered Q&A**: Uses vector embeddings and retrieval to provide accurate, context-aware answers
- **Custom Knowledge Bases**: Easy to set up with your own documents
- **Multiple Interface Options**: Command-line interface or web-based chat interface
- **Vector Visualization**: 2D and 3D visualizations of your knowledge base embeddings
- **Flexible Embeddings**: Support for both OpenAI and free HuggingFace embeddings
- **Markdown Support**: Works with Markdown files for easy content creation

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (for OpenAI embeddings) and internet connection

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/ryan-griego/ai-knowledge-worker-rag
   cd knowledge-worker-rag
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Quick Start

### Option 1: Use the existing knowledge base
```bash
# Run with the default knowledge base
python knowledge_worker.py

# Or launch the chat interface directly
python knowledge_worker.py --chat
```

### Option 2: Create your own knowledge base
```bash
# Create a new knowledge base structure
python setup_knowledge_base.py --name "my-company"

# Run with your custom knowledge base
python knowledge_worker.py --knowledge-base knowledge-base-my-company
```

## Creating Your Own Knowledge Base

### Step 1: Generate the Structure
```bash
python setup_knowledge_base.py --name "your-domain"
```

This creates a folder structure like:
```
knowledge-base-your-domain/
├── company/
├── products/
├── employees/
├── contracts/
├── policies/
├── procedures/
└── README.md
```

### Step 2: Add Your Content
- Replace the example files with your actual content
- Add more documents as needed
- Organize documents into appropriate subdirectories
- All files should be in Markdown (.md) format

### Step 3: Run the Application
```bash
python knowledge_worker.py --knowledge-base knowledge-base-your-domain
```

## 🔧 Usage Options

### Command Line Interface
```bash
# Basic usage
python knowledge_worker.py

# With custom knowledge base
python knowledge_worker.py --knowledge-base path/to/knowledge-base

# Launch chat interface after setup
python knowledge_worker.py --chat

# Show vector visualizations
python knowledge_worker.py --visualize

# Use free HuggingFace embeddings instead of OpenAI
python knowledge_worker.py --no-openai
```

### Programmatic Usage
```python
from knowledge_worker import KnowledgeWorker

# Create knowledge worker
kw = KnowledgeWorker(knowledge_base_path="my-knowledge-base")

# Run full setup
kw.run_full_setup()

# Ask questions
answer = kw.ask_question("What is your company's mission?")

# Launch chat interface
kw.chat_interface()

# Visualize vectors
kw.visualize_vectors(dimensions=2)
```

## Web Interface

The application includes a Gradio-based web interface for easy interaction:

```bash
python knowledge_worker.py --chat
```

This launches a web server (usually at http://127.0.0.1:7860) where you can chat with your knowledge base through a user-friendly interface.

## How It Works

1. **Document Loading**: Loads Markdown files from your knowledge base folders
2. **Text Chunking**: Splits documents into smaller, manageable chunks
3. **Vector Embeddings**: Converts text chunks into numerical vectors using AI models
4. **Vector Storage**: Stores embeddings in a Chroma vector database
5. **Retrieval**: When you ask a question, finds the most relevant text chunks
6. **Generation**: Uses an LLM to generate answers based on retrieved context
7. **Response**: Provides accurate, context-aware answers

## Vector Visualization

The application can create 2D and 3D visualizations of your knowledge base embeddings:

```bash
python knowledge_worker.py --visualize
```

This helps you understand how your documents are organized in vector space and identify potential improvements.

## Customization Ideas

- **Company Knowledge Base**: Employee handbooks, policies, procedures
- **Product Documentation**: User manuals, technical specs, FAQs
- **Research Repository**: Academic papers, research notes, literature reviews
- **Personal Knowledge**: Notes, journals, learning materials
- **Customer Support**: FAQ databases, troubleshooting guides
- **Legal Documents**: Contracts, policies, compliance materials

## Configuration

### Environment Variables
Create a `.env` file with:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

### Model Selection
Edit `knowledge_worker.py` to change the LLM model:
```python
MODEL = "gpt-4o-mini"  # Change to your preferred model
```

### Embedding Options
- **OpenAI**: Higher quality, requires API key, costs money
- **HuggingFace**: Free, runs locally, good quality

## Troubleshooting

### Common Issues

1. **"No folders found in knowledge-base"**
   - Make sure your knowledge base folder exists and contains subdirectories
   - Check the path in the `--knowledge-base` argument

2. **OpenAI API errors**
   - Verify your API key is set in `.env`
   - Check your OpenAI account has sufficient credits

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Vector visualization not working**
   - Install additional dependencies: `pip install plotly matplotlib scikit-learn`
   - Some systems may require additional system packages

### Help

- Check the error messages for specific issues
- Verify your knowledge base structure matches the expected format
- Ensure all required dependencies are installed


## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Vector database powered by [Chroma](https://www.trychroma.com/)
- Web interface built with [Gradio](https://gradio.app/)
- Embeddings from OpenAI and HuggingFace
