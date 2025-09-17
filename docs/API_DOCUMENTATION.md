# Smart Home System API Documentation System

This document describes the automated API documentation generation system for the Smart Home System.

## Overview

The API documentation system provides:
- 📝 **Template-based documentation generation**
- 🔍 **Automatic validation and quality checks**
- ⚡ **GitHub Actions automation**
- 📊 **Validation reports and metrics**
- 🔒 **Security scanning for sensitive information**

## File Structure

```
smart-home-system/
├── docs/
│   ├── templates/
│   │   └── api-docs-template.md      # Main documentation template
│   ├── api/
│   │   └── endpoints.md              # Generated documentation (auto)
│   └── API_DOCUMENTATION.md          # This file
├── scripts/
│   ├── generate-api-docs.py          # Documentation generator
│   └── requirements.txt              # Python dependencies
├── .github/
│   └── workflows/
│       └── api-docs-generation.yml   # GitHub Actions workflow
└── reports/
    └── api-docs-validation.json      # Validation reports (auto)
```

## Usage

### Manual Generation

To generate API documentation manually:

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Generate documentation
python scripts/generate-api-docs.py

# Validate only
python scripts/generate-api-docs.py --validate-only
```

### Automated Generation

The documentation is automatically generated:
1. **On push** to main/develop branches when template files change
2. **On pull request** when API-related files are modified
3. **Weekly** (every Sunday at midnight)
4. **Manually** via GitHub Actions UI

## Template Structure

The API documentation template (`docs/templates/api-docs-template.md`) must include:

### Required Sections
1. **## Overview** - System introduction and base URL
2. **## Authentication** - Authentication methods and examples
3. **## Endpoints** - All API endpoints with descriptions
4. **## Request/Response Examples** - HTTP and JSON examples
5. **## Error Codes** - Error handling and status codes

### Validation Requirements
- Must contain all required section headers
- Must include HTTP code examples (````http`)
- Must include JSON examples (````json`)
- Must not contain sensitive information

## GitHub Actions Workflow

The automation workflow includes:

1. **Documentation Generation** - Creates docs from template
2. **Validation** - Checks for required sections and content
3. **Quality Checks** - Ensures documentation completeness
4. **Security Scan** - Detects potential sensitive information
5. **Reporting** - Generates validation reports and metrics

## Validation Metrics

The system tracks:
- ✅ Required section presence
- 📊 Line and word counts
- 🔍 Code example validation
- 🛡️ Security compliance
- ⚡ Generation performance

## Customization

### Adding New Sections

1. Update the template file with new content
2. Add validation rules in `scripts/generate-api-docs.py`
3. Update the GitHub Actions workflow if needed

### Modifying Validation

Edit the `validate_template_content()` and `validate_generated_docs()` functions in the generation script.

### Changing Automation Triggers

Modify the `on:` section in `.github/workflows/api-docs-generation.yml`.

## Troubleshooting

### Common Issues

1. **Validation fails** - Check missing sections in template
2. **Generation errors** - Verify Python dependencies
3. **Security alerts** - Remove sensitive data from examples

### Debug Mode

Add `--debug` flag to the generation script for detailed output:

```bash
python scripts/generate-api-docs.py --debug
```

## Contributing

When contributing to API documentation:

1. Update the template file (`docs/templates/api-docs-template.md`)
2. Test locally with the generation script
3. Ensure all validation checks pass
4. Create a pull request

## Support

For issues with the documentation system:
- Check GitHub Actions logs
- Review validation reports
- Consult this documentation

---

*This documentation system was automatically generated and is maintained by the automated API documentation generation workflow.*