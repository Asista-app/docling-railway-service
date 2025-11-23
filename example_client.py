"""
Example client for using the Docling API
Replace BASE_URL with your Railway deployment URL
"""
import requests
import json
from pathlib import Path

# Update this with your Railway URL after deployment
BASE_URL = "https://your-app.railway.app"

class DoclingClient:
    """Simple client for Docling API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def health_check(self):
        """Check if the service is healthy"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def convert_url(self, url: str, output_format: str = "markdown"):
        """
        Convert a document from URL
        
        Args:
            url: URL of the document to convert
            output_format: Output format (markdown, json, html)
            
        Returns:
            dict: Response with converted content
        """
        payload = {
            "url": url,
            "output_format": output_format
        }
        response = requests.post(f"{self.base_url}/convert/url", json=payload)
        return response.json()
    
    def convert_file(self, file_path: str, output_format: str = "markdown"):
        """
        Convert a local file
        
        Args:
            file_path: Path to the file to convert
            output_format: Output format (markdown, json, html)
            
        Returns:
            dict: Response with converted content
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, self._get_mime_type(file_path))}
            data = {"output_format": output_format}
            response = requests.post(f"{self.base_url}/convert/file", files=files, data=data)
        
        return response.json()
    
    @staticmethod
    def _get_mime_type(file_path: Path) -> str:
        """Get MIME type based on file extension"""
        mime_types = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ".html": "text/html",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        return mime_types.get(file_path.suffix.lower(), "application/octet-stream")


def example_1_convert_pdf_from_url():
    """Example: Convert a PDF from URL to Markdown"""
    print("Example 1: Convert PDF from URL to Markdown")
    print("-" * 50)
    
    client = DoclingClient(BASE_URL)
    
    # Convert a research paper from arXiv
    result = client.convert_url(
        url="https://arxiv.org/pdf/2408.09869",
        output_format="markdown"
    )
    
    if result["success"]:
        print(f"✓ Conversion successful!")
        print(f"Pages: {result['metadata']['num_pages']}")
        print(f"\nFirst 500 characters of content:")
        print(result["content"][:500])
        print("...")
    else:
        print(f"✗ Conversion failed: {result['error']}")
    
    print()


def example_2_convert_to_json():
    """Example: Convert document to JSON format"""
    print("Example 2: Convert to JSON format")
    print("-" * 50)
    
    client = DoclingClient(BASE_URL)
    
    result = client.convert_url(
        url="https://arxiv.org/pdf/2408.09869",
        output_format="json"
    )
    
    if result["success"]:
        print(f"✓ Conversion successful!")
        print(f"\nJSON structure preview:")
        # Parse the content string as JSON if it's a string
        content = result["content"]
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except:
                pass
        print(json.dumps(content, indent=2)[:500])
        print("...")
    else:
        print(f"✗ Conversion failed: {result['error']}")
    
    print()


def example_3_convert_local_file():
    """Example: Convert a local file"""
    print("Example 3: Convert local file")
    print("-" * 50)
    
    client = DoclingClient(BASE_URL)
    
    # This assumes you have a file named 'sample.pdf' in the current directory
    file_path = "sample.pdf"
    
    try:
        result = client.convert_file(
            file_path=file_path,
            output_format="markdown"
        )
        
        if result["success"]:
            print(f"✓ Conversion successful!")
            print(f"Filename: {result['metadata']['filename']}")
            print(f"\nFirst 500 characters of content:")
            print(result["content"][:500])
            print("...")
        else:
            print(f"✗ Conversion failed: {result['error']}")
    except FileNotFoundError as e:
        print(f"✗ {e}")
        print("  Please place a PDF file named 'sample.pdf' in the current directory")
    
    print()


def example_4_save_to_file():
    """Example: Convert and save to file"""
    print("Example 4: Convert and save to file")
    print("-" * 50)
    
    client = DoclingClient(BASE_URL)
    
    result = client.convert_url(
        url="https://arxiv.org/pdf/2408.09869",
        output_format="markdown"
    )
    
    if result["success"]:
        output_file = "converted_document.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["content"])
        
        print(f"✓ Conversion successful!")
        print(f"✓ Saved to: {output_file}")
        print(f"File size: {len(result['content'])} characters")
    else:
        print(f"✗ Conversion failed: {result['error']}")
    
    print()


def example_5_batch_conversion():
    """Example: Convert multiple documents"""
    print("Example 5: Batch conversion")
    print("-" * 50)
    
    client = DoclingClient(BASE_URL)
    
    urls = [
        "https://arxiv.org/pdf/2408.09869",
        "https://arxiv.org/pdf/2206.01062",
    ]
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"Converting document {i}/{len(urls)}...")
        result = client.convert_url(url, output_format="markdown")
        results.append(result)
        
        if result["success"]:
            print(f"  ✓ Success - {result['metadata']['num_pages']} pages")
        else:
            print(f"  ✗ Failed - {result['error']}")
    
    successful = sum(1 for r in results if r["success"])
    print(f"\nCompleted: {successful}/{len(urls)} successful conversions")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("Docling API Client Examples")
    print("=" * 50)
    print(f"Base URL: {BASE_URL}")
    print()
    
    # Check if service is available
    try:
        client = DoclingClient(BASE_URL)
        health = client.health_check()
        print(f"✓ Service is {health.get('status', 'unknown')}")
        print()
    except Exception as e:
        print(f"✗ Cannot connect to service: {e}")
        print("\nPlease update BASE_URL with your Railway deployment URL")
        exit(1)
    
    # Run examples
    try:
        example_1_convert_pdf_from_url()
        example_2_convert_to_json()
        # example_3_convert_local_file()  # Uncomment if you have a local file
        example_4_save_to_file()
        # example_5_batch_conversion()  # Uncomment for batch processing
        
    except Exception as e:
        print(f"Error running examples: {e}")
    
    print("=" * 50)
    print("Examples completed!")
    print("=" * 50)
