"""
Simple test script for the Docling API
"""
import requests
import json

# Change this to your Railway URL after deployment
# BASE_URL = "http://localhost:8000"  # For local testing
BASE_URL = "https://asista-docling.up.railway.app"  # Production

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_convert_url():
    """Test URL conversion"""
    print("Testing URL conversion...")
    payload = {
        "url": "https://arxiv.org/pdf/2408.09869",
        "output_format": "markdown"
    }
    response = requests.post(f"{BASE_URL}/convert/url", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"Success! Converted {result.get('metadata', {}).get('num_pages', 'N/A')} pages")
        print(f"Content preview (first 200 chars):")
        print(result.get("content", "")[:200] + "...\n")
    else:
        print(f"Error: {result.get('error')}\n")
    
    return response.status_code == 200

def test_convert_file():
    """Test file upload conversion"""
    print("Testing file upload...")
    print("Note: This test requires a local PDF file named 'test.pdf'")
    
    try:
        with open("test.pdf", "rb") as f:
            files = {"file": ("test.pdf", f, "application/pdf")}
            data = {"output_format": "markdown"}
            response = requests.post(f"{BASE_URL}/convert/file", files=files, data=data)
            
            print(f"Status: {response.status_code}")
            result = response.json()
            
            if result.get("success"):
                print(f"Success! Converted file")
                print(f"Content preview (first 200 chars):")
                print(result.get("content", "")[:200] + "...\n")
            else:
                print(f"Error: {result.get('error')}\n")
            
            return response.status_code == 200
    except FileNotFoundError:
        print("Skipping file upload test (test.pdf not found)\n")
        return True

def test_chunking():
    """Test document chunking with HybridChunker"""
    print("Testing document chunking...")
    
    # Google Drive document for testing
    test_url = "https://drive.google.com/uc?export=download&id=1-uvOaGNCSJOKcCuKkHD4pez4dMqazwzL"
    
    payload = {
        "url": test_url,
        "max_tokens": 512,
        "merge_peers": True,
        "file_id": "test-doc-001"
    }
    
    print(f"Document URL: {test_url}")
    print(f"Max tokens per chunk: {payload['max_tokens']}")
    print(f"Merge peers: {payload['merge_peers']}")
    
    response = requests.post(f"{BASE_URL}/chunk", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"✓ Success! Document chunked")
        print(f"  Total chunks: {result.get('total_chunks', 0)}")
        print(f"  Total tokens: {result.get('total_tokens', 0)}")
        
        if result.get('total_chunks', 0) > 0:
            avg_tokens = result['total_tokens'] / result['total_chunks']
            print(f"  Avg tokens/chunk: {avg_tokens:.1f}")
            
            # Show first chunk details
            first_chunk = result['chunks'][0]
            print(f"\n  First chunk details:")
            print(f"    Chunk index: {first_chunk['chunk']}")
            print(f"    Chunk size: {first_chunk['chunk_size']} chars")
            print(f"    Tokens: {first_chunk['tokens']}")
            print(f"    Content preview: {first_chunk['content'][:150]}...")
            
            if first_chunk.get('metadata'):
                print(f"    Metadata: {first_chunk['metadata']}")
        
        print()
        return response.status_code == 200
    else:
        print(f"✗ Error: {result.get('error')}\n")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Docling API Test Suite")
    print("=" * 50 + "\n")
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("URL Conversion", test_convert_url),
        ("File Upload", test_convert_file),
        ("Document Chunking", test_chunking),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"Error in {name}: {str(e)}\n")
            results.append((name, False))
    
    print("=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
