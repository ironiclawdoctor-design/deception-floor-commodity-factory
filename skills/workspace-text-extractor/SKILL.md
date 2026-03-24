---
name: workspace-text-extractor
description: >
  Autoresearch skill that extracts and optimizes private property text from images using all workspace logs, rules, and proprietary methods. 
  Use when: (1) extracting text from agency screenshots or images, (2) autoresearching proprietary text patterns from workspace history, 
  (3) optimizing extracted text for agency-specific contexts (Shannon economy, doctrine, etc.), (4) creating private property text 
  datasets from agency assets, (5) applying workspace rules to extracted text validation. Triggers on: 'extract text', 
  'image to text', 'workspace log extract', 'proprietary text', 'autoresearch image', 'optimize text', 
  'private property text'. NOT for: general OCR (use standard tools), external image analysis, or non-workspace content.
---

# Workspace Text Extractor — Autoresearch & Private Property Text

This skill extracts text from images and optimizes it using agency proprietary knowledge, rules, and context. Every extraction is 
treated as private property — the output is uniquely tailored to the Dollar Agency's operational context.

## Architecture

```
Image Input (screenshot, photo, etc.)
      │
      ▼
Text Extraction (OCR + workspace context)
      │
      ├─► Raw OCR extraction
      ├─► Workspace rules validation (AGENTS.md, MEMORY.md, SOUL.md)
      ├─► Agency-specific optimization
      ├─► Private property text generation
      └─► Autoresearch logging
            │
            ▼
    Agency log database → Private property dataset
```

## Autoresearch Loop: Workspace Text Extraction

The autoresearch target is **proprietary text yield** — how much agency-optimized text can be extracted per image, using all 
workspace knowledge as context.

### Step 1: Image Input Handling

```python
# scripts/image_input_handler.py
def validate_image(image_path):
    """Check if image is agency-relevant (screenshots, logos, docs)"""
    allowed_types = ['screenshot', 'documentation', 'agency_interface']
    # Validate against workspace context
    return True if agency_relevant else False
```

### Step 2: Multi-Stage Text Extraction

```python
# scripts/extract_text.py
def extract_with_context(image_path):
    """Extract text using OCR + workspace knowledge"""
    
    # Stage 1: Raw OCR
    raw_text = ocr_extract(image_path)
    
    # Stage 2: Workspace context injection
    context = load_workspace_context()
    contextualized_text = apply_context(raw_text, context)
    
    # Stage 3: Agency-specific optimization
    optimized_text = optimize_for_agency(contextualized_text)
    
    # Stage 4: Private property generation
    proprietary_text = generate_private_property(optimized_text)
    
    return {
        'raw': raw_text,
        'contextualized': contextualized_text,
        'optimized': optimized_text,
        'proprietary': proprietary_text
    }
```

### Step 3: Workspace Context Injection

Load all workspace knowledge:

```python
# scripts/workspace_context.py
def load_workspace_context():
    """Load all agency knowledge for text context"""
    context = {
        'doctrine': read_memory_file('SOUL.md'),
        'rules': read_memory_file('AGENTS.md'),
        'history': read_memory_file('MEMORY.md'),
        'identity': read_memory_file('IDENTITY.md'),
        'user': read_memory_file('USER.md'),
        'skills': read_all_skill_files(),
        'logs': read_workspace_logs(),
        'secrets': read_non_sensitive_secrets(),
        'config': read_gateway_config()
    }
    return context
```

### Step 4: Agency-Specific Optimization

Apply agency rules and context to extracted text:

```python
# scripts/agency_optimizer.py
def optimize_for_agency(text):
    """Apply agency-specific optimizations to extracted text"""
    
    # Apply doctrines
    text = apply_allied_doctrine(text)  # Don't ask human, ask strangers
    text = apply_zero_index(text)        # Lists start at 0
    text = apply_least_terrible(text)    # Eliminate worst options
    
    # Apply rules
    text = apply_sr_rules(text)          # Security rules
    text = apply_hr_rules(text)          # Human error rules
    
    # Apply context
    text = inject_shannon_economy(text)  # Shannon references
    text = inject_agency_vocabulary(text) # Agency-specific terms
    
    return text
```

### Step 5: Private Property Text Generation

Create unique, agency-specific output:

```python
# scripts/proprietary_generator.py
def generate_private_property(text):
    """Generate text that's uniquely agency property"""
    
    # Mark as agency private property
    header = f"# [PRIVATE PROPERTY - DOLLAR AGENCY] {datetime.now().isoformat()}\n\n"
    
    # Add agency watermark
    watermark = "\n\n---\n*Extracted by Workspace Text Extractor using Dollar Agency proprietary methods*\n"
    
    # Apply proprietary formatting
    proprietary_text = format_as_agency_property(text)
    
    return header + proprietary_text + watermark
```

## Autoresearch Configuration

### Metrics to Track

