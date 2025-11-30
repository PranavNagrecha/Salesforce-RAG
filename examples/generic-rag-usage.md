# Using This RAG Library with Generic RAG Frameworks

This guide shows how to integrate this Salesforce RAG library with popular RAG frameworks like LangChain, LlamaIndex, and others.

## Overview

The library provides two main entry points for RAG systems:

1. **`rag-library.json`**: Structured metadata for programmatic retrieval
2. **`rag/rag-index.md`**: Human-readable index for semantic search
3. **Individual markdown files**: Detailed knowledge content

## Integration Approaches

### Approach 1: JSON-Based Retrieval (Recommended)

Use `rag-library.json` to build a retrieval system that matches questions to relevant files.

#### Python Example (LangChain)

```python
import json
from pathlib import Path
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load the RAG library metadata
with open('rag/rag-library.json', 'r') as f:
    rag_library = json.load(f)

# Build a question-to-file mapping
def find_relevant_files(question: str, rag_library: dict) -> list:
    """Find relevant files based on whenToRetrieve criteria."""
    relevant_files = []
    
    for file_entry in rag_library['files']:
        # Simple keyword matching (can be enhanced with embeddings)
        question_lower = question.lower()
        for retrieval_trigger in file_entry['whenToRetrieve']:
            if any(word in question_lower for word in retrieval_trigger.lower().split()):
                relevant_files.append(file_entry['path'])
                break
    
    return relevant_files

# Load and index relevant documents
def load_rag_documents(question: str):
    relevant_files = find_relevant_files(question, rag_library)
    
    documents = []
    for file_path in relevant_files:
        loader = TextLoader(file_path)
        documents.extend(loader.load())
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    return vectorstore

# Use the RAG system
question = "How do I implement Platform Events for asynchronous integration?"
vectorstore = load_rag_documents(question)

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

answer = qa_chain.run(question)
print(answer)
```

#### Python Example (LlamaIndex)

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI
import json

# Load RAG library metadata
with open('rag/rag-library.json', 'r') as f:
    rag_library = json.load(f)

def get_relevant_files(question: str, rag_library: dict) -> list:
    """Find relevant files based on whenToRetrieve criteria."""
    relevant_files = []
    
    for file_entry in rag_library['files']:
        question_lower = question.lower()
        for retrieval_trigger in file_entry['whenToRetrieve']:
            if any(word in question_lower for word in retrieval_trigger.lower().split()):
                relevant_files.append(file_entry['path'])
                break
    
    return relevant_files

# Load relevant documents
question = "How should I design external IDs for integration?"
relevant_files = get_relevant_files(question, rag_library)

documents = SimpleDirectoryReader(input_files=relevant_files).load_data()

# Create index
service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo"))
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

# Query
query_engine = index.as_query_engine()
response = query_engine.query(question)
print(response)
```

### Approach 2: Semantic Search on All Files

Load all markdown files and use semantic search to find relevant content.

#### Python Example (LangChain)

```python
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load all markdown files from rag directory
loader = DirectoryLoader('rag/', glob="**/*.md", recursive=True)
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(splits, embeddings)

# Query
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

answer = qa_chain.run("How do I implement permission set-driven security?")
print(answer)
```

### Approach 3: Hybrid Approach (JSON + Semantic Search)

Use JSON metadata to filter files, then use semantic search within those files.

#### Python Example

```python
import json
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load RAG library
with open('rag/rag-library.json', 'r') as f:
    rag_library = json.load(f)

def get_files_by_domain(domain: str, rag_library: dict) -> list:
    """Get all files in a specific domain."""
    return [f['path'] for f in rag_library['files'] if f['domain'] == domain]

def get_files_by_keywords(question: str, rag_library: dict) -> list:
    """Get files that match question keywords."""
    question_words = set(question.lower().split())
    relevant_files = []
    
    for file_entry in rag_library['files']:
        # Check summary and keyTopics
        summary_words = set(file_entry['summary'].lower().split())
        topics_words = set(' '.join(file_entry['keyTopics']).lower().split())
        
        if question_words.intersection(summary_words) or question_words.intersection(topics_words):
            relevant_files.append(file_entry['path'])
    
    return relevant_files

# Hybrid retrieval
question = "How do I implement event-driven architecture with Platform Events?"

# Step 1: Use JSON to find candidate files
candidate_files = get_files_by_keywords(question, rag_library)

# Step 2: Load and create embeddings for candidate files
documents = []
for file_path in candidate_files:
    loader = TextLoader(file_path)
    documents.extend(loader.load())

# Step 3: Semantic search within candidates
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(splits, embeddings)

# Step 4: Query
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

answer = qa_chain.run(question)
print(answer)
```

## Using the Index File

The `rag-index.md` file can be used as a retrieval guide or for generating summaries:

```python
from langchain.document_loaders import TextLoader

