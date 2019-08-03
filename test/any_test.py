#from Task import *
#import multiprocessing as mp
#print("Number of processors: ", mp.cpu_count())

from email.header import decode_header

def get_decoded_str(line):
    """Decode email field - From.
    :param line: Raw 7-bit message body input e.g. from imaplib.
    :return: Body of the letter in the desired encoding
    """
    lines = decode_header(line)
    print(lines)
    final_text = ""
    for text, charset in lines:
        if charset is None:
            final_text = text.decode()
        else:
            final_text = text.decode(str(charset), "ignore")
    return final_text

line1 = """=?utf-8?b?0K/QvdC00LXQutGBLtCf0LDRgdC/0L7RgNGC?=
 <noreply@passport.yandex.ru>"""

print(get_decoded_str(line1))

