#!/bin/bash
# Quick check script for Cursor indexing status
# This script helps verify if files are being indexed

echo "=========================================="
echo "Cursor RAG Indexing Check"
echo "=========================================="
echo ""

# Check if rag directory exists
if [ -d "rag" ]; then
    echo "✅ rag/ directory exists"
    
    # Count markdown files
    MD_COUNT=$(find rag -name "*.md" -type f | wc -l | tr -d ' ')
    echo "   Found $MD_COUNT markdown files"
    
    # Check key files
    KEY_FILES=(
        "rag/rag-index.md"
        "rag/rag-library.json"
        "rag/architecture/event-driven-architecture.md"
        "rag/development/apex-patterns.md"
        "rag/integrations/etl-vs-api-vs-events.md"
    )
    
    echo ""
    echo "Checking key files:"
    for file in "${KEY_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "   ✅ $file"
        else
            echo "   ❌ $file (MISSING)"
        fi
    done
    
    # Check for ignore files that might block indexing
    echo ""
    echo "Checking for ignore files:"
    if [ -f ".cursorignore" ]; then
        echo "   ⚠️  .cursorignore exists - checking if rag/ is excluded:"
        if grep -q "^rag/" .cursorignore 2>/dev/null || grep -q "^rag$" .cursorignore 2>/dev/null; then
            echo "      ❌ rag/ is in .cursorignore - this will prevent indexing!"
        else
            echo "      ✅ rag/ is NOT excluded"
        fi
    else
        echo "   ✅ No .cursorignore file (rag/ will be indexed)"
    fi
    
    if [ -f ".gitignore" ]; then
        if grep -q "^rag/" .gitignore 2>/dev/null || grep -q "^rag$" .gitignore 2>/dev/null; then
            echo "   ⚠️  rag/ is in .gitignore (this shouldn't affect Cursor indexing)"
        fi
    fi
    
else
    echo "❌ rag/ directory does not exist"
    exit 1
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo "1. Open Cursor Settings (Cmd+, or Ctrl+,)"
echo "2. Go to 'Indexing & Docs'"
echo "3. Check that indexing is enabled and shows progress"
echo "4. Click 'Sync' if needed"
echo "5. Wait for indexing to complete"
echo "6. Test with queries from test-rag-queries.txt"
echo ""
