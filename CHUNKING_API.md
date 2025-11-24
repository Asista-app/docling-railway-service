# 🔥 Hybrid Chunking API Documentation

## Overview

The Docling API now includes intelligent document chunking using HybridChunker - perfect for RAG systems, vector databases, and semantic search applications.

---

## 🎯 Endpoint

```
POST /chunk
```

**Base URL:** `https://asista-docling.up.railway.app`

---

## 📥 Request Format

### Headers
```
Content-Type: application/json
```

### Body Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string (URL) | Yes | - | URL of the document to chunk |
| `max_tokens` | integer | No | 512 | Maximum tokens per chunk |
| `merge_peers` | boolean | No | true | Merge small adjacent chunks |

### Example Request

```bash
curl -X POST "https://asista-docling.up.railway.app/chunk" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://arxiv.org/pdf/2408.09869",
    "max_tokens": 512,
    "merge_peers": true
  }'
```

---

## 📤 Response Format

### Success Response

```json
{
  "success": true,
  "chunks": [
    {
      "content": "Document content for this chunk...",
      "chunk": 0,
      "chunk_size": 1234,
      "tokens": 450,
      "metadata": {
        "doc_items": [...],
        "headings": [...],
        "origin": {...}
      }
    },
    {
      "content": "Next chunk content...",
      "chunk": 1,
      "chunk_size": 1156,
      "tokens": 498,
      "metadata": {...}
    }
  ],
  "total_chunks": 10,
  "total_tokens": 4523
}
```

### Error Response

```json
{
  "success": false,
  "chunks": null,
  "total_chunks": null,
  "total_tokens": null,
  "error": "Error message here"
}
```

---

## 📊 Response Fields

### Chunk Object

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | The text content of the chunk |
| `chunk` | integer | Zero-based chunk index |
| `chunk_size` | integer | Character count of the chunk |
| `tokens` | integer | Token count (for embedding models) |
| `metadata` | object | Document structure metadata |

### Metadata Object

Contains information about:
- **doc_items**: Document structure elements
- **headings**: Section headings and hierarchy
- **origin**: Source document information
- **page_numbers**: Page references (if applicable)

---

## 🎯 Use Cases

### 1. RAG Systems (Retrieval Augmented Generation)

Perfect for chunking documents before embedding:

```python
import requests

response = requests.post(
    "https://asista-docling.up.railway.app/chunk",
    json={
        "url": "https://example.com/knowledge-base.pdf",
        "max_tokens": 512
    }
)

chunks = response.json()["chunks"]

# Now embed each chunk and store in vector database
for chunk in chunks:
    embedding = embed_text(chunk["content"])
    store_in_vector_db(
        text=chunk["content"],
        embedding=embedding,
        metadata=chunk["metadata"]
    )
```

### 2. Postgres PGVector Integration

The chunk format is designed for PGVector compatibility:

```sql
CREATE TABLE documents_pg (
    id SERIAL PRIMARY KEY,
    content TEXT,
    chunk INTEGER,
    chunk_size INTEGER,
    tokens INTEGER,
    metadata JSONB,
    embedding vector(384)
);
```

Insert chunks:
```python
for chunk in chunks:
    cursor.execute("""
        INSERT INTO documents_pg (content, chunk, chunk_size, tokens, metadata)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        chunk["content"],
        chunk["chunk"],
        chunk["chunk_size"],
        chunk["tokens"],
        json.dumps(chunk["metadata"])
    ))
```

### 3. n8n Workflow

Use the provided n8n nodes to automate document processing:

1. **Trigger** (Webhook, Schedule, etc.)
2. **Docling Chunk** node
3. **Split Into Items** node
4. **Postgres PGVector** node

See `n8n-chunk-to-pgvector-workflow.json` for complete example.

---

## 🔧 Configuration Options

### max_tokens

Controls the maximum number of tokens per chunk.

**Common values:**
- `256` - For smaller, more granular chunks
- `512` - Default, good for most embedding models
- `1024` - For larger context windows
- `2048` - For models with large context support

**Recommendation:** Match your embedding model's token limit.

### merge_peers

When `true`, merges small adjacent chunks to optimize chunk sizes.

**Benefits:**
- Reduces number of chunks
- Better utilization of token budget
- More context per chunk

**When to disable:**
- Need strict chunk boundaries
- Want maximum granularity
- Processing very structured documents

---

## ⚡ Performance

### Processing Time

Typical processing times:

| Document Size | Pages | Chunks | Time |
|--------------|-------|--------|------|
| Small PDF | 1-5 | 5-20 | 10-20s |
| Medium PDF | 10-50 | 50-200 | 30-60s |
| Large PDF | 100+ | 500+ | 2-5min |

**Note:** First request may take longer (~30s extra) due to tokenizer model download.

### Optimization Tips

