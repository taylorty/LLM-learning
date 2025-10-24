# Wikipedia RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows you to have intelligent conversations about Wikipedia content using state-of-the-art language models. The system dynamically indexes Wikipedia pages and uses a ReAct agent to answer questions based on the retrieved information.

## 🌟 Features

- **Multi-Model Support**: Choose between multiple LLM providers:
  - DeepSeek models via OpenRouter (free tier available)
  - Google Gemini models (2.0 Flash, 1.5 Pro, 1.5 Flash)
- **Dynamic Wikipedia Indexing**: Automatically fetches and indexes Wikipedia pages based on user queries
- **RAG Architecture**: Combines retrieval and generation for accurate, context-aware responses
- **ReAct Agent**: Uses reasoning and acting to provide thoughtful answers
- **Interactive UI**: Built with Chainlit for a smooth chat experience
- **Vector Search**: Employs HuggingFace embeddings for semantic search
- **Real-time Configuration**: Change models and Wikipedia topics on-the-fly

## 🏗️ Architecture

The system consists of three main components:

1. **Wikipedia Indexer** (`index_wikipages.py`): Extracts page names from queries, fetches Wikipedia content, and creates vector embeddings
2. **Chat Agent** (`chat_agent.py`): Manages the conversational interface and ReAct agent
3. **Utilities** (`utils.py`): Handles API key management and configuration

```
User Query → LLM (Extract Pages) → Wikipedia API → Document Chunking 
→ Vector Embeddings → Index Creation → Query Engine → ReAct Agent → Response
```

## 📋 Prerequisites

- Python 3.8+
- API Keys:
  - OpenRouter API key (for DeepSeek models)
  - Google Gemini API key (for Gemini models)

## 🚀 Installation

1. **Clone the repository**
```bash
cd rag_chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Required packages:
```txt
chainlit
llama-index
llama-index-llms-openai
llama-index-llms-gemini
llama-index-embeddings-huggingface
google-generativeai
wikipedia
pydantic
PyYAML
sentence-transformers
```

3. **Configure API Keys**

Edit the `apikeys.yml` file with your API keys:

```yaml
openrouter:
  api_key: your-openrouter-api-key-here

deepseek:
  api_key: your-deepseek-api-key-here

gemini:
  api_key: your-gemini-api-key-here
```

### Getting API Keys

- **OpenRouter**: Sign up at [openrouter.ai](https://openrouter.ai/)
- **Google Gemini**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 💻 Usage

### Starting the Chatbot

Run the following command to start the Chainlit interface:

```bash
chainlit run chat_agent.py
chainlit run chat_agent.py -h --host=0.0.0.0 --port=8000
```

The application will open in your default web browser at `http://localhost:8000`.

### Configuring the Agent

1. **Access Settings**: Click the settings icon (⚙️) in the bottom left corner
2. **Select Model**: Choose from available models:
   - `deepseek/deepseek-r1:free` (reasoning model)
   - `deepseek/deepseek-chat-v3-0324:free` (chat model)
   - `gemini-2.0-flash-exp` (latest Gemini)
   - `gemini-1.5-pro` (most capable Gemini)
   - `gemini-1.5-flash` (fastest Gemini)
3. **Enter Wikipedia Pages**: Type the topics you want to index, e.g.:
   - "Natural language processing, Machine learning"
   - "Paris, London, Barcelona"
   - "Quantum computing"
4. **Confirm Settings**: Save and wait for the indexing confirmation

### Example Conversations

After indexing "Artificial Intelligence":
```
User: What is artificial intelligence?
Agent: Based on the Wikipedia article, artificial intelligence (AI) is...

User: How does machine learning relate to AI?
Agent: Machine learning is a subset of AI that focuses on...
```

## 📁 Project Structure

