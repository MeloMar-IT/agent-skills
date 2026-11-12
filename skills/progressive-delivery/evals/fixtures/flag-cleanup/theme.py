from flagclient import is_on


def theme():
    return "dark" if is_on("dark-mode") else "light"
