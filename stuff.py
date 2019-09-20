import transliterate


def translit_name(name):
    return transliterate.translit(name, reversed=True).replace("'", "")
