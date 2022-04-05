# M5 : masKey
# Beállítások értékeinek feldolgozásáért felelős python kód
# https://github.com/tcgmilan/mbot-mask-detection


def to_bool(x : str):
    """
    'str' típusú érték átalalkítása 'bool' típusúvá.
    Ha az átalakítás sikertelen, 'False' értéket kapunk vissza.\n
    true, igen, yes, igaz = True\n
    false, nem, no, hamis = False
    """
    if x.lower() in ["true", "igen", "yes", "igaz"]:
        return True
    elif x.lower() in ["false", "nem", "no", "hamis"]:
        return False
    else:
        return False

def to_int(x : str):
    """
    'str' típusú érték átalakítása 'int' típusúvá.
    Ha az átalakítás sikertelen, 0 értéket kapunk vissza.
    """
    try:
        return int(x)
    except:
        return 0