import random
from sys import argv


def password_for_sf():
    """
    Генератор паролей для КПД, слово из словаря английских слов по маске AAffaa33
    :return:
    """
    word = words[random.randint(1, 536)]
    digit_char = random.randint(1, 9)
    # special_chars = "@#$&"
    # special_char_index = random.randint(0, 3)
    # password = f"{word[0].upper()}{word[0].upper()}{word[1]}{word[1]}{word[2]}{word[2]}{str(digit_char)}" \
    #            f"{special_chars[special_char_index]}"
    password = f"{word[0].upper()}{word[0].upper()}{word[1]}{word[1]}{word[2]}{word[2]}{str(digit_char)}{str(digit_char)}"
    return password


words = {
    1: 'aas', 2: 'afa', 3: 'aff', 4: 'aga', 5: 'ags', 6: 'aha', 7: 'ahs', 8: 'ake',
    9: 'ama', 10: 'amp', 11: 'ana', 12: 'and', 13: 'ane', 14: 'ant', 15: 'any', 16: 'ape',
    17: 'app', 18: 'apt', 19: 'arb', 20: 'arc', 21: 'ard', 22: 'are', 23: 'arf', 24: 'ark',
    25: 'arm', 26: 'art', 27: 'ash', 28: 'ask', 29: 'asp', 30: 'ate', 31: 'att', 32: 'auk',
    33: 'ava', 34: 'ave', 35: 'awa', 36: 'awn', 37: 'axe', 38: 'ayr', 39: 'ays', 40: 'bag',
    41: 'bak', 42: 'bam', 43: 'ban', 44: 'bap', 45: 'bas', 46: 'bat', 47: 'bay', 48: 'baz',
    49: 'bee', 50: 'beg', 51: 'bes', 52: 'bet', 53: 'bey', 54: 'brr', 55: 'bub', 56: 'bud',
    57: 'bug', 58: 'bum', 59: 'bun', 60: 'bur', 61: 'bus', 62: 'but', 63: 'buy', 64: 'bye',
    65: 'bys', 66: 'cab', 67: 'cad', 68: 'cam', 69: 'can', 70: 'cap', 71: 'car', 72: 'caw',
    73: 'cay', 74: 'cee', 75: 'cep', 76: 'cru', 77: 'cry', 78: 'cub', 79: 'cud', 80: 'cue',
    81: 'cup', 82: 'cur', 83: 'cut', 84: 'cwm', 85: 'dab', 86: 'dad', 87: 'dag', 88: 'dah',
    89: 'dak', 90: 'dan', 91: 'dap', 92: 'dat', 93: 'dau', 94: 'daw', 95: 'day', 96: 'deb',
    97: 'dee', 98: 'def', 99: 'deg', 100: 'den', 101: 'dev', 102: 'dew', 103: 'dex', 104: 'dey',
    105: 'dry', 106: 'dub', 107: 'dud', 108: 'due', 109: 'dug', 110: 'duh', 111: 'dun', 112: 'dup',
    113: 'dux', 114: 'dye', 115: 'ear', 116: 'eat', 117: 'eau', 118: 'ebb', 119: 'ecu', 120: 'edh',
    121: 'eds', 122: 'eek', 123: 'eep', 124: 'eet', 125: 'eff', 126: 'efs', 127: 'eft', 128: 'egg',
    129: 'eke', 130: 'eme', 131: 'ems', 132: 'emu', 133: 'end', 134: 'eng', 135: 'ens', 136: 'ent',
    137: 'era', 138: 'ere', 139: 'erk', 140: 'ern', 141: 'err', 142: 'ers', 143: 'esh', 144: 'esp',
    145: 'ess', 146: 'eta', 147: 'eth', 148: 'ety', 149: 'eve', 150: 'ewe', 151: 'exy', 152: 'eye',
    153: 'fab', 154: 'fad', 155: 'fag', 156: 'fah', 157: 'fan', 158: 'fap', 159: 'fas', 160: 'fat',
    161: 'fax', 162: 'fay', 163: 'fed', 164: 'fee', 165: 'feh', 166: 'fem', 167: 'fen', 168: 'fer',
    169: 'fes', 170: 'fet', 171: 'feu', 172: 'few', 173: 'fey', 174: 'fez', 175: 'fry', 176: 'fub',
    177: 'fud', 178: 'fug', 179: 'fun', 180: 'fur', 181: 'gab', 182: 'gad', 183: 'gae', 184: 'gag',
    185: 'gam', 186: 'gan', 187: 'gap', 188: 'gar', 189: 'gas', 190: 'gat', 191: 'gau', 192: 'gaw',
    193: 'gay', 194: 'ged', 195: 'gee', 196: 'gem', 197: 'gen', 198: 'get', 199: 'gey', 200: 'gnu',
    201: 'gry', 202: 'gum', 203: 'gun', 204: 'gut', 205: 'guv', 206: 'guy', 207: 'gym', 208: 'gyp',
    209: 'had', 210: 'hae', 211: 'hag', 212: 'hah', 213: 'ham', 214: 'han', 215: 'hap', 216: 'har',
    217: 'has', 218: 'hat', 219: 'haw', 220: 'hay', 221: 'hed', 222: 'heh', 223: 'hem', 224: 'hen',
    225: 'hep', 226: 'hes', 227: 'het', 228: 'hew', 229: 'hex', 230: 'hey', 231: 'hmm', 232: 'hub',
    233: 'hue', 234: 'hug', 235: 'huh', 236: 'hum', 237: 'hun', 238: 'hup', 239: 'hyp', 240: 'Jap',
    241: 'kab', 242: 'kae', 243: 'kaf', 244: 'kas', 245: 'kat', 246: 'kaw', 247: 'kay', 248: 'kea',
    249: 'kef', 250: 'keg', 251: 'ken', 252: 'kep', 253: 'ket', 254: 'kex', 255: 'key', 256: 'khu',
    257: 'kue', 258: 'kut', 259: 'kye', 260: 'mac', 261: 'mae', 262: 'mam', 263: 'man', 264: 'mar',
    265: 'mat', 266: 'maw', 267: 'max', 268: 'may', 269: 'med', 270: 'meg', 271: 'meh', 272: 'mem',
    273: 'men', 274: 'met', 275: 'meu', 276: 'mew', 277: 'mud', 278: 'mug', 279: 'mum', 280: 'mus',
    281: 'mut', 282: 'mux', 283: 'myc', 284: 'naa', 285: 'nab', 286: 'nae', 287: 'nag', 288: 'nah',
    289: 'nam', 290: 'nan', 291: 'nap', 292: 'naw', 293: 'nay', 294: 'neb', 295: 'ned', 296: 'nee',
    297: 'neg', 298: 'nen', 299: 'net', 300: 'neu', 301: 'new', 302: 'nth', 303: 'nub', 304: 'num',
    305: 'nun', 306: 'nus', 307: 'nut', 308: 'pac', 309: 'pam', 310: 'pan', 311: 'pap', 312: 'par',
    313: 'pas', 314: 'pat', 315: 'pav', 316: 'paw', 317: 'pax', 318: 'pea', 319: 'pec', 320: 'ped',
    321: 'pee', 322: 'peh', 323: 'pep', 324: 'per', 325: 'pes', 326: 'pew', 327: 'pht', 328: 'pry',
    329: 'pst', 330: 'pub', 331: 'pud', 332: 'pug', 333: 'pun', 334: 'pup', 335: 'pur', 336: 'pus',
    337: 'put', 338: 'pwn', 339: 'pya', 340: 'pye', 341: 'pyx', 342: 'qat', 343: 'qua', 344: 'rad',
    345: 'rag', 346: 'rah', 347: 'ram', 348: 'ran', 349: 'rap', 350: 'ras', 351: 'rat', 352: 'raw',
    353: 'rax', 354: 'ray', 355: 'reb', 356: 'rec', 357: 'ree', 358: 'ref', 359: 'reg', 360: 'rem',
    361: 'ren', 362: 'rep', 363: 'res', 364: 'ret', 365: 'rev', 366: 'rex', 367: 'rez', 368: 'rub',
    369: 'rue', 370: 'rug', 371: 'rum', 372: 'run', 373: 'rut', 374: 'rya', 375: 'sab', 376: 'sac',
    377: 'sae', 378: 'sag', 379: 'sam', 380: 'sap', 381: 'sat', 382: 'sau', 383: 'sav', 384: 'saw',
    385: 'sax', 386: 'say', 387: 'sea', 388: 'sec', 389: 'sed', 390: 'see', 391: 'seg', 392: 'ser',
    393: 'set', 394: 'sew', 395: 'sex', 396: 'sha', 397: 'she', 398: 'shh', 399: 'shy', 400: 'ska',
    401: 'sky', 402: 'spa', 403: 'spy', 404: 'ssh', 405: 'sss', 406: 'sty', 407: 'sub', 408: 'sue',
    409: 'suk', 410: 'sum', 411: 'sun', 412: 'sup', 413: 'suq', 414: 'syn', 415: 'taa', 416: 'tab',
    417: 'tad', 418: 'tae', 419: 'tag', 420: 'tam', 421: 'tan', 422: 'tap', 423: 'tar', 424: 'tas',
    425: 'tat', 426: 'tau', 427: 'tav', 428: 'taw', 429: 'tax', 430: 'tea', 431: 'ted', 432: 'teg',
    433: 'teh', 434: 'ten', 435: 'tet', 436: 'tew', 437: 'tey', 438: 'thy', 439: 'try', 440: 'tsk',
    441: 'tub', 442: 'tug', 443: 'tum', 444: 'tun', 445: 'tup', 446: 'tut', 447: 'tux', 448: 'twa',
    449: 'tye', 450: 'uey', 451: 'ugh', 452: 'uke', 453: 'ume', 454: 'umm', 455: 'ump', 456: 'uns',
    457: 'ups', 458: 'urb', 459: 'urd', 460: 'urn', 461: 'urp', 462: 'use', 463: 'uta', 464: 'uts',
    465: 'vac', 466: 'van', 467: 'var', 468: 'vas', 469: 'vat', 470: 'vau', 471: 'vav', 472: 'vaw',
    473: 'vee', 474: 'veg', 475: 'ven', 476: 'vet', 477: 'vex', 478: 'vug', 479: 'vum', 480: 'wab',
    481: 'wad', 482: 'wae', 483: 'wag', 484: 'wan', 485: 'wap', 486: 'war', 487: 'was', 488: 'wat',
    489: 'waw', 490: 'way', 491: 'web', 492: 'wed', 493: 'wee', 494: 'wem', 495: 'wen', 496: 'wet',
    497: 'wey', 498: 'wha', 499: 'why', 500: 'wry', 501: 'wud', 502: 'wye', 503: 'wyn', 504: 'yag',
    505: 'yah', 506: 'yak', 507: 'yam', 508: 'yap', 509: 'yar', 510: 'yaw', 511: 'yay', 512: 'yea',
    513: 'yeh', 514: 'yem', 515: 'yen', 516: 'yep', 517: 'yes', 518: 'yet', 519: 'yew', 520: 'yex',
    521: 'yuk', 522: 'yum', 523: 'yup', 524: 'yus', 525: 'zag', 526: 'zak', 527: 'zap', 528: 'zas',
    529: 'zed', 530: 'zee', 531: 'zek', 532: 'zen', 533: 'zep', 534: 'zun', 535: 'zuz', 536: 'zzz'
}

if __name__ == '__main__':
    n = 1
    try:
        n = int(argv[1])
    except:  # noqa: E722
        pass
    for _ in range(n):
        print(password_for_sf())

"""
    chars = set('ljio')
    i = 1
    temp_str = "    "
    j = 1
    for key, value in words.items():
        if any((c in chars) for c in value):
            pass
        else:
            temp_str += f"{j}: '{value}', "
            i += 1
            j += 1
            if i == 9:
                print(temp_str)
                i = 1
                temp_str = "    "
"""
