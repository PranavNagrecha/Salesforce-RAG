# Cursor Prompt Usage Guide

## What Was Actually Done

Two main prompt files were created and used to build the knowledge base. Each serves a specific purpose in the extraction and compilation workflow.

### Master Extraction Prompt

**File**: `cursor/prompts/master-extraction-prompt.md`

**Purpose**: Comprehensive extraction prompt for initial knowledge base creation from ChatGPT exports.

**When to Use**:
- Initial extraction from ChatGPT dump
- Large-scale knowledge base creation
- When you have a complete ChatGPT export to process
- Setting up the knowledge base structure for the first time

**Key Features**:
- Domain model and file layout structure
- Content structure standards (What Was Actually Done, Rules and Patterns, etc.)
- Privacy and redaction rules
- Extraction workflow steps
- Schema file creation

**Workflow**:
1. Place ChatGPT export in `chatgpt/outputs/latest-extraction-notes.md`
2. Run Auto Mode with this prompt
3. Follow the extraction workflow steps
4. Files are created in `knowledge/` domain structure
5. Extraction log is updated in `cursor/outputs/extraction-log.md`

### Compile Real Knowledge Prompt

**File**: `cursor/prompts/compile-real-knowledge.md`

**Purpose**: Refined prompt emphasizing "real work only" - searches both ChatGPT dump AND workspace files for evidence.

**When to Use**:
- After initial extraction is complete
- When you want to enrich knowledge base from workspace files
- When you need to cross-reference dump with actual project files
- When you want to ensure no invented content
- Ongoing knowledge base maintenance

**Key Features**:
- Hard rules: No invented history, only real work
- Workspace search strategy
- Quality checks before adding content
- Source documentation requirements
- Example workflows for handling workspace files

**Workflow**:
1. Have ChatGPT dump available (in workspace or specified file)
2. Run Auto Mode with this prompt
3. Cursor searches ALL workspace files for evidence
4. Extracts concrete details from project files
5. Cross-references with ChatGPT dump
6. Updates knowledge files with validated content
7. Marks uncertain items as "To Validate"

## Rules and Patterns

### Choosing the Right Prompt

- **Use Master Extraction Prompt** for:
  - First-time knowledge base creation
  - Processing large ChatGPT exports
  - Setting up domain structure
  - Initial extraction phase

- **Use Compile Real Knowledge Prompt** for:
  - Enriching existing knowledge base
  - Adding details from workspace files
  - Validating and cross-referencing content
  - Ongoing maintenance and updates

### Prompt Execution

- Always specify which file is the ChatGPT dump
- Review extraction log after each run
- Check "To Validate" sections regularly
- Update addition summaries for tracking
- Keep changes focused (few files per run)

### Workspace Search Strategy

When using Compile Real Knowledge prompt:
1. Identify project folders that might contain relevant files
2. Search for patterns mentioned in ChatGPT dump
3. Extract concrete details (field names, configs, code patterns)
4. Cross-reference with dump for validation
5. Document sources when adding to knowledge base

### Content Validation

Before accepting Cursor's additions:
- Verify content is backed by evidence
- Check that it's your real work (not generic docs)
- Ensure proper anonymization
- Confirm it's useful and actionable
- Review "To Validate" sections

## Suggested Improvements (From AI)

### Prompt Versioning

Implement prompt versioning:
- Track prompt file versions
- Document changes to prompts
- Maintain changelog for prompt updates
- Test prompt changes before full runs

### Automated Prompt Selection

Build automated prompt selection:
- Detect if knowledge base exists (use Compile Real Knowledge)
- Detect if initial setup needed (use Master Extraction)
- Suggest appropriate prompt based on workspace state
- Provide prompt usage recommendations

### Prompt Templates

Create prompt templates for specific scenarios:
- Template for adding new domain
- Template for updating existing files
- Template for workspace-only extraction
- Template for validation and cleanup

## To Validate

- Specific scenarios where each prompt is most effective
- Workspace search patterns that work best
- How to handle conflicts between dump and workspace
- Prompt execution frequency and timing
- Integration with other Cursor workflows

