#!/usr/bin/env python3
"""
Knowledge Base Setup Script

This script helps you create a new knowledge base structure for your own domain.
It creates the necessary folders and provides examples of how to organize your documents.

Usage:
    python setup_knowledge_base.py --name "my-domain"
"""

import os
import argparse
import shutil

def create_knowledge_base_structure(base_name):
    """Create a new knowledge base structure"""

    # Create main knowledge base directory
    kb_path = f"knowledge-base-{base_name}"
    if os.path.exists(kb_path):
        print(f"Warning: {kb_path} already exists. Removing it...")
        shutil.rmtree(kb_path)

    os.makedirs(kb_path)

    # Create example subdirectories
    subdirs = [
        "company",
        "products",
        "employees",
        "contracts",
        "policies",
        "procedures"
    ]

    for subdir in subdirs:
        os.makedirs(os.path.join(kb_path, subdir))

    # Create example markdown files
    examples = {
        "company": {
            "about.md": """# About Our Company

## Company Overview
[Describe your company here]

## Mission
[Your company mission]

## Values
[Your company values]

## History
[Company history and milestones]
""",
            "overview.md": """# Company Overview

## What We Do
[Brief description of what your company does]

## Industry
[Your industry and market position]

## Key Facts
- Founded: [Year]
- Headquarters: [Location]
- Employees: [Number]
- Revenue: [Range if public]
"""
        },
        "products": {
            "product1.md": """# Product 1

## Description
[Product description]

## Features
- Feature 1
- Feature 2
- Feature 3

## Target Market
[Who this product is for]

## Pricing
[Pricing information]
""",
            "product2.md": """# Product 2

## Description
[Product description]

## Features
- Feature 1
- Feature 2
- Feature 3

## Target Market
[Who this product is for]

## Pricing
[Pricing information]
"""
        },
        "employees": {
            "employee1.md": """# Employee Name

## Position
[Job title]

## Department
[Department name]

## Contact Information
- Email: [email]
- Phone: [phone]
- Office: [location]

## Responsibilities
[Key responsibilities and areas of expertise]

## Background
[Education, experience, skills]
""",
            "employee2.md": """# Employee Name

## Position
[Job title]

## Department
[Department name]

## Contact Information
- Email: [email]
- Phone: [phone]
- Office: [location]

## Responsibilities
[Key responsibilities and areas of expertise]

## Background
[Education, experience, skills]
"""
        },
        "contracts": {
            "contract1.md": """# Contract with [Client/Vendor Name]

## Contract Details
- Contract ID: [ID]
- Start Date: [Date]
- End Date: [Date]
- Value: [Amount]

## Scope of Work
[Description of what the contract covers]

## Key Terms
[Important terms and conditions]

## Contact Person
[Primary contact for this contract]
""",
            "contract2.md": """# Contract with [Client/Vendor Name]

## Contract Details
- Contract ID: [ID]
- Start Date: [Date]
- End Date: [Date]
- Value: [Amount]

## Scope of Work
[Description of what the contract covers]

## Key Terms
[Important terms and conditions]

## Contact Person
[Primary contact for this contract]
"""
        },
        "policies": {
            "policy1.md": """# Policy Name

## Purpose
[Why this policy exists]

## Scope
[Who this policy applies to]

## Policy Details
[Specific policy requirements]

## Compliance
[How to ensure compliance]

## Contact
[Who to contact with questions]
""",
            "policy2.md": """# Policy Name

## Purpose
[Why this policy exists]

## Scope
[Who this policy applies to]

## Policy Details
[Specific policy requirements]

## Compliance
[How to ensure compliance]

## Contact
[Who to contact with questions]
"""
        },
        "procedures": {
            "procedure1.md": """# Procedure Name

## Purpose
[What this procedure accomplishes]

## Prerequisites
[What needs to be in place before starting]

## Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Outcome
[What should happen when complete]

## Troubleshooting
[Common issues and solutions]
""",
            "procedure2.md": """# Procedure Name

## Purpose
[What this procedure accomplishes]

## Prerequisites
[What needs to be in place before starting]

## Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Outcome
[What should happen when complete]

## Troubleshooting
[Common issues and solutions]
"""
        }
    }

    # Create example files
    for subdir, files in examples.items():
        for filename, content in files.items():
            filepath = os.path.join(kb_path, subdir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    # Create README for the knowledge base
    readme_content = f"""# Knowledge Base: {base_name.title()}

This knowledge base contains information about {base_name} and can be used with the Knowledge Worker RAG application.

## Structure

The knowledge base is organized into the following categories:

- **company/**: Company information, about us, overview
- **products/**: Product descriptions, features, pricing
- **employees/**: Employee information, contact details, responsibilities
- **contracts/**: Contract details, terms, client information
- **policies/**: Company policies and procedures
- **procedures/**: Step-by-step procedures and workflows

## Usage

1. Replace the example content with your actual information
2. Add more documents as needed
3. Organize documents into appropriate subdirectories
4. Use the Knowledge Worker application to query this knowledge base

## File Format

All documents should be in Markdown (.md) format for best compatibility with the Knowledge Worker application.

## Customization

Feel free to:
- Rename subdirectories to match your organization
- Add new subdirectories for additional categories
- Modify the document structure to fit your needs
- Add more example documents

## Getting Started

1. Edit the example files with your actual content
2. Add your own documents to the appropriate folders
3. Run the Knowledge Worker application pointing to this knowledge base:
   ```bash
   python knowledge_worker.py --knowledge-base knowledge-base-{base_name}
   ```
"""

    with open(os.path.join(kb_path, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"\n✅ Knowledge base '{kb_path}' created successfully!")
    print(f"\n📁 Structure created:")
    for subdir in subdirs:
        print(f"   - {kb_path}/{subdir}/")

    print(f"\n📝 Example files created in each directory")
    print(f"\n📖 README.md created with usage instructions")

    print(f"\n🚀 Next steps:")
    print(f"1. Edit the example files in {kb_path}/ with your actual content")
    print(f"2. Add more documents as needed")
    print(f"3. Run: python knowledge_worker.py --knowledge-base {kb_path}")

    return kb_path

def main():
    parser = argparse.ArgumentParser(description="Create a new knowledge base structure")
    parser.add_argument("--name", required=True, help="Name for your knowledge base")

    args = parser.parse_args()

    try:
        kb_path = create_knowledge_base_structure(args.name)
        print(f"\n🎉 Your knowledge base is ready at: {kb_path}")

    except Exception as e:
        print(f"Error creating knowledge base: {str(e)}")

if __name__ == "__main__":
    main()
