import sqlite3
import sys

from scorelib import *


def create_schema(c):
    # Open and read the file as a single buffer
    fd = open('scorelib.sql', 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            c.execute(command)
        except sqlite3.OperationalError as msg:
            print("Command skipped: " + msg)


def get_unique_entities():
    for print_entity in prints:
        authors = []
        authors.extend(print_entity.edition.authors)
        authors.extend(print_entity.edition.composition.authors)
        for author in authors:
            if author.name not in processed_persons:
                processed_persons[author.name] = author
            else:
                if not processed_persons[author.name].born:
                    processed_persons[author.name].born = author.born
                if not processed_persons[author.name].died:
                    processed_persons[author.name].died = author.died

        processed_editions.add(print_entity.edition)
        processed_compositions.add(print_entity.edition.composition)


# Connecting to the database file
txt_file = sys.argv[1]
db_file = sys.argv[2]
conn = sqlite3.connect(db_file)
c = conn.cursor()
create_schema(c)

prints = load(txt_file)
processed_persons = {}
processed_compositions = set()
processed_editions = set()

get_unique_entities()

for person in processed_persons.values():
    c.execute("INSERT INTO person ( born, died, name ) values (?, ?, ?)", (person.born, person.died, person.name))
for score in processed_compositions:
    c.execute("INSERT INTO score ( name, genre, key, incipit, year ) values (?, ?, ?, ?, ?)",
              (score.name, score.genre, score.key, score.incipit, score.year))

for print_entity in prints:
    edition = print_entity.edition
    score = edition.composition
    c.execute('SELECT id from score where name = ? and genre = ? and key = ? and incipit = ? ',
              (score.name, score.genre, score.key, score.incipit))
    score_id = c.fetchone()[0]

    # voice
    for idx, voice in enumerate(score.voices):
        c.execute("INSERT INTO voice ( number, score, range, name ) values (?, ?, ?, ?)",
                  (idx + 1, score_id, voice.range, voice.name))

    # score_author
    for author in score.authors:
        c.execute('SELECT id from person where name=?', (author.name,))
        author_id = c.fetchone()[0]
        c.execute("INSERT INTO score_author ( score, composer ) values (?, ?)",
                  (score_id, author_id))

    c.execute("INSERT INTO edition ( score, name) values (?, ?)",
              (score_id, edition.name))
    edition_id = c.lastrowid

    # edition_author
    for author in edition.authors:
        c.execute('SELECT id from person where name = ?', (author.name,))
        author_id = c.fetchone()[0]
        c.execute("INSERT INTO edition_author ( edition, editor ) values (?, ?)",
                  (edition_id, author_id))

    # print
    partiture = 'N'
    if print_entity.partiture == 'yes':
        partiture = 'Y'
    c.execute("INSERT INTO print ( id, partiture, edition ) values (?, ?, ?)",
              (print_entity.print_id, print_entity.partiture, edition_id))

conn.commit()
conn.close()
