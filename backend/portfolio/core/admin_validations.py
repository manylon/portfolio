def validate_tags(tags):
    """Validate the number of tags."""
    if isinstance(tags, str):  # If it's a string (unlikely, but good to check)
        tags = [tags]

    if len(tags) > 3:
        raise ValueError("You can only add up to 3 tags.")

    return tags
