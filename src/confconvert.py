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



config = configparser.ConfigParser()
config.read("./BEALLITASOK.cfg", encoding = "utf-8")

test = config["BEALLITASOK"]["video_kimenet"]
test2 = config["BEALLITASOK"]["figyelmeztetes_varakozas"]
print(to_bool(test))
print(to_int(test2))