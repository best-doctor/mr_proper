

def is_python_class_name(name: str) -> bool:
    return name[0] == name[0].upper() and name[1:] == name[1:].lower()
