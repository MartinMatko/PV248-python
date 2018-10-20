import re


class Print:
    def __init__(self, print_id=None, partiture=None):
        self.edition = Edition()
        self.print_id = print_id
        self.partiture = partiture

    def composition(self):
        return self.edition.composition

    def format(self):
        print('\nPrint Number: ' + str(self.print_id))
        if self.edition.composition.authors:
            print('Composer: ' + Person.get_author_string(self.edition.composition.authors))
        print('Title: ' + self.edition.composition.name)
        if self.composition().genre:
            print('Genre: ' + self.edition.composition.genre)
        if self.edition.composition.key:
            print('Key: ' + self.edition.composition.key)
        if self.edition.composition.year:
            print('Composition Year: ' + str(self.edition.composition.year))
        if self.edition.name:
            print('Edition: ' + self.edition.name)
        if self.edition.authors:
            print('Editor: ' + Person.get_author_string(self.edition.authors))
        for idx, voice in enumerate(self.edition.composition.voices):
            print('Voice ' + str(idx + 1) + ': ' + str(voice)) #voices start from one
        if self.partiture:
            print('Partiture: ' + 'yes')
        else:
            print('Partiture: ' + 'no')
        if self.edition.composition.incipit:
            print('Incipit: ' + self.edition.composition.incipit)


class Composition:
    def __init__(self, name=None, incipit=None, genre=None, year=None, voices=[], authors=[]):
        self.name = name
        self.incipit = incipit
        self.genre = genre
        self.year = year
        self.voices = []
        self.authors = authors


class Edition:
    def __init__(self, composition=None, authors=[], name=None):
        self.composition = composition
        self.authors = authors
        self.name = name


class Voice:
    def __init__(self, name=None, range=None):
        self.name = name
        self.range = range

    def __str__(self):
        result = ''
        if self.range:
            result += self.range
        if self.name and self.range:
            result += ', '
        if self.name:
            result += self.name
        return result


class Person:
    def __init__(self, name, born=None, died=None):
        self.name = name
        self.born = born
        self.died = died

    def __str__(self):
        result = self.name
        if self.born:
            result += ' (' + str(self.born) + '--'
            if self.died:
                result += str(self.died)
            result += ')'
        return result

    @staticmethod
    def get_author_list(string):
        persons = []
        if string:
            personal_data_of_all_persons = string.split('; ')
            if personal_data_of_all_persons:
                for personal_data_of_person in personal_data_of_all_persons:
                    if ' (' in personal_data_of_person:
                        name_and_years = personal_data_of_person.split(' (')
                        name = name_and_years[0].strip()
                        years = re.findall('\d\d\d\d', name_and_years[1] )
                        person = Person(name)
                        if years:
                            person.born = int(years[0])
                        if len(years) > 1:
                            person.died = int(years[1])
                    else:
                        person = Person(personal_data_of_person)
                    persons.append(person)
        return persons

    @staticmethod
    def get_author_string(list):
        return '%s' % '; '.join(map(str, list))

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

    for i in range(1, 10):
        voice_data = record.get('Voice ' + str(i))
        if not voice_data:
            break
        else:
            voice = Voice()
            if '--' in voice_data:
                range_and_name = voice_data.split(', ')
                voice.range = range_and_name[0]
                if len(range_and_name) > 1:
                    voice.name = ', '.join(range_and_name[1:])
            else:
                voice.name = voice_data
            composition.voices.append(voice)

    edition.composition = composition
    print.edition = edition
    return print

