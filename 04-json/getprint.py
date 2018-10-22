import json
import sqlite3
import sys

db_file = 'scorelib.dat'
conn = sqlite3.connect(db_file)
c = conn.cursor()
print_id = sys.argv[1]
query = 'select person.name, person.born, person.died from print ' \
        'join edition on edition.id = print.edition ' \
        'join score on score.id = edition.score ' \
        'join score_author on score_author.score = score.id ' \
        'join person on score_author.composer = person.id ' \
        'where print.id = ?'

c.execute(query, (print_id,))
r = [dict((c.description[i][0], value) \
          for i, value in enumerate(row)) for row in c.fetchall()]
c.connection.close()

json.dump(r, sys.stdout, indent=4, ensure_ascii=False)

conn.close()
