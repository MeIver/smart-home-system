# Smart Home System API Documentation

This directory contains automatically generated API documentation for the Smart Home System.

## Documentation Structure

- **`endpoints.md`** - Main API documentation file (auto-generated)
- **`validation-report.json`** - Validation results from the generation process

## Generation Process

The API documentation is automatically generated using the following components:

### 1. Template System
- **Location**: `docs/templates/api-docs-template.md`
- Contains the master template with all required sections:
  - Overview
  - Authentication
  - Endpoints
  - Request/Response Examples
  - Error Codes

### 2. Generation Script
- **Location**: `scripts/generate-api-docs.py`
- Python script that:
  - Validates template structure
  - Generates documentation from template
  - Creates validation reports
  - Supports error detection and reporting

### 3. GitHub Actions Workflow
- **Location**: `.github/workflows/api-docs-generation.yml`
- Automatically triggers on:
  - Push to main/develop branches
  - Pull requests
  - Manual trigger
  - Weekly schedule (Sunday midnight)

## Usage

### Manual Generation
```bash
# Generate documentation
python scripts/generate-api-docs.py --generate

# Validate template only
python scripts/generate-api-docs.py --validate

# Check system health
python scripts/generate-api-docs.py --health
```

### Required Sections

The template must include these sections:
1. `## Overview` - General API description
2. `## Authentication` - Authentication methods
3. `## Endpoints` - API endpoints documentation
4. `## Request/Response Examples` - Example requests/responses
5. `## Error Codes` - Error handling information

### Validation

The generation script validates:
- Required sections are present
- JSON examples are valid
- HTTP examples follow correct format
- No sensitive information in examples
- Proper code block formatting

## Automation

The documentation is automatically:
1. **Generated** when templates change
2. **Validated** for format and content
3. **Secured** against sensitive information
4. **Committed** to the repository (main branch only)

## Contributing

To update the API documentation:
1. Edit `docs/templates/api-docs-template.md`
2. Follow the required section structure
3. Use proper code blocks for examples
4. Avoid hardcoded credentials
5. Test with `python scripts/generate-api-docs.py --validate`

## Security

The generation process includes security checks for:
- API keys and secrets
- Hardcoded credentials
- Sensitive patterns in examples
- Proper use of placeholders (`YOUR_`, `example`, `placeholder`)

## Dependencies

- Python 3.9+
- PyYAML library
- GitHub Actions environment