import configparser

def to_bool(x : str):
    if x.lower() in ["true", "igen", "yes", "igaz"]:
        return True
    elif x.lower() in ["false", "nem", "no", "hamis"]:
        return False
def to_int(x : str):
    try:
        return int(x)
    except:
        return 0