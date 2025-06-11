def is_hash_key(key: str) -> bool:
    """Check if a key is a Pipedrive hash key (40 character hex string)"""
    return len(key) == 40 and all(c in '0123456789abcdef' for c in key.lower())


def make_custom_field_database_key(field_name):
    if not isinstance(field_name, str):
        return ""

    # Convert to lowercase
    key = field_name.lower()

    # Replace spaces with underscores
    key = key.replace(" ", "_")

    # Remove special characters (keeping only letters, numbers, and underscores)
    # This regex matches any character that is NOT a letter, number, or underscore.
    import re
    key = re.sub(r'[^a-z0-9_]', '', key)

    return key