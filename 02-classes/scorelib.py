import re


class Print:
    def __init__(self, print_id=None, partiture=None):
        self.edition = Edition()
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print('\nPrint Number: ' + self.print_id)
        if self.edition.composition.authors:
            print('Composer: ' + Person.get_author_string(self.edition.composition.authors))
        print('Title: ' + self.edition.composition.name)
        if self.edition.composition.genre:
            print('Genre: ' + self.edition.composition.genre)
        if self.edition.composition.key:
            print('Key: ' + self.edition.composition.key)
        if self.edition.composition.year:
            print('Composition Year: ' + self.edition.composition.year)
        if self.edition.name:
            print('Edition: ' + self.edition.name)
        if self.edition.authors:
            print('Editor: ' + Person.get_author_string(self.edition.authors))
        for idx, voice in enumerate(self.edition.composition.voices):
            print('Voice ' + str(idx) + ': ' + str(voice))
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
            result += self.range + ', '
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
            result += ' (' + self.born + '--'
            if self.died:
                result += self.died
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
                            person.born = years[0]
                        if len(years) > 1:
                            person.died = years[1]
                    else:
                        person = Person(personal_data_of_person)
                    persons.append(person)
        return persons

    @staticmethod
    def get_author_string(list):
        return ('%s' % '; '.join(map(str, list)))


