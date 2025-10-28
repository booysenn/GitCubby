from os import environ

def get_env_stripped(key, default=None, cast=None, required=False):
    """
    Get environment variable, strip whitespace, and optionally cast type
    
    Args:
        key: Environment variable name
        default: Default value if not found
        cast: Optional type to cast to (int, bool, etc.)
        required: If True, raise error if not found or empty
    
    Raises:
        ValueError: If required=True and variable not found/empty
        ValueError: If cast fails
    """
    value = environ.get(key)
    
    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{key}' not set")
        return default
    
    value = value.strip()
    
    if not value:  # Empty after stripping
        if required:
            raise ValueError(f"Environment variable '{key}' is empty")
        return default
    
    if cast:
        try:
            return cast(value)
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Failed to cast '{key}'='{value}' to {cast.__name__}: {e}"
            )
    
    return value


def set_environment_variable():
    with open('/usr/local/bin/environment', 'w') as f:
        f.write("#!/usr/bash")
        for k in environ:
            f.write(f"export {k}={environ.get(k)}\n") 

import re
from pathlib import Path

def set_git_shell_variable(key, value, section=None):
    """
    Set a variable in constants.py with optional section organization
    
    Args:
        key: Variable name
        value: Variable value
        section: Optional section comment (e.g., "# Network Settings")
    """
    constants_file = Path('/usr/local/bin/shell_utility/constants.py')
    constants_file.parent.mkdir(parents=True, exist_ok=True)
    
    if constants_file.exists():
        lines = constants_file.read_text().split('\n')
    else:
        lines = ['# Auto-generated constants', '']
    
    key_pattern = re.compile(rf'^\s*{re.escape(key)}\s*=')
    found = False
    new_lines = []
    
    for line in lines:
        if key_pattern.match(line):
            new_lines.append(f"{key} = {repr(value)}")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        # Add section header if provided and not exists
        if section:
            if section not in '\n'.join(new_lines):
                if new_lines and new_lines[-1].strip():
                    new_lines.append('')
                new_lines.append(section)
        
        new_lines.append(f"{key} = {repr(value)}")
    
    constants_file.write_text('\n'.join(new_lines) + '\n')
