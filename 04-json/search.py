import json
import sqlite3
import sys


def cursor_to_list_of_dictionaries(c):
    return [dict(zip([column[0] for column in c.description], row)) for row in c.fetchall()]


def get_voices(c, score_id):
    c.execute('select * from voice where score = ?', (score_id,))
    result = []
    for row in cursor_to_list_of_dictionaries(c):
        voice = {'name': row['name'], 'range': row['range']}
        result.append(voice)
    return result


def get_composers(c, score_id):
    c.execute('select * from score_author join person on score_author.composer = person.id where score = ?',
              (score_id,))
    result = []
    for row in cursor_to_list_of_dictionaries(c):
        person = {'name': row['name'], 'born': row['born'], 'died': row['died']}
        result.append(person)
    return result


def get_editors(c, edition_id):
    c.execute('select * from edition_author join person on edition_author.editor = person.id where edition = ?',
              (edition_id,))
    result = []
    for row in cursor_to_list_of_dictionaries(c):
        person = {'name': row['name'], 'born': row['born'], 'died': row['died']}
        result.append(person)
    return result


db_file = 'scorelib.dat'
conn = sqlite3.connect(db_file)
c = conn.cursor()
composer_name = sys.argv[1]
c.execute('select person.id, person.name from person where person.name like ?', ('%' + composer_name + '%',))
composers = cursor_to_list_of_dictionaries(c)
result = {}
for composer in composers:
    query = 'select print.id as print_id, print.partiture, edition.name as edition, edition.year as publication, ' \
            'score.name as title, score.year as composition, score.genre, score.key, score.incipit,' \
            'edition.id as edition_id, score.id as score_id from print ' \
            'join edition on edition.id = print.edition ' \
            'join score on score.id = edition.score ' \
            'join score_author on score_author.score = score.id ' \
            'join person on score_author.composer = person.id ' \
            'where person.id = ?'
    c.execute(query, (str(composer['id']),))
    print_data = cursor_to_list_of_dictionaries(c)
    prints = []
    for row in print_data:
        if row['partiture'] == 'y':
            row['partiture'] = True
        else:
            row['partiture'] = False
        row['print number'] = row.pop('print_id')
        row['publication year'] = row.pop('publication')
        row['composition year'] = row.pop('composition')
        row['voices'] = get_voices(c, row['score_id'])
        row['composer'] = get_composers(c, row['score_id'])
        row['editor'] = get_editors(c, row['edition_id'])
        row.pop('score_id')
        row.pop('edition_id')
        row_without_empty_values = {k: v for k, v in row.items() if v}#getting rid of all empty strings
        prints.append(row_without_empty_values)
    result[composer['name']] = prints
c.connection.close()

json.dump(result, sys.stdout, indent=4, ensure_ascii=False)

conn.close()
