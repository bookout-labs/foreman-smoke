def greet(name: str, punctuation: str = ".") -> str:
    if not name.strip():
        raise ValueError("name must not be empty")
    if punctuation not in (".", "!", "?"):
        raise ValueError("punctuation must be one of . ! ?")
    return f"Hello, {name}{punctuation}"
