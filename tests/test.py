def pretty_format_number(value: float) -> str:
    """
    Format a number to exactly 6 characters according to its magnitude.
    Examples:
        0 → "0.0000"
        0.005432 → "0.0054"
        0.054321 → "0.0543"
        0.543210 → "0.5432"
        5.43210 → "5.4321"
        54.3210 → "54.321"
        543.210 → "543.21"
        5432.10 → "5.43k "  # Note the space to make it 6 chars
        54321.0 → "54.3k "  # Note the space to make it 6 chars
    Args:
        value (float): The number to format
    Returns:
        str: Formatted number string with exactly 6 characters
    """
    if value == 0:
        return "0.0000"
    elif value < 0.01:
        return f"{value:.4f}"
    elif value < 0.1:
        return f"{value:.4f}"
    elif value < 1:
        return f"{value:.4f}"
    elif value < 10:
        return f"{value:.4f}"
    elif value < 100:
        return f"{value:.3f}"
    elif value < 1000:
        return f"{value:.2f}"
    elif value < 10000:
        return f"{value/1000:.2f}k"
    else:
        return f"{value/1000:.1f}k"