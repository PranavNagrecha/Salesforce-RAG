#!/bin/bash

# Clear Research - Archive research sources and topics
# This script moves research files to archive without deleting them

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESEARCH_DIR="$SCRIPT_DIR/Knowledge/research"
ARCHIVE_BASE="$SCRIPT_DIR/archive/research"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
ARCHIVE_DIR="$ARCHIVE_BASE/$TIMESTAMP"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Clearing Research - Archiving files...${NC}"

# Check if research directory exists
if [ ! -d "$RESEARCH_DIR" ]; then
    echo "Error: Research directory not found at $RESEARCH_DIR"
    exit 1
fi

# Create archive directory structure
mkdir -p "$ARCHIVE_DIR/sources"
mkdir -p "$ARCHIVE_DIR/topics"

# Count files to archive
SOURCE_COUNT=$(find "$RESEARCH_DIR/sources" -type f 2>/dev/null | wc -l | tr -d ' ')
TOPIC_COUNT=$(find "$RESEARCH_DIR/topics" -type f 2>/dev/null | wc -l | tr -d ' ')
TOTAL_COUNT=$((SOURCE_COUNT + TOPIC_COUNT))

if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}No research files found to archive.${NC}"
    exit 0
fi

# Move source files
if [ -d "$RESEARCH_DIR/sources" ] && [ "$SOURCE_COUNT" -gt 0 ]; then
    echo -e "Archiving ${SOURCE_COUNT} source file(s)..."
    mv "$RESEARCH_DIR/sources"/* "$ARCHIVE_DIR/sources/" 2>/dev/null
    echo -e "${GREEN}✓ Sources archived${NC}"
fi

# Move topic files
if [ -d "$RESEARCH_DIR/topics" ] && [ "$TOPIC_COUNT" -gt 0 ]; then
    echo -e "Archiving ${TOPIC_COUNT} topic file(s)..."
    mv "$RESEARCH_DIR/topics"/* "$ARCHIVE_DIR/topics/" 2>/dev/null
    echo -e "${GREEN}✓ Topics archived${NC}"
fi

# Create archive info file
cat > "$ARCHIVE_DIR/archive-info.txt" << EOF
Research Archive
================
Archived: $(date)
Source Files: $SOURCE_COUNT
Topic Files: $TOPIC_COUNT
Total Files: $TOTAL_COUNT

Original Location: $RESEARCH_DIR
Archive Location: $ARCHIVE_DIR
EOF

echo ""
echo -e "${GREEN}✓ Research cleared successfully!${NC}"
echo -e "  Archived ${TOTAL_COUNT} file(s) to: ${ARCHIVE_DIR}"
echo -e "  Files are preserved and can be retrieved if needed."




