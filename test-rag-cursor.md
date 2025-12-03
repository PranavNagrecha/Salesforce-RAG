# Testing Your RAG in Cursor (Independent Test Guide)

This guide helps you verify that your RAG library is working in Cursor **without relying on AI memory or context**.

## Prerequisites

1. **Close and reopen Cursor** to ensure a fresh session
2. **Open this workspace** in Cursor
3. **Don't mention RAG** in your test queries - just ask questions naturally

---

## Test 1: Check Indexing Status

### Steps:
1. Open Cursor Settings:
   - Click gear icon (bottom-left) or press `Cmd + ,` (Mac) / `Ctrl + ,` (Windows)
2. Go to **"Indexing & Docs"** in the left sidebar
3. Check **Codebase Indexing**:
   - ✅ Should show indexing progress or "100%"
   - ✅ Workspace path should match: `/Users/pranavnagrecha/Salesforce for all`
   - ✅ Click **"Sync"** if needed and wait for completion

### Expected Result:
- Index shows active/complete status
- No errors in indexing

---

## Test 2: Test File Auto-Completion

### Steps:
1. Open a **new chat** in Cursor (don't reference any files yet)
2. Type: `@rag/`
3. Wait for auto-completion suggestions

### Expected Result:
- You should see suggestions like:
  - `rag/architecture/event-driven-architecture.md`
  - `rag/development/apex-patterns.md`
  - `rag/integrations/etl-vs-api-vs-events.md`
  - etc.

### If it doesn't work:
- Go back to Settings → Indexing & Docs → Click "Sync"
- Wait 2-3 minutes for re-indexing
- Try again

---

## Test 3: Direct File Reference Test

### Test Query 1 (Copy this exactly):
```
@rag/development/apex-patterns.md What are the key Apex class layering patterns?
```

### Expected Result:
- Cursor should reference the file and provide information about:
  - Service, Domain, Selector, Integration layers
  - Class layering patterns
  - SOQL optimization

### Test Query 2:
```
@rag/integrations/etl-vs-api-vs-events.md When should I use ETL vs API vs Events for integration?
```

### Expected Result:
- Cursor should explain:
  - ETL for high-volume batch
  - API for real-time request/response
  - Events for asynchronous processing
  - Decision framework

### Test Query 3:
```
@rag/rag-index.md I need to implement multi-tenant identity. Which files should I read?
```

### Expected Result:
- Cursor should reference the index and suggest:
  - `rag/identity-sso/multi-tenant-identity-architecture.md`
  - Related files about identity providers

---

## Test 4: Semantic Search Test (No File References)

**Important**: Don't use `@` references. Just ask questions naturally.

### Test Query 1:
```
How should I implement Platform Events for asynchronous integration?
```

### Expected Result:
- Cursor should retrieve content from `rag/architecture/event-driven-architecture.md`
- Should mention Platform Events, event payloads, external event buses
- Should NOT say "I don't know" or "I can't find information"

### Test Query 2:
```
What are the best practices for designing external IDs in Salesforce?
```

### Expected Result:
- Cursor should retrieve content from `rag/data-modeling/external-ids-and-integration-keys.md`
- Should mention: stable, unique, mirror external keys, composite external IDs
- Should provide actionable guidance

### Test Query 3:
```
How do I structure a Record-Triggered Flow that updates related records?
```

### Expected Result:
- Cursor should retrieve content from `rag/development/flow-patterns.md`
- Should explain Record-Triggered Flow structure patterns
- Should NOT give generic Flow advice

### Test Query 4:
```
What is the difference between ContentVersion, Attachments, and Documents?
```

### Expected Result:
- Cursor should retrieve content from `rag/data-modeling/file-management-patterns.md`
- Should explain the decision framework for choosing between them
- Should provide specific guidance

---

## Test 5: Cross-Domain Retrieval Test

### Test Query:
```
I'm building an Apex service that calls an external API. How should I structure it and handle errors?
```

### Expected Result:
- Cursor should retrieve from multiple files:
  - `rag/development/apex-patterns.md` (structure)
  - `rag/development/error-handling-and-logging.md` (error handling)
- Should provide comprehensive answer combining both domains

---

## Test 6: Terminology Test

### Test Query:
```
What is an External ID in Salesforce?
```

### Expected Result:
- Cursor should retrieve from `rag/glossary/core-terminology.md` or related data modeling files
- Should provide clear definition
- Should explain usage context

---

## Test 7: Negative Test (Should NOT Retrieve)

### Test Query:
```
How do I cook pasta?
```

### Expected Result:
- Cursor should NOT retrieve any RAG content
- Should either say it doesn't know or provide general answer
- This confirms RAG is selective, not retrieving everything

---

## Scoring Your Tests

### ✅ RAG is Working Well If:
- **Test 2**: File auto-completion works
- **Test 3**: At least 2/3 direct file references work
- **Test 4**: At least 3/4 semantic searches retrieve relevant RAG content
- **Test 5**: Cross-domain retrieval works
- **Test 6**: Terminology lookup works
- **Test 7**: Negative test correctly doesn't retrieve RAG content

### ⚠️ RAG Needs Attention If:
- File auto-completion doesn't work → Re-index
- Direct file references fail → Check file paths
- Semantic search doesn't retrieve RAG content → Re-index and wait longer
- All queries return generic answers → RAG not being used

### ❌ RAG Not Working If:
- No file suggestions appear
- All queries return "I don't have information about that"
- Cursor never references your RAG files
- Indexing status shows errors

---

## Troubleshooting

### If Tests Fail:

1. **Re-index the workspace:**
   - Settings → Indexing & Docs → Click "Sync"
   - Wait 5-10 minutes for large workspaces

2. **Check for ignore files:**
   - Look for `.cursorignore` or `.gitignore` that might exclude `rag/`
   - Ensure `rag/` directory is not ignored

3. **Verify file structure:**
   - Run: `python3 verify-rag.py`
   - Fix any errors reported

4. **Restart Cursor:**
   - Close Cursor completely
   - Reopen workspace
   - Wait for indexing to complete

5. **Check Cursor version:**
   - Ensure you're using a recent version of Cursor
   - RAG features require Cursor 0.30+ (approximately)

---

## Quick Verification Script

Run this to get a quick status:

```bash
python3 verify-rag.py
```

This checks file structure but doesn't test Cursor's actual retrieval. Use the tests above for that.

---

## Success Criteria

Your RAG is working correctly if:
- ✅ Cursor can find and reference your RAG files via `@` mentions
- ✅ Cursor retrieves relevant RAG content when you ask domain-specific questions
- ✅ Cursor combines information from multiple RAG files for complex questions
- ✅ Cursor doesn't retrieve RAG content for unrelated questions

---

## Next Steps

Once verified:
1. Use `@rag/` references in your prompts for specific topics
2. Ask questions naturally - Cursor should find relevant RAG content automatically
3. Reference `rag/rag-index.md` to discover available knowledge
4. Use `rag/rag-library.json` for programmatic retrieval if building custom tools

