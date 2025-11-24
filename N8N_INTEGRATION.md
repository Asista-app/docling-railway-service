# n8n Integration for Docling API

This guide shows you how to use the Docling API for document chunking in your n8n workflows.

## 🎯 Complete Workflow

**File:** `n8n-docling-chunk-workflow.json`

This workflow provides everything you need: URL → Convert → Chunk → PGVector

### How to Import:

1. In n8n, go to **Workflows**
2. Click **"Import from File"**
3. Select `n8n-docling-chunk-workflow.json`
4. The complete workflow will be imported

### Workflow Steps:

```
1. Manual Trigger
   ↓
2. Set Parameters
   - url: Document URL
   - file_id: Your file ID from metadata table
   - max_tokens: 512 (default)
   - merge_peers: true (default)
   ↓
3. Chunk Document
   POST /chunk
   - Converts and chunks in one step
   ↓
4. Split Into Items
   - Splits chunks array
   ↓
5. Insert to PGVector
   - Inserts each chunk to database
```

### Input Parameters:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | Yes | - | Document URL to process |
| `file_id` | string | Yes | - | Your file ID for linking to metadata |
| `max_tokens` | number | No | 512 | Maximum tokens per chunk |
| `merge_peers` | boolean | No | true | Merge small adjacent chunks |

### Output Format:

Each chunk includes:
```json
{
  "content": "chunk text...",
  "chunk": 0,
  "chunk_size": 1234,
  "tokens": 450,
  "metadata": {
    "file_id": "your-file-id-here"
  }
}
```

---

## 🎯 What This Workflow Does

✅ **Converts** document from URL using Docling  
✅ **Chunks** intelligently using HybridChunker  
✅ **Respects** document structure (paragraphs, sections, tables)  
✅ **Token-aware** - fits within embedding model limits  
✅ **Includes** file_id for linking to your metadata table  
✅ **PGVector ready** - direct insertion to database  

**Perfect for:**
- RAG (Retrieval Augmented Generation) systems
- Semantic search
- Document Q&A chatbots
- Knowledge bases

---

## 📋 Supported Input Formats

Your Docling API supports these document types:
- PDF files
- DOCX (Microsoft Word)
- PPTX (Microsoft PowerPoint)
- HTML files
- XLSX (Excel)
- Images (with OCR)
- Markdown
- And more!

## 📤 Output Formats

Choose one of these formats:
- `markdown` - Markdown text (default)
- `json` - Structured JSON
- `html` - HTML format

## 🔧 Configuration Options

### Timeout
The node is configured with a 120-second timeout (2 minutes) to handle large documents.

To change it:
1. Click on the node
2. Go to **"Options"** → **"Timeout"**
3. Set your desired timeout in milliseconds (e.g., 180000 for 3 minutes)

### Error Handling

The node returns errors in the response:
```json
{
  "success": false,
  "content": null,
  "metadata": null,
  "error": "Error message here"
}
```

You can use an **IF** node to check `success` and handle errors.

---

## 💡 Example Workflows

### Example 1: Convert PDF from URL

```
[Manual Trigger] → [Set URL] → [Docling Convert] → [Output]
```

**Set URL node:**
```json
{
  "documentUrl": "https://arxiv.org/pdf/2408.09869",
  "outputFormat": "markdown"
}
```

### Example 2: Batch Convert Multiple Documents

```
[Webhook/Trigger] → [Loop Over Items] → [Docling Convert] → [Save to Database]
```

**Input data:**
```json
[
  {"url": "https://example.com/doc1.pdf"},
  {"url": "https://example.com/doc2.docx"},
  {"url": "https://example.com/doc3.html"}
]
```

### Example 3: Convert and Extract Content

```
[Trigger] → [Docling Convert] → [Extract Data] → [Send Email]
```

Use **Code** node to extract specific content:
```javascript
// Extract just the content
return [{
  json: {
    content: $input.item.json.content,
    pages: $input.item.json.metadata.num_pages
  }
}];
```

### Example 4: Convert with Error Handling

```
[Trigger] → [Docling Convert] → [IF] 
                                   ├─ Success → [Process Content]
                                   └─ Error → [Send Alert]
```

**IF node condition:**
```
{{ $json.success }} equals true
```

---

## 🔗 Using with Other Nodes

### With Google Drive
```
[Google Drive Trigger] → [Get File URL] → [Docling Convert] → [Save to Database]
```

### With Webhook
```
[Webhook] → [Docling Convert] → [HTTP Response]
```

**Webhook payload:**
```json
{
  "documentUrl": "https://example.com/file.pdf",
  "outputFormat": "markdown"
}
```

### With Airtable
```
[Airtable Trigger] → [Docling Convert] → [Update Airtable Record]
```

---

## 🎯 Field Mapping

The node accepts these input field names (flexible):

| Field | Alternative Names | Required | Default |
|-------|------------------|----------|---------|
| Document URL | `documentUrl`, `url` | Yes | - |
| Output Format | `outputFormat`, `format` | No | `markdown` |

---

## 🐛 Troubleshooting

### "Timeout Error"
- Increase timeout in node settings
- Large PDFs take longer to process
- Try with a smaller document first

### "Invalid URL"
- Ensure URL is publicly accessible
- Check URL format (must include https://)
- Test URL in browser first

### "Conversion Failed"
- Check document format is supported
- Verify document is not corrupted
- Check error message in output

### "No Output"
- Check if node executed successfully
- Verify input data format
- Look at execution logs

---

## 📊 Performance Tips

1. **Batch Processing**: Process documents in parallel using **Split In Batches** node
2. **Caching**: Store converted documents to avoid re-processing
3. **Async Processing**: Use webhooks for long-running conversions
4. **Error Retry**: Add retry logic for failed conversions

---

## 🔒 Security Notes

- Your API is publicly accessible at: `https://asista-docling.up.railway.app`
- Consider adding authentication if needed
- Don't expose sensitive documents via public URLs
- Monitor API usage in Railway dashboard

---

## 📝 API Endpoint

The node calls this endpoint:
```
POST https://asista-docling.up.railway.app/convert/url
```

**Request:**
```json
{
  "url": "https://example.com/document.pdf",
  "output_format": "markdown"
}
```

**Response:**
```json
{
  "success": true,
  "content": "converted content...",
  "metadata": {
    "num_pages": 5,
    "source": "https://example.com/document.pdf",
    "format": "markdown"
  },
  "error": null
}
```

---

## 🎉 You're Ready!

Import the JSON file into n8n and start converting documents!

**Files Available:**
- `n8n-simple-docling-node.json` - Single node (easiest)
- `n8n-docling-workflow.json` - Complete workflow example
- `n8n-docling-node.json` - Basic node template

**Need Help?**
- Check n8n documentation: https://docs.n8n.io/
- Test your API: https://asista-docling.up.railway.app/docs
