#!/bin/bash

# Your Railway URL
API_URL="https://asista-docling.up.railway.app"

echo "=========================================="
echo "Testing Docling API Deployment"
echo "URL: $API_URL"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -s "$API_URL/health" | jq '.'
echo ""
echo ""

# Test 2: Root Endpoint
echo "2. Testing Root Endpoint..."
curl -s "$API_URL/" | jq '.'
echo ""
echo ""

# Test 3: Convert a small document
echo "3. Testing Document Conversion (this may take 30-60 seconds)..."
echo "Converting: https://arxiv.org/pdf/2408.09869"
echo ""

curl -X POST "$API_URL/convert/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://arxiv.org/pdf/2408.09869", "output_format": "markdown"}' \
  -s | jq '.'

echo ""
echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo ""
echo "To view interactive API docs, open:"
echo "$API_URL/docs"