```
rag_chatbot/
├── chat_agent.py           # Main chatbot application with ReAct agent
├── index_wikipages.py      # Wikipedia indexing and document processing
├── utils.py                # API key management utilities
├── test_wiki_query.py      # Testing script for index querying
├── apikeys.yml             # API key configuration file
├── chainlit.md             # Welcome message for Chainlit UI
└── README.md               # This file
```

## 🔧 Configuration

### Model Selection

The system automatically routes requests based on the model name:
- Models starting with `gemini` → Google Gemini API
- Other models → OpenRouter API

### Embedding Model

The system uses `sentence-transformers/all-MiniLM-L6-v2` for creating document embeddings. This is a lightweight, efficient model that balances performance and speed.

### Document Chunking

- **Chunk Size**: 150 tokens
- **Chunk Overlap**: 45 tokens
- **Top K Results**: 3 most relevant chunks per query

These parameters can be modified in `index_wikipages.py` and `chat_agent.py`.

## 🧪 Testing

Run the test script to verify Wikipedia querying functionality:

```bash
python test_wiki_query.py
```

This script demonstrates:
- Loading Wikipedia content
- Creating a vector index
- Querying the index with sample questions

## 🎯 How It Works

### 1. Wikipedia Page Extraction
When you specify topics, the system uses an LLM to extract structured Wikipedia page names from natural language.

### 2. Content Retrieval
The Wikipedia API fetches full content for each page, handling disambiguation and errors gracefully.

### 3. Document Processing
Content is split into overlapping chunks and converted to vector embeddings using HuggingFace's sentence transformers.

### 4. Vector Indexing
Embeddings are stored in a vector index powered by LlamaIndex for fast semantic search.

### 5. Query Processing
User questions are embedded and matched against the index to retrieve relevant context.

### 6. ReAct Agent
The agent uses a reasoning and acting loop to:
- Understand the user's question
- Decide when to use the Wikipedia tool
- Generate informed responses based on retrieved context

## 🐛 Troubleshooting

### Common Issues

**Error: "Agent not initialized"**
- Solution: Configure a Wikipedia topic in the settings before chatting

**Error: "Wikipedia page not found"**
- Solution: Check spelling or try a more specific page title

**Error: "Could not parse LLM response"**
- Solution: The LLM might have returned malformed JSON. The system will retry with fallback parsing

**Error: "API key not found"**
- Solution: Verify your `apikeys.yml` file contains valid API keys

### Debug Mode

Check the terminal output for detailed logs:
- Wikipedia page loading status
- Index creation progress
- LLM reasoning steps (verbose mode enabled)
- Error messages and stack traces

## 🔐 Security Notes

- Never commit `apikeys.yml` with real API keys to version control
- Consider using environment variables for production deployments
- The current implementation includes a fallback hardcoded key (remove in production)

## 🚀 Advanced Usage

### Custom Models

To add more models, edit the dropdown in `chat_agent.py`:

```python
Select(
    id="MODEL",
    label="Model Selection",
    values=[
        "your-new-model-here",
        # ... existing models
    ],
    initial_index=0,
),
```

### Custom Embeddings

Change the embedding model in `index_wikipages.py`:

```python
embed_model = HuggingFaceEmbedding(
    model_name="your-preferred-embedding-model"
)
```

### Adjust Retrieval Parameters

Modify query engine settings in `chat_agent.py`:

```python
query_engine = index.as_query_engine(
    response_mode="compact",      # or "tree_summarize", "refine"
    similarity_top_k=5,           # increase for more context
    llm=llm
)
```

## 🙏 Acknowledgments

- Built with [LlamaIndex](https://www.llamaindex.ai/)
- UI powered by [Chainlit](https://chainlit.io/)
- Embeddings from [HuggingFace](https://huggingface.co/)
- Wikipedia content via [Wikipedia API](https://pypi.org/project/wikipedia/)
- LLM access via [OpenRouter](https://openrouter.ai/) and [Google Gemini](https://deepmind.google/technologies/gemini/)
