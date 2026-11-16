from configparser import ConfigParser

def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename, encoding="utf-8")
    if not parser.has_section(section):
        raise Exception("Missing [postgresql] section in database.ini")
    return dict(parser.items(section))
