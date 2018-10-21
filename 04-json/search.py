import json
import sqlite3
import sys

def cursor_to_list_of_dictionaries(c):
    return [dict(zip([column[0] for column in c.description], row)) for row in c.fetchall()]

db_file = 'scorelib.dat'
conn = sqlite3.connect(db_file)
c = conn.cursor()
composer_name = 'Bach'#sys.argv[1]
c.execute('select person.id, person.name from person where person.name like ?', ('%' + composer_name + '%', ))
composers = cursor_to_list_of_dictionaries(c)
result = {}
for composer in composers:
    query = 'select print.id as print_id, print.partiture, edition.name as edition, edition.year as publication, ' \
            'score.name as title, score.year as composition, score.genre, score.key, score.incipit from print ' \
            'join edition on edition.id = print.edition ' \
            'join score on score.id = edition.score ' \
            'join score_author on score_author.score = score.id ' \
            'join person on score_author.composer = person.id ' \
            'where person.id = ?'
    c.execute(query, (str(composer['id']), ))
    print_data = cursor_to_list_of_dictionaries(c)
    for row in print_data:
        row['print number'] = row.pop('print_id')
        row['publication year'] = row.pop('publication')
        row['composition year'] = row.pop('composition')

    result[composer['name']] = print_data
c.connection.close()


json.dump(result, sys.stdout, indent=4, ensure_ascii=False)


conn.close()