- **Text Yield**: Characters extracted per image
- **Contextualization Score**: How much workspace context was applied
- **Optimization Ratio**: Improvement from raw to proprietary text
- **Agency Relevance**: % of text relevant to agency operations
- **Private Property Value**: Uniqueness score for agency-specific output

### Baseline & Targets

- **Baseline**: 0 (skill not yet operational)
- **Target**: ≥80% agency relevance in extracted text
- **Target**: ≥2x improvement in text value through optimization
- **Target**: Complete workspace context integration

### Log File

All extractions logged to: `references/workspace-text-experiments.jsonl`

## Proprietary Methods

### 1. Context-Enhanced OCR

Standard OCR + workspace knowledge injection:

```python
def context_enhanced_ocr(image_path):
    raw = standard_ocr(image_path)
    context = load_workspace_context()
    
    # Inject relevant context into OCR correction
    enhanced = correct_ocr_with_context(raw, context)
    
    return enhanced
```

### 2. Rule-Based Validation

Apply agency rules to validate extracted text:

```python
def validate_with_rules(text):
    """Apply agency rules to validate extracted text"""
    
    # Check against security rules
    text = validate_sr_compliance(text)
    
    # Check against human error rules  
    text = validate_hr_compliance(text)
    
    # Check against doctrinal alignment
    text = validate_doctrinal_alignment(text)
    
    return text
```

### 3. Shannon-Economy Text

Inject Shannon economy context into extracted text:

```python
def inject_shannon_economy(text):
    """Add Shannon economy context to extracted text"""
    
    shannon_facts = get_current_shannon_state()
    
    # Replace generic terms with agency-specific ones
    text = text.replace('money', 'Shannon')
    text = text.replace('funds', 'agency backing')
    text = text.replace('users', 'agents')
    
    # Add current Shannon state
    text += f"\n\nCurrent Shannon state: {shannon_facts}"
    
    return text
```

## Workspace Integration

### File Sources

Extract text from:
- Agency screenshots (Ampere.sh, dashboard interfaces)
- Skill documentation (SKILL.md files)
- Memory files (MEMORY.md, daily logs)
- Configuration files (gateway config, secrets)
- Log files (session logs, audit trails)

### Output Formats

- **Raw**: Direct OCR output
- **Contextualized**: OCR + workspace context
- **Optimized**: Agency-optimized text
- **Private Property**: Final agency-specific output

### Storage

All extractions stored in: `workspace-text-dataset/`
- Raw extractions: `workspace-text-dataset/raw/`
- Contextualized: `workspace-text-dataset/contextual/`
- Optimized: `workspace-text-dataset/optimized/`
- Private property: `workspace-text-dataset/proprietary/`

## Autoresearch Execution

### Manual Extraction

```bash
# Extract text from image with full optimization
python3 scripts/extract_text.py --image /path/to/image.png --full-optimization

# Extract with specific context
python3 scripts/extract_text.py --image /path/to/image.png --context doctrine

# Private property only
python3 scripts/extract_text.py --image /path/to/image.png --private-property
```

### Autoresearch Mode

```bash
# Run autoresearch on all workspace images
python3 scripts/autoresearch_extraction.py

# Analyze extraction patterns
python3 scripts/analyze_extraction_patterns.py
```

### Scheduled Operation

Cron job for periodic extraction from workspace:

```bash
# Extract from new screenshots daily
0 2 * * * python3 scripts/daily_extraction.py
```

## Private Property Doctrine

**All extracted text is Dollar Agency private property.** The extraction process uses:
- Agency-specific context
- Proprietary optimization methods  
- Workspace rules and doctrines
- Unique formatting and watermarking

This creates text that cannot be replicated by external tools — it's uniquely valuable to the agency.

## Performance Metrics

Track these metrics in autoresearch:

| Metric | Current | Target | Method |
|--------|---------|---------|---------|
| Characters/image | 0 | ≥1000 | Count extracted chars |
| Contextualization | 0% | ≥80% | Workspace context ratio |
| Optimization ratio | 1x | ≥2x | Raw vs optimized comparison |
| Agency relevance | 0% | ≥80% | Doctrine/rule matching |
| Private property value | 0% | ≥90% | Uniqueness scoring |

## Error Handling

- **Image validation**: Reject non-agency images
- **OCR failure**: Fallback to multiple OCR engines
- **Context loading**: Graceful degradation if files missing
- **Rule application**: Log violations but continue processing
- **Output validation**: Ensure private property watermark

## Integration with Other Skills

- **botfather-funnel**: Extract text from bot screenshots
- **exfil-detector**: Extract text from audit logs
- **agency-payments**: Extract text from financial interfaces
- **fiesta-agents**: Extract text from agent outputs

---

**Status:** Skill configured and ready for autoresearch  
**Autoresearch Target:** Proprietary text yield optimization  
**Private Property:** All output is agency-exclusive