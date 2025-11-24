# 🔗 File ID Integration Guide

## Overview

The chunking endpoints now support `file_id` parameter to link chunks with your existing metadata table.

---

## ✅ What Changed

Both chunking endpoints now accept an optional `file_id` parameter:
- `/chunk` (URL-based chunking)
- `/chunk/content` (Content-based chunking)

---

## 📋 Usage

### Endpoint: `/chunk/content`

**Request:**
```json
{
  "content": "Your document content...",
  "max_tokens": 512,
  "merge_peers": true,
  "file_id": "1GUbsAxJB2CmEInyrp7_WJrZDjgisWaR9"
}
```

**Response:**
```json
{
  "success": true,
  "chunks": [
    {
      "content": "chunk text...",
      "chunk": 0,
      "chunk_size": 1234,
      "tokens": 450,
      "metadata": {
        "file_id": "1GUbsAxJB2CmEInyrp7_WJrZDjgisWaR9"
      }
    }
  ],
  "total_chunks": 10,
  "total_tokens": 4500
}
```

---

## 🔄 n8n Workflow

### Complete Workflow: Document → Chunks → PGVector

```
1. [Set Variables]
   - documentUrl: "https://example.com/doc.pdf"
   - file_id: "1GUbsAxJB2CmEInyrp7_WJrZDjgisWaR9"
   ↓
2. [Convert Document]
   POST /convert/url
   ↓
3. [Chunk Content]
   POST /chunk/content
   {
     "content": "{{ $json.content }}",
     "file_id": "{{ $('Set Variables').item.json.file_id }}"
   }
   ↓
4. [Split Items]
   ↓
5. [Insert to PGVector]
   Each chunk has file_id in metadata
```

---

## 🗄️ Database Schema

### Your Existing Metadata Table
```sql
-- You already have this
CREATE TABLE files_metadata (
  file_id TEXT PRIMARY KEY,
  company TEXT,
  project TEXT,
  sub_project TEXT,
  file_title TEXT,
  -- ... other fields
);
```

### Your PGVector Chunks Table
```sql
CREATE TABLE documents_pg (
  id SERIAL PRIMARY KEY,
  content TEXT,
  chunk INTEGER,
  chunk_size INTEGER,
  tokens INTEGER,
  file_id TEXT,  -- Links to files_metadata
  embedding vector(384)
);
```

### Query with JOIN
```sql
-- Get chunks with metadata
SELECT 
  d.content,
  d.chunk,
  f.company,
  f.project,
  f.file_title
FROM documents_pg d
JOIN files_metadata f ON d.file_id = f.file_id
WHERE d.embedding <-> $1 < 0.5
ORDER BY d.embedding <-> $1
LIMIT 5;
```

---

## 🎯 Your Chatbot Workflow

### 1. User Asks Question
```
"What are the specifications for MJL Al Jazi?"
```

### 2. Vector Search
```sql
SELECT 
  d.id,
  d.content,
  d.chunk,
  d.file_id,
  d.embedding <-> $embedding AS distance
FROM documents_pg d
WHERE d.embedding <-> $embedding < 0.5
ORDER BY distance
LIMIT 5;
```

### 3. Get File Metadata
```sql
SELECT 
  f.file_title,
  f.company,
  f.project,
  f.sub_project
FROM files_metadata f
WHERE f.file_id IN ('file_id_1', 'file_id_2', ...);
```

### 4. Generate Response
```
Answer: "Based on the specifications in Final-MJL_Al-Jazi_FP_A.pdf 
(Nakheel - Madinat Jumeirah Living - MJL Al Jazi)..."

[Attach file link if needed]
```

---

## 📊 Benefits

✅ **Minimal Storage** - Only file_id in chunks, not full metadata  
✅ **Easy Updates** - Change company/project in one place  
✅ **Fast Queries** - Smaller chunk records = faster vector search  
✅ **Flexible** - Add new metadata fields without touching chunks  
✅ **Cost Effective** - Less data to store and embed  

---

## 🧪 Testing

### Test with curl:

```bash
# Step 1: Convert
curl -X POST "https://asista-docling.up.railway.app/convert/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://arxiv.org/pdf/2408.09869", "output_format": "markdown"}' \
  > converted.json

# Step 2: Chunk with file_id
curl -X POST "https://asista-docling.up.railway.app/chunk/content" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": $(jq -r '.content' converted.json | jq -Rs .),
    \"max_tokens\": 512,
    \"file_id\": \"1GUbsAxJB2CmEInyrp7_WJrZDjgisWaR9\"
  }" | jq '.chunks[0].metadata'
```

**Expected output:**
```json
{
  "file_id": "1GUbsAxJB2CmEInyrp7_WJrZDjgisWaR9"
}
```

---

## 📝 n8n Node Configuration

The `n8n-chunk-content-node.json` now accepts:

**Input fields:**
- `content` - Document content (from converter)
- `max_tokens` - Max tokens per chunk (default: 512)
- `merge_peers` - Merge small chunks (default: true)
- `file_id` - Your file ID from metadata table

**Output:**
- Each chunk includes `file_id` in metadata
- Ready for direct insertion to PGVector

---

## ✅ Summary

- ✅ Added `file_id` parameter to both chunking endpoints
- ✅ File ID is included in each chunk's metadata
- ✅ Works with your existing metadata table
- ✅ Minimal storage, maximum flexibility
- ✅ Perfect for your chatbot use case

**Deployed and ready to use!** 🚀
