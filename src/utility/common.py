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