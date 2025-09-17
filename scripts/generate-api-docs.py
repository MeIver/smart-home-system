#!/usr/bin/env python3
"""
API Documentation Generator for Smart Home System

This script generates API documentation from templates and validates the format.
It supports automatic documentation generation with error detection and reporting.
"""

import os
import re
import json
import yaml
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIDocsGenerator:
    """API Documentation Generator class"""
    
    def __init__(self, template_dir: str = "docs/templates", output_dir: str = "docs/api"):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.template_file = self.template_dir / "api-docs-template.md"
        self.output_file = self.output_dir / "endpoints.md"
        
        # Ensure directories exist
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_template(self) -> Dict[str, Any]:
        """Validate the API documentation template"""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "sections_found": []
        }
        
        if not self.template_file.exists():
            validation_results["valid"] = False
            validation_results["errors"].append(f"Template file not found: {self.template_file}")
            return validation_results
        
        try:
            content = self.template_file.read_text(encoding='utf-8')
            
            # Check for required sections
            required_sections = [
                "Overview",
                "Authentication", 
                "Endpoints",
                "Request/Response Examples",
                "Error Codes"
            ]
            
            for section in required_sections:
                if f"## {section}" in content:
                    validation_results["sections_found"].append(section)
                else:
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Missing required section: {section}")
            
            # Validate HTTP examples
            http_examples = re.findall(r'```http\n(.*?)\n```', content, re.DOTALL)
            if not http_examples:
                validation_results["warnings"].append("No HTTP examples found in template")
            
            # Validate JSON examples
            json_examples = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
            for json_example in json_examples:
                try:
                    json.loads(json_example)
                except json.JSONDecodeError as e:
                    validation_results["warnings"].append(f"Invalid JSON in example: {str(e)}")
            
            # Check for code blocks
            code_blocks = re.findall(r'```(?:http|json|bash|python)\n(.*?)\n```', content, re.DOTALL)
            if len(code_blocks) < 5:
                validation_results["warnings"].append("Few code examples found - consider adding more")
            
            # Check table formatting
            tables = re.findall(r'\|.*?\|.*?\|', content)
            if not tables:
                validation_results["warnings"].append("No tables found - consider adding tables for error codes or parameters")
            
        except Exception as e:
            validation_results["valid"] = False
            validation_results["errors"].append(f"Error reading template: {str(e)}")
        
        return validation_results
    
    def generate_documentation(self, validate: bool = True) -> Dict[str, Any]:
        """Generate API documentation from template"""
        result = {
            "success": False,
            "message": "",
            "validation": {},
            "output_file": str(self.output_file)
        }
        
        if validate:
            validation = self.validate_template()
            result["validation"] = validation
            
            if not validation["valid"]:
                result["message"] = "Template validation failed"
                return result
        
        try:
            if not self.template_file.exists():
                result["message"] = f"Template file not found: {self.template_file}"
                return result
            
            # Read template content
            content = self.template_file.read_text(encoding='utf-8')
            
            # Add generation metadata
            generation_info = f"\n\n---\n\n*Generated on {datetime.now().isoformat()} by API Documentation Generator*"
            content += generation_info
            
            # Write to output file
            self.output_file.write_text(content, encoding='utf-8')
            
            result["success"] = True
            result["message"] = f"API documentation generated successfully: {self.output_file}"
            
            # Generate validation report
            self._generate_validation_report(validation)
            
        except Exception as e:
            result["message"] = f"Error generating documentation: {str(e)}"
            logger.error(f"Generation error: {e}")
        
        return result
    
    def _generate_validation_report(self, validation: Dict[str, Any]) -> None:
        """Generate a validation report file"""
        report_file = self.output_dir / "validation-report.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "template_file": str(self.template_file),
            "output_file": str(self.output_file),
            "valid": validation["valid"],
            "errors": validation["errors"],
            "warnings": validation["warnings"],
            "sections_found": validation["sections_found"]
        }
        
        try:
            report_file.write_text(json.dumps(report_data, indent=2), encoding='utf-8')
            logger.info(f"Validation report generated: {report_file}")
        except Exception as e:
            logger.error(f"Error generating validation report: {e}")
    
    def check_health(self) -> Dict[str, Any]:
        """Check the health of the documentation system"""
        health = {
            "healthy": True,
            "issues": [],
            "template_exists": self.template_file.exists(),
            "output_dir_exists": self.output_dir.exists(),
            "template_dir_exists": self.template_dir.exists()
        }
        
        if not health["template_dir_exists"]:
            health["healthy"] = False
            health["issues"].append("Template directory does not exist")
        
        if not health["output_dir_exists"]:
            health["healthy"] = False
            health["issues"].append("Output directory does not exist")
        
        if not health["template_exists"]:
            health["healthy"] = False
            health["issues"].append("Template file does not exist")
        
        return health

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate API documentation from templates")
    parser.add_argument("--validate", action="store_true", help="Validate template only")
    parser.add_argument("--generate", action="store_true", help="Generate documentation")
    parser.add_argument("--health", action="store_true", help="Check system health")
    parser.add_argument("--template-dir", default="docs/templates", help="Template directory")
    parser.add_argument("--output-dir", default="docs/api", help="Output directory")
    
    args = parser.parse_args()
    
    generator = APIDocsGenerator(args.template_dir, args.output_dir)
    
    if args.health:
        health = generator.check_health()
        print(json.dumps(health, indent=2))
        return 0 if health["healthy"] else 1
    
    if args.validate:
        validation = generator.validate_template()
        print(json.dumps(validation, indent=2))
        return 0 if validation["valid"] else 1
    
    if args.generate:
        result = generator.generate_documentation()
        print(json.dumps(result, indent=2))
        return 0 if result["success"] else 1
    
    # Default action: generate with validation
    result = generator.generate_documentation()
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1

if __name__ == "__main__":
    exit(main())