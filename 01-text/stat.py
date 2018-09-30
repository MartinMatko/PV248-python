import re
import sys
from collections import Counter


def composer(file):
    counter_of_composers = Counter()
    for line in open(file, 'r', encoding="utf8"):
        if line.startswith("Composer: "):
            composers = line.split(": ")[1].split(";")
            for composer in composers:
                composer = composer.split("(")[0].strip()
                if composer:
                    counter_of_composers[composer] += 1
    for k, v in counter_of_composers.items():
        print(k + ": " + str(v))
    return counter_of_composers.items()


def century(file):
    counter_of_centuries = Counter()
    for line in open(file, 'r', encoding="utf8"):
        if line.startswith("Composition Year: "):
            dates_list = re.findall(r"[0-9]{4}|[0-9]{2}[a-zA-Z]{2}", line)
            if dates_list:
                date_string = dates_list[0].strip()
                # special case for likes of 17th century and 1700
                if re.search('[0-9]{2}[a-zA-Z]{2}|[0-9]{2}00', date_string):
                    century_string = date_string[:2]
                    counter_of_centuries[century_string] += 1
                else:
                    # year 1650 falls into 17th century
                    century_string = str(int(date_string[:2]) + 1)
                    counter_of_centuries[century_string] += 1

    for k, v in counter_of_centuries.items():
        print(k + ": " + str(v))
    return counter_of_centuries.items()


if not len(sys.argv) == 3:
    raise Exception("Invalid number of parameters")
else:
    file_name = sys.argv[1]
    method_name = sys.argv[2]
    if method_name == 'composer':
        composer(file_name)
    else:
        century(file_name)
