def greet(name: str, punctuation: str = ".") -> str:
    if not name.strip():
        raise ValueError("name must not be empty")
    if len(name) > 20:
        raise ValueError("name must be at most 20 characters")
    if any("0" <= char <= "9" for char in name):
        raise ValueError("name must not contain digits")
    if "@" in name:
        raise ValueError("name must not contain @")
    if "," in name:
        raise ValueError("name must not contain a comma")
    if "\t" in name or "\n" in name:
        raise ValueError("name must not contain a tab or newline")
    if punctuation not in (".", "!", "?"):
        raise ValueError("punctuation must be one of . ! ?")
    return f"Hello, {name}{punctuation}"
