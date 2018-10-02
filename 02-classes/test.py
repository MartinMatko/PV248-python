import sys
from scorelib import *

def load(file_name):
    prints = []
    with open(file_name, 'r', encoding="utf8") as file:
        records = file.read().split('\n\n')
    for record in records:
        dict = {}
        for line in record.split('\n'):
            if re.match('^[A-Z]+', line) is not None:
                key_value = line.split(':')
                dict[key_value[0]] = key_value[1].strip()
        prints.append(create_print_from_dictionary(dict))
    return prints


def create_print_from_dictionary(record):
    print = Print()
    print.print_id = int(record.get('Print Number'))
    partiture = record.get('Partiture')
    if 'es' in partiture:
        print.partiture = True
    else:
        print.partiture = False

    edition = Edition()
    edition.name = record.get('Edition')
    editors = record.get('Editor')
    edition.authors = Person.get_author_list(editors)

    composition = Composition()
    composition.name = record.get('Title')
    composition.incipit = record.get('Incipit')
    composition.key = record.get('Key')
    composition.genre = record.get('Genre')
    if record.get('Year'):
        composition.year = int(record.get('Year'))
    composers = record.get('Composer')
    composition.authors = Person.get_author_list(composers)

    for i in range(1, 10):#total hack
        voice_data = record.get('Voice ' + str(i))
        if not voice_data:
            break
        else:
            voice = Voice()
            if '--' in voice_data:
                range_and_name = voice_data.split(', ')
                voice.range = range_and_name[0]
                if len(range_and_name) > 1:
                    voice.name = range_and_name[1]
            else:
                voice.name = voice_data
            composition.voices.append(voice)

    edition.composition = composition
    print.edition = edition
    return print



if not len(sys.argv) == 2:
    raise Exception("Invalid number of parameters")
else:
    file_name = sys.argv[1]
    prints = load(file_name)
    for print_entity in prints:
        print_entity.format()
