def optional_dict(**entries):
    return {k: v for k, v in entries.items() if v is not None and v != ''}
