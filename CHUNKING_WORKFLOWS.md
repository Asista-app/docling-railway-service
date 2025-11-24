# 🔄 Chunking Workflows Guide

## Two Ways to Chunk Documents

Your Docling API provides **two chunking endpoints** for different use cases:

---

## Option 1: Chunk from URL (`/chunk`)

**Use when:** You want to chunk a document directly from a URL in one step.

### Endpoint
```
POST /chunk
```

### Request
```json
{
  "url": "https://example.com/document.pdf",
  "max_tokens": 512,
  "merge_peers": true
}
```

### n8n Workflow
```
[Trigger] → [Docling Chunk URL] → [Split Items] → [PGVector]
```

**File:** `n8n-chunk-node.json`

---

## Option 2: Chunk from Content (`/chunk/content`) ⭐ **RECOMMENDED**

**Use when:** You already have converted content from `/convert/url` endpoint.

### Endpoint
```
POST /chunk/content
```

### Request
```json
{
  "content": "Your document text content here...",
  "max_tokens": 512,
  "merge_peers": true
}
```

### n8n Workflow
```
[Trigger] 
  → [Convert Document] 
  → [Chunk Content] 
  → [Split Items] 
  → [PGVector]
```

**File:** `n8n-convert-chunk-pgvector-workflow.json`

---

## 🎯 Which One Should You Use?

### Use `/chunk` (URL-based) when:
- ✅ You only need chunks, not the full document
- ✅ You want a single-step process
- ✅ You're processing documents in batch

### Use `/chunk/content` (Content-based) when: ⭐
- ✅ You already converted the document
- ✅ You want both full content AND chunks
- ✅ You're building a workflow in n8n
- ✅ You need more control over the process

---

## 📋 Complete n8n Workflow Example

### Workflow: Document URL → Chunks → PGVector

**Step 1: Set Document URL**
```json
{
  "documentUrl": "https://example.com/document.pdf"
}
```

**Step 2: Convert Document**
```
POST /convert/url
{
  "url": "{{ $json.documentUrl }}",
  "output_format": "markdown"
}
```

**Output:**
```json
{
  "success": true,
  "content": "# Document Title\n\nDocument content...",
  "metadata": {...}
}
```

**Step 3: Chunk Content**
```
POST /chunk/content
{
  "content": "{{ $json.content }}",
  "max_tokens": 512,
  "merge_peers": true
}
```

**Output:**
```json
{
  "success": true,
  "chunks": [
    {
      "content": "chunk 0 text...",
      "chunk": 0,
      "chunk_size": 1234,
      "tokens": 450,
      "metadata": {...}
    }
  ],
  "total_chunks": 10,
  "total_tokens": 4500
}
```

**Step 4: Split Into Items**

Splits the `chunks` array into individual items for processing.

**Step 5: Insert to PGVector**

Each chunk becomes a row in your database:
```sql
INSERT INTO documents_pg (content, chunk, chunk_size, tokens, metadata)
VALUES (
  'chunk 0 text...',
  0,
  1234,
  450,
  '{"doc_items": [...], "headings": [...]}'
);
```

---

## 🔥 Advanced Workflow: Store Both Full Document and Chunks

```
[Trigger]
  ↓
[Convert Document] ──┬──→ [Store Full Document]
                     │
                     └──→ [Chunk Content]
                            ↓
                         [Split Items]
                            ↓
                         [Store Chunks in PGVector]
```

This gives you:
- ✅ Full document for display/reference
- ✅ Chunks for semantic search/RAG
- ✅ Link between full doc and chunks

---

## 💡 Example Use Cases

### Use Case 1: Simple RAG System

```
User uploads PDF
  → Convert to markdown
  → Chunk content
  → Generate embeddings
  → Store in PGVector
  → Ready for semantic search!
```

### Use Case 2: Document Q&A

```
User asks question
  → Search PGVector for relevant chunks
  → Retrieve chunk content
  → Pass to LLM with question
  → Get answer with source citation
```

### Use Case 3: Knowledge Base

```
Multiple documents
  → Convert each to markdown
  → Chunk all content
  → Store with metadata (source, date, author)
  → Build searchable knowledge base
```

---

## 🧪 Testing Both Endpoints

### Test URL-based Chunking

```bash
curl -X POST "https://asista-docling.up.railway.app/chunk" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://arxiv.org/pdf/2408.09869",
    "max_tokens": 512
  }'
```

### Test Content-based Chunking

```bash
# First convert
CONTENT=$(curl -X POST "https://asista-docling.up.railway.app/convert/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://arxiv.org/pdf/2408.09869", "output_format": "markdown"}' \
  | jq -r '.content')

# Then chunk
curl -X POST "https://asista-docling.up.railway.app/chunk/content" \
  -H "Content-Type: application/json" \
  -d "{\"content\": $(echo $CONTENT | jq -Rs .), \"max_tokens\": 512}"
```

---

## 📊 Performance Comparison

| Method | Steps | Total Time | Use Case |
|--------|-------|------------|----------|
| `/chunk` | 1 | ~30-60s | Quick chunking only |
| `/convert` + `/chunk/content` | 2 | ~40-80s | Full document + chunks |

**Note:** Content-based chunking adds ~10-20s but gives you both the full document and chunks.

---

## 🎯 Recommended Workflow for n8n + PGVector

**Best Practice:**

1. **Convert Document** (`/convert/url`)
   - Get full markdown content
   - Store in main documents table

2. **Chunk Content** (`/chunk/content`)
   - Pass the converted content
   - Get optimized chunks

3. **Split Items**
   - Separate chunks for processing

4. **Insert to PGVector**
   - Store each chunk with embedding
   - Link back to source document

**Why this is better:**
- ✅ You have both full document and chunks
- ✅ Can display full document to users
- ✅ Can search chunks for RAG
- ✅ Maintains document-chunk relationship
- ✅ More flexible for future features

---

## 📁 n8n Files Available

1. **`n8n-chunk-node.json`** - URL-based chunking (single step)
2. **`n8n-chunk-content-node.json`** - Content-based chunking (single node)
3. **`n8n-convert-chunk-pgvector-workflow.json`** - Complete workflow ⭐
4. **`n8n-chunk-to-pgvector-workflow.json`** - URL-based workflow

---

## 🚀 Quick Start

### For n8n Users:

1. Import `n8n-convert-chunk-pgvector-workflow.json`
2. Configure your Postgres PGVector credentials
3. Set your document URL
4. Run the workflow
5. Done! Your chunks are in PGVector

### For API Users:

```python
import requests

# Step 1: Convert
convert_response = requests.post(
    "https://asista-docling.up.railway.app/convert/url",
    json={"url": "https://example.com/doc.pdf", "output_format": "markdown"}
)
content = convert_response.json()["content"]

# Step 2: Chunk
chunk_response = requests.post(
    "https://asista-docling.up.railway.app/chunk/content",
    json={"content": content, "max_tokens": 512}
)
chunks = chunk_response.json()["chunks"]

# Step 3: Store in PGVector
for chunk in chunks:
    # Your PGVector insertion code here
    pass
```

---

## ✅ Summary

- **Two endpoints**: `/chunk` (URL) and `/chunk/content` (content)
- **Recommended**: Use `/chunk/content` for n8n workflows
- **Output**: Same PGVector-compatible format for both
- **Workflow**: Convert → Chunk → Split → Store
- **Files**: Complete n8n workflows provided

**You're ready to build your RAG system!** 🎉