# Load the index
loader = TextLoader('rag/rag-index.md')
index_doc = loader.load()[0]

# Use index to understand what knowledge is available
# Can be used for:
# 1. Generating summaries of available knowledge
# 2. Routing questions to appropriate domains
# 3. Providing context about the knowledge base structure
```

## Best Practices

### 1. Use Domain Filtering

Filter files by domain first to reduce search space:

```python
# Get all development-related files
dev_files = [f['path'] for f in rag_library['files'] if f['domain'] == 'development']
```

### 2. Leverage whenToRetrieve

The `whenToRetrieve` arrays are designed to match common questions:

```python
def match_question_to_files(question: str, rag_library: dict) -> list:
    """Match question to files using whenToRetrieve criteria."""
    question_lower = question.lower()
    matches = []
    
    for file_entry in rag_library['files']:
        for trigger in file_entry['whenToRetrieve']:
            # Simple keyword matching (enhance with embeddings for better matching)
            if any(word in question_lower for word in trigger.lower().split()[:3]):
                matches.append({
                    'file': file_entry['path'],
                    'summary': file_entry['summary'],
                    'relevance': trigger
                })
                break
    
    return matches
```

### 3. Combine Multiple Files

For complex questions, retrieve from multiple related files:

```python
# Question about integration with error handling
question = "How do I implement an API integration with proper error handling?"

# Find integration files
integration_files = [f['path'] for f in rag_library['files'] 
                    if f['domain'] == 'integrations']

# Find error handling files
error_files = [f['path'] for f in rag_library['files'] 
               if 'error' in f['file'].lower()]

# Combine and retrieve
all_files = integration_files + error_files
```

### 4. Use Summaries for Context

Include file summaries in your prompts for better context:

```python
def get_context_for_files(file_paths: list, rag_library: dict) -> str:
    """Get summary context for files."""
    context = []
    
    for file_path in file_paths:
        file_entry = next((f for f in rag_library['files'] if f['path'] == file_path), None)
        if file_entry:
            context.append(f"File: {file_entry['file']}\nSummary: {file_entry['summary']}\n")
    
    return "\n".join(context)
```

## Example: Complete RAG Pipeline

```python
import json
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

class SalesforceRAG:
    def __init__(self, rag_library_path='rag/rag-library.json'):
        with open(rag_library_path, 'r') as f:
            self.rag_library = json.load(f)
        
        self.embeddings = OpenAIEmbeddings()
        self.llm = OpenAI()
    
    def find_relevant_files(self, question: str) -> list:
        """Find relevant files using JSON metadata."""
        question_lower = question.lower()
        relevant = []
        
        for file_entry in self.rag_library['files']:
            # Check whenToRetrieve
            for trigger in file_entry['whenToRetrieve']:
                if any(word in question_lower for word in trigger.lower().split()[:3]):
                    relevant.append(file_entry['path'])
                    break
        
        return relevant[:5]  # Limit to top 5
    
    def query(self, question: str) -> str:
        """Query the RAG system."""
        # Find relevant files
        files = self.find_relevant_files(question)
        
        if not files:
            return "No relevant knowledge found for this question."
        
        # Load documents
        documents = []
        for file_path in files:
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        
        # Split and embed
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        vectorstore = FAISS.from_documents(splits, self.embeddings)
        
        # Query
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        
        return qa_chain.run(question)

# Usage
rag = SalesforceRAG()
answer = rag.query("How do I implement Platform Events?")
print(answer)
```

## Integration with Other Frameworks

### Haystack

```python
from haystack import Document, Pipeline
from haystack.components.embedders import OpenAIDocumentEmbedder, OpenAITextEmbedder
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.generators import OpenAIGenerator

# Load documents from RAG library
# (Similar to LangChain examples above)

# Build pipeline
pipeline = Pipeline()
pipeline.add_component("embedder", OpenAIDocumentEmbedder())
pipeline.add_component("retriever", InMemoryEmbeddingRetriever())
pipeline.add_component("prompt_builder", PromptBuilder(template="..."))
pipeline.add_component("llm", OpenAIGenerator())

# Connect components and query
```

### Chroma

```python
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Create Chroma client
client = chromadb.Client()

# Load documents (similar to examples above)
# ...

# Use Chroma as vector store
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(),
    client=client
)
```

## Tips

1. **Pre-filter by domain**: Use the `domain` field to narrow down files before semantic search
2. **Use summaries**: Include file summaries in your prompts for better context
3. **Combine approaches**: Use JSON metadata for initial filtering, then semantic search within results
4. **Cache embeddings**: Pre-compute and cache embeddings for faster retrieval
5. **Monitor retrieval quality**: Track which files are retrieved for different question types

