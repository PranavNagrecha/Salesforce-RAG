# Salesforce Knowledge → RAG → Public Workflow

This document explains **how all the prompts fit together** and the recommended order of execution.

There are four main steps:

1. Extract knowledge from ChatGPT (history + long-term memory)
2. Extract knowledge from Cursor (real code + docs)
3. Build / refresh the RAG library from both dumps
4. Clean the RAG library for public release

---

## Step 0 – Repo Layout (once)

Recommended repo structure:

```text
Knowledge/              # raw dumps (never edited by hand)
rag/                    # cleaned RAG library (what others will use)
cursor/prompts/         # Cursor-side prompts
chatgpt/                # ChatGPT-side prompts (optional)
```

Prompts:

- ChatGPT:
  - `chatgpt/01-chatgpt-master-extraction.md`
- Cursor:
  - `cursor/prompts/02-cursor-master-extraction.md`
  - `cursor/prompts/03-rag-refresh-from-knowledge.md`
  - `cursor/prompts/04-public-clean-pass.md`

---

## Step 1 – ChatGPT Master Extraction (GPT → Knowledge)

**Prompt:** `01-chatgpt-master-extraction.md` (run in ChatGPT)  
**Output file:** `Knowledge/GPT Response.md`

What you do:

1. Open ChatGPT.
2. Paste the contents of `01-chatgpt-master-extraction.md` as the system/user prompt.
3. Let ChatGPT produce a single large Markdown file that captures your real Salesforce experience.
4. Copy the full output and save it in your repo as:
   - `Knowledge/GPT Response.md`

Rules:

- You never edit this file directly after saving.
- When you want a new snapshot, overwrite it with a fresh run.

---

## Step 2 – Cursor Master Extraction (Workspace → Knowledge)

**Prompt:** `cursor/prompts/02-cursor-master-extraction.md` (run in Cursor)  
**Output file:** `Knowledge/cursor-responses.md`

What you do:

1. Open the repo as a **workspace** in Cursor.
2. Open `cursor/prompts/02-cursor-master-extraction.md` in a tab.
3. Start a new chat in Cursor and paste that prompt.
4. Let Cursor scan the workspace and generate an article-style dump.
5. Save the model’s output as:
   - `Knowledge/cursor-responses.md`

Rules:

- Only workspace evidence (code, metadata, docs) is treated as truth.
- The file is anonymized and structured by real project context, integrations, identity, data modeling, etc.
- As with the GPT dump, treat this as read-only after creation.

---

## Step 3 – RAG Refresh From Knowledge Dumps

**Prompt:** `cursor/prompts/03-rag-refresh-from-knowledge.md` (run in Cursor)  
**Inputs:**

- `Knowledge/GPT Response.md`
- `Knowledge/cursor-responses.md`
- Real code + docs in the repo

**Outputs:**
- New/updated files under `rag/**`
- Updated `rag-index.md`
- Updated `rag-library.json`

What you do:

1. In Cursor, open `cursor/prompts/03-rag-refresh-from-knowledge.md`.
2. Start a chat and paste the prompt.
3. Optionally tell it which domain to focus on (e.g. integrations, identity, data modeling).
4. Let it:
   - Read relevant portions of the two dumps + any workspace evidence.
   - Create or update RAG docs in `rag/**`.
   - Update the index and manifest.

You can run this step repeatedly as you iterate on the RAG library.

---

## Step 4 – Public Release Clean Pass

**Prompt:** `cursor/prompts/04-public-clean-pass.md` (run in Cursor)  
**Inputs:**

- `README.md`
- `rag/**`
- `rag-index.md`
- `rag-library.json`
- `examples/**`
- Any public-facing prompt docs (e.g. `cursor/prompts/Public RAG Command.md`, if you create it)

**Outputs:**

- Same files, but with:
  - AI-generation boilerplate removed
  - Placeholder license text removed or normalized

What you do:

1. Once you’re happy with the RAG content, open `cursor/prompts/04-public-clean-pass.md`.
2. Run it in a chat.
3. Review the changes in Git to confirm nothing important was removed.

This step is safe to rerun whenever you add new docs and want to clean them before publishing.

---

## Typical End-to-End Run

When you want to refresh everything end-to-end:

1. **Run ChatGPT extraction**  
   - Use `01-chatgpt-master-extraction.md` in ChatGPT  
   - Save output → `Knowledge/GPT Response.md`

2. **Run Cursor extraction**  
   - Use `02-cursor-master-extraction.md` in Cursor  
   - Save output → `Knowledge/cursor-responses.md`

3. **Refresh RAG**  
   - Use `03-rag-refresh-from-knowledge.md` in Cursor  
   - Update `rag/**`, `rag-index.md`, `rag-library.json`

4. **Clean for public**  
   - Use `04-public-clean-pass.md` in Cursor  
   - Scrub AI/license boilerplate

After that, you can:

- Commit and push `rag/**`, `rag-index.md`, `rag-library.json`, `README.md`, `examples/**`, and any public prompts.
- Keep `Knowledge/**` private or git-ignored if you don’t want to expose raw dumps.

This gives you a repeatable, 4-step pipeline from **lived experience → dumps → structured RAG → public-safe repository**.
