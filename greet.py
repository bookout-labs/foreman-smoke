def greet(name: str, punctuation: str = ".") -> str:
    if not name.strip():
        raise ValueError("name must not be empty")
    if len(name) > 20:
        raise ValueError("name must be at most 20 characters")
    name = name.strip()
    if any("0" <= char <= "9" for char in name):
        raise ValueError("name must not contain digits")
    if "@" in name:
        raise ValueError("name must not contain @")
    if "," in name:
        raise ValueError("name must not contain a comma")
    if "\t" in name or "\n" in name:
        raise ValueError("name must not contain a tab or newline")
    if ";" in name:
        raise ValueError("name must not contain a semicolon")
    if "/" in name:
        raise ValueError("name must not contain a slash")
    if "#" in name:
        raise ValueError("name must not contain a hash")
    if "^" in name:
        raise ValueError("name must not contain a caret")
    if "~" in name:
        raise ValueError("name must not contain a tilde")
    if "|" in name:
        raise ValueError("name must not contain a pipe")
    if punctuation not in (".", "!", "?"):
        raise ValueError("punctuation must be one of . ! ?")
    return f"Hello, {name}{punctuation}"


def greet_all(names: list, punctuation: str = ".") -> str:
    if not names:
        raise ValueError("names must not be empty")
    greetings = []
    for position, name in enumerate(names, start=1):
        try:
            # Validate the name alone first so only name errors get a position.
            greet(name)
        except ValueError as error:
            raise ValueError(f"name {position}: {error}") from None
        # The name is valid, so the only error left is the unprefixed punctuation one.
        greetings.append(greet(name, punctuation))
    return " | ".join(greetings)