1. **Batch Processing**: Process multiple documents in parallel
2. **Caching**: Cache chunks for frequently accessed documents
3. **Async Processing**: Use webhooks for large documents
4. **Token Limits**: Use appropriate max_tokens for your use case

---

## 🧪 Testing

### Quick Test

```bash
curl -X POST "https://asista-docling.up.railway.app/chunk" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://arxiv.org/pdf/2408.09869",
    "max_tokens": 256
  }' | jq '.total_chunks'
```

### Python Test

```python
import requests

def test_chunking():
    response = requests.post(
        "https://asista-docling.up.railway.app/chunk",
        json={
            "url": "https://arxiv.org/pdf/2408.09869",
            "max_tokens": 512,
            "merge_peers": True
        }
    )
    
    result = response.json()
    
    if result["success"]:
        print(f"✓ Success!")
        print(f"  Total chunks: {result['total_chunks']}")
        print(f"  Total tokens: {result['total_tokens']}")
        print(f"  Avg tokens/chunk: {result['total_tokens'] / result['total_chunks']:.1f}")
        
        # Show first chunk
        first_chunk = result["chunks"][0]
        print(f"\nFirst chunk:")
        print(f"  Content: {first_chunk['content'][:100]}...")
        print(f"  Tokens: {first_chunk['tokens']}")
    else:
        print(f"✗ Error: {result['error']}")

test_chunking()
```

---

## 🔍 How It Works

### HybridChunker Algorithm

1. **Document Conversion**: Converts document to structured format
2. **Structure Analysis**: Identifies paragraphs, sections, tables
3. **Token Calculation**: Counts tokens using sentence-transformers tokenizer
4. **Intelligent Splitting**: Splits at semantic boundaries
5. **Merge Optimization**: Merges small chunks if enabled
6. **Metadata Preservation**: Maintains document structure info

### Why Hybrid?

- **Structure-Aware**: Respects document hierarchy
- **Token-Aware**: Fits embedding model limits
- **Semantic**: Doesn't split mid-sentence
- **Optimized**: Balances chunk size and coherence

---

## 📚 Examples

### Example 1: Basic Chunking

```bash
curl -X POST "https://asista-docling.up.railway.app/chunk" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/doc.pdf"}'
```

### Example 2: Custom Token Limit

```bash
curl -X POST "https://asista-docling.up.railway.app/chunk" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/doc.pdf",
    "max_tokens": 1024
  }'
```

### Example 3: Disable Merging

```bash
curl -X POST "https://asista-docling.up.railway.app/chunk" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/doc.pdf",
    "max_tokens": 512,
    "merge_peers": false
  }'
```

---

## 🐛 Troubleshooting

### "Timeout Error"
- Increase timeout in your HTTP client
- Large documents take longer to process
- Consider async processing for very large files

### "Invalid URL"
- Ensure URL is publicly accessible
- Check URL format includes https://
- Verify document is not password-protected

### "Too Many Chunks"
- Increase `max_tokens` to reduce chunk count
- Enable `merge_peers` to consolidate small chunks
- Consider document size and complexity

### "Tokenizer Loading Slow"
- First request downloads ~90MB model
- Subsequent requests use cached model
- Model is cached on Railway server

---

## 🔒 Security & Limits

### Rate Limiting
Currently no rate limits, but recommended:
- Max 10 concurrent requests
- Max 100MB document size
- Max 5 minute processing time

### Data Privacy
- Documents are processed in memory
- No documents are stored on server
- Temporary files are cleaned up immediately

---

## 🚀 Integration Examples

### With LangChain

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests

# Get chunks from Docling
response = requests.post(
    "https://asista-docling.up.railway.app/chunk",
    json={"url": "https://example.com/doc.pdf"}
)

chunks = [c["content"] for c in response.json()["chunks"]]

# Use with LangChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.from_texts(chunks, embeddings)
```

### With Pinecone

```python
import pinecone
import requests

# Get chunks
response = requests.post(
    "https://asista-docling.up.railway.app/chunk",
    json={"url": "https://example.com/doc.pdf"}
)

chunks = response.json()["chunks"]

# Upload to Pinecone
for chunk in chunks:
    embedding = get_embedding(chunk["content"])
    pinecone.upsert(
        vectors=[(
            f"chunk-{chunk['chunk']}",
            embedding,
            {"text": chunk["content"], **chunk["metadata"]}
        )]
    )
```

---

## 📞 Support

- **API Issues**: Check Railway logs
- **Chunking Questions**: See `04_hybrid_chunking.py` for implementation
- **n8n Integration**: See `N8N_INTEGRATION.md`

---

## 🎉 Summary

✅ **Endpoint**: `POST /chunk`  
✅ **Input**: Document URL + chunking parameters  
✅ **Output**: Array of chunks with metadata  
✅ **Format**: PGVector compatible  
✅ **Use Case**: RAG, semantic search, vector databases  
✅ **Integration**: n8n workflows included  

**Ready to use!** 🚀
