#!/usr/bin/env python3
"""
Generate environment variable documentation from constants.py
Extracts descriptions from inline comments
"""

import ast
import re
from pathlib import Path
from typing import List, Tuple, Optional

def extract_env_vars_with_comments(file_path: str) -> List[Tuple[str, any, Optional[str]]]:
    """Extract with comments from line above"""
    content = Path(file_path).read_text()
    lines = content.split('\n')
    tree = ast.parse(content)
    
    env_vars = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if (isinstance(node.func, ast.Name) and 
                node.func.id == 'get_env_stripped'):
                
                if node.args:
                    var_name = ast.literal_eval(node.args[0])
                    
                    default = None
                    if len(node.args) > 1:
                        try:
                            default = ast.literal_eval(node.args[1])
                        except (ValueError, SyntaxError):
                            default = ast.unparse(node.args[1])
                    
                    # Try inline comment first
                    description = None
                    if hasattr(node, 'lineno'):
                        # Check current line for inline comment
                        line = lines[node.lineno - 1]
                        comment_match = re.search(r'#\s*(.+)$', line)
                        if comment_match:
                            description = comment_match.group(1).strip()
                        else:
                            # Check previous line for comment
                            if node.lineno > 1:
                                prev_line = lines[node.lineno - 2].strip()
                                if prev_line.startswith('#'):
                                    description = prev_line.lstrip('#').strip()
                    
                    env_vars.append((var_name, default, description))
    
    return env_vars

def generate_env_file(env_vars: List[Tuple], output_path: str = '.env.example'):
    """Generate .env.example file with descriptions"""
    with open(output_path, 'w') as f:
        f.write("# Environment Variables\n")
        f.write("# Copy this to .env and customize\n\n")
        
        for var_name, default, description in sorted(env_vars, key=lambda x: x[0]):
            # Write description if available
            if description:
                f.write(f"# {description}\n")
            
            # Write default value info
            if default is not None:
                f.write(f"# Default: {default}\n")
            else:
                f.write(f"# Required (no default)\n")
            
            # Write the variable
            default_str = str(default) if default is not None else ""
            f.write(f"{var_name}={default_str}\n\n")

def generate_markdown(env_vars: List[Tuple], output_path: str = 'ENV_VARS.md'):
    """Generate markdown documentation"""
    with open(output_path, 'w') as f:
        f.write("# Environment Variables\n\n")
        f.write("| Variable | Default | Description |\n")
        f.write("|----------|---------|-------------|\n")
        
        for var_name, default, description in sorted(env_vars, key=lambda x: x[0]):
            default_str = str(default) if default is not None else "*Required*"
            desc_str = description if description else ""
            f.write(f"| `{var_name}` | `{default_str}` | {desc_str} |\n")

def generate_table(env_vars: List[Tuple]):
    """Print as table to console"""
    print("\nEnvironment Variables:\n")
    print(f"{'Variable':<35} {'Default':<20} Description")
    print("-" * 100)
    
    for var_name, default, description in sorted(env_vars, key=lambda x: x[0]):
        default_str = str(default) if default is not None else "Required"
        desc_str = description[:40] if description else ""
        print(f"{var_name:<35} {default_str:<20} {desc_str}")

def main():
    constants_file = 'src/utility/constants.py'
    
    if not Path(constants_file).exists():
        print(f"Error: {constants_file} not found")
        return
    
    # Extract environment variables
    env_vars = extract_env_vars_with_comments(constants_file)
    
    # Generate .env.example
    generate_env_file(env_vars, '.env.example')
    
    # Generate markdown documentation
    generate_markdown(env_vars, 'ENV_VARS.md')
    
    # Print to console
    generate_table(env_vars)
    
    print(f"\nGenerated .env.example with {len(env_vars)} variables")
    print(f"Generated ENV_VARS.md")

if __name__ == '__main__':
    main()