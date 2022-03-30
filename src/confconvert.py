import configparser

def to_bool(x : str):
    if x.lower() in ["true", "igen", "yes", "igaz"]:
        return True
    return False
def to_int(x : str):
    try:
        return int(x)
    except:
        return 0