#!/usr/bin/env python3
"""
Generate environment variable documentation from constants.py
Updates README.md with the table between markers
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

def generate_markdown_table(env_vars: List[Tuple]) -> str:
    """Generate markdown table as string"""
    lines = []
    lines.append("| Variable | Default | Description |")
    lines.append("|----------|---------|-------------|")
    
    for var_name, default, description in sorted(env_vars, key=lambda x: x[0]):
        default_str = str(default) if default is not None else "*Required*"
        desc_str = description if description else ""
        lines.append(f"| `{var_name}` | `{default_str}` | {desc_str} |")
    
    return '\n'.join(lines)

def update_readme_section(readme_path: str, table_content: str, 
                         start_marker: str = "<!-- ENV_VARS_START -->",
                         end_marker: str = "<!-- ENV_VARS_END -->") -> bool:
    """
    Update a section of README.md between markers
    
    Args:
        readme_path: Path to README.md
        table_content: The table content to insert
        start_marker: Start marker comment
        end_marker: End marker comment
    
    Returns:
        True if updated, False if markers not found
    """
    readme_file = Path(readme_path)
    
    if not readme_file.exists():
        print(f"Warning: {readme_path} not found, creating new file")
        content = f"{start_marker}\n{table_content}\n{end_marker}\n"
        readme_file.write_text(content)
        return True
    
    content = readme_file.read_text()
    
    # Check if markers exist
    if start_marker not in content or end_marker not in content:
        print(f"Warning: Markers not found in {readme_path}")
        print(f"Add the following markers to your README where you want the table:")
        print(f"\n{start_marker}")
        print(f"{end_marker}\n")
        return False
    
    # Replace content between markers
    pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
    replacement = f"{start_marker}\n{table_content}\n{end_marker}"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write back
    readme_file.write_text(new_content)
    return True

def generate_env_file(env_vars: List[Tuple], output_path: str = '.env.example'):
    """Generate .env.example file with descriptions"""
    with open(output_path, 'w') as f:
        f.write("# Environment Variables\n")
        f.write("# Copy this to .env and customize\n\n")
        
        for var_name, default, description in sorted(env_vars, key=lambda x: x[0]):
            if description:
                f.write(f"# {description}\n")
            
            if default is not None:
                f.write(f"# Default: {default}\n")
            else:
                f.write(f"# Required (no default)\n")
            
            default_str = str(default) if default is not None else ""
            f.write(f"{var_name}={default_str}\n\n")

def main():
    constants_file = 'src/utility/constants.py'
    readme_file = 'README.md'
    
    if not Path(constants_file).exists():
        print(f"Error: {constants_file} not found")
        return 1
    
    print("=" * 60)
    print("Environment Variable Documentation Generator")
    print("=" * 60 + "\n")
    
    # Extract environment variables
    print(f"Reading {constants_file}...")
    env_vars = extract_env_vars_with_comments(constants_file)
    print(f"Found {len(env_vars)} environment variables\n")
    
    # Generate markdown table
    print("Generating markdown table...")
    table_content = generate_markdown_table(env_vars)
    
    # Update README.md
    print(f"Updating {readme_file}...")
    if update_readme_section(readme_file, table_content):
        print(f"Updated {readme_file}")
    else:
        print(f"Failed to update {readme_file}")
        return 1
    
    # Generate .env.example
    print(f"\nGenerating .env.example...")
    generate_env_file(env_vars, '.env.example')
    print(f"Generated .env.example")
    
    print("\n" + "=" * 60)
    print("Documentation generation complete")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())