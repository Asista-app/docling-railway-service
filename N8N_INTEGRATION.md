# n8n Integration for Docling API

This guide shows you how to use the Docling document converter and chunking in your n8n workflows.

## 🆕 NEW: Document Chunking for PGVector

The API now includes a `/chunk` endpoint that chunks documents using HybridChunker - perfect for RAG systems and vector databases!

## 🚀 Quick Start

### Option 1: Simple Single Node (Recommended)

**File:** `n8n-simple-docling-node.json`

This is the easiest way to use Docling in n8n - just one HTTP Request node.

#### How to Import:

1. Open your n8n workflow
2. Click the **"+"** button to add a node
3. Click **"Import from File"** or paste JSON
4. Select `n8n-simple-docling-node.json`
5. The node will be added to your canvas

#### How to Use:

**Input Data Required:**
```json
{
  "documentUrl": "https://arxiv.org/pdf/2408.09869",
  "outputFormat": "markdown"
}
```

Or use these alternative field names:
```json
{
  "url": "https://example.com/document.pdf",
  "format": "json"
}
```

**Output Data:**
```json
{
  "success": true,
  "content": "# Document Title\n\nConverted content here...",
  "metadata": {
    "num_pages": 10,
    "source": "https://arxiv.org/pdf/2408.09869",
    "format": "markdown"
  },
  "error": null
}
```

---

### Option 2: Complete Workflow

**File:** `n8n-docling-workflow.json`

This includes a complete workflow with:
- Manual trigger
- Input configuration
- Document conversion
- Output extraction

#### How to Import:

1. In n8n, go to **Workflows**
2. Click **"Import from File"**
3. Select `n8n-docling-workflow.json`
4. The complete workflow will be imported

#### How to Use:

1. Open the **"Set Document URL"** node
2. Change the `documentUrl` value to your document URL
3. Change the `outputFormat` if needed (markdown, json, or html)
4. Click **"Execute Workflow"**
5. View the output in the **"Extract Output"** node

---

## 🔥 Document Chunking Endpoint

**File:** `n8n-chunk-node.json`

### What is Document Chunking?

Chunks documents intelligently for RAG systems and vector databases. Uses HybridChunker which:
- Respects document structure (paragraphs, sections, tables)
- Ensures chunks fit within token limits
- Maintains semantic coherence
- Preserves metadata and context

### How to Use:

**Input Data:**
```json
{
  "documentUrl": "https://example.com/document.pdf",
  "max_tokens": 512,
  "merge_peers": true
}
```

**Output Data (PGVector Compatible):**
```json
{
  "success": true,
  "chunks": [
    {
      "content": "chunk text content...",
      "chunk": 0,
      "chunk_size": 1234,
      "tokens": 450,
      "metadata": {
        "doc_items": [...],
        "headings": [...]
      }
    }
  ],
  "total_chunks": 10,
  "total_tokens": 4500
}
```

### Complete Workflow: Chunk to PGVector

**File:** `n8n-chunk-to-pgvector-workflow.json`

This workflow shows the complete process:
1. Set document URL
2. Call chunk endpoint
3. Extract chunks array
4. Split into individual items
5. Insert into Postgres PGVector table

**Perfect for:**
- RAG (Retrieval Augmented Generation) systems
- Semantic search
- Document Q&A systems
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
