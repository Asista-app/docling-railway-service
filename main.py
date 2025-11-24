"""
Docling Web Service - FastAPI wrapper for Docling document conversion
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from transformers import AutoTokenizer
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import tempfile
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Docling API",
    description="Document conversion service powered by Docling",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize converter
converter = DocumentConverter()

# Initialize tokenizer for chunking (lazy loading)
_tokenizer = None

def get_tokenizer():
    """Lazy load tokenizer to avoid startup delay"""
    global _tokenizer
    if _tokenizer is None:
        logger.info("Loading tokenizer: sentence-transformers/all-MiniLM-L6-v2")
        _tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return _tokenizer


class URLConvertRequest(BaseModel):
    url: HttpUrl
    output_format: str = "markdown"


class ConvertResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None


class ChunkRequest(BaseModel):
    url: HttpUrl
    max_tokens: int = 512
    merge_peers: bool = True


class ChunkObject(BaseModel):
    content: str
    chunk: int
    chunk_size: int
    tokens: int
    metadata: Optional[dict] = None


class ChunkResponse(BaseModel):
    success: bool
    chunks: Optional[List[ChunkObject]] = None
    total_chunks: Optional[int] = None
    total_tokens: Optional[int] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Docling API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "convert_url": "/convert/url",
            "convert_file": "/convert/file",
            "chunk": "/chunk",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint for Railway"""
    return {"status": "healthy"}


@app.post("/convert/url", response_model=ConvertResponse)
async def convert_from_url(request: URLConvertRequest):
    """
    Convert a document from URL to the specified format
    
    Args:
        request: URLConvertRequest containing URL and output format
        
    Returns:
        ConvertResponse with converted content
    """
    try:
        logger.info(f"Converting document from URL: {request.url}")
        
        # Convert the document
        result = converter.convert(str(request.url))
        
        # Export based on format
        if request.output_format.lower() == "markdown":
            content = result.document.export_to_markdown()
        elif request.output_format.lower() == "json":
            content = result.document.export_to_dict()
        elif request.output_format.lower() == "html":
            content = result.document.export_to_html()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported output format: {request.output_format}"
            )
        
        # Extract metadata
        metadata = {
            "num_pages": len(result.document.pages) if hasattr(result.document, 'pages') else None,
            "source": str(request.url),
            "format": request.output_format
        }
        
        return ConvertResponse(
            success=True,
            content=content if isinstance(content, str) else str(content),
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"Error converting document: {str(e)}")
        return ConvertResponse(
            success=False,
            error=str(e)
        )


@app.post("/convert/file", response_model=ConvertResponse)
async def convert_from_file(
    file: UploadFile = File(...),
    output_format: str = Form("markdown")
):
    """
    Convert an uploaded document file to the specified format
    
    Args:
        file: Uploaded file
        output_format: Desired output format (markdown, json, html)
        
    Returns:
        ConvertResponse with converted content
    """
    temp_file = None
    try:
        logger.info(f"Converting uploaded file: {file.filename}")
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Convert the document
        result = converter.convert(temp_file_path)
        
        # Export based on format
        if output_format.lower() == "markdown":
            converted_content = result.document.export_to_markdown()
        elif output_format.lower() == "json":
            converted_content = result.document.export_to_dict()
        elif output_format.lower() == "html":
            converted_content = result.document.export_to_html()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported output format: {output_format}"
            )
        
        # Extract metadata
        metadata = {
            "filename": file.filename,
            "num_pages": len(result.document.pages) if hasattr(result.document, 'pages') else None,
            "format": output_format
        }
        
        return ConvertResponse(
            success=True,
            content=converted_content if isinstance(converted_content, str) else str(converted_content),
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"Error converting file: {str(e)}")
        return ConvertResponse(
            success=False,
            error=str(e)
        )
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file: {str(e)}")


@app.post("/chunk", response_model=ChunkResponse)
async def chunk_document(request: ChunkRequest):
    """
    Chunk a document from URL using HybridChunker
    
    Args:
        request: ChunkRequest containing URL, max_tokens, and merge_peers settings
        
    Returns:
        ChunkResponse with array of chunks compatible with PGVector
    """
    try:
        logger.info(f"Chunking document from URL: {request.url}")
        
        # Step 1: Convert the document
        result = converter.convert(str(request.url))
        doc = result.document
        
        # Step 2: Get tokenizer (lazy loaded)
        tokenizer = get_tokenizer()
        
        # Step 3: Create HybridChunker
        chunker = HybridChunker(
            tokenizer=tokenizer,
            max_tokens=request.max_tokens,
            merge_peers=request.merge_peers
        )
        
        # Step 4: Generate chunks
        chunk_iter = chunker.chunk(dl_doc=doc)
        chunks_list = list(chunk_iter)
        
        # Step 5: Format chunks for PGVector compatibility
        formatted_chunks = []
        total_tokens = 0
        
        for i, chunk in enumerate(chunks_list):
            # Get chunk text
            chunk_text = chunk.text
            
            # Calculate tokens
            tokens = tokenizer.encode(chunk_text)
            token_count = len(tokens)
            total_tokens += token_count
            
            # Extract metadata if available
            chunk_metadata = {}
            if hasattr(chunk, 'meta') and chunk.meta:
                chunk_metadata = chunk.meta.model_dump() if hasattr(chunk.meta, 'model_dump') else dict(chunk.meta)
            
            # Format matching your PGVector structure
            formatted_chunks.append(ChunkObject(
                content=chunk_text,
                chunk=i,
                chunk_size=len(chunk_text),
                tokens=token_count,
                metadata=chunk_metadata
            ))
        
        logger.info(f"Successfully chunked document into {len(formatted_chunks)} chunks")
        
        return ChunkResponse(
            success=True,
            chunks=formatted_chunks,
            total_chunks=len(formatted_chunks),
            total_tokens=total_tokens
        )
        
    except Exception as e:
        logger.error(f"Error chunking document: {str(e)}")
        return ChunkResponse(
            success=False,
            error=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
