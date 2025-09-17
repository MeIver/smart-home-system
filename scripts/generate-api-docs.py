#!/usr/bin/env python3
"""
Smart Home System API Documentation Generator

This script generates API documentation from templates and validates the output.
"""

import os
import sys
import json
import yaml
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_template(template_path: str) -> str:
    """Load the API documentation template."""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading template: {e}")
        sys.exit(1)


def validate_template_content(template_content: str) -> bool:
    """Validate that the template contains all required sections."""
    required_sections = [
        "## Overview",
        "## Authentication", 
        "## Endpoints",
        "## Request/Response Examples",
        "## Error Codes"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in template_content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"Error: Template missing required sections: {missing_sections}")
        return False
    
    return True


def generate_api_docs(template_content: str, output_path: str, metadata: Optional[Dict] = None) -> bool:
    """Generate API documentation from template."""
    try:
        # Add metadata if provided
        content = template_content
        if metadata:
            metadata_section = f"\n<!-- Generated: {datetime.datetime.now().isoformat()} -->\n"
            metadata_section += f"<!-- Version: {metadata.get('version', '1.0.0')} -->\n"
            content = content.replace("# Smart Home System API Documentation", 
                                    f"# Smart Home System API Documentation{metadata_section}")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"API documentation generated successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error generating documentation: {e}")
        return False


def validate_generated_docs(docs_path: str) -> Dict[str, Any]:
    """Validate the generated API documentation."""
    validation_results = {
        'has_overview': False,
        'has_authentication': False,
        'has_endpoints': False,
        'has_examples': False,
        'has_error_codes': False,
        'has_http_examples': False,
        'has_json_examples': False,
        'line_count': 0,
        'word_count': 0,
        'validation_passed': False
    }
    
    try:
        with open(docs_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Basic validation
        validation_results['has_overview'] = '## Overview' in content
        validation_results['has_authentication'] = '## Authentication' in content
        validation_results['has_endpoints'] = '## Endpoints' in content
        validation_results['has_examples'] = '## Request/Response Examples' in content
        validation_results['has_error_codes'] = '## Error Codes' in content
        validation_results['has_http_examples'] = '```http' in content
        validation_results['has_json_examples'] = '```json' in content
        
        # Count metrics
        validation_results['line_count'] = len(content.split('\n'))
        validation_results['word_count'] = len(content.split())
        
        # Check if all required sections are present
        required_checks = [
            validation_results['has_overview'],
            validation_results['has_authentication'],
            validation_results['has_endpoints'], 
            validation_results['has_examples'],
            validation_results['has_error_codes'],
            validation_results['has_http_examples'],
            validation_results['has_json_examples']
        ]
        
        validation_results['validation_passed'] = all(required_checks)
        
        return validation_results
        
    except Exception as e:
        print(f"Error validating documentation: {e}")
        validation_results['error'] = str(e)
        return validation_results


def generate_validation_report(validation_results: Dict[str, Any], report_path: str) -> bool:
    """Generate a validation report in JSON format."""
    try:
        report_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'validation_results': validation_results,
            'summary': {
                'passed': validation_results['validation_passed'],
                'total_checks': 7,
                'passed_checks': sum([
                    1 for check in [
                        validation_results['has_overview'],
                        validation_results['has_authentication'],
                        validation_results['has_endpoints'],
                        validation_results['has_examples'],
                        validation_results['has_error_codes'],
                        validation_results['has_http_examples'],
                        validation_results['has_json_examples']
                    ] if check
                ])
            }
        }
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"Validation report generated: {report_path}")
        return True
        
    except Exception as e:
        print(f"Error generating validation report: {e}")
        return False


def main():
    """Main function to generate and validate API documentation."""
    parser = argparse.ArgumentParser(description='Generate API documentation from template')
    parser.add_argument('--template', '-t', default='docs/templates/api-docs-template.md', 
                       help='Path to template file')
    parser.add_argument('--output', '-o', default='docs/api/endpoints.md', 
                       help='Output path for generated documentation')
    parser.add_argument('--report', '-r', default='reports/api-docs-validation.json', 
                       help='Path for validation report')
    parser.add_argument('--validate-only', action='store_true', 
                       help='Only validate existing documentation without generating')
    
    args = parser.parse_args()
    
    if not args.validate_only:
        # Generate documentation
        print("Loading template...")
        template_content = load_template(args.template)
        
        print("Validating template content...")
        if not validate_template_content(template_content):
            sys.exit(1)
        
        print("Generating API documentation...")
        metadata = {
            'version': '1.0.0',
            'generated_at': datetime.datetime.now().isoformat(),
            'template_version': '1.0'
        }
        
        if not generate_api_docs(template_content, args.output, metadata):
            sys.exit(1)
    
    # Validate generated documentation
    print("Validating generated documentation...")
    validation_results = validate_generated_docs(args.output)
    
    # Generate validation report
    print("Generating validation report...")
    if not generate_validation_report(validation_results, args.report):
        sys.exit(1)
    
    # Print summary
    print(f"\n=== VALIDATION SUMMARY ===")
    print(f"Overview Section: {'✓' if validation_results['has_overview'] else '✗'}")
    print(f"Authentication Section: {'✓' if validation_results['has_authentication'] else '✗'}")
    print(f"Endpoints Section: {'✓' if validation_results['has_endpoints'] else '✗'}")
    print(f"Examples Section: {'✓' if validation_results['has_examples'] else '✗'}")
    print(f"Error Codes Section: {'✓' if validation_results['has_error_codes'] else '✗'}")
    print(f"HTTP Examples: {'✓' if validation_results['has_http_examples'] else '✗'}")
    print(f"JSON Examples: {'✓' if validation_results['has_json_examples'] else '✗'}")
    print(f"Line Count: {validation_results['line_count']}")
    print(f"Word Count: {validation_results['word_count']}")
    print(f"Overall Validation: {'PASSED' if validation_results['validation_passed'] else 'FAILED'}")
    
    if not validation_results['validation_passed']:
        print("\n❌ Documentation validation failed!")
        sys.exit(1)
    else:
        print("\n✅ Documentation validation passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()